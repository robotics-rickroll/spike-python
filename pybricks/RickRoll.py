from robot import *

#start on the 6 squares from the left
def missions1and2():
    #reset_arms()
    move_straight_gyro(740, DriveSpeed.PUSHING)
    left_arm_up(180, ArmSpeed.COLLECT)
    wait(500)
    move_straight_gyro(-740, DriveSpeed.PUSHING)

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


if __name__ == "__main__":
    """
    Main execution - run different demos
    """

    #missions1and2()
    mission1_Part2()