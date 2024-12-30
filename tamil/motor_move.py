import motor
from hub import light_matrix, port
import runloop
import math
import motor_pair

diameter_of_wheel_centimeter = 5.6
circumference_of_wheel_centimeter = diameter_of_wheel_centimeter * math.pi
motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

async def move(distance=0):
    rotations = distance / circumference_of_wheel_centimeter
    degrees_to_rotate= int(360 * rotations)
    await light_matrix.write(str(degrees_to_rotate))
    await motor_pair.move_for_degrees (motor_pair.PAIR_1, degrees_to_rotate,0, velocity=1000)
runloop.run(move(90))
