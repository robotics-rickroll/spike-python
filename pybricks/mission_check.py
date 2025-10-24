#!/usr/bin/env pybricks-micropython
"""
MISSION CHECK - Competition Readiness Verification
===================================================

**RUN THIS BEFORE EVERY COMPETITION ROUND!**

This file performs essential pre-competition checks to ensure your robot
is ready to run missions. It focuses on critical verifications, not
extensive testing.

Checks performed:
1. Battery voltage (must be >4400mV for reliable operation)
2. Gyro calibration and stability
3. Motor connectivity and response
4. Basic alignment verification
5. Hub status

Time: ~30 seconds (fast enough to run before every round!)

Usage:
    1. Place robot on flat surface in home position
    2. Run this file
    3. Wait for GREEN light = Ready to compete!
    4. RED light = Fix issues before running mission

Created: 2025-10-19
For: FLL teams who need quick, reliable pre-competition verification
"""

from robot import (
    # Core functions
    hub,
    wait,
    Color,

    # Motors
    left_motor,
    right_motor,
    attachment_motor_left,
    attachment_motor_right,

    # Utility functions
    check_battery,
    calibrate_gyro,

    # Speed constants
    DriveSpeed,
    ArmSpeed,
)

# ============================================================================
# CONFIGURATION
# ============================================================================

# Minimum battery voltage for competition (mV)
MIN_BATTERY_VOLTAGE = 4400  # Adjust if needed (4400-4800 mV is typical)

# Gyro stability tolerance (degrees)
GYRO_STABILITY_TOLERANCE = 5  # Robot shouldn't drift more than 5° when stationary

# Motor response test distance (degrees)
MOTOR_TEST_DEGREES = 90

# ============================================================================
# CHECK FUNCTIONS
# ============================================================================

def check_1_battery():
    """
    CHECK 1: Battery Voltage

    Ensures battery has enough charge for reliable operation.
    Low battery = inconsistent motor speeds and sensor readings.

    Returns:
        tuple: (passed, voltage_mv)
    """
    print("\n[1/5] Checking battery voltage...")

    voltage, ok = check_battery()

    if ok:
        print(f"  ✓ Battery OK: {voltage}mV")
        return True, voltage
    else:
        print(f"  ✗ Battery LOW: {voltage}mV (need >{MIN_BATTERY_VOLTAGE}mV)")
        print(f"  → Charge battery before competition!")
        return False, voltage


def check_2_gyro_calibration():
    """
    CHECK 2: Gyro Calibration

    Calibrates the IMU gyro sensor for accurate turning and straight movement.
    Robot MUST be stationary during this check.

    Returns:
        bool: True if calibration successful
    """
    print("\n[2/5] Calibrating gyro sensor...")
    print("  (Robot must be still on flat surface)")

    # Reset and wait for stability
    hub.imu.reset_heading(0)
    wait(1500)  # Give gyro time to settle

    # Check if gyro is stable
    heading = hub.imu.heading()

    if abs(heading) > GYRO_STABILITY_TOLERANCE:
        print(f"  ✗ Gyro UNSTABLE: {heading}° (should be near 0°)")
        print(f"  → Check robot is on flat surface")
        print(f"  → Robot must not be moving")
        return False

    print(f"  ✓ Gyro calibrated: {heading}° (stable)")
    return True


def check_3_motors():
    """
    CHECK 3: Motor Connectivity and Response

    Verifies that drive motors are connected and responding correctly.
    Small test movements ensure motors work before starting mission.

    Returns:
        bool: True if all motors responding
    """
    print("\n[3/5] Checking drive motors...")

    issues = []

    # Test left motor
    try:
        initial_left = left_motor.angle()
        left_motor.run_angle(100, MOTOR_TEST_DEGREES, wait=True)
        final_left = left_motor.angle()
        movement_left = abs(final_left - initial_left)

        if movement_left < MOTOR_TEST_DEGREES - 10:
            issues.append(f"Left motor only moved {movement_left}° (expected {MOTOR_TEST_DEGREES}°)")
        else:
            print(f"  ✓ Left motor OK (moved {movement_left}°)")

    except Exception as e:
        issues.append(f"Left motor error: {e}")

    # Test right motor
    try:
        initial_right = right_motor.angle()
        right_motor.run_angle(100, MOTOR_TEST_DEGREES, wait=True)
        final_right = right_motor.angle()
        movement_right = abs(final_right - initial_right)

        if movement_right < MOTOR_TEST_DEGREES - 10:
            issues.append(f"Right motor only moved {movement_right}° (expected {MOTOR_TEST_DEGREES}°)")
        else:
            print(f"  ✓ Right motor OK (moved {movement_right}°)")

    except Exception as e:
        issues.append(f"Right motor error: {e}")

    # Return motors to original position
    try:
        left_motor.run_angle(-100, MOTOR_TEST_DEGREES, wait=False)
        right_motor.run_angle(-100, MOTOR_TEST_DEGREES, wait=True)
    except:
        pass

    if issues:
        print("  ✗ Motor issues detected:")
        for issue in issues:
            print(f"    - {issue}")
        return False

    return True


def check_4_attachments():
    """
    CHECK 4: Attachment Motors (Optional)

    Checks if attachment motors are connected and responsive.
    This is informational - not required for mission readiness.

    Returns:
        bool: Always True (informational only)
    """
    print("\n[4/5] Checking attachment motors...")

    # Check left attachment
    if attachment_motor_left is not None:
        try:
            initial = attachment_motor_left.angle()
            attachment_motor_left.run_angle(200, 45, wait=True)
            wait(100)
            attachment_motor_left.run_angle(200, -45, wait=True)
            print(f"  ✓ Left attachment OK (Port A)")
        except Exception as e:
            print(f"  ⚠ Left attachment warning: {e}")
    else:
        print(f"  ⚠ No attachment on Port A")

    # Check right attachment
    if attachment_motor_right is not None:
        try:
            initial = attachment_motor_right.angle()
            attachment_motor_right.run_angle(200, 45, wait=True)
            wait(100)
            attachment_motor_right.run_angle(200, -45, wait=True)
            print(f"  ✓ Right attachment OK (Port E)")
        except Exception as e:
            print(f"  ⚠ Right attachment warning: {e}")
    else:
        print(f"  ⚠ No attachment on Port E")

    # Attachments are optional, so always pass
    return True


def check_5_alignment():
    """
    CHECK 5: Alignment Verification

    Final check to ensure robot is in correct starting position.
    This is a visual confirmation - robot should be aligned with
    home area markings on the mat.

    Returns:
        bool: Always True (visual check)
    """
    print("\n[5/5] Alignment verification...")
    print("  ✓ Visual check: Is robot aligned in home area?")
    print("  → Wheels should be straight")
    print("  → Robot should be in starting position")
    print("  → Attachments should be in starting configuration")

    # Visual confirmation with LED
    print("\n  Flashing BLUE for 2 seconds - check alignment now...")
    for _ in range(4):
        hub.light.on(Color.BLUE)
        wait(250)
        hub.light.off()
        wait(250)

    return True


# ============================================================================
# MAIN CHECK ROUTINE
# ============================================================================

def run_competition_check():
    """
    Main competition readiness check routine.

    Runs all 5 checks and reports overall status.

    Returns:
        bool: True if robot is competition ready
    """
    print("=" * 50)
    print("COMPETITION READINESS CHECK")
    print("=" * 50)
    print()
    print("⚠ Important:")
    print("  - Robot must be on FLAT surface")
    print("  - Robot must be STATIONARY")
    print("  - Do NOT touch robot during checks")
    print()
    print("Starting checks in 2 seconds...")
    wait(2000)

    # Track results
    checks_passed = []
    checks_failed = []

    # Run all checks

    # Check 1: Battery
    battery_ok, voltage = check_1_battery()
    if battery_ok:
        checks_passed.append("Battery")
    else:
        checks_failed.append("Battery (charge needed)")

    # Check 2: Gyro
    gyro_ok = check_2_gyro_calibration()
    if gyro_ok:
        checks_passed.append("Gyro")
    else:
        checks_failed.append("Gyro (unstable or moving)")

    # Check 3: Motors
    motors_ok = check_3_motors()
    if motors_ok:
        checks_passed.append("Motors")
    else:
        checks_failed.append("Motors (check connections)")

    # Check 4: Attachments (informational)
    attachments_ok = check_4_attachments()
    if attachments_ok:
        checks_passed.append("Attachments")

    # Check 5: Alignment (visual)
    alignment_ok = check_5_alignment()
    if alignment_ok:
        checks_passed.append("Alignment")

    # Final report
    print("\n" + "=" * 50)
    print("CHECK RESULTS")
    print("=" * 50)

    if checks_failed:
        print(f"\n✗ FAILED CHECKS ({len(checks_failed)}):")
        for check in checks_failed:
            print(f"  ✗ {check}")

        print(f"\n✓ PASSED CHECKS ({len(checks_passed)}):")
        for check in checks_passed:
            print(f"  ✓ {check}")

        print("\n" + "=" * 50)
        print("⚠ ROBOT NOT READY FOR COMPETITION")
        print("=" * 50)
        print("\nFix failed checks before running mission!")

        # Flash RED
        for _ in range(3):
            hub.light.on(Color.RED)
            wait(300)
            hub.light.off()
            wait(300)

        hub.light.on(Color.RED)
        return False

    else:
        print(f"\n✓ ALL CHECKS PASSED ({len(checks_passed)}):")
        for check in checks_passed:
            print(f"  ✓ {check}")

        print("\n" + "=" * 50)
        print("✓✓✓ ROBOT READY FOR COMPETITION! ✓✓✓")
        print("=" * 50)
        print("\nYou may run your mission now!")
        print(f"Battery: {voltage}mV")
        print(f"Gyro: Calibrated")
        print(f"Motors: Responding")

        # Flash GREEN
        for _ in range(5):
            hub.light.on(Color.GREEN)
            wait(200)
            hub.light.off()
            wait(200)

        hub.light.on(Color.GREEN)
        wait(1000)
        hub.light.off()

        return True


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Main execution.

    Run this file before EVERY competition round to verify robot readiness.

    Usage:
        pybricksdev run ble mission_check.py

    Expected time: ~30 seconds
    """
    try:
        ready = run_competition_check()

        if ready:
            print("\n✓ Ready to compete!")
        else:
            print("\n✗ Fix issues before competing")

    except KeyboardInterrupt:
        print("\n\nCheck interrupted by user")
        hub.light.on(Color.ORANGE)

    except Exception as e:
        print(f"\n\nERROR during check: {e}")
        hub.light.on(Color.RED)

    finally:
        print("\nCheck complete.")
