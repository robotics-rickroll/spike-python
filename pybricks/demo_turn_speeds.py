#!/usr/bin/env pybricks-micropython
"""
TURN SPEED DEMONSTRATION - FLL 2025 Unearthed
=============================================

Demonstrates the TurnSpeed class with different turn scenarios:
- Precise alignment turns
- Standard mission turns
- Quick repositioning turns
- Comparison of turn methods (turn, spin_turn, pivot_turn)

Perfect for understanding when to use each turn speed!
"""

from robot import (
    # Movement functions
    move_straight,
    move_straight_gyro,
    turn,
    spin_turn,
    pivot_turn,

    # Speed constants
    DriveSpeed,
    TurnSpeed,
    ArmSpeed,

    # Utilities
    wait,
    check_battery,
    hub,
)


def demo_turn_speeds():
    """Demo 1: Compare all TurnSpeed categories"""
    print("\n=== TURN SPEED COMPARISON ===")

    turn_speeds = [
        ("ALIGNMENT", TurnSpeed.ALIGNMENT, "Ultra-precise"),
        ("PRECISE", TurnSpeed.PRECISE, "High precision"),
        ("STANDARD", TurnSpeed.STANDARD, "Balanced"),
        ("APPROACH", TurnSpeed.APPROACH, "Fast approach"),
        ("QUICK", TurnSpeed.QUICK, "Quick reposition"),
        ("REPOSITION", TurnSpeed.REPOSITION, "Maximum speed"),
    ]

    for name, speed, description in turn_speeds:
        print(f"\n{name} ({speed} deg/s) - {description}")

        # Reset heading
        hub.imu.reset_heading(0)
        wait(500)

        # Perform 90° turn
        turn(90, speed)
        wait(1000)

        # Check actual angle
        actual_angle = hub.imu.heading()
        error = abs(90 - actual_angle)
        print(f"  Target: 90°, Actual: {actual_angle}°, Error: {error}°")

        # Return to start
        turn(-90, TurnSpeed.STANDARD)
        wait(1000)

    print("\n=== COMPARISON COMPLETE ===")


def demo_precision_turns():
    """Demo 2: High-precision turns with spin_turn()"""
    print("\n=== PRECISION TURNS (spin_turn) ===")

    # Ultra-precise alignment
    print("1. Ultra-precise alignment (ALIGNMENT)")
    spin_turn(90, TurnSpeed.ALIGNMENT)
    wait(1000)

    print("2. High precision turn (PRECISE)")
    spin_turn(90, TurnSpeed.PRECISE)
    wait(1000)

    print("3. Standard speed turn (STANDARD)")
    spin_turn(90, TurnSpeed.STANDARD)
    wait(1000)

    # Return to start
    print("4. Returning to start")
    spin_turn(-270, TurnSpeed.REPOSITION)

    print("\n=== PRECISION DEMO COMPLETE ===")


def demo_turn_methods():
    """Demo 3: Compare turn(), spin_turn(), pivot_turn()"""
    print("\n=== TURN METHODS COMPARISON ===")

    # Test 1: Regular turn (open-loop)
    print("1. Regular turn() - Open loop, fast")
    hub.imu.reset_heading(0)
    wait(100)
    turn(90, TurnSpeed.STANDARD)
    wait(1000)
    error_1 = abs(90 - hub.imu.heading())
    print(f"   Error: {error_1}°")

    # Test 2: Spin turn (IMU-based)
    print("2. spin_turn() - IMU feedback, precise")
    hub.imu.reset_heading(0)
    wait(100)
    final_angle = spin_turn(90, TurnSpeed.PRECISE)
    wait(1000)
    error_2 = abs(90 - final_angle)
    print(f"   Error: {error_2}°")

    # Test 3: Pivot turn (one wheel)
    print("3. pivot_turn() - Tight radius")
    hub.imu.reset_heading(0)
    wait(100)
    pivot_turn(90, TurnSpeed.PIVOT)
    wait(1000)
    error_3 = abs(90 - hub.imu.heading())
    print(f"   Error: {error_3}°")

    # Summary
    print("\nAccuracy Summary:")
    print(f"  turn():       ±{error_1}° (fastest, least accurate)")
    print(f"  spin_turn():  ±{error_2}° (slowest, most accurate)")
    print(f"  pivot_turn(): ±{error_3}° (tight space, moderate accuracy)")

    print("\n=== METHOD COMPARISON COMPLETE ===")


def mission_mixed_turn_speeds():
    """Demo 4: Complete mission using different turn speeds"""
    print("\n=== MIXED TURN SPEED MISSION ===")

    # Check battery
    voltage, ok = check_battery()
    if not ok:
        print("Battery low!")
        return False

    # Phase 1: Fast transit
    print("Phase 1: Fast transit to mission area")
    move_straight_gyro(600, DriveSpeed.TRANSIT)
    turn(90, TurnSpeed.APPROACH)  # Fast approach turn
    wait(500)

    # Phase 2: Approach mission
    print("Phase 2: Approaching mission model")
    move_straight_gyro(400, DriveSpeed.APPROACH)
    spin_turn(45, TurnSpeed.PRECISE)  # Now need precision
    wait(500)

    # Phase 3: Final alignment
    print("Phase 3: Final precise alignment")
    move_straight(150, DriveSpeed.PRECISE)
    spin_turn(30, TurnSpeed.ALIGNMENT)  # Critical alignment!
    wait(500)

    # Phase 4: Execute mission (simulated)
    print("Phase 4: Execute mission")
    wait(2000)

    # Phase 5: Quick return
    print("Phase 5: Quick return to base")
    turn(180, TurnSpeed.QUICK)  # Fast 180
    move_straight_gyro(-1200, DriveSpeed.RETURN)

    print("\n✓ MISSION COMPLETE!")
    return True


def test_turn_accuracy():
    """Demo 5: Test turn accuracy with verification"""
    print("\n=== TURN ACCURACY TEST ===")

    angles_to_test = [45, 90, 180, -45, -90]

    for angle in angles_to_test:
        print(f"\nTesting {angle}° turn:")

        # Reset IMU
        hub.imu.reset_heading(0)
        wait(100)

        # Perform turn
        final_angle = spin_turn(angle, TurnSpeed.PRECISE)

        # Calculate error
        error = abs(angle - final_angle)

        # Report
        status = "✓ PASS" if error < 3 else "✗ FAIL"
        print(f"  Target:  {angle}°")
        print(f"  Actual:  {final_angle}°")
        print(f"  Error:   {error}°")
        print(f"  Status:  {status}")

        wait(1000)

        # Return to zero
        spin_turn(-final_angle, TurnSpeed.STANDARD)
        wait(1000)

    print("\n=== ACCURACY TEST COMPLETE ===")


def demo_space_constrained():
    """Demo 6: Pivot turns for tight spaces"""
    print("\n=== SPACE-CONSTRAINED TURNS ===")

    print("Simulating tight space navigation...")

    # Scenario: Robot needs to turn in tight corner
    print("1. Standard turn (needs ~30cm diameter)")
    turn(90, TurnSpeed.STANDARD)
    wait(1000)

    print("2. Pivot turn (needs ~15cm diameter)")
    pivot_turn(90, TurnSpeed.PIVOT)
    wait(1000)

    print("Pivot turn = Half the space needed!")

    # Return
    spin_turn(-180, TurnSpeed.QUICK)

    print("\n=== SPACE DEMO COMPLETE ===")


def demo_adaptive_turns():
    """Demo 7: Adaptive turn speed based on conditions"""
    print("\n=== ADAPTIVE TURN SELECTION ===")

    def select_turn_speed(precision_needed, time_critical):
        """Smart turn speed selection"""
        if precision_needed == "high":
            return TurnSpeed.ALIGNMENT
        elif precision_needed == "medium":
            return TurnSpeed.PRECISE
        elif time_critical:
            return TurnSpeed.QUICK
        else:
            return TurnSpeed.STANDARD

    # Test different scenarios
    scenarios = [
        ("Final alignment", "high", False),
        ("Mission approach", "medium", False),
        ("Mid-run reposition", "low", True),
        ("General turn", "low", False),
    ]

    for name, precision, time_critical in scenarios:
        speed = select_turn_speed(precision, time_critical)
        print(f"{name}: {speed} deg/s")

        turn(90, speed)
        wait(1000)
        turn(-90, TurnSpeed.STANDARD)
        wait(500)

    print("\n=== ADAPTIVE DEMO COMPLETE ===")


if __name__ == "__main__":
    """
    Main execution - run different demos
    Uncomment the demo you want to run!
    """

    print("=================================")
    print("TURN SPEED DEMONSTRATION")
    print("=================================")

    # Demo 1: Compare all turn speeds
    # demo_turn_speeds()

    # Demo 2: Precision turns with spin_turn()
    # demo_precision_turns()

    # Demo 3: Compare turn methods
    # demo_turn_methods()

    # Demo 4: Complete mission with mixed speeds
    mission_mixed_turn_speeds()

    # Demo 5: Test turn accuracy
    # test_turn_accuracy()

    # Demo 6: Space-constrained pivots
    # demo_space_constrained()

    # Demo 7: Adaptive turn selection
    # demo_adaptive_turns()

    print("\n=================================")
    print("DEMO COMPLETE!")
    print("=================================")
