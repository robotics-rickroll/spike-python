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

#align at square 8
def missions3():
    move_straight_gyro(400, DriveSpeed.PUSHING)
    move_straight_gyro(280, DriveSpeed.PRECISE)
    spin_turn(90, TurnSpeed.PRECISE)
    move_straight_gyro(150, DriveSpeed.PUSHING)
    move_straight_gyro(180, DriveSpeed.PRECISE)
    spin_turn(-90, TurnSpeed.PRECISE)
    left_arm_up(300, ArmSpeed.DELICATE)
    wait(1000)
    left_arm_down(270, ArmSpeed.DELICATE)
    spin_turn(90, TurnSpeed.PRECISE)
    move_straight_gyro(-150, DriveSpeed.PUSHING)
    move_straight_gyro(-180, DriveSpeed.PRECISE)
    spin_turn(-90, TurnSpeed.PRECISE)
    move_straight_gyro(-680, DriveSpeed.PUSHING)
    
#Align at square 2
def missions12Pull():
    #reset_arms()
    move_straight_gyro(450, DriveSpeed.PUSHING)
    right_arm_down(90, ArmSpeed.COLLECT)
    wait(500)
    move_straight_gyro(-50, DriveSpeed.PUSHING)
    right_arm_up(90, ArmSpeed.COLLECT)
    move_straight_gyro(-350, DriveSpeed.PUSHING)


#Align at square 6
def missions12Push():
    #reset_arms()
    move_straight_gyro(550, DriveSpeed.PUSHING)
    move_straight_gyro(135, DriveSpeed.PRECISE)
    move_straight_gyro(-100, DriveSpeed.RETURN)


def boulder_mission():
    move_straight_gyro(650, DriveSpeed.PUSHING)
    left_arm_up(90, ArmSpeed.DELICATE)
    move_straight_gyro(-650, DriveSpeed.PUSHING)
    
#Align at square 6 from left
def marketplace_flippy_and_boulder_mission():
    move_straight_gyro(590, DriveSpeed.PUSHING)
    move_straight_gyro(-100, DriveSpeed.PUSHING)
    spin_turn(-15, TurnSpeed.ALIGNMENT)
    move_straight_gyro(200, DriveSpeed.PRECISE)
    right_arm_down(70, ArmSpeed.DELICATE)
    #move_straight_gyro(-710, DriveSpeed.PUSHING)


if __name__ == "__main__":
    """
    Main execution - run different demos
    """
    #missions1and2()
    #mission1_Part2
    #missions3()
    #missions12Pull()
    #missions12Push()
    marketplace_flippy_and_boulder_mission()