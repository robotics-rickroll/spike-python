from robot import *

#start on the 6 squares from the left
def missions1and2():
    #reset_arms()
    move_straight_gyro(740, DriveSpeed.PUSHING)
    left_arm_up(240, ArmSpeed.COLLECT)
    wait(500)
    move_straight_gyro(-10, DriveSpeed.PUSHING)
    spin_turn(-45)
    move_straight_gyro(80, DriveSpeed.PRECISE)
    move_straight_gyro(-80, DriveSpeed.PRECISE)
    spin_turn(45)
    move_straight_gyro(-720, DriveSpeed.PUSHING)

#start on the 12 squares from the left
def mission1_Part2():
    move_straight_gyro(445, DriveSpeed.PUSHING)
    move_straight_gyro(180, DriveSpeed.PRECISE)
    spin_turn(-90)
    move_straight_gyro(90, DriveSpeed.PRECISE)
    left_arm_up(180, ArmSpeed.COLLECT)
    wait(500)
    move_straight_gyro(-90, DriveSpeed.PRECISE)
    spin_turn(90)
    move_straight_gyro(-605, DriveSpeed.PUSHING)

#align at square 12
def missions3():
    move_straight_gyro(400, DriveSpeed.PUSHING)
    move_straight_gyro(270, DriveSpeed.PRECISE)
    spin_turn(90, TurnSpeed.PRECISE)
    move_straight_gyro(50, DriveSpeed.PUSHING)
    move_straight_gyro(180, DriveSpeed.PRECISE)
    spin_turn(-90, TurnSpeed.PRECISE)
    left_arm_up(300, ArmSpeed.DELICATE)
    wait(1000)
    left_arm_down(270, ArmSpeed.DELICATE)
    spin_turn(90, TurnSpeed.PRECISE)
    move_straight_gyro(-50, DriveSpeed.PUSHING)
    move_straight_gyro(-180, DriveSpeed.PRECISE)
    spin_turn(-90, TurnSpeed.PRECISE)
    move_straight_gyro(-660, DriveSpeed.PUSHING)
    
#Align at square 1
def missions12Pull():
    move_straight_gyro(325, DriveSpeed.PUSHING)
    move_straight_gyro(100, DriveSpeed.PRECISE)
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
    
    move_straight_gyro(650, DriveSpeed.PUSHING)
    wait(500)
    move_straight_gyro(-100, DriveSpeed.PRECISE)
    spin_turn(-90, TurnSpeed.PRECISE)
    move_straight_gyro(10, DriveSpeed.PRECISE)
    spin_turn(+90, TurnSpeed.PRECISE)
    move_straight_gyro(140, DriveSpeed.PRECISE)
    left_arm_down(135, ArmSpeed.DELICATE)
    move_straight_gyro(-710, DriveSpeed.PUSHING)
    
#Align at square 6 from left
def mission9_hit():
    move_straight_gyro(330, DriveSpeed.APPROACH)
    turn(-60)
    move_straight_gyro(112, DriveSpeed.PRECISE)
    left_arm_down(100, ArmSpeed.DELICATE )
    move_straight_gyro(-400, ArmSpeed.QUICK)

#Align at square 6 from left
def mission9_pull():
    move_straight_gyro(500, DriveSpeed.TRANSIT)
    turn(-50, TurnSpeed.PRECISE)
    move_straight_gyro(430, DriveSpeed.PRECISE)     
    turn(-90, TurnSpeed.PRECISE)
    move_straight_gyro(50, DriveSpeed.PRECISE)
    left_arm_down(300, ArmSpeed.PUSH)
    left_arm_up(300, ArmSpeed.PUSH)
    move_straight_gyro(-20, DriveSpeed.PRECISE)
    turn(-60, TurnSpeed.PRECISE)
    move_straight_gyro(200, DriveSpeed.PRECISE)
    move_straight_gyro(-100, DriveSpeed.PRECISE)
    turn(-45, TurnSpeed.PRECISE)
    move_straight_gyro(280, DriveSpeed.PRECISE)
    turn(45, TurnSpeed.PRECISE)
    move_straight_gyro(500, DriveSpeed.TRANSIT)

#Align at 3 squares from left    
def mission7():
    move_straight_gyro(650, DriveSpeed.APPROACH)
    move_straight_gyro(100, DriveSpeed.PRECISE)
    spin_turn(55, TurnSpeed.ALIGNMENT)
    wait(500)
    right_arm_down(425, ArmSpeed.DELICATE)
    move_straight_gyro(-50, DriveSpeed.PRECISE)
    right_arm_up(180, ArmSpeed.DELICATE)
    spin_turn(100, 10)
    move_straight_gyro(500, DriveSpeed.RETURN)

def DisplayFunctions():
    hub.display.text("Missions 1 and 2")
    # Display a single letter (e.g., 'H')
    hub.display.text("Hello")

    # Display a number (e.g., 42)
    #hub.display.number(42)
    #wait(1000)

    # Display a sequence of characters, one by one
    #hub.display.scroll("HELLO", on=500, off=2000) # on/off duration in ms

#Align at square 6 from left
def mission10_pull():
    move_straight_gyro(200, DriveSpeed.APPROACH)
    move_straight_gyro(125, DriveSpeed.PRECISE)
    spin_turn(-90, TurnSpeed.ALIGNMENT)
    move_straight_gyro(250, DriveSpeed.PRECISE)
    right_arm_down(100, ArmSpeed.DELICATE)
    spin_turn(-90, TurnSpeed.ALIGNMENT)
    move_straight_gyro(70, DriveSpeed.PRECISE)
    spin_turn(-90, 10)
    move_straight_gyro(300, DriveSpeed.APPROACH)

#Align at square 11 form Left or right
def mission8():
    move_straight_gyro(300, DriveSpeed.APPROACH)
    wait(100)
    move_straight_gyro(70, DriveSpeed.PRECISE)
    for _ in range(4):
        left_arm_down(270, ArmSpeed.QUICK)
        left_arm_up(270, ArmSpeed.QUICK)


if __name__ == "__main__":
    """
    Main execution - run different demos
    """
    hub = PrimeHub()
    #hub.display.text("1")
    #missions1and2()
    #hub.display.text("2-1")
    #mission1_Part2()
    #missions3()
    #missions12Pull()
    #missions12Push()

    hub.display.text("67")
    mission8()
    #mission7()
    #marketplace_flippy_and_boulder_mission()
    #mission9_pull()
    #mission10_pull()