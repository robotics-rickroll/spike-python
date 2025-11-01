from robot import *

#start on the 6 squares from the left
def missions1and2():
    #reset_arms()
    move_straight_gyro(740, DriveSpeed.PUSHING)
    left_arm_up(180, ArmSpeed.COLLECT)
    wait(500)
    move_straight_gyro(-10, DriveSpeed.PUSHING)
    spin_turn(-45)
    move_straight_gyro(100, DriveSpeed.PRECISE)
    move_straight_gyro(-100, DriveSpeed.PRECISE)
    spin_turn(45)
    move_straight_gyro(-730, DriveSpeed.PUSHING)

#start on the 12 squares from the left
def mission1_Part2():
    move_straight_gyro(425, DriveSpeed.PUSHING)
    move_straight_gyro(180, DriveSpeed.PRECISE)
    spin_turn(-90)
    move_straight_gyro(90, DriveSpeed.PRECISE)
    left_arm_up(180, ArmSpeed.COLLECT)
    wait(500)
    move_straight_gyro(-90, DriveSpeed.PRECISE)
    spin_turn(90)
    move_straight_gyro(-605, DriveSpeed.PUSHING)

async def boulder_mission():
    move_straight_gyro(65, DriveSpeed.PUSHING)
    await arm_left(90)
    await backward(65, 700)

async def marketplace_flippy_and_boulder_mission():
    await forward(68,700)
    await runloop.sleep_ms(100)
    await turn_right(35)
    await arm_left(70)
    await backward(71,700)



if __name__ == "__main__":
    """
    Main execution - run different demos
    """

    #missions1and2()
    missions1and2()