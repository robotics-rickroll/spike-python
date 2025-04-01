from hub import light_matrix, port, motion_sensor , button
import motor
import color_sensor
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
turn_velocity= 100

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

async def gyro_move_straight():
    #motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)
    # Reset the yaw angle and wait for it to stabilize
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)
    while True:
        # compute the error in degrees. See Turning with Gyro for explanation.
        error = motion_sensor.tilt_angles()[0] * -0.1
        # correction is an integer which is the negative of the error
        correction = int(error * -2)
        # apply steering to correct the error
        motor_pair.move(drive_motor_pair, correction, velocity=1000)

PIVOT_CIRCUMFERENCE = 2 * DISTANCE_BETWEEN_WHEELS * math.pi
async def pivot_turn(robot_degrees, motor_speed=turn_velocity):
    # Add a multiplier for gear ratios if you’re using gears
    motor_degrees = int((PIVOT_CIRCUMFERENCE/WHEEL_CIRCUMFERENCE) * abs(robot_degrees))
    if robot_degrees > 0:
        # pivot clockwise
        await motor_pair.move_for_degrees(motor_pair.PAIR_1, motor_degrees, 50, velocity=motor_speed)
    else:
        #pivot counter clockwise
        await motor_pair.move_for_degrees(motor_pair.PAIR_1, motor_degrees, -50, velocity=motor_speed)

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

async def spin_turn(degrees, velocity=100):
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

#move straight
async def all_done():
    return (motor.velocity(port.A) is 0 and motor.velocity(port.B) is 0)
# Function to move motor until the sensor in front of it senses black
# Parameters:
# motor_port: The port of the motor
# sensor_port: port of the color sensor in front of the motor
# direction: 1 for clockwise, -1 for counterclockwise
async def move_until_black(motor_port, color_port, direction):
    motor.run(motor_port, 200 * direction)
    while color_sensor.reflection(color_port) > 50:
        await runloop.sleep_ms(50)
    motor.stop(motor_port)
async def align_robot():
    # create two async functions to send to the runloop
    a = move_until_black(port.A, port.E, -1)
    b = move_until_black(port.B, port.F, 1)
    # run both the functions together
    runloop.run(*[a,b])
    # wait until both motors have stopped
    await runloop.until(all_done())

async def release_things_left():
    #reset arm
    #await move_front_arm(90,"up")

    #move
    #await pivot_turn(18)
    await move_for_distance(72)
    await spin_turn(-47)
    #await spin_turn(-47)
    await move_for_distance(8)
    await runloop.sleep_ms(500)

    #release shark
    await move_front_arm(210,"down","fast")
    await runloop.sleep_ms(300)
    await move_front_arm(180,"up")
    #await move_for_distance(-10)
    await spin_turn(90)
    await runloop.sleep_ms(100)
    await move_for_distance(12)
    #come back to base
    #oush coral reef
    await runloop.sleep_ms(100)
    await move_front_arm(300,"down","fast")
    await runloop.sleep_ms(300)
    await move_front_arm(180,"up")
    await move_for_distance(-5)
    #await move_for_distance(10)
    #release coral nursery
    await spin_turn(179)
    await move_front_arm(100,"down","fast")
    await runloop.sleep_ms(300)
    await move_for_distance(3)
    await move_front_arm(180,"up")
    #await move_for_distance(10)
    await runloop.sleep_ms(100)
    await spin_turn(-40)
    await move_for_distance(60)
    #await move_for_distance(-10)

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

async def mission_3_backpush():

    await move_front_arm(230,"up")
    await runloop.sleep_ms(100)
    await move_front_arm(120,"down")
    await runloop.sleep_ms(100)
    await move_for_distance(90.5)
    await runloop.sleep_ms(50)
    await pivot_turn(90)
    await runloop.sleep_ms(50)
    await move_front_arm(200,"down")
    await runloop.sleep_ms(50)
    await move_front_arm(100,"up")
    await runloop.sleep_ms(50)
    await pivot_turn(90)
    await move_for_distance(90)


async def mission_flip():
    await reset_back_arm()
    await move_back_arm(230,"up")
    await runloop.sleep_ms(100)
    await move_front_arm(120,"down")

async def mission_move_boat():
    #await reset_back_arm()
    await move_for_distance(23)
    await runloop.sleep_ms(50)
    await spin_turn(90)
    await runloop.sleep_ms(50)
    await move_for_distance(46)
    await runloop.sleep_ms(50)
    await move_back_arm(120,"up")
    await gyro_move_straight()

async def move():
    await motor.run_for_degrees(FRONT_MOTOR_PORT, 180, 1000)
async def collect_everything_backward():
    #reset the arm to lifted position
    await motor.run_for_degrees(FRONT_MOTOR_PORT,110,400)
    #move to first three objects
    await move_for_distance(66)
    #move to coral
    await spin_turn(52)
    await move_for_distance(-5)
    #move for the other 2 krill
    await spin_turn(-25)
    await move_for_distance(-8)
    await spin_turn(-60)
    await move_for_distance(-10)
    #Uturn
    await spin_turn(140)
    #move to other side
    await move_for_distance(-30)
    await spin_turn(-25)
    await move_for_distance(-30)
    await spin_turn(30)
    #collect another water sampler
    await move_for_distance(-12)
    await spin_turn(-30)
    #collect krill
    await move_for_distance(-10)
    #collect seaweed
    await pivot_turn(85)
    await move_for_distance(-10)


async def collect_everything_2():
    #reset arm
    await move_front_arm(40,"up")
    await runloop.sleep_ms(50)
    #collect first three objects
    await move_for_distance(69)
    await runloop.sleep_ms(50)
    #collect krill infront of whale
    await spin_turn(35)
    await runloop.sleep_ms(50)
    await move_for_distance(13)
    await runloop.sleep_ms(50)
    #move to other side of mat and collect the thing in bamboo forest
    await spin_turn(-150)
    await runloop.sleep_ms(50)
    await move_for_distance(7)
    await runloop.sleep_ms(50)
    await spin_turn(28)
    # await runloop.sleep_ms(50)
    # await move_for_distance(-4)
    # await runloop.sleep_ms(50)
    # await move_back_arm(170,"down")
    # #await runloop.sleep_ms(50)
    # await move_for_distance(4)
    # await runloop.sleep_ms(50)
    # await move_back_arm(170,"up")
    # await runloop.sleep_ms(50)
    await spin_turn(-9)
    await runloop.sleep_ms(50)
#right side done

    await move_for_distance(65)
    await runloop.sleep_ms(10)
    #push ship wreck side arm
    await spin_turn(10,velocity=25)
    await runloop.sleep_ms(50)
    await move_for_distance(60,velocity=500)
    await runloop.sleep_ms(50)
    await spin_turn(-90)
    await runloop.sleep_ms(50)
    #collect the two coral and a krill
    await move_for_distance(17,velocity=500)
    await runloop.sleep_ms(50)
    await spin_turn(40)
    await runloop.sleep_ms(50)
    await move_for_distance(55,velocity=500)

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
    await move_for_distance(20)
    await spin_turn(-43)
    await move_for_distance(23)
    await move_for_distance(-3)
    await spin_turn(45)
    await move_for_distance(20)
    await spin_turn(-48)
    await runloop.sleep_ms(100)
    await move_front_arm(20,"up")
    await move_for_distance(49)
    await move_front_arm(250,"up","fast")

async def move_back_lift(degree, direction,speed="slow"):
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
    await motor.run_for_degrees(BACK_MOTOR_PORT, degree, velocity,acceleration=1000)

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

def wait_for_button():
    while True:
        if button.pressed(button.RIGHT):
            break
async def launcher():
    #wait_for_button()
    #await collect_everything_2()
    #wait_for_button()
    #await release_things_left()

    #await release_squid()

    #await mission_3()
    #await mission_3_backpush()
    #await mission_move_boat()
    #await test()
    #await move_for_distance(-15)
    # await move_back_lift(150, "down","slow")
    # await move_back_lift(150, "up","slow")
    #await move_for_distance(4)
    await move_front_arm2(60,"up","slow")
    await move_front_arm2(60,"down","slow")


runloop.run(launcher())
