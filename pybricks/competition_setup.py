#!/usr/bin/env pybricks-micropython
"""
COMPETITION SETUP - FLL 2025 Unearthed Season
==============================================

Load all competition missions to hub slots for computer-free operation.

**FLL 2025 Unearthed Season Missions**

This file contains mission templates for the 2025 Unearthed season. Customize these
missions based on your team's strategy and robot design.

Competition Workflow:
1. Run this file ONCE before competition to load all missions
2. At competition, use hub buttons to select mission (no computer!)
3. Press center button to run selected mission

Mission Models (2025 Unearthed):
1. Angler Artifacts
2. Tip the Scales
3. Map Reveal
4. Statue Rebuild
5. Surface Brushing
6. Mineshaft Explorer
7. Careful Recovery
8. Forum
9. Site Marking
10. What's on Sale?
11. Who Lived Here?
12. Forge
13. Heavy Lifting
14. Silo
15. Salvage Operation
16. Precision tokens, season tiles, and coach pins

Created: 2025-10-23
For: FLL 2025 Unearthed Season
"""

from mission_loader import (
    register_mission,
    list_missions,
    competition_mode,
    export_mission_list,
    run_mission,
)

# Import robot control functions
from robot import (
    # Movement functions
    move_straight,
    move_straight_gyro,
    turn,
    spin_turn,
    pivot_turn,
    push_until_resistance,

    # Arm functions
    left_arm_up,
    left_arm_down,
    right_arm_up,
    right_arm_down,
    both_arms_up,
    both_arms_down,
    reset_arms,

    # Advanced arm control
    grab_until_load,
    lift_adaptive,

    # Speed constants
    DriveSpeed,
    TurnSpeed,
    ArmSpeed,

    # Utilities
    hub,
    wait,
    Color,
    check_battery,
    calibrate_gyro,
)

# Import mission check
from mission_check import run_competition_check

# ============================================================================
# MISSION CONFIGURATION
# ============================================================================

# Competition settings
RUN_PRE_CHECK = True  # Run mission_check before each mission?
AUTO_CALIBRATE = True  # Auto-calibrate gyro before each mission?

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def pre_mission_setup():
    """
    Standard pre-mission setup.
    Call this at the start of every mission.
    """
    if AUTO_CALIBRATE:
        print("Calibrating gyro...")
        calibrate_gyro()
        wait(500)

    # Check battery (warning only, doesn't stop mission)
    voltage, ok = check_battery()
    if not ok:
        print(f"⚠ Battery low: {voltage}mV")
        hub.light.on(Color.ORANGE)
        wait(1000)


def mission_complete(name):
    """
    Standard mission completion.
    Call this at the end of every mission.
    """
    print(f"✓ {name} complete!")
    hub.light.on(Color.GREEN)
    wait(1000)
    hub.light.off()


# ============================================================================
# MISSION 01: ANGLER ARTIFACTS (LEFT SIDE)
# ============================================================================

def mission_01_angler_artifacts():
    """
    Mission 1: Angler Artifacts

    Strategy:
    - Start from left home area
    - Navigate to artifact site
    - Collect/place angler artifacts
    - Return to base

    Estimated Points: 30-40
    Estimated Time: 25 seconds
    """
    print("Starting Mission 1: Angler Artifacts")
    pre_mission_setup()

    # Reset arms to starting position
    reset_arms()
    wait(500)

    # === PHASE 1: Navigate to Artifact Site ===
    print("Phase 1: Navigate to artifacts")
    move_straight_gyro(450, DriveSpeed.TRANSIT)
    spin_turn(-35, TurnSpeed.PRECISE)
    move_straight_gyro(200, DriveSpeed.APPROACH)

    # === PHASE 2: Collect Artifact ===
    print("Phase 2: Collect artifact")
    move_straight(80, DriveSpeed.PRECISE)
    result = grab_until_load(target_load=35, max_degrees=90, arm='left')

    if result['grabbed']:
        print(f"  Artifact grabbed! Load: {result['final_load']}%")
        lift_adaptive(60, arm='left')
    else:
        left_arm_down(90, ArmSpeed.GRAB)
        wait(500)
        left_arm_up(90, ArmSpeed.GRAB)

    # === PHASE 3: Return to Base ===
    print("Phase 3: Return to base")
    move_straight(-280, DriveSpeed.APPROACH)
    spin_turn(35, TurnSpeed.QUICK)
    move_straight_gyro(-450, DriveSpeed.RETURN)

    # === PHASE 4: Deposit Artifact ===
    print("Phase 4: Deposit artifact")
    left_arm_down(90, ArmSpeed.DELICATE)
    wait(500)

    mission_complete("Angler Artifacts")
    return True


# ============================================================================
# MISSION 02: TIP THE SCALES (CENTER)
# ============================================================================

def mission_02_tip_scales():
    """
    Mission 2: Tip the Scales

    Strategy:
    - Navigate to scales
    - Place weight/objects to tip scales
    - Balance mechanism with precision
    - Return

    Estimated Points: 25-35
    Estimated Time: 20 seconds
    """
    print("Starting Mission 2: Tip the Scales")
    pre_mission_setup()

    # === PHASE 1: Navigate to Scales ===
    print("Phase 1: Navigate to scales")
    move_straight_gyro(550, DriveSpeed.TRANSIT)
    spin_turn(0, TurnSpeed.STANDARD)  # Straight ahead

    # === PHASE 2: Approach with Precision ===
    print("Phase 2: Precise approach")
    move_straight(200, DriveSpeed.APPROACH)
    move_straight(50, DriveSpeed.PRECISE)
    spin_turn(-5, TurnSpeed.ALIGNMENT)

    # === PHASE 3: Tip Scales (Push) ===
    print("Phase 3: Tip the scales")
    right_arm_down(60, ArmSpeed.GRAB)
    wait(300)
    move_straight(120, DriveSpeed.PUSHING)
    wait(500)
    right_arm_up(60, ArmSpeed.GRAB)

    # === PHASE 4: Return ===
    print("Phase 4: Return")
    move_straight(-370, DriveSpeed.RETURN)
    spin_turn(5, TurnSpeed.QUICK)
    move_straight_gyro(-550, DriveSpeed.RETURN)

    mission_complete("Tip the Scales")
    return True


# ============================================================================
# MISSION 03: MAP REVEAL (RIGHT SIDE)
# ============================================================================

def mission_03_map_reveal():
    """
    Mission 3: Map Reveal

    Strategy:
    - Navigate to map area
    - Reveal hidden map sections
    - Use arm to flip/uncover map
    - Return

    Estimated Points: 20-30
    Estimated Time: 22 seconds
    """
    print("Starting Mission 3: Map Reveal")
    pre_mission_setup()

    reset_arms()
    wait(500)

    # === PHASE 1: Navigate to Map ===
    print("Phase 1: Navigate to map area")
    move_straight_gyro(500, DriveSpeed.TRANSIT)
    spin_turn(30, TurnSpeed.PRECISE)
    move_straight(180, DriveSpeed.APPROACH)

    # === PHASE 2: Reveal Map ===
    print("Phase 2: Reveal map")
    move_straight(60, DriveSpeed.PRECISE)
    left_arm_down(80, ArmSpeed.COLLECT)
    wait(300)
    move_straight(100, DriveSpeed.PUSHING)
    left_arm_up(80, ArmSpeed.COLLECT)
    wait(500)

    # === PHASE 3: Return ===
    print("Phase 3: Return")
    move_straight(-340, DriveSpeed.RETURN)
    spin_turn(-30, TurnSpeed.QUICK)
    move_straight_gyro(-500, DriveSpeed.RETURN)

    mission_complete("Map Reveal")
    return True


# ============================================================================
# MISSION 04: STATUE REBUILD (PRECISION)
# ============================================================================

def mission_04_statue_rebuild():
    """
    Mission 4: Statue Rebuild

    Strategy:
    - Navigate to statue site
    - Carefully position statue pieces
    - Ultra-precise alignment required
    - Return

    Estimated Points: 35-50
    Estimated Time: 30 seconds
    """
    print("Starting Mission 4: Statue Rebuild")
    pre_mission_setup()

    # === PHASE 1: Navigate to Statue ===
    print("Phase 1: Navigate to statue site")
    move_straight_gyro(400, DriveSpeed.TRANSIT)
    spin_turn(-45, TurnSpeed.PRECISE)
    move_straight_gyro(250, DriveSpeed.APPROACH)

    # === PHASE 2: Precision Approach ===
    print("Phase 2: Ultra-precise approach")
    move_straight(100, DriveSpeed.APPROACH)
    move_straight(40, DriveSpeed.PRECISE)
    spin_turn(-8, TurnSpeed.ALIGNMENT)  # Ultra-precise
    move_straight(20, DriveSpeed.PRECISE)

    # === PHASE 3: Place Statue Piece ===
    print("Phase 3: Place statue piece")
    both_arms_down(70, ArmSpeed.DELICATE)
    wait(500)
    move_straight(60, DriveSpeed.PRECISE)
    both_arms_up(70, ArmSpeed.DELICATE)
    wait(1000)  # Let piece settle

    # === PHASE 4: Return ===
    print("Phase 4: Return")
    move_straight(-220, DriveSpeed.APPROACH)
    spin_turn(53, TurnSpeed.REPOSITION)
    move_straight_gyro(-650, DriveSpeed.RETURN)

    mission_complete("Statue Rebuild")
    return True


# ============================================================================
# MISSION 05: SURFACE BRUSHING (CLEANING)
# ============================================================================

def mission_05_surface_brushing():
    """
    Mission 5: Surface Brushing

    Strategy:
    - Navigate to artifact surface
    - Use attachment to brush/clean surface
    - Move along surface systematically
    - Return

    Estimated Points: 20-25
    Estimated Time: 25 seconds
    """
    print("Starting Mission 5: Surface Brushing")
    pre_mission_setup()

    # === PHASE 1: Navigate to Surface ===
    print("Phase 1: Navigate to brushing area")
    move_straight_gyro(520, DriveSpeed.TRANSIT)
    spin_turn(15, TurnSpeed.STANDARD)

    # === PHASE 2: Position Brush ===
    print("Phase 2: Position brush attachment")
    move_straight(180, DriveSpeed.APPROACH)
    right_arm_down(50, ArmSpeed.GRAB)
    wait(300)

    # === PHASE 3: Brush Surface ===
    print("Phase 3: Brush surface")
    move_straight(150, DriveSpeed.COLLECTION)  # Slow brushing
    wait(300)
    move_straight(80, DriveSpeed.COLLECTION)
    wait(300)
    right_arm_up(50, ArmSpeed.GRAB)

    # === PHASE 4: Return ===
    print("Phase 4: Return")
    move_straight(-410, DriveSpeed.RETURN)
    spin_turn(-15, TurnSpeed.QUICK)
    move_straight_gyro(-520, DriveSpeed.RETURN)

    mission_complete("Surface Brushing")
    return True


# ============================================================================
# MISSION 06: MINESHAFT EXPLORER (COMBO)
# ============================================================================

def mission_06_mineshaft_explorer():
    """
    Mission 6: Mineshaft Explorer

    Strategy:
    - Navigate to mineshaft entrance
    - Deploy explorer vehicle/robot
    - Activate mechanisms
    - Combo mission for multiple objectives

    Estimated Points: 40-60
    Estimated Time: 35 seconds
    """
    print("Starting Mission 6: Mineshaft Explorer")
    pre_mission_setup()

    reset_arms()
    wait(500)

    # === PHASE 1: Navigate to Mineshaft ===
    print("Phase 1: Navigate to mineshaft")
    move_straight_gyro(650, DriveSpeed.TRANSIT)
    spin_turn(20, TurnSpeed.STANDARD)
    move_straight(220, DriveSpeed.APPROACH)

    # === PHASE 2: Deploy Explorer ===
    print("Phase 2: Deploy explorer")
    left_arm_down(80, ArmSpeed.GRAB)
    wait(500)
    move_straight(120, DriveSpeed.PUSHING)
    left_arm_up(80, ArmSpeed.GRAB)
    wait(500)

    # === PHASE 3: Activate Mechanism ===
    print("Phase 3: Activate mineshaft mechanism")
    spin_turn(30, TurnSpeed.STANDARD)
    move_straight(100, DriveSpeed.APPROACH)
    right_arm_down(90, ArmSpeed.COLLECT)
    wait(300)
    move_straight(80, DriveSpeed.PRECISE)
    right_arm_up(90, ArmSpeed.COLLECT)

    # === PHASE 4: Return ===
    print("Phase 4: Return")
    move_straight(-320, DriveSpeed.RETURN)
    spin_turn(-50, TurnSpeed.REPOSITION)
    move_straight_gyro(-870, DriveSpeed.RETURN)

    mission_complete("Mineshaft Explorer")
    return True


# ============================================================================
# MISSION 07: CAREFUL RECOVERY (DELICATE)
# ============================================================================

def mission_07_careful_recovery():
    """
    Mission 7: Careful Recovery

    Strategy:
    - Navigate to fragile artifact
    - Use adaptive grabbing and lifting
    - Extremely gentle handling
    - Return with artifact

    Estimated Points: 30-40
    Estimated Time: 32 seconds
    """
    print("Starting Mission 7: Careful Recovery")
    pre_mission_setup()

    # === PHASE 1: Navigate to Artifact ===
    print("Phase 1: Navigate to fragile artifact")
    move_straight_gyro(480, DriveSpeed.TRANSIT)
    spin_turn(-28, TurnSpeed.PRECISE)
    move_straight(230, DriveSpeed.APPROACH)

    # === PHASE 2: Smart Grab (Ultra-Delicate) ===
    print("Phase 2: Careful grab with load sensing")
    move_straight(70, DriveSpeed.PRECISE)

    # Use adaptive grabbing with low load threshold
    result = grab_until_load(target_load=25, max_degrees=90, arm='right')

    if result['grabbed']:
        print(f"  Artifact grabbed gently! Load: {result['final_load']}%")

        # Adaptive lift - extra gentle
        lift_result = lift_adaptive(
            70,
            min_speed=ArmSpeed.DELICATE,
            max_speed=ArmSpeed.COLLECT,
            arm='right'
        )
        print(f"  Lifted carefully! Avg load: {lift_result['avg_load']}%")
    else:
        print("  Using standard delicate grab")
        right_arm_down(90, ArmSpeed.DELICATE)
        wait(500)
        right_arm_up(90, ArmSpeed.DELICATE)

    # === PHASE 3: Return with Artifact (Gentle) ===
    print("Phase 3: Return with artifact")
    move_straight(-300, DriveSpeed.APPROACH)  # Very careful
    spin_turn(28, TurnSpeed.STANDARD)
    move_straight_gyro(-480, DriveSpeed.COLLECTION)  # Not too fast

    # === PHASE 4: Deposit Artifact ===
    print("Phase 4: Deposit artifact gently")
    right_arm_down(90, ArmSpeed.DELICATE)
    wait(800)  # Extra settling time

    mission_complete("Careful Recovery")
    return True


# ============================================================================
# MISSION 08: QUICK TEST / VERIFICATION
# ============================================================================

def mission_08_quick_test():
    """
    Mission 8: Quick Test

    Strategy:
    - Fast movement verification
    - Test basic robot functions
    - Use before competition for final check
    - No points, just verification

    Time: 15 seconds
    """
    print("Starting Mission 8: Quick Test")
    pre_mission_setup()

    # Test forward movement
    print("Test: Forward")
    move_straight(300, DriveSpeed.APPROACH)
    wait(500)

    # Test turn
    print("Test: Turn right")
    spin_turn(90, TurnSpeed.STANDARD)
    wait(500)

    # Test backward
    print("Test: Backward")
    move_straight(-300, DriveSpeed.RETURN)
    wait(500)

    # Test turn left
    print("Test: Turn left")
    spin_turn(-90, TurnSpeed.STANDARD)
    wait(500)

    # Test arms
    print("Test: Arms")
    both_arms_up(45, ArmSpeed.GRAB)
    wait(300)
    both_arms_down(45, ArmSpeed.GRAB)

    mission_complete("Quick Test")
    return True


# ============================================================================
# LOAD MISSIONS TO SLOTS
# ============================================================================

def load_all_missions():
    """
    Load all missions to program slots.

    Slot Assignment:
    0: Angler Artifacts (left side)
    1: Tip the Scales (center)
    2: Map Reveal (right side)
    3: Statue Rebuild (precision)
    4: Surface Brushing (cleaning)
    5: Mineshaft Explorer (combo)
    6: Careful Recovery (delicate)
    7: Quick Test (verification)
    8-19: Reserved for additional missions
    """
    print("\n" + "=" * 70)
    print("LOADING FLL 2025 UNEARTHED MISSIONS")
    print("=" * 70)

    # Primary missions (high value)
    register_mission(
        0,
        "Angler-40pts",
        mission_01_angler_artifacts,
        "Left: Angler artifacts with adaptive grab (25s)"
    )

    register_mission(
        1,
        "Scales-35pts",
        mission_02_tip_scales,
        "Center: Tip the scales with precision (20s)"
    )

    register_mission(
        2,
        "Map-30pts",
        mission_03_map_reveal,
        "Right: Map reveal mechanism (22s)"
    )

    # Secondary missions
    register_mission(
        3,
        "Statue-50pts",
        mission_04_statue_rebuild,
        "Precision: Statue rebuild ultra-precise (30s)"
    )

    register_mission(
        4,
        "Brush-25pts",
        mission_05_surface_brushing,
        "Cleaning: Surface brushing (25s)"
    )

    # Combo and specialized missions
    register_mission(
        5,
        "Mineshaft-60pts",
        mission_06_mineshaft_explorer,
        "COMBO: Mineshaft explorer multi-objective (35s)"
    )

    register_mission(
        6,
        "Recovery-40pts",
        mission_07_careful_recovery,
        "Delicate: Careful recovery with load sensing (32s)"
    )

    # Test mission
    register_mission(
        7,
        "Test-0pts",
        mission_08_quick_test,
        "Quick verification (15s)"
    )

    print("\n✓ All missions loaded!")
    print("=" * 70)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    """
    Main execution - loads missions and starts competition mode.

    Workflow:
    1. Optional: Run mission_check.py for verification
    2. Load all missions to slots
    3. Display mission list
    4. Enter competition mode (hub button selector)
    """

    print("\n" + "=" * 70)
    print("FLL 2025 UNEARTHED - COMPETITION SETUP")
    print("=" * 70)

    # Optional: Run pre-competition check
    if RUN_PRE_CHECK:
        print("\nRunning pre-competition check...")
        print("(Set RUN_PRE_CHECK = False to skip)")
        wait(2000)

        ready = run_competition_check()

        if not ready:
            print("\n⚠ Robot not ready!")
            print("Fix issues before loading missions")
            hub.light.on(Color.RED)
            # Don't exit - allow user to decide
            print("\nContinuing anyway in 5 seconds...")
            print("(Turn off hub to abort)")
            wait(5000)

    # Load all missions
    load_all_missions()

    # Display mission list
    list_missions()

    # Export for printing
    print("\n")
    export_mission_list()

    # Instructions
    print("\n" + "=" * 70)
    print("READY FOR COMPETITION!")
    print("=" * 70)
    print("\nHub Controls:")
    print("  Left button  = Previous mission")
    print("  Right button = Next mission")
    print("  Center button = RUN selected mission")
    print("\nStarting competition mode in 3 seconds...")
    print("(Turn off hub to skip)")
    wait(3000)

    # Enter competition mode
    try:
        competition_mode()

    except KeyboardInterrupt:
        print("\n\nCompetition setup interrupted")
        hub.light.on(Color.ORANGE)

    except Exception as e:
        print(f"\n\nSetup error: {e}")
        hub.light.on(Color.RED)

    finally:
        print("\nCompetition setup complete")
