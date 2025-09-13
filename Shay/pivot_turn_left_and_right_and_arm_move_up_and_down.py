import motor
from hub import port
import motor_pair
import runloop
import math
async def move_arm_up(degrees):
    await motor.run_for_degrees(port.D, degrees, 360)
async def move_arm_down(degrees):
    await motor.run_for_degrees(port.D, degrees, -360)
motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)
#convert distance to degree is not part of the project, I just added it just in case
def convert_distance_to_degree(distance_cm):
    return int((distance_cm/17.5) * 360)
async def pivot_turn_right(degrees, motor_speed):
    motor_degrees = int((PIVOT_CIRCUMFERENCE/WHEEL_CIRCUMFERENCE) * abs(degrees))
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, motor_degrees, 50, velocity=motor_speed)
async def pivot_turn_left(degrees, motor_speed):
    motor_degrees = int((PIVOT_CIRCUMFERENCE/WHEEL_CIRCUMFERENCE) * abs(degrees))
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, motor_degrees, -50, velocity=motor_speed)
