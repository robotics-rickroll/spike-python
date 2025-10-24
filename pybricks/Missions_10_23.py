from robot import *

#start on the 5.75 squares from the left
def missions1and2():
    
    #move_straight_gyro(400, DriveSpeed.PUSHING)
    spin_turn(45, TurnSpeed.PRECISE)
    wait(500)

    #await arm_down(90)
    #await forward(76,1000)
    #await arm_up(90)
    #await backward(75,1000)

async def boulder_mission():
    await forward(65, 700)
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

    print("=================================")
    print("MOVEMENT DEMONSTRATION")
    print("=================================")

    move_straight(200)
    #left_arm_down(90)
    #right_arm_down(90)
    #turn(90)
    #spin_turn(90)
    #pivot_turn(90)
    #missions1and2()
