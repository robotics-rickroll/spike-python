#!/usr/bin/env pybricks-micropython
"""
ADVANCED ARM CONTROL - Demo of Load Sensing and Adaptive Functions
===================================================================

Demonstrates the new intelligent arm control functions:
- Load sensing and monitoring
- Smart grabbing with load feedback
- Adaptive lifting based on weight
- Stall detection for calibration
- Push until resistance

Perfect for missions with unknown object weights or positions!
"""

from robot import (
    # Core movement
    move_straight,
    move_straight_gyro,
    spin_turn,

    # Basic arms
    reset_arms,
    left_arm_down,
    left_arm_up,

    # Advanced arm control with load sensing
    get_arm_load,
    left_arm_up_monitored,
    right_arm_up_monitored,
    grab_until_load,
    lift_adaptive,
    reset_arm_to_limit,
    push_until_resistance,

    # Speed constants
    DriveSpeed,
    ArmSpeed,

    # Utilities
    wait,
    check_battery,
)


def demo_load_sensing():
    """Demo 1: Check load on arm during movement"""
    print("\n=== Demo 1: Load Sensing ===")

    # Reset arms
    reset_arms()
    wait(500)

    # Lower arm and check load
    left_arm_down(45, ArmSpeed.GRAB)
    wait(500)

    # Get current load
    load = get_arm_load('left')
    print(f"Current left arm load: {load}%")

    # Lift and monitor
    left_arm_up(45, ArmSpeed.GRAB)
    wait(500)

    final_load = get_arm_load('left')
    print(f"Final load after lifting: {final_load}%")


def demo_monitored_lift():
    """Demo 2: Lift with safety cutoff"""
    print("\n=== Demo 2: Monitored Lift (with safety) ===")

    # Try to lift - stops if load exceeds 70%
    result = left_arm_up_monitored(90, ArmSpeed.GRAB, max_load=70)

    if result['success']:
        print(f"✓ Lifted successfully!")
        print(f"  Initial load: {result['initial_load']}%")
        print(f"  Max load:     {result['max_load']}%")
        print(f"  Final load:   {result['final_load']}%")
    else:
        print(f"✗ Load too high! Stopped for safety at {result['final_load']}%")


def demo_smart_grab():
    """Demo 3: Smart grab - detects when object is grabbed"""
    print("\n=== Demo 3: Smart Grab ===")

    # Approach object
    move_straight_gyro(300, DriveSpeed.APPROACH)
    wait(500)

    # Open arms
    reset_arms()
    wait(500)

    # Smart grab - closes until load reaches 40%
    result = grab_until_load(target_load=40, max_degrees=90, arm='left')

    if result['grabbed']:
        print(f"✓ Object grabbed!")
        print(f"  Final load: {result['final_load']}%")
        print(f"  Moved: {result['degrees_moved']}°")

        # Lift the grabbed object
        left_arm_up(30, ArmSpeed.GRAB)
        wait(500)
    else:
        print(f"✗ Nothing grabbed")
        print(f"  Final load: {result['final_load']}%")
        print(f"  Moved: {result['degrees_moved']}°")


def demo_adaptive_lift():
    """Demo 4: Adaptive lifting - speed adjusts to weight"""
    print("\n=== Demo 4: Adaptive Lift ===")

    # First, grab something
    left_arm_down(90, ArmSpeed.GRAB)
    wait(500)

    # Lift adaptively - speed will adjust based on load
    # Heavy object → slower (more torque)
    # Light object → faster (more efficient)
    result = lift_adaptive(90, arm='left')

    if result['success']:
        print(f"✓ Lifted adaptively!")
        print(f"  Average load: {result['avg_load']}%")
        print(f"  Average speed: {result['avg_speed']} deg/s")

        if result['avg_load'] > 60:
            print("  → Heavy object detected (used slower speed)")
        elif result['avg_load'] > 30:
            print("  → Medium object (used medium speed)")
        else:
            print("  → Light object (used faster speed)")


def demo_arm_calibration():
    """Demo 5: Calibrate arm to mechanical limit"""
    print("\n=== Demo 5: Arm Calibration with Stall Detection ===")

    # Find mechanical zero using stall detection
    if reset_arm_to_limit('left'):
        print("✓ Left arm calibrated to mechanical zero!")
        print("  Position is now reliably at 0°")

        # Now we can use absolute positioning confidently
        wait(1000)

        # Move to known positions
        left_arm_up(45, ArmSpeed.GRAB)
        wait(1000)

        left_arm_up(45, ArmSpeed.GRAB)  # Now at 90° from zero
        wait(1000)

        # Return to calibrated zero
        left_arm_down(90, ArmSpeed.GRAB)
    else:
        print("✗ Calibration failed")


def demo_push_until_resistance():
    """Demo 6: Push mission model until resistance"""
    print("\n=== Demo 6: Push Until Resistance ===")

    # Approach mission model
    move_straight_gyro(400, DriveSpeed.APPROACH)
    wait(500)

    # Lower arm to push position
    left_arm_down(45, ArmSpeed.GRAB)
    wait(500)

    # Push until hitting resistance
    result = push_until_resistance(
        distance_mm=200,
        speed=DriveSpeed.PUSHING,
        load_threshold=75
    )

    print(f"Stopped: {result['stopped_reason']}")
    print(f"Distance traveled: {result['distance_traveled']}mm")
    print(f"Final load: {result['final_load']}%")

    if result['stopped_reason'] == 'resistance':
        print("✓ Mission model pushed into place!")
    elif result['stopped_reason'] == 'distance':
        print("Reached max distance")
    else:
        print("Timeout or error")

    # Back away
    move_straight(-50, DriveSpeed.PRECISE)


def mission_adaptive_collection():
    """
    Complete mission: Collect object with adaptive control
    Demonstrates real-world use of load sensing
    """
    print("\n=== ADAPTIVE COLLECTION MISSION ===")

    # Check battery
    voltage, ok = check_battery()
    if not ok:
        print("Battery low! Charge first.")
        return False

    # Calibrate arms to known zero
    print("1. Calibrating arms...")
    reset_arm_to_limit('left')
    reset_arm_to_limit('right')
    wait(1000)

    # Approach collection area
    print("2. Moving to collection area...")
    move_straight_gyro(600, DriveSpeed.TRANSIT)
    spin_turn(45)
    move_straight(200, DriveSpeed.APPROACH)

    # Final precise approach
    print("3. Final approach...")
    move_straight(50, DriveSpeed.PRECISE)
    wait(500)

    # Smart grab with load sensing
    print("4. Attempting smart grab...")
    grab_result = grab_until_load(target_load=35, max_degrees=90, arm='left')

    if not grab_result['grabbed']:
        print("Nothing to collect here!")
        return False

    print(f"✓ Collected! Load: {grab_result['final_load']}%")

    # Adaptive lift based on weight
    print("5. Lifting adaptively...")
    lift_result = lift_adaptive(60, arm='left')

    if lift_result['avg_load'] > 60:
        print("Heavy object - using careful transport")
        transport_speed = DriveSpeed.APPROACH
    else:
        print("Light object - using fast transport")
        transport_speed = DriveSpeed.COLLECTION

    # Transport back
    print("6. Transporting back...")
    spin_turn(-45)
    move_straight_gyro(-800, transport_speed)

    # Release
    print("7. Releasing...")
    left_arm_down(60, ArmSpeed.COLLECT)
    wait(500)

    # Reset
    print("8. Resetting...")
    reset_arms(ArmSpeed.QUICK)

    print("\n✓ MISSION COMPLETE!")
    return True


if __name__ == "__main__":
    """
    Main execution - run different demos
    Uncomment the demo you want to run!
    """

    print("=================================")
    print("ADVANCED ARM CONTROL DEMO")
    print("=================================")

    # Demo 1: Basic load sensing
    # demo_load_sensing()

    # Demo 2: Monitored lift with safety
    # demo_monitored_lift()

    # Demo 3: Smart grab
    # demo_smart_grab()

    # Demo 4: Adaptive lift
    # demo_adaptive_lift()

    # Demo 5: Arm calibration
    # demo_arm_calibration()

    # Demo 6: Push until resistance
    # demo_push_until_resistance()

    # Complete mission
    mission_adaptive_collection()

    print("\n=================================")
    print("DEMO COMPLETE!")
    print("=================================")
