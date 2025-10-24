#!/usr/bin/env pybricks-micropython
"""
MOVEMENT DEMONSTRATION - FLL 2025 Unearthed
============================================

Demonstrates all movement functions with DriveSpeed categories:
- Straight movement (open-loop)
- Straight movement with gyro (closed-loop)
- Speed categories (PRECISE, APPROACH, COLLECTION, TRANSIT, RETURN, PUSHING)
- Sensor-based movement (line following, distance sensing)

Perfect for understanding robot movement capabilities!
"""

from robot import (
    # Movement functions
    move_straight,
    move_straight_gyro,
    turn,
    spin_turn,
    pivot_turn,
    tank_move,
    move_until_line,
    move_until_distance,
    push_until_resistance,

    # Speed constants
    DriveSpeed,
    TurnSpeed,

    # Utilities
    wait,
    check_battery,
    calibrate_gyro,
    hub,
    Port,
)


def demo_basic_movement():
    """Demo 1: Basic straight movement"""
    print("\n=== BASIC MOVEMENT DEMO ===")

    print("1. Forward 300mm at default speed")
    move_straight(300)
    wait(1000)

    print("2. Backward 300mm at default speed")
    move_straight(-300)
    wait(1000)

    print("3. Forward 500mm at TRANSIT speed")
    move_straight(500, DriveSpeed.TRANSIT)
    wait(1000)

    print("4. Backward 500mm at RETURN speed")
    move_straight(-500, DriveSpeed.RETURN)
    wait(1000)

    print("\n=== BASIC MOVEMENT COMPLETE ===")


def demo_speed_categories():
    """Demo 2: Compare all DriveSpeed categories"""
    print("\n=== DRIVESPEED CATEGORIES ===")

    speeds = [
        ("PRECISE", DriveSpeed.PRECISE, "Slow & accurate"),
        ("APPROACH", DriveSpeed.APPROACH, "Moderate speed"),
        ("COLLECTION", DriveSpeed.COLLECTION, "Good balance"),
        ("TRANSIT", DriveSpeed.TRANSIT, "Fast movement"),
        ("RETURN", DriveSpeed.RETURN, "Maximum speed"),
        ("PUSHING", DriveSpeed.PUSHING, "High power"),
    ]

    for name, speed, description in speeds:
        print(f"\n{name} ({speed} mm/s) - {description}")
        move_straight(300, speed)
        wait(1000)
        move_straight(-300, DriveSpeed.RETURN)  # Quick return
        wait(500)

    print("\n=== SPEED DEMO COMPLETE ===")


def demo_gyro_movement():
    """Demo 3: Gyro-corrected vs open-loop movement"""
    print("\n=== GYRO CORRECTION DEMO ===")

    # Test 1: Open-loop (may drift)
    print("1. Open-loop movement (no gyro)")
    hub.imu.reset_heading(0)
    wait(100)
    move_straight(800, DriveSpeed.TRANSIT)
    wait(500)
    drift_1 = hub.imu.heading()
    print(f"   Heading drift: {drift_1}°")
    move_straight(-800, DriveSpeed.RETURN)
    wait(1000)

    # Test 2: Gyro-corrected (stays straight)
    print("2. Gyro-corrected movement (with feedback)")
    hub.imu.reset_heading(0)
    wait(100)
    move_straight_gyro(800, DriveSpeed.TRANSIT)
    wait(500)
    drift_2 = hub.imu.heading()
    print(f"   Heading drift: {drift_2}°")
    move_straight_gyro(-800, DriveSpeed.RETURN)
    wait(1000)

    # Summary
    print(f"\nDrift Comparison:")
    print(f"  Without gyro: {drift_1}°")
    print(f"  With gyro:    {drift_2}°")
    print(f"  Improvement:  {abs(drift_1) - abs(drift_2)}°")

    print("\n=== GYRO DEMO COMPLETE ===")


def demo_precision_movement():
    """Demo 4: Precision movement patterns"""
    print("\n=== PRECISION MOVEMENT DEMO ===")

    print("1. Precise approach pattern")
    print("   - Fast transit")
    move_straight_gyro(600, DriveSpeed.TRANSIT)
    wait(500)

    print("   - Slow down for approach")
    move_straight_gyro(200, DriveSpeed.APPROACH)
    wait(500)

    print("   - Final precise positioning")
    move_straight(50, DriveSpeed.PRECISE)
    wait(1000)

    print("2. Quick return")
    move_straight(-850, DriveSpeed.RETURN)

    print("\n=== PRECISION DEMO COMPLETE ===")


def demo_tank_movement():
    """Demo 5: Tank-style controls"""
    print("\n=== TANK MOVEMENT DEMO ===")

    print("1. Forward (both wheels same speed)")
    tank_move(50, 50, 2000)
    wait(500)

    print("2. Spin right (wheels opposite)")
    tank_move(30, -30, 1000)
    wait(500)

    print("3. Curve right (right wheel slower)")
    tank_move(50, 20, 2000)
    wait(500)

    print("4. Curve left (left wheel slower)")
    tank_move(20, 50, 2000)
    wait(500)

    print("5. Backward")
    tank_move(-50, -50, 2000)
    wait(500)

    print("\n=== TANK DEMO COMPLETE ===")


def demo_square_pattern():
    """Demo 6: Drive in square pattern"""
    print("\n=== SQUARE PATTERN DEMO ===")

    for i in range(4):
        print(f"Side {i+1}/4")
        # Drive forward with gyro
        move_straight_gyro(400, DriveSpeed.COLLECTION)
        wait(500)

        # Turn 90 degrees
        spin_turn(90, TurnSpeed.PRECISE)
        wait(500)

    print("Square complete!")
    print("\n=== SQUARE DEMO COMPLETE ===")


def demo_figure_eight():
    """Demo 7: Figure-8 pattern using curves"""
    print("\n=== FIGURE-8 PATTERN DEMO ===")

    print("Drawing figure-8...")

    # First loop
    print("First loop")
    for _ in range(2):
        tank_move(50, 25, 1500)  # Curve right
        wait(100)

    # Second loop (opposite direction)
    print("Second loop")
    for _ in range(2):
        tank_move(25, 50, 1500)  # Curve left
        wait(100)

    print("Figure-8 complete!")
    print("\n=== FIGURE-8 DEMO COMPLETE ===")


def demo_sensor_movement():
    """Demo 8: Sensor-based movement (if sensors connected)"""
    print("\n=== SENSOR MOVEMENT DEMO ===")

    try:
        print("1. Move until line detected")
        print("   (Connect color sensor to Port E)")
        print("   Starting in 3 seconds...")
        wait(3000)

        result = move_until_line(
            speed=DriveSpeed.APPROACH,
            sensor_port=Port.E,
            target_reflection=20,
            timeout_ms=5000
        )

        if result:
            print("   ✓ Line detected!")
        else:
            print("   ✗ No line found (timeout)")

        wait(1000)

    except Exception as e:
        print(f"   Color sensor not available: {e}")

    try:
        print("2. Move until distance sensor detects object")
        print("   (Connect ultrasonic sensor to Port F)")
        print("   Starting in 3 seconds...")
        wait(3000)

        result = move_until_distance(
            speed=DriveSpeed.APPROACH,
            sensor_port=Port.F,
            target_distance_mm=100,
            timeout_ms=5000
        )

        if result:
            print("   ✓ Object detected!")
        else:
            print("   ✗ No object found (timeout)")

        wait(1000)

    except Exception as e:
        print(f"   Distance sensor not available: {e}")

    print("\n=== SENSOR DEMO COMPLETE ===")


def demo_push_until_resistance():
    """Demo 9: Push until hitting resistance"""
    print("\n=== PUSH RESISTANCE DEMO ===")

    print("Place object 20cm ahead")
    print("Starting in 3 seconds...")
    wait(3000)

    result = push_until_resistance(
        distance_mm=300,
        speed=DriveSpeed.PUSHING,
        load_threshold=75,
        timeout_ms=5000
    )

    print(f"\nStopped: {result['stopped_reason']}")
    print(f"Distance: {result['distance_traveled']}mm")
    print(f"Load: {result['final_load']}%")

    if result['stopped_reason'] == 'resistance':
        print("✓ Resistance detected!")
        # Back away
        move_straight(-100, DriveSpeed.PRECISE)
    else:
        print("No resistance detected")

    print("\n=== PUSH DEMO COMPLETE ===")


def demo_speed_vs_accuracy():
    """Demo 10: Speed vs accuracy tradeoff"""
    print("\n=== SPEED VS ACCURACY TEST ===")

    test_distance = 500  # mm

    speeds = [
        ("PRECISE", DriveSpeed.PRECISE),
        ("APPROACH", DriveSpeed.APPROACH),
        ("COLLECTION", DriveSpeed.COLLECTION),
        ("TRANSIT", DriveSpeed.TRANSIT),
    ]

    print(f"Target distance: {test_distance}mm")
    print("Measure actual distance traveled for each speed\n")

    for name, speed in speeds:
        print(f"{name} ({speed} mm/s)")
        print("Mark start position. Press to continue...")
        wait(3000)

        # Move forward
        move_straight_gyro(test_distance, speed)
        print(f"Measure distance now. Target: {test_distance}mm")
        wait(5000)

        # Return
        print("Returning...")
        move_straight_gyro(-test_distance, DriveSpeed.RETURN)
        wait(2000)

    print("\n=== ACCURACY TEST COMPLETE ===")


def mission_complete_navigation():
    """Demo 11: Complete navigation mission"""
    print("\n=== COMPLETE NAVIGATION MISSION ===")

    # Check battery
    voltage, ok = check_battery()
    if not ok:
        print("Battery low! Charge first.")
        return False

    # Calibrate gyro
    print("Calibrating gyro...")
    if not calibrate_gyro():
        print("Gyro calibration failed!")
        return False

    # === Mission Start ===
    print("\nMission starting...")

    # Phase 1: Fast transit
    print("Phase 1: Transit to area")
    move_straight_gyro(800, DriveSpeed.TRANSIT)
    spin_turn(45, TurnSpeed.PRECISE)
    wait(500)

    # Phase 2: Approach mission
    print("Phase 2: Approach mission")
    move_straight_gyro(500, DriveSpeed.APPROACH)
    spin_turn(45, TurnSpeed.PRECISE)
    wait(500)

    # Phase 3: Precise positioning
    print("Phase 3: Final positioning")
    move_straight(200, DriveSpeed.APPROACH)
    move_straight(50, DriveSpeed.PRECISE)
    wait(1000)

    # Phase 4: Execute (simulated)
    print("Phase 4: Execute mission")
    wait(2000)

    # Phase 5: Return home
    print("Phase 5: Return home")
    spin_turn(-90, TurnSpeed.QUICK)
    move_straight_gyro(-1550, DriveSpeed.RETURN)

    print("\n✓ MISSION COMPLETE!")
    return True


if __name__ == "__main__":
    """
    Main execution - run different demos
    Uncomment the demo you want to run!
    """

    print("=================================")
    print("MOVEMENT DEMONSTRATION")
    print("=================================")

    # Demo 1: Basic movement
    # demo_basic_movement()

    # Demo 2: Speed categories
    # demo_speed_categories()

    # Demo 3: Gyro correction
    # demo_gyro_movement()

    # Demo 4: Precision patterns
    # demo_precision_movement()

    # Demo 5: Tank controls
    # demo_tank_movement()

    # Demo 6: Square pattern
    # demo_square_pattern()

    # Demo 7: Figure-8 pattern
    # demo_figure_eight()

    # Demo 8: Sensor-based movement
    # demo_sensor_movement()

    # Demo 9: Push until resistance
    # demo_push_until_resistance()

    # Demo 10: Speed vs accuracy
    # demo_speed_vs_accuracy()

    # Demo 11: Complete mission
    mission_complete_navigation()

    print("\n=================================")
    print("DEMO COMPLETE!")
    print("=================================")
