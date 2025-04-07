from hub import light_matrix, port, motion_sensor , button
import motor
import color_sensor
import color
import runloop
import math
import motor_pair
from math import *
import sys

WHEEL_CIRCUMFERENCE = 17.6
DISTANCE_BETWEEN_WHEELS = 9.6 #cm - please measure your own robot.

motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
drive_motor_pair = motor_pair.PAIR_1
default_velocity = 1000
default_turn_velocity= 200

FRONT_MOTOR_PORT = port.D
BACK_MOTOR_PORT = port.C
# input must be in the same unit as WHEEL_CIRCUMFERENCE
def convert_distance_to_degree(distance_cm):
    # Add multiplier for gear ratio if needed
    return int((distance_cm/WHEEL_CIRCUMFERENCE) * 360)

# input must be in the same unit as WHEEL_CIRCUMFERENCE
def move_for_distance(distance_cm,velocity=default_velocity):
        degrees = convert_distance_to_degree(distance_cm)
        return motor_pair.move_for_degrees(drive_motor_pair,degrees,0, velocity=velocity, acceleration=1000,stop= motor.SMART_BRAKE)



async def move_for_distance_gyro(distance_cm, velocity=default_velocity):
    """
    Move straight with distance control using individual motor encoders

    Args:
        target_distance (float): Distance in centimeters
        velocity (int): Movement speed (0-100%)
    """

    # Hardware initialization
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)

    target_degrees = convert_distance_to_degree(distance_cm)

    #for backward movement , don't use gyro move
    if(distance_cm<0):
        return motor_pair.move_for_degrees(drive_motor_pair,target_degrees,0, velocity=velocity, acceleration=1000,stop= motor.SMART_BRAKE)

    #For Forward movement
    # Reset individual encoders
    motor.reset_relative_position(port.A,0)
    motor.reset_relative_position(port.B,0)

    # Movement control loop
    while True:
        current_left = abs(motor.relative_position(port.A))
        current_right = abs(motor.relative_position(port.B))
        avg_position = (current_left + current_right) / 2

        if avg_position >= target_degrees:
            motor_pair.stop(drive_motor_pair,stop=motor.SMART_BRAKE)
            break

        error = motion_sensor.tilt_angles()[0] * -0.1
        correction = int(error * -2)

        motor_pair.move(drive_motor_pair,
            correction,
            velocity=int(math.copysign(velocity, distance_cm)),
            acceleration=1000

        )
        await runloop.sleep_ms(100)

      


PIVOT_CIRCUMFERENCE = 2 * DISTANCE_BETWEEN_WHEELS * math.pi
async def pivot_turn(robot_degrees, velocity=default_turn_velocity):
    # Add a multiplier for gear ratios if you’re using gears
    motor_degrees = int((PIVOT_CIRCUMFERENCE/WHEEL_CIRCUMFERENCE) * abs(robot_degrees))
    if robot_degrees > 0:
        # pivot clockwise
        await motor_pair.move_for_degrees(motor_pair.PAIR_1, motor_degrees, 50, velocity=velocity)
    else:
        #pivot counter clockwise
        await motor_pair.move_for_degrees(motor_pair.PAIR_1, motor_degrees, -50, velocity=velocity)

#Spin Turn Functions
global degrees_to_turn, stop_angle
# Function that returns true when the absolute yaw angle is 90 degrees
def turn_done():
    global degrees_to_turn, stop_angle
    # convert tuple decidegree into the same format as in app and blocks
    yaw_angle = motion_sensor.tilt_angles()[0] * -0.1
    # if we need to turn less than 180 degrees, check the absolute values
    if abs(degrees_to_turn) < 180 :
        return abs(yaw_angle) > stop_angle
    # If we need to turn more than 180 degrees, compute the yaw angle we need to stop at.
    if degrees_to_turn >= 0: # moving clockwise
    # The adjusted yaw angle is positive until we cross 180.
    # Then, we are negative numbers counting up.
        return yaw_angle < 0 and yaw_angle > stop_angle
    else:
    # The adjusted yaw angle is negative until we cross 180
    # Then, we are positive numbers counting down.
        return yaw_angle > 0 and yaw_angle < stop_angle

async def spin_turn(degrees, velocity=default_turn_velocity):
    if abs(degrees) > 355:
        print("Out of range")
        return
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)
    global degrees_to_turn, stop_angle
    degrees_to_turn = degrees # set the global to use in the turn_done function
    # set the stop_angle global to use in the turn_done function
    if (abs(degrees) < 180):
        stop_angle = abs(degrees_to_turn)
    else:
        stop_angle = (360 - abs(degrees)) if degrees < 0 else (abs(degrees) - 360)
    # set the steering vlaue based on turn direction
    steering_val = 100 if degrees >= 0 else -100
    motor_pair.move(drive_motor_pair, steering_val, velocity=velocity)
    await runloop.until(turn_done)
    motor_pair.stop(drive_motor_pair)

async def move_arm(degree, direction, arm, speed="slow"):
    if(direction=="up"):
        #up is minus degree
        degree = abs(degree)
    else:
        degree = - abs(degree)
    velocity=360
    if speed=="high":
        velocity = 1000
    elif speed=="medium":
        velocity =640
    else:
        velocity= 360

    await motor.run_for_degrees(arm, degree, velocity,acceleration=100)

async def move_front_arm(degree, direction, speed="slow"):
    await move_arm(degree,direction,FRONT_MOTOR_PORT,speed=speed)

async def reset_back_arm():
      await motor.run_to_relative_position(BACK_MOTOR_PORT,20,500)

async def move_back_arm(degree, direction,speed="slow"):
    await move_arm(degree,direction,BACK_MOTOR_PORT,speed=speed)

#align straight
def align_done():
    if motor.velocity(port.A) == 0 and motor.velocity(port.B) == 0:
        return True
    return False

# Function to move motor until the sensor in front of it senses black
# Parameters:
# motor_port: The port of the motor
# sensor_port: port of the color sensor in front of the motor
# direction: 1 for clockwise, -1 for counterclockwise
async def move_until_black(motor_port, color_port, direction):
    motor.run(motor_port, 50 * direction)
    #while color_sensor.reflection(color_port) > 99:
    while color_sensor.color(color_port) == color.WHITE and color_sensor.reflection(color_port) > 98:
        await runloop.sleep_ms(50)
    motor.stop(motor_port)
async def align_robot_on_black():
    # create two async functions to send to the runloop
    a = move_until_black(port.A, port.E, -1)
    b = move_until_black(port.B, port.F, 1)
    # run both the functions together
    runloop.run(*[a,b])
    # wait until both motors have stopped
    await runloop.until(align_done)

async def move_until_red(motor_port, color_port, direction):
    motor.run(motor_port, 10 * direction)
    while color_sensor.color(color_port) == color.RED:
        await runloop.sleep_ms(10)
    motor.stop(motor_port)
async def align_robot_on_red():
    await move_for_distance(6,velocity=100)
    # create two async functions to send to the runloop
    a = move_until_red(port.A, port.E, -1)
    b = move_until_red(port.B, port.F, 1)
    # run both the functions together
    runloop.run(*[a,b])
    # wait until both motors have stopped
    await runloop.until(align_done)

async def move_until_white(motor_port, color_port, direction):
    motor.run(motor_port, 50 * direction,acceleration=100)
    while color_sensor.reflection(color_port) < 95:
        await runloop.sleep_ms(1)
    motor.stop(motor_port)
async def align_robot_on_white():
    # create two async functions to send to the runloop
    a = move_until_white(port.A, port.E, -1)
    b = move_until_white(port.B, port.F, 1)
    # run both the functions together
    runloop.run(*[a,b])
    # wait until both motors have stopped
    await runloop.until(align_done)


async def release_things_left():
    #reset arm
    await move_front_arm2(60,"up")
    await move_for_distance(-2)
    await runloop.sleep_ms(50)
    await align_robot_on_red()
    await runloop.sleep_ms(50)

    #move
    #await pivot_turn(18)
    await move_for_distance(69)
    await spin_turn(-48)
    #await spin_turn(-47)
    await move_for_distance(4)
    await runloop.sleep_ms(500)

    #release shark
    await move_front_arm2(80,"down","slow")
    await runloop.sleep_ms(300)
    await move_front_arm2(60,"up")
    await runloop.sleep_ms(100)
    #await move_for_distance(-10)
    await spin_turn(88)
    await runloop.sleep_ms(100)
    await move_for_distance(15)
    #come back to base
    #oush coral reef
    await runloop.sleep_ms(100)
    await move_front_arm2(80,"down","fast")
    await runloop.sleep_ms(300)
    await move_front_arm2(50,"up")
    await runloop.sleep_ms(100)
    await move_for_distance(-5)
    await spin_turn(-43)
    await move_front_arm2(20,"up")
    await move_for_distance(-15)
    await spin_turn(-90)
    await move_for_distance(-3)
    #release coral nursery
    #await spin_turn()
    # await spin_turn(179)
    await move_front_arm2(50,"down","slow")
    await runloop.sleep_ms(300)
    await move_for_distance(5)
    await move_front_arm2(60,"up")
    # await runloop.sleep_ms(100)
    await spin_turn(-60)
    await move_for_distance(60)


async def release_things_left2():
    #reset arm
    await move_front_arm2(60,"up")
    await move_for_distance(-2)
    await runloop.sleep_ms(50)
    await align_robot_on_red()
    await runloop.sleep_ms(100)

    #move
    await spin_turn(15)
    await move_for_distance(69)
    await spin_turn(-74)
    #await spin_turn(-47)
    await move_for_distance(19)
    await runloop.sleep_ms(100)
    #wait_for_button()
    #release shark
    await move_front_arm2(80,"down","slow")
    await runloop.sleep_ms(300)
    await move_front_arm2(60,"up")
    await runloop.sleep_ms(100)
    #await move_for_distance(-10)
    await spin_turn(97)
    await runloop.sleep_ms(100)
    await move_for_distance(10)
    #come back to base
    #oush coral reef
    await runloop.sleep_ms(100)
    await move_front_arm2(80,"down","fast")
    await runloop.sleep_ms(300)
    await move_front_arm2(50,"up")
    await runloop.sleep_ms(100)
    await move_for_distance(-3)
    await move_front_arm2(50,"up")
    await spin_turn(150)
    await move_for_distance(-18,velocity=200)
    #await spin_turn(-10)
    ##release coral nursery
    # await spin_turn(-40)
    # await move_front_arm2(20,"up")
    # await move_for_distance(-15)
    # await spin_turn(-90)
    # await move_for_distance(-3)
    # await move_front_arm2(50,"down","slow")
    # await runloop.sleep_ms(300)
    # await move_for_distance(5)
    # await move_front_arm2(60,"up")
    # await spin_turn(-60)

    #come back
    #await spin_turn(-40)
    await move_for_distance(43)
    await spin_turn(90)
    await move_for_distance(16)
    await move_front_arm2(60,"down")
    await spin_turn(-90)
    await move_for_distance(43)

async def pull_coral_reef():
    #reset arm
    await move_front_arm2(60,"up")
    await move_for_distance(-2)
    await runloop.sleep_ms(50)
    #await align_robot_on_red()
    #await runloop.sleep_ms(50)
    await move_for_distance(53)
    await runloop.sleep_ms(50)
    await spin_turn(36)
    await runloop.sleep_ms(50)
    await move_for_distance(6)
    await runloop.sleep_ms(50)
    await move_front_arm2(70,"down")
    #wait_for_button()
    await runloop.sleep_ms(50)
    await move_for_distance(-10,velocity=100)
    await runloop.sleep_ms(50)
    await move_front_arm2(60,"up")
    #await move_for_distance(-3)
    await runloop.sleep_ms(50)
    await spin_turn(120)
    await move_for_distance(30)

async def move_to_shark_habitat():
    #hold the shark
    await motor.run_for_degrees(FRONT_MOTOR_PORT,-90, 720)
    #move the shark to habitat
    await move_for_distance(45)
    #release shark
    await motor.run_for_degrees(FRONT_MOTOR_PORT,90, 720)
async def mission_3():
    # #collect first coral
    # await move_for_distance(13)
    # await pivot_turn(19)
    # await move_for_distance(30)
    # #collect second coral and third coral
    # await pivot_turn(-28)
    # await move_for_distance(10)
    # await pivot_turn(-10)
    await move_front_arm(230,"up")
    await runloop.sleep_ms(100)
    await move_front_arm(220,"down")
    await runloop.sleep_ms(100)
    await move_for_distance(62)
    await runloop.sleep_ms(50)
    await pivot_turn(90)
    await runloop.sleep_ms(50)
    await move_for_distance(5)
    await runloop.sleep_ms(50)
    await pivot_turn(-90)
    #await move_front_arm(210,"down","slow")
    await runloop.sleep_ms(500)
    await move_for_distance(4)
    await runloop.sleep_ms(50)
    await move_front_arm(80,"up","fast")
    await runloop.sleep_ms(1000)
    await move_front_arm(40,"down","slow")
    await move_for_distance(-5)

    await pivot_turn(10)
    await move_for_distance(-70)


async def move_from_left_to_right():
    #reset arm
    # await move_front_arm2(60,"up")
    # await move_for_distance(-2)
    # await runloop.sleep_ms(50)
    # await align_robot_on_red()
    # await runloop.sleep_ms(50)
    # await move_for_distance(25)
    # await runloop.sleep_ms(50)
    # await spin_turn(90)
    # await runloop.sleep_ms(50)
    await move_for_distance(170,velocity=1000)


async def mission_move_boat():
    #await reset_back_arm()
    await move_for_distance(23)
    await runloop.sleep_ms(50)
    await spin_turn(90)
    await runloop.sleep_ms(50)
    await move_for_distance(46)
    await runloop.sleep_ms(50)
    await move_back_arm(120,"up")
    #await gyro_move_straight()

async def move_crab_cage():
    await move_for_distance(-1)
    await move_for_distance(22)
    await spin_turn(-89)
    await move_back_lift(1500,"up")
    await move_for_distance(25)
    await spin_turn(45)
    await move_for_distance(20)
    #await spin_turn(-45)
    #await gyro_move_straight()
    #await gyro_move_straight()


async def collect_everything_2():
    #reset arm
    await move_for_distance(-2, velocity=50)
    await move_front_arm2(60,"up")
    await runloop.sleep_ms(50)
    #collect first three objects
    await move_for_distance(69)
    await runloop.sleep_ms(50)
    #collect krill infront of whale
#     await spin_turn(35)
#     await runloop.sleep_ms(50)
#     await move_for_distance(13) #old 13
#     #wait_for_button()
#     await runloop.sleep_ms(50)
#     await align_robot_on_black()
#     #wait_for_button()
#     await runloop.sleep_ms(500)
#     await move_for_distance(-4)
#     #move to other side of mat and collect the thing in bamboo forest
#     await spin_turn(-150)
#     #wait_for_button()
#     #await runloop.sleep_ms(50)
#     await move_for_distance(7)
#     await runloop.sleep_ms(50)
#     await spin_turn(25)
#     # await runloop.sleep_ms(50)
#     await runloop.sleep_ms(50)
#     await move_for_distance(-7)
#     await runloop.sleep_ms(50)
#     # await runloop.sleep_ms(50)
#     await move_back_arm2(130,"down")
#     await runloop.sleep_ms(50)
#    # wait_for_button()
#      #await runloop.sleep_ms(50)
#     await move_for_distance(7)
#     await runloop.sleep_ms(50)
#     # await runloop.sleep_ms(50)
#     await move_back_arm2(90,"up")
    await runloop.sleep_ms(50)
    await spin_turn(-92)
    await runloop.sleep_ms(50)
#right side done

    await move_for_distance(65)
    #wait_for_button()
    await runloop.sleep_ms(10)
    #push ship wreck side arm
    await spin_turn(10,velocity=25)
    await runloop.sleep_ms(50)
    await move_for_distance_gyro(60,velocity=300)
    await runloop.sleep_ms(50)
    await spin_turn(-90)
    await runloop.sleep_ms(50)
    #collect the two coral and a krill
    await move_for_distance(17,velocity=500)
    await runloop.sleep_ms(50)
    await spin_turn(20)
    await runloop.sleep_ms(50)
    await move_for_distance(45,velocity=500)

async def test():
    #await motor.run_for_degrees(FRONT_MOTOR_PORT,100,400)
    #await spin_turn(90)
    #await spin_turn(-90)
    #await move_for_distance(10)
    #await move_back_arm(260,"up")
    #await move_back_arm(110,"down")


    # await move_front_arm(10,"down")
    await runloop.sleep_ms(100)
    await move_front_arm(210,"down")
    await runloop.sleep_ms(100)
    await move_front_arm(180,"up")


    #await move_front_arm(270,"up")
    # await reset_back_arm()
    # await move_back_arm(90, "up")


async def release_squid():
    #initalize
    #await move_for_distance(-2)
    #await move_front_arm2(15,"up")
    #await runloop.sleep_ms(100)
    #move to squid
    # await move_for_distance(21)
    # await runloop.sleep_ms(100)
    # await spin_turn(-33)
    # await runloop.sleep_ms(100)
    await move_for_distance(40,velocity=2000)
    await runloop.sleep_ms(50)
    await move_for_distance(-40)
    #await spin_turn(36)
    #await move_for_distance(-21)

async def release_submarine():
    #go to subermissible
    await move_for_distance(-2)
    await move_front_arm2(40,"up")
    await runloop.sleep_ms(50)
    await move_for_distance(47)
    #final turn towards submarine
    await spin_turn(-43)
    await runloop.sleep_ms(50)
    await move_for_distance(65)
    await move_for_distance(-5)
    await align_robot_on_white()
    #await align_robot_on_black()
    await runloop.sleep_ms(50)
    await move_for_distance(3)
    await runloop.sleep_ms(100)
    await move_front_arm2(70,"up","slow")
    await runloop.sleep_ms(1000)
    await move_front_arm2(20,"down","slow")
    await move_front_arm2(70,"up","slow")
    await runloop.sleep_ms(1000)
    await move_front_arm2(20,"down","slow")
    await move_for_distance(-5)
    await align_robot_on_white()
    await spin_turn(-33)
    await move_for_distance(20)
    await spin_turn(90)
    #await spin_turn(-2)
    #await move_for_distance(-80)

async def move_back_lift(time, direction,speed="slow"):
    velocity=360
    if speed=="high":
        velocity = 1000
    elif speed=="medium":
        velocity =640
    else:
        velocity= 360
    
    if(direction=="up"):
    #up is minus degree
        velocity = - abs(velocity)
    else:
        velocity = abs(velocity)
    await motor.run_for_time(BACK_MOTOR_PORT,time, velocity,acceleration=200)
    #await motor.run_for_degrees(BACK_MOTOR_PORT, degree, velocity,acceleration=1000)

async def move_front_arm2(degree, direction,speed="slow"):
    if(direction=="up"):
    #up is minus degree
        degree = - abs(degree)
    else:
        degree = abs(degree)
    velocity=360
    if speed=="high":
        velocity = 1000
    elif speed=="medium":
        velocity =640
    else:
        velocity= 360
    
    await motor.run_for_degrees(FRONT_MOTOR_PORT, degree, velocity,acceleration=200)


async def move_back_arm2(degree, direction,speed="slow"):
    if(direction=="up"):
    #up is minus degree
        degree = - abs(degree)
    else:
        degree = abs(degree)
    velocity=360
    if speed=="high":
        velocity = 1000
    elif speed=="medium":
        velocity =640
    else:
        velocity= 360

    await motor.run_for_degrees(BACK_MOTOR_PORT, degree, velocity,acceleration=200)

async def push_coral():
    await move_for_distance(-4,velocity=100)
    await runloop.sleep_ms(100)
    await move_for_distance(20)



    # await move_back_lift(2000,"down")

def wait_for_button():
    while True:
        if button.pressed(button.RIGHT):
            break
async def launcher():
    #await align_robot_on_black()
    #wait_for_button()
    #1
    #await collect_everything_2()
    #await move_back_arm2(140,"down")
    #wait_for_button()
    #2
    await release_things_left2()
    #3
    #await pull_coral_reef()
    #await align_robot_on_red()

    #4 Push coral
    #await push_coral()
    #5
    #await move_from_left_to_right()

    #6
    #await release_squid()

    #7
    #await release_submarine()
    #await align_robot_on_white()
    #await move_for_distance_gyro(-3)
    # await move_front_arm2(60,"up","slow")
    # await move_front_arm2(60,"down","slow")
    #await mission_3()
    #await mission_3_backpush()
    #await mission_move_boat()
    #await test()
    #await move_for_distance(-15)
    # await move_back_lift(150, "down","slow")
    # await move_back_lift(150, "up","slow")
    #await move_for_distance(4)
    # await move_front_arm2(60,"up","slow")
    # await move_front_arm2(60,"up","fast")
    # await runloop.sleep_ms(1000)
    # await move_front_arm2(30,"down","slow")
    # await move_back_lift(2000,"up")
    # await move_back_lift(2000,"down")
    #await move_crab_cage()
    #await move_for_distance(80,velocity=500)

runloop.run(launcher())
