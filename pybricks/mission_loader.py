#!/usr/bin/env pybricks-micropython
"""
MISSION LOADER - Program Slot Management Utility
=================================================

Utility for loading mission functions into SPIKE Prime hub's program slots (0-19).

The SPIKE Prime hub has 20 program slots that can be accessed via the hub
buttons or programmatically. This utility helps organize and load your
missions into specific slots for easy competition access.

Program Slots:
- Slot 0-19: Available for custom programs
- Access: Left/Right buttons to select, Center button to run

Competition Workflow:
1. Load all missions to different slots using this utility
2. At competition, use hub buttons to select mission (no computer needed!)
3. Press center button to run selected mission

Features:
- Load mission functions to specific slots
- List all loaded missions
- Clear individual slots
- Export mission metadata
- Competition-ready organization

Created: 2025-10-19
For: FLL teams who need organized mission management at competitions
"""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Color, Button
from pybricks.tools import wait, StopWatch

# Initialize hub
hub = PrimeHub()

# ============================================================================
# MISSION REGISTRY
# ============================================================================

# Dictionary mapping slot numbers to mission information
# Format: slot_number: {'name': str, 'function': callable, 'description': str}
MISSION_REGISTRY = {}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def register_mission(slot, name, function, description=""):
    """
    Register a mission function to a specific program slot.

    Args:
        slot (int): Program slot number (0-19)
        name (str): Short name for the mission (e.g., "Mission 1")
        function (callable): The mission function to execute
        description (str): Optional description of what mission does

    Returns:
        bool: True if registered successfully

    Example:
        def my_mission():
            move_straight(500)
            turn(90)

        register_mission(0, "Test Mission", my_mission, "Basic movement test")
    """
    if not 0 <= slot <= 19:
        print(f"ERROR: Slot must be 0-19, got {slot}")
        return False

    if not callable(function):
        print(f"ERROR: function must be callable")
        return False

    MISSION_REGISTRY[slot] = {
        'name': name,
        'function': function,
        'description': description
    }

    print(f"✓ Registered '{name}' to slot {slot}")
    return True


def run_mission(slot):
    """
    Run the mission registered to a specific slot.

    Args:
        slot (int): Program slot number (0-19)

    Returns:
        bool: True if mission completed successfully

    Example:
        run_mission(0)  # Runs mission in slot 0
    """
    if slot not in MISSION_REGISTRY:
        print(f"ERROR: No mission registered in slot {slot}")
        hub.light.on(Color.RED)
        return False

    mission = MISSION_REGISTRY[slot]
    print(f"\n{'=' * 50}")
    print(f"Running: {mission['name']} (Slot {slot})")
    if mission['description']:
        print(f"Description: {mission['description']}")
    print('=' * 50)

    try:
        # Visual feedback - starting mission
        hub.light.on(Color.BLUE)
        wait(500)

        # Execute mission
        result = mission['function']()

        # Visual feedback - mission complete
        if result is False:
            print(f"\n✗ Mission '{mission['name']}' FAILED")
            hub.light.on(Color.RED)
            return False
        else:
            print(f"\n✓ Mission '{mission['name']}' COMPLETE")
            hub.light.on(Color.GREEN)
            return True

    except KeyboardInterrupt:
        print(f"\n⚠ Mission '{mission['name']}' INTERRUPTED")
        hub.light.on(Color.ORANGE)
        return False

    except Exception as e:
        print(f"\n✗ Mission '{mission['name']}' ERROR: {e}")
        hub.light.on(Color.RED)
        return False


def list_missions():
    """
    List all registered missions.

    Prints a formatted table of all missions currently registered.
    """
    if not MISSION_REGISTRY:
        print("No missions registered")
        return

    print("\n" + "=" * 70)
    print("REGISTERED MISSIONS")
    print("=" * 70)
    print(f"{'Slot':<6} {'Name':<20} {'Description':<40}")
    print("-" * 70)

    for slot in sorted(MISSION_REGISTRY.keys()):
        mission = MISSION_REGISTRY[slot]
        name = mission['name'][:19]  # Truncate if too long
        desc = mission['description'][:39]  # Truncate if too long
        print(f"{slot:<6} {name:<20} {desc:<40}")

    print("=" * 70)
    print(f"Total: {len(MISSION_REGISTRY)} missions")


def clear_mission(slot):
    """
    Clear a mission from a specific slot.

    Args:
        slot (int): Program slot number (0-19)

    Returns:
        bool: True if cleared successfully
    """
    if slot not in MISSION_REGISTRY:
        print(f"Slot {slot} is already empty")
        return False

    mission_name = MISSION_REGISTRY[slot]['name']
    del MISSION_REGISTRY[slot]
    print(f"✓ Cleared '{mission_name}' from slot {slot}")
    return True


def clear_all_missions():
    """
    Clear all registered missions.

    Returns:
        int: Number of missions cleared
    """
    count = len(MISSION_REGISTRY)
    MISSION_REGISTRY.clear()
    print(f"✓ Cleared {count} missions")
    return count


# ============================================================================
# INTERACTIVE MISSION SELECTOR
# ============================================================================

def select_mission_interactive():
    """
    Interactive mission selector using hub buttons.

    Controls:
    - Left button: Previous mission
    - Right button: Next mission
    - Center button: Run selected mission

    Returns:
        int: Selected slot number, or None if cancelled
    """
    if not MISSION_REGISTRY:
        print("No missions to select")
        hub.light.on(Color.RED)
        return None

    # Get sorted list of available slots
    available_slots = sorted(MISSION_REGISTRY.keys())
    current_index = 0

    print("\n" + "=" * 50)
    print("MISSION SELECTOR")
    print("=" * 50)
    print("Controls:")
    print("  Left button  = Previous mission")
    print("  Right button = Next mission")
    print("  Center button = Select and run")
    print("=" * 50)

    while True:
        # Get current slot and mission
        slot = available_slots[current_index]
        mission = MISSION_REGISTRY[slot]

        # Display current selection
        print(f"\n[{current_index + 1}/{len(available_slots)}] Slot {slot}: {mission['name']}")
        if mission['description']:
            print(f"  {mission['description']}")

        # Visual feedback - show slot number via LED color
        # Colors cycle: Red, Orange, Yellow, Green, Cyan, Blue, Violet
        colors = [Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN,
                  Color.CYAN, Color.BLUE, Color.VIOLET]
        hub.light.on(colors[slot % len(colors)])

        # Wait for button press
        pressed = []
        while not pressed:
            pressed = hub.buttons.pressed()
            wait(10)

        if Button.LEFT in pressed:
            # Previous mission
            current_index = (current_index - 1) % len(available_slots)
            wait(300)  # Debounce

        elif Button.RIGHT in pressed:
            # Next mission
            current_index = (current_index + 1) % len(available_slots)
            wait(300)  # Debounce

        elif Button.CENTER in pressed:
            # Select and run this mission
            print(f"\n✓ Selected slot {slot}")
            wait(300)  # Debounce
            return slot


# ============================================================================
# MISSION SEQUENCE RUNNER
# ============================================================================

def run_mission_sequence(slots, delay_ms=1000):
    """
    Run multiple missions in sequence.

    Args:
        slots (list): List of slot numbers to run in order
        delay_ms (int): Delay between missions in milliseconds (default: 1000)

    Returns:
        dict: Results for each mission

    Example:
        # Run missions 0, 1, 2 in sequence with 2 second delay
        results = run_mission_sequence([0, 1, 2], delay_ms=2000)
    """
    results = {}

    print("\n" + "=" * 50)
    print(f"MISSION SEQUENCE: {len(slots)} missions")
    print("=" * 50)

    for i, slot in enumerate(slots, 1):
        print(f"\n[{i}/{len(slots)}] Starting mission in slot {slot}")

        # Run mission
        success = run_mission(slot)
        results[slot] = success

        if not success:
            print(f"\n⚠ Mission {slot} failed, stopping sequence")
            break

        # Delay before next mission (except after last mission)
        if i < len(slots):
            print(f"\nWaiting {delay_ms}ms before next mission...")
            wait(delay_ms)

    # Summary
    print("\n" + "=" * 50)
    print("SEQUENCE COMPLETE")
    print("=" * 50)
    successful = sum(1 for r in results.values() if r)
    print(f"Successful: {successful}/{len(slots)}")

    return results


# ============================================================================
# COMPETITION MODE
# ============================================================================

def competition_mode():
    """
    Competition mode - interactive mission selector with continuous operation.

    Workflow:
    1. Select mission using hub buttons
    2. Run selected mission
    3. After completion, return to selector
    4. Repeat until hub is turned off

    This mode is perfect for competition use - no computer needed!
    """
    print("\n" + "=" * 50)
    print("COMPETITION MODE ACTIVATED")
    print("=" * 50)
    print("Use hub buttons to select and run missions")
    print("Turn off hub to exit")
    print("=" * 50)

    while True:
        try:
            # Select mission
            slot = select_mission_interactive()

            if slot is None:
                continue

            # Run selected mission
            run_mission(slot)

            # Wait before returning to selector
            print("\nReturning to mission selector in 3 seconds...")
            wait(3000)

        except KeyboardInterrupt:
            print("\nCompetition mode interrupted")
            hub.light.on(Color.ORANGE)
            break

        except Exception as e:
            print(f"\nError in competition mode: {e}")
            hub.light.on(Color.RED)
            wait(2000)


# ============================================================================
# EXPORT MISSION METADATA
# ============================================================================

def export_mission_list():
    """
    Export mission list as text for printing/reference.

    Returns:
        str: Formatted mission list
    """
    if not MISSION_REGISTRY:
        return "No missions registered"

    output = []
    output.append("=" * 70)
    output.append("MISSION REFERENCE SHEET")
    output.append("=" * 70)
    output.append("")

    for slot in sorted(MISSION_REGISTRY.keys()):
        mission = MISSION_REGISTRY[slot]
        output.append(f"Slot {slot}: {mission['name']}")
        if mission['description']:
            output.append(f"  Description: {mission['description']}")
        output.append("")

    output.append("=" * 70)
    output.append(f"Total: {len(MISSION_REGISTRY)} missions")

    text = "\n".join(output)
    print(text)
    return text


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    """
    Example usage of mission loader utility.

    Demonstrates:
    - Registering missions to slots
    - Listing missions
    - Running individual missions
    - Interactive mission selection
    - Competition mode
    """

    # Example: Import your mission functions
    # from mission_2025 import mission_1, mission_2, mission_3

    # Example: Define some simple test missions
    def test_mission_1():
        """Test mission 1 - Basic movement"""
        print("Executing test mission 1...")
        wait(1000)
        print("Mission 1 complete!")
        return True

    def test_mission_2():
        """Test mission 2 - Object collection"""
        print("Executing test mission 2...")
        wait(1000)
        print("Mission 2 complete!")
        return True

    def test_mission_3():
        """Test mission 3 - Delivery"""
        print("Executing test mission 3...")
        wait(1000)
        print("Mission 3 complete!")
        return True

    # Register missions to slots
    print("\nRegistering missions...")
    register_mission(0, "Test Mission 1", test_mission_1, "Basic movement test")
    register_mission(1, "Test Mission 2", test_mission_2, "Object collection test")
    register_mission(2, "Test Mission 3", test_mission_3, "Delivery test")

    # List all registered missions
    list_missions()

    # Export mission list for reference
    print("\n")
    export_mission_list()

    # Example 1: Run a specific mission
    print("\n\nExample 1: Running slot 0...")
    run_mission(0)
    wait(2000)

    # Example 2: Interactive selection (commented out for automated testing)
    # print("\n\nExample 2: Interactive selection...")
    # selected = select_mission_interactive()
    # if selected is not None:
    #     run_mission(selected)

    # Example 3: Run mission sequence
    # print("\n\nExample 3: Running mission sequence...")
    # run_mission_sequence([0, 1, 2], delay_ms=2000)

    # Example 4: Competition mode (commented out - runs indefinitely)
    # print("\n\nExample 4: Starting competition mode...")
    # competition_mode()

    print("\n\nMission loader examples complete!")
