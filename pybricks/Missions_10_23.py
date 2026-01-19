from robot import *

run_missions = False

#start on the 6 squares from the left
def mission1_Brush_2MapReveal():
    #reset_arms()
    move_straight_gyro(740, DriveSpeed.PUSHING)
    left_arm_up(240, ArmSpeed.COLLECT)
    wait(500)
    move_straight_gyro(-10, DriveSpeed.PUSHING)
    spin_turn(-45)
    move_straight_gyro(90, DriveSpeed.PRECISE)
    move_straight_gyro(-90, DriveSpeed.PRECISE)
    spin_turn(45)
    move_straight_gyro(-650, DriveSpeed.PUSHING)

#start on the 12 squares from the left
def mission1_Brush_Pull():
    move_straight_gyro(445, DriveSpeed.PUSHING)
    move_straight_gyro(180, DriveSpeed.PRECISE)
    spin_turn(-90)
    move_straight_gyro(90, DriveSpeed.PRECISE)
    left_arm_up(180, ArmSpeed.COLLECT)
    wait(500)
    move_straight_gyro(-90, DriveSpeed.PRECISE)
    spin_turn(90)
    move_straight_gyro(-580, DriveSpeed.PUSHING)

#align at square 6
def missions3_Minecart_Push():
    move_straight_gyro(300, DriveSpeed.PUSHING)
    move_straight_gyro(120, DriveSpeed.PRECISE)
    spin_turn(50, TurnSpeed.PRECISE)
    move_straight_gyro(200, DriveSpeed.PUSHING)
    move_straight_gyro(180, DriveSpeed.PRECISE)
    #spin_turn(-90, TurnSpeed.PRECISE)
    left_arm_up(300, ArmSpeed.DELICATE)
    wait(1000)
    left_arm_down(270, ArmSpeed.DELICATE)
    move_straight_gyro(-250, DriveSpeed.PUSHING)
    #move_straight_gyro(-80, DriveSpeed.PRECISE)
    spin_turn(-45, TurnSpeed.PRECISE)
    move_straight_gyro(-350, DriveSpeed.PUSHING)
    
#Align at square 1 - 7 seconds
def missions12_Ship_Sand_Pull():
    move_straight_gyro(325, DriveSpeed.PUSHING)
    move_straight_gyro(100, DriveSpeed.PRECISE)
    right_arm_down(400, ArmSpeed.COLLECT)
    wait(500)
    move_straight_gyro(-50, DriveSpeed.PUSHING)
    right_arm_up(90, ArmSpeed.COLLECT)
    move_straight_gyro(-250, DriveSpeed.PUSHING)


#Align at square 7 - 12 seconds
def missions12_Ship_Push():
    #reset_arms()
    move_straight_gyro(550, DriveSpeed.PUSHING)
    move_straight_gyro(135, DriveSpeed.PRECISE)
    wait(200)
    move_straight_gyro(-50, DriveSpeed.RETURN)
    spin_turn(-60)
    move_straight_gyro(50, DriveSpeed.RETURN)
    spin_turn(62)
    move_straight_gyro(950, DriveSpeed.RETURN)
    #spin_turn(10)
    #move_straight_gyro(450, DriveSpeed.RETURN)

#Not being used currently
def boulder_mission():
    move_straight_gyro(650, DriveSpeed.PUSHING)
    left_arm_up(90, ArmSpeed.DELICATE)
    move_straight_gyro(-650, DriveSpeed.PUSHING)
    
#Align at square 5 from left
def mission5_StructureFloor():
    
    move_straight_gyro(610, DriveSpeed.PUSHING)
    wait(500)
    #move_straight_gyro(-100, DriveSpeed.PRECISE)
    #spin_turn(-90, TurnSpeed.PRECISE)
    #move_straight_gyro(10, DriveSpeed.PRECISE)
    #spin_turn(+90, TurnSpeed.PRECISE)
    move_straight_gyro(40, DriveSpeed.PRECISE)
    left_arm_down(160, ArmSpeed.DELICATE)
    left_arm_up(160, ArmSpeed.DELICATE)
    move_straight_gyro(-260, DriveSpeed.RETURN)
    spin_turn(-45, TurnSpeed.QUICK)
    move_straight_gyro(-300, DriveSpeed.RETURN)
    
#Align at square 6 from left
def mission9_Market_Raise():
    move_straight_gyro(330, DriveSpeed.APPROACH)
    turn(-60)
    move_straight_gyro(115, DriveSpeed.PRECISE)
    left_arm_down(100, ArmSpeed.QUICK)
    move_straight_gyro(-300, DriveSpeed.RETURN)

#Align at square 6 from left
def mission10_Scale_Down():
    move_straight_gyro(410, DriveSpeed.TRANSIT)
    wait(200)
    move_straight_gyro(100, DriveSpeed.PRECISE)
    turn(-45, TurnSpeed.PRECISE)
    move_straight_gyro(230, DriveSpeed.TRANSIT)     
    wait(200)
    turn(-45, TurnSpeed.PRECISE)
    move_straight_gyro(250, DriveSpeed.PRECISE)     
    turn(-90, TurnSpeed.PRECISE)
    move_straight_gyro(-45, DriveSpeed.PRECISE)
    left_arm_down(300, ArmSpeed.PUSH)
    left_arm_up(300, ArmSpeed.PUSH)
    move_straight_gyro(-25, DriveSpeed.PRECISE)
    turn(-50, TurnSpeed.PRECISE)
    move_straight_gyro(300, DriveSpeed.PRECISE)
    wait(200)
    move_straight_gyro(-120, DriveSpeed.PRECISE)
    turn(-45, TurnSpeed.PRECISE)
    move_straight_gyro(200, DriveSpeed.RETURN)
    turn(60, TurnSpeed.PRECISE)
    move_straight_gyro(600, DriveSpeed.RETURN)

#Align at 3 squares from left    
def mission7_HeavyLifting():
    move_straight_gyro(640, DriveSpeed.APPROACH)
    move_straight_gyro(100, DriveSpeed.PRECISE)
    spin_turn(49, TurnSpeed.ALIGNMENT)
    wait(500)
    left_arm_down(180, ArmSpeed.QUICK)
    left_arm_up(150, ArmSpeed.QUICK)
    right_arm_down(425, ArmSpeed.DELICATE)
    wait(500)
    move_straight_gyro(-40, DriveSpeed.PRECISE)
    right_arm_up(180, ArmSpeed.DELICATE)
    spin_turn(120, 10)
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
def mission10_Pan_Pull():
    move_straight_gyro(200, DriveSpeed.APPROACH)
    move_straight_gyro(125, DriveSpeed.PRECISE)
    spin_turn(-90, TurnSpeed.ALIGNMENT)
    move_straight_gyro(250, DriveSpeed.PRECISE)
    right_arm_down(425, ArmSpeed.DELICATE)
    spin_turn(-90, TurnSpeed.ALIGNMENT)
    move_straight_gyro(70, DriveSpeed.PRECISE)
    spin_turn(-90, 10)
    move_straight_gyro(300, DriveSpeed.APPROACH)

#Align at square 10 from Left
def mission8_Silo():
    move_straight_gyro(300, DriveSpeed.APPROACH)
    wait(100)
    move_straight_gyro(70, DriveSpeed.PRECISE)
    for _ in range(4):
        left_arm_down(300, ArmSpeed.QUICK)
        left_arm_up(300, ArmSpeed.QUICK)
    move_straight_gyro(-300, DriveSpeed.APPROACH)

def run_missions_with_buttons():
    # mission_list = [mission1, mission2, mission3] # Your actual mission functions/files
    mission_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B"] # Placeholder for demonstration

    # --- Main Menu Logic ---
    active_index = 0

    print(f"Length: {len(mission_list)}")


    while True:
        # Display current selection (optional, could use hub.display)
        #print(f"Selected: {mission_list[active_index]}") # Or hub.display.text(...)

        # Check for button presses
        pressed_buttons = hub.buttons.pressed()

        if Button.LEFT in pressed_buttons:
            print("******************************************")
            print("Left button pressed")
            if active_index > 0:
                active_index = (active_index - 1) # Move left, wrap around
            hub.display.text(mission_list[active_index])
            hub.light.on(Color.YELLOW) # Feedback
            print(f"Mission changed to {mission_list[active_index]}...")
        elif Button.RIGHT in pressed_buttons:
            print("******************************************")
            print("Right button pressed")
            if active_index < len(mission_list) - 1:
                active_index = (active_index + 1) # Move right, wrap around
            hub.display.text(mission_list[active_index])
            hub.light.on(Color.ORANGE) # Feedback
            print(f"Mission changed to {mission_list[active_index]}...")
        elif Button.CENTER in pressed_buttons:
            print("******************************************")
            print("Center button pressed - launching mission")
            hub.display.text(mission_list[active_index])
            print(f"Starting {mission_list[active_index]}...")
            mission_function_name = f"mission_{mission_list[active_index]}"
            if mission_function_name in globals():
                mission_function = globals().get(f"mission_{mission_list[active_index]}")
                hub.light.on(Color.GREEN) # Feedback
                # Call the actual mission program
                mission_function()
                #Increment to next mission after completion
                active_index = active_index + 1
                #Show next mission on hub display
                hub.display.text(mission_list[active_index])
            else:
                print(f"Mission function {mission_function_name} not found.")
                hub.display.text("E")
                hub.light.on(Color.RED) # Feedback

        # Small delay to prevent rapid-fire button reads (optional but good practice)
        wait(20) # milliseconds

def mission_1():
    print("Running mission 1")
    if run_missions == True:
        mission1_Brush_2MapReveal()

def mission_2():
    print("Running mission 2")
    if run_missions == True:
        mission1_Brush_Pull()

def mission_3():
    print("Running mission 3")
    if run_missions == True:
        missions3_Minecart_Push()

def mission_4():
    print("Running mission 4")
    if run_missions == True:
        missions12_Ship_Sand_Pull()

def mission_5():
    print("Running mission 5")
    if run_missions == True:
        missions12_Ship_Push()

def mission_6():
    print("Running mission 6")
    if run_missions == True:
        mission7_HeavyLifting()

def mission_7():
    print("Running mission 7")
    if run_missions == True:
        mission5_StructureFloor()

def mission_8():
    print("Running mission 8")
    if run_missions == True:
        mission9_Market_Raise()

def mission_9():
    print("Running mission 9")
    if run_missions == True:
        mission8_Silo()

def mission_A():
    print("Running mission A")
    if run_missions == True:
        mission10_Scale_Down()

def mission_B():
    print("Running mission B")
    if run_missions == True:
        mission10_Pan_Pull()


def wait_for_launch():
    # Clear any previous button presses
    while hub.buttons.pressed():
        wait(10)
    # Wait until a button is pressed to start
    while not hub.buttons.pressed():
        wait(10)
    # Wait for release to prevent accidental double-starts
    while hub.buttons.pressed():
        wait(10)

def launch_missions():
    mission_1()
    wait_for_launch()
    mission_2()
    wait_for_launch()
    mission_3()

if __name__ == "__main__":
    """
    Main execution - run different demos
    """
    hub = PrimeHub()

    hub.light.on(Color.BLUE) # Indicate menu is ready

    # Configure the stop button combination. Now, your program stops
    # if you press the center and Bluetooth buttons simultaneously.
    hub.system.set_stop_button((Button.CENTER, Button.BLUETOOTH))
    # Now we can use the center button as a normal button.

    # test changing missions by pressing left, and right and launching by center button
    run_missions_with_buttons()

    #launch_missions()

    #hub.display.text("W")
    #check_battery()
    #******************
    # Left Side Missions - 52 seconds without attachment change or alignments
    # 5 missions - 4 attachment changes or alignments
    #******************
    #hub.display.text("1")
    
    #start on the 6 squares from the left - 11 seconds
    #mission1_Brush_2MapReveal()

    #start on the 12 squares from the left - 10 seconds
    #mission1_Brush_Pull()
    
    #align at square 6 - 12 seconds
    #missions3_Minecart_Push()
    
    #Align at square 1 - 7 seconds
    #missions12_Ship_Sand_Pull()
    
    #Align at square 7 - 12 seconds
    #missions12_Ship_Push()

    #******************
    # Right Side Missions - 80 seconds without attachment change or alignments
    # 6 missions - 6 attachment changes or alignments
    #******************

    #Align at 3 squares from left  - 15 seconds  
    #mission7_HeavyLifting()

    #Align at square 5 from left - 10 seconds
    #mission5_StructureFloor()
    
    #Align at square 6 from left - 7 seconds
    #mission9_Market_Raise()
        
    #Align at square 10 form Left - 11 seconds
    #mission8_Silo()
    
    #Align at square 6 from left - 25 seconds
    #mission10_Scale_Down()
    
    #Align at square 6 from left - 12 seconds
    #mission10_Pan_Pull()
