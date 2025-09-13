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
