#!/usr/bin/env pybricks-micropython
"""
MISSION.PY - FLL 2025 Unearthed Test Mission
============================================
"""

# Import all robot control functions
from robot import (
    # Core movement functions
    move_straight,
    move_straight_gyro,
    turn,
    spin_turn,
    pivot_turn,
    hub,
    ATTACHMENT_PORT_LEFT,
    ATTACHMENT_PORT_RIGHT,
    LEFT_MOTOR_PORT,
    RIGHT_MOTOR_PORT,

    # Left arm control (Port A)
    left_arm_up,
    left_arm_down,
    left_arm_to,

    # Right arm control (Port E)
    right_arm_up,
    right_arm_down,
    right_arm_to,

    # Both arms control
    both_arms_up,
    both_arms_down,
    reset_arms,

    # Sensor-based movement
    move_until_line,
    move_until_distance,

    # Utility functions
    check_battery,
    calibrate_gyro,
    get_robot_status,
    competition_ready_check,
    safe_move_with_retry,

    # Speed constants for driving/movement
    DriveSpeed,

    # Speed constants for arms/attachments
    ArmSpeed,

    # Hub and tools
    hub,
    wait,
    Port,
    Color,
)

def arm_demo():
    """
    Simple arm test mission demonstrating the new clear arm functions.
    Perfect for 11-year-olds to understand!
    """

    print("=== ARM TEST MISSION ===")
    print("Testing left and right arms separately\n")

    # Reset both arms to starting position
    print("1. Reset both arms to home position")
    reset_arms()
    wait(1000)

    # Test LEFT arm (Port A)
    print("2. Raise LEFT arm 90 degrees")
    left_arm_up(90)
    wait(1000)

    print("3. Lower LEFT arm 90 degrees")
    left_arm_down(90)
    wait(1000)

    # Test RIGHT arm (Port E)
    print("4. Raise RIGHT arm 90 degrees")
    right_arm_up(90)
    wait(1000)

    print("5. Lower RIGHT arm 90 degrees")
    right_arm_down(90)
    wait(1000)

    # Test BOTH arms together
    print("6. Raise BOTH arms 90 degrees")
    both_arms_up(90)
    wait(1000)

    print("7. Lower BOTH arms 90 degrees")
    both_arms_down(90)
    wait(1000)

    # Move arms to specific positions
    print("8. Move LEFT arm to 45 degrees")
    left_arm_to(45)
    wait(1000)

    print("9. Move RIGHT arm to 135 degrees")
    right_arm_to(135)
    wait(1000)

    # Final reset
    print("10. Reset both arms")
    reset_arms()
    wait(1000)

    print("\n=== ARM TEST COMPLETE ===")

if __name__ == "__main__":
    left_arm_up(90,ArmSpeed.PUSH)