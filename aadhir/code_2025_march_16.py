from hub import light_matrix, port, motion_sensor
import motor
import runloop
import math
import motor_pair
from math import *

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
        return motor_pair.move_for_degrees(drive_motor_pair,degrees,0, velocity=velocity)


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

async def spin_turn(degrees):
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
    motor_pair.move(drive_motor_pair, steering_val, velocity=100)
    await runloop.until(turn_done)
    motor_pair.stop(drive_motor_pair)

async def move_arm(degree, direction, arm):
    if(direction=="up"):
        #up is minus degree
        degree = abs(degree)
    else:
        degree = - abs(degree)
    await motor.run_for_degrees(arm, degree, 360)

async def move_front_arm(degree, direction):
    await move_arm(degree,direction,FRONT_MOTOR_PORT)


async def move_back_arm(degree, direction):
    await move_arm(degree,direction,BACK_MOTOR_PORT)

async def mission_2():
    #reset arm
    await move_front_arm(90,"up")

    #move
    #await pivot_turn(18)
    await move_for_distance(72)
    await spin_turn(-45)
    #await spin_turn(-47)
    #await move_for_distance(10)
    await runloop.sleep_ms(500)

    #release shark
    await move_front_arm(180,"down")
    await runloop.sleep_ms(1000)
    await move_front_arm(180,"up")
    #come back to base
    await runloop.sleep_ms(500)
    #await move_for_distance(-10)
    await spin_turn(45)
    await runloop.sleep_ms(500)
    await move_for_distance(-72)
    #await pivot_turn(-18)
    #await move_for_distance(-15) 
async def move_to_shark_habitat():
    #hold the shark
    await motor.run_for_degrees(FRONT_MOTOR_PORT,-90, 720)
    #move the shark to habitat
    await move_for_distance(45)
    #release shark
    await motor.run_for_degrees(FRONT_MOTOR_PORT,90, 720)
async def mission_3():
    #collect first coral
    await move_for_distance(13)
    await pivot_turn(19)
    await move_for_distance(30)
    #collect second coral and third coral
    await pivot_turn(-28)
    await move_for_distance(10)
    await pivot_turn(-10)
    await move_for_distance(40)
    await pivot_turn(17)
    await move_for_distance(1)
    await motor.run_for_degrees(FRONT_MOTOR_PORT,-100,400)
    await runloop.sleep_ms(1500)
    await motor.run_for_degrees(FRONT_MOTOR_PORT,80,400)
    await move_for_distance(-2)
    await pivot_turn(-45, 400)
    await move_for_distance(25)
    await spin_turn(-70)
    await move_for_distance(20)
    await move_for_distance(20)
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

async def test():
    #await motor.run_for_degrees(FRONT_MOTOR_PORT,100,400)
    #await spin_turn(90)
    #await spin_turn(-90)
    #await move_for_distance(10)
    await move_back_arm(90,"up")
    await move_front_arm(90,"up")


async def collect_everything_2():
    #reset arm
    await move_back_arm(180,"up")
    #collect first three objects
    await move_for_distance(69)
    #collect krill infront of whale
    await spin_turn(35)
    await move_for_distance(13)
    #move to other side of mat
    await spin_turn(-150)
    await move_for_distance(7)
    await spin_turn(28)
    await move_for_distance(-5)
    await move_back_arm(220,"down")
    await spin_turn(-3)
    await move_for_distance(85)
    await spin_turn(-4)
    await move_for_distance(49,velocity=500)
    await spin_turn(-90)
    await move_for_distance(13,velocity=500)
    await spin_turn(30)
    await move_for_distance(55,velocity=500)
runloop.run(collect_everything_2()) 