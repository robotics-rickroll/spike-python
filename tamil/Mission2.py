import motor
from hub import port
import motor_pair
import color_sensor
import color
import runloop
async def move():
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)
    await motor.run_for_degrees(port.A, 55, -180)
    await motor_pair.move_tank_for_time(motor_pair.PAIR_1, 200, 200, 4000)
    await motor.run_for_degrees(port.E, 165, 360)
    await motor.run_for_degrees(port.D, -300, 360)
    await motor.run_for_degrees(port.D, 180, 360)


    await motor.run_for_degrees(port.E, 165, -360)
    await motor_pair.move_tank_for_time(motor_pair.PAIR_1, -200, -200, 4000)
    await motor.run_for_degrees(port.A, 55, 180)
runloop.run(move())
