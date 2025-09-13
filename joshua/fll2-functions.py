from hub import light_matrix, port, motion_sensor, power_off
import motor
import runloop
import math
import motor_pair
from math import *
import hub
#functions
#forward(centimeters,speed) and bacwards(centimeters,speed)
#turn_right(deegres) and turn_left(deegres) cannot go over 355 deegrees in one turn
#arm_up(deegres) and arm_down(deegres)
#
#
#
WHEEL_CIRCUMFERENCE = 17.5
DISTANCE_BETWEEN_WHEELS = 14.2 #cm - please measure your own robot.
#ports underneath
motor_pair.pair(motor_pair.PAIR_1, port.A, port.C)
drive_motor_pair = motor_pair.PAIR_1
default_velocity = 30
turn_velocity= 100

# input must be in the same unit as WHEEL_CIRCUMFERENCE
def convert_distance_to_degree(distance_cm):
    # Add multiplier for gear ratio if needed
    return int((distance_cm/WHEEL_CIRCUMFERENCE) * 360)

# input must be in the same unit as WHEEL_CIRCUMFERENCE
def backward(distance_cm, speed):
        degrees = convert_distance_to_degree(distance_cm)
        return motor_pair.move_for_degrees(drive_motor_pair,degrees,0, velocity=speed)


def move_for_distance(distance_cm):
        degrees = convert_distance_to_degree(distance_cm)
        return motor_pair.move_for_degrees(drive_motor_pair,degrees,0)

def forward(distance_cm, speed):
        degrees = convert_distance_to_degree(distance_cm)
        return motor_pair.move_for_degrees(drive_motor_pair,degrees,0, velocity=speed)


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

# Function that returns true when the absolute yaw angle is 90 degrees
def turn_done():
    # convert tuple decidegree into same format as in app and blocks
    return abs(motion_sensor.tilt_angles()[0] * -0.1) > 90



async def turn(degrees):
    if abs(degrees) > 355: #cannot be used over 355 degrees
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
    # set the steering laue based on turn direction
    steering_val = 100 if degrees >= 0 else -100
    motor_pair.move(motor_pair.PAIR_1, steering_val, velocity=200)
    await runloop.until(turn_done)
    motor_pair.stop(motor_pair.PAIR_1)

async def turn_left(degrees):
    await turn(abs(degrees))

async def turn_right(degrees):
    await turn(abs(degrees)*-1 )

async def arm_up(degrees:int):
    await motor.run_for_degrees(port.B, degrees, 360)

async def arm_down(degrees:int):
    await motor.run_for_degrees(port.B, degrees*-1, 360)

async def testrun(x,z,y):
    await forward(x,z)
    await turn(y)

runloop.run(testrun(1,500,200))
