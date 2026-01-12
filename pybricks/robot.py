#!/usr/bin/env pybricks-micropython
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Color, Stop, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, hub_menu

# ============================================================================
# ROBOT CONFIGURATION CONSTANTS
# ============================================================================

# Physical Robot Measurements (measure your specific robot!)
WHEEL_DIAMETER = 56  # mm - SPIKE Prime small wheels
AXLE_TRACK = 96     # mm - distance between wheel centers
WHEEL_CIRCUMFERENCE = 3.14159 * WHEEL_DIAMETER  # mm - calculated

# Movement Performance Constants
DEFAULT_SPEED = 300              # mm/s - default straight movement speed
DEFAULT_TURN_SPEED = 100         # deg/s - default turning speed
DEFAULT_ACCELERATION = 500       # mm/s² - acceleration for straight movement
DEFAULT_TURN_ACCELERATION = 200  # deg/s² - acceleration for turning
GYRO_PROPORTIONAL_GAIN = 2.0     # Proportional gain for gyro correction

# Mission-Optimized Speed Presets (based on FLL analysis)
# Type-safe speed constants (prevents typos with autocomplete)
class DriveSpeed:
    """
    Mission-optimized speed presets for FLL robot DRIVE/MOVEMENT control.

    Using DriveSpeed.PRECISE, DriveSpeed.APPROACH, etc. provides autocomplete
    and prevents typos compared to numeric literals.

    Usage:
        move_straight(300, DriveSpeed.TRANSIT)     # Use predefined constant (recommended)
        move_straight(300, 800)                     # Custom numeric speed
        move_straight_gyro(500, DriveSpeed.APPROACH)  # With gyro correction
    """
    PRECISE = 100       # Final positioning, delicate operations (±0.5cm accuracy)
    APPROACH = 300      # Approaching mission models (±1cm accuracy)
    COLLECTION = 500    # Object collection runs (±2cm accuracy)
    TRANSIT = 700       # Moving between areas (speed priority)
    RETURN = 900        # Returning to base (maximum safe speed)
    PUSHING = 600       # Pushing heavy objects (use slower speed with high power)

# Turn Speed Presets (based on FLL competition analysis and robotics best practices)
# Optimized for turn accuracy vs speed tradeoffs in different mission scenarios
class TurnSpeed:
    """
    Mission-optimized turn speed presets for FLL robot TURNING control.

    Different turn scenarios require different speed/accuracy tradeoffs.
    Using TurnSpeed.PRECISE, TurnSpeed.QUICK, etc. provides clear intent
    and prevents magic numbers.

    Usage:
        turn(90, TurnSpeed.STANDARD)       # Balanced turn
        spin_turn(45, TurnSpeed.PRECISE)   # Precise IMU turn
        turn(180, TurnSpeed.QUICK)         # Fast repositioning
    """
    # PRECISE TURNS (40-80 deg/s) - Highest accuracy
    ALIGNMENT = 40      # Final alignment with mission models (±0.5° accuracy)
                        # Use: Precise positioning before pickup/delivery, docking
                        # Example: Aligning with narrow slots, critical angles

    PRECISE = 60        # High-precision turns for critical angles (±1° accuracy)
                        # Use: IMU-based turns, angle-critical missions
                        # Most common for spin_turn() operations
                        # Default for missions requiring reliable angles

    # STANDARD TURNS (80-120 deg/s) - Good balance
    STANDARD = 100      # Default turn speed, good accuracy (±2° accuracy)
                        # Use: General purpose turning, most missions
                        # Best balance of speed and accuracy for typical missions

    APPROACH = 120      # Approaching turn position (±3° accuracy)
                        # Use: Turns while moving between mission areas
                        # Good for transitions where precision not critical

    # FAST TURNS (150-200 deg/s) - Speed priority
    QUICK = 150         # Quick repositioning turns (±4° accuracy)
                        # Use: Mid-run repositioning, non-critical angles
                        # Time-saving turns when angle is approximate

    REPOSITION = 200    # Fast turns for time-critical situations (±5° accuracy)
                        # Use: Emergency repositioning, return to base
                        # Maximum safe turn speed

    # SPECIALIZED TURNS
    PIVOT = 80          # Pivot turn speed (one wheel stationary)
                        # Use: Space-constrained environments, tight turns
                        # Slower because less predictable than spin turns

    CURVE = 60          # Curved path speed (continuous turning while moving)
                        # Use: Following curved paths, arc movements
                        # Smooth continuous turning with good control

# Arm Speed Presets (based on FLL 2025 mission analysis)
# Optimized for SPIKE Prime small motors controlling arms/attachments
class ArmSpeed:
    """
    Mission-optimized speed presets for FLL robot ARM/ATTACHMENT control.

    Based on analysis of FLL 2025 Submerged/Unearthed missions and successful
    team implementations. Speeds in degrees/second for small motors.

    Usage:
        left_arm_up(90, ArmSpeed.GRAB)       # Grab object carefully
        right_arm_down(45, ArmSpeed.QUICK)   # Quick release
        both_arms_up(90, ArmSpeed.COLLECT)   # Standard collection speed
    """
    # DELICATE OPERATIONS (200-360 deg/s) - Highest accuracy
    DELICATE = 200      # Ultra-precise for fragile objects, final positioning
                        # Use: Placing coral in nursery, aligning with small targets

    GRAB = 360          # Default safe speed, best accuracy (±0-1 degrees)
                        # Use: Grabbing sharks, picking up krill, controlled grips
                        # Most common speed used by successful teams

    # COLLECTION OPERATIONS (500-640 deg/s) - Good balance
    COLLECT = 500       # Standard collection missions, routine operations
                        # Use: Collecting coral pieces, grabbing multiple objects

    MODERATE = 640      # Faster collections, medium-priority operations
                        # Use: Multi-object sequences, timed missions

    # QUICK OPERATIONS (720-1000 deg/s) - Speed priority
    RESET = 720         # Arm resets, non-critical movements
                        # Use: Moving to home position, repositioning between tasks

    QUICK = 1000        # Maximum safe speed for urgent actions
                        # Use: Fast releases, emergency returns, clearing obstacles

    # FORCE OPERATIONS (200-400 deg/s) - Power priority
    PUSH = 400          # Pushing objects, applying force
                        # Use: Pushing building structures, sliding heavy objects

    STALL = 200         # Slow speed for stall detection operations
                        # Use: Finding mechanical limits, pushing until resistance

# Drive Speed Selection Guide - Use DriveSpeed class constants:
#   move_straight(300, DriveSpeed.TRANSIT)       # Fast movement (700 mm/s)
#   move_straight_gyro(500, DriveSpeed.APPROACH) # Moderate speed (300 mm/s)
#   move_straight(100, DriveSpeed.PRECISE)       # Slow, accurate (100 mm/s)
#   move_straight(400, 650)                      # Custom numeric speed
#
# Usage Guide:
# - DriveSpeed.PRECISE (100) for: Final alignment, close to models
# - DriveSpeed.APPROACH (300) for: Moving toward mission areas with moderate precision
# - DriveSpeed.COLLECTION (500) for: Collecting objects, moderate speed missions
# - DriveSpeed.TRANSIT (700) for: Long straight runs between areas
# - DriveSpeed.RETURN (900) for: Returning to base when precision doesn't matter
# - DriveSpeed.PUSHING (600) for: Heavy objects, ramps, need extra power

# Spin Turn Constants (for precise IMU-based turning)
SPIN_TURN_BASE_SPEED = 60   # deg/s - base motor speed for spin turns
SPIN_TURN_KP = 9            # Proportional gain for spin turn control
SPIN_TURN_TOLERANCE = 2     # degrees - stopping tolerance for spin turns

# Validation Limits
MAX_DISTANCE = 2000  # mm - maximum single movement distance
MAX_SPEED = 1000     # mm/s - maximum safe speed
MAX_TURN_RATE = 500  # deg/s - maximum turn rate

# Port Assignments (modify these to match your robot wiring)
LEFT_MOTOR_PORT = Port.B
RIGHT_MOTOR_PORT = Port.F
ATTACHMENT_PORT_LEFT = Port.A  # Front/left attachment
ATTACHMENT_PORT_RIGHT = Port.E  # Back/right attachment

# ============================================================================
# ROBOT INITIALIZATION
# ============================================================================

# Initialize the hub
hub = PrimeHub()

# Initialize the drive motors
# NOTE: If robot spins instead of going straight, swap CLOCKWISE/COUNTERCLOCKWISE
left_motor = Motor(LEFT_MOTOR_PORT, Direction.COUNTERCLOCKWISE)
right_motor = Motor(RIGHT_MOTOR_PORT, Direction.CLOCKWISE)

# Initialize the drive base
robot = DriveBase(left_motor, right_motor,
                 wheel_diameter=WHEEL_DIAMETER,
                 axle_track=AXLE_TRACK)

# Configure drive base performance settings
robot.settings(
    straight_speed=DEFAULT_SPEED,
    straight_acceleration=DEFAULT_ACCELERATION,
    turn_rate=DEFAULT_TURN_SPEED,
    turn_acceleration=DEFAULT_TURN_ACCELERATION
)

# Reset IMU heading to zero at startup
hub.imu.reset_heading(0)

# Initialize attachment motors (if connected)
# These are initialized once and reused to avoid "device busy" errors
attachment_motor_left = None
attachment_motor_right = None

try:
    attachment_motor_left = Motor(ATTACHMENT_PORT_LEFT)
    print(f"Attachment motor on {ATTACHMENT_PORT_LEFT} initialized")
except Exception as e:
    print(f"No attachment motor on {ATTACHMENT_PORT_LEFT}: {e}")

try:
    attachment_motor_right = Motor(ATTACHMENT_PORT_RIGHT)
    print(f"Attachment motor on {ATTACHMENT_PORT_RIGHT} initialized")
except Exception as e:
    print(f"No attachment motor on {ATTACHMENT_PORT_RIGHT}: {e}")

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_distance(distance_mm):
    """
    Validate movement distance parameter.

    Args:
        distance_mm: Distance in millimeters

    Returns:
        bool: True if validation passes (always returns True, logs warnings only)
    """
    if not isinstance(distance_mm, (int, float)):
        print(f"WARNING: Distance must be numeric, got {type(distance_mm).__name__}")
        return True

    # Allow negative values for backward movement
    if abs(distance_mm) > MAX_DISTANCE:
        print(f"WARNING: Distance {distance_mm}mm exceeds maximum {MAX_DISTANCE}mm")

    return True

def validate_speed(speed_mm_s):
    """
    Validate speed parameter.

    Args:
        speed_mm_s: Speed in mm/s or deg/s (numeric or Speed constant)

    Returns:
        bool: True if validation passes (always returns True, logs warnings only)
    """
    # Speed.CONSTANT values are already integers, no conversion needed
    if not isinstance(speed_mm_s, (int, float)):
        print(f"WARNING: Speed must be numeric, got {type(speed_mm_s).__name__}")
        return True

    # Allow negative speed for backward movement (but DriveBase expects positive speed)
    if speed_mm_s < 0:
        print(f"WARNING: Speed must be positive (use negative distance for backward), got {speed_mm_s}")

    if speed_mm_s > MAX_SPEED:
        print(f"WARNING: Speed {speed_mm_s} exceeds maximum {MAX_SPEED}mm/s")

    return True

def validate_angle(angle_degrees):
    """
    Validate angle parameter.

    Args:
        angle_degrees: Angle in degrees

    Returns:
        bool: True if validation passes (always returns True, logs warnings only)
    """
    if not isinstance(angle_degrees, (int, float)):
        print(f"WARNING: Angle must be numeric, got {type(angle_degrees).__name__}")

    return True

# ============================================================================
# CORE MOVEMENT FUNCTIONS
# ============================================================================

def move_straight(distance_mm, speed=DEFAULT_SPEED):
    """
    Move the robot straight for a given distance in millimeters.

    Uses DriveBase open-loop control (no gyro correction).
    For gyro-corrected movement, use move_straight_gyro().

    Args:
        distance_mm (int/float): Distance to move in millimeters
                                Positive = forward, Negative = backward
        speed (int/DriveSpeed): Speed in mm/s (default: DEFAULT_SPEED=300)
                               Options:
                               - DriveSpeed.TRANSIT (700) - Fast movement (recommended)
                               - DriveSpeed.PRECISE (100) - Slow, accurate
                               - DriveSpeed.APPROACH (300) - Moderate speed
                               - Numeric: 100-900 (custom speed)

    Returns:
        bool: True if movement completed successfully

    Raises:
        TypeError: If parameters are not numeric
        ValueError: If parameters are out of valid range

    Example:
        move_straight(300)                        # Default speed
        move_straight(500, DriveSpeed.TRANSIT)    # Fast movement (700 mm/s)
        move_straight(100, DriveSpeed.PRECISE)    # Slow, accurate (100 mm/s)
        move_straight(400, 600)                   # Custom numeric speed
    """
    # Validate inputs
    validate_distance(distance_mm)
    validate_speed(speed)

    # Apply speed setting and execute movement
    try:
        print(f"[DEBUG] move_straight called with distance_mm={distance_mm}, speed={speed}")
        robot.settings(straight_speed=speed)
        print(f"[DEBUG] robot.settings(straight_speed={speed}) applied")
        robot.straight(distance_mm)
        print(f"[DEBUG] robot.straight({distance_mm}) executed")
        return True
    except Exception as e:
        print(f"move_straight error: {e}")
        # Pybricks MicroPython does not support sys or traceback modules
        return False

def turn(angle_degrees, speed=None):
    """
    Turn the robot by a specified angle in degrees (both wheels in opposite directions).

    Uses DriveBase open-loop control (no gyro correction).
    For precise gyro-corrected turns, use spin_turn().

    Args:
        angle_degrees (int/float): Angle to turn in degrees
                                   Positive = right (clockwise)
                                   Negative = left (counterclockwise)
        speed (int/TurnSpeed): Turn rate in degrees/s or TurnSpeed constant
                              Default: TurnSpeed.STANDARD (100 deg/s)
                              Options:
                              - TurnSpeed.ALIGNMENT (40) - Ultra-precise
                              - TurnSpeed.PRECISE (60) - High precision
                              - TurnSpeed.STANDARD (100) - Balanced (default)
                              - TurnSpeed.APPROACH (120) - Fast approach
                              - TurnSpeed.QUICK (150) - Quick repositioning
                              - TurnSpeed.REPOSITION (200) - Maximum speed
                              - Numeric: Custom turn rate

    Returns:
        bool: True if turn completed successfully

    Raises:
        TypeError: If parameters are not numeric
        ValueError: If speed is out of valid range

    Example:
        turn(90)                           # Default STANDARD speed
        turn(90, TurnSpeed.QUICK)          # Fast turn
        turn(-45, TurnSpeed.PRECISE)       # Precise turn
        turn(180, TurnSpeed.REPOSITION)    # Maximum speed
        turn(90, 150)                      # Custom numeric speed
    """
    # Default speed
    if speed is None:
        speed = TurnSpeed.STANDARD

    # Validate inputs
    validate_angle(angle_degrees)
    validate_speed(speed)

    # Apply turn rate setting and execute turn
    try:
        robot.settings(turn_rate=speed)
        robot.turn(angle_degrees)
        return True
    except Exception as e:
        print(f"turn error: {e}")
        return False

def pivot_turn(angle_degrees, speed=None):
    """
    Make a pivot turn around one stationary wheel (sharper turn than spin turn).

    FIXED: Now includes correct geometric conversion from robot angle to motor degrees.

    The robot pivots around one wheel while the other wheel moves in an arc.
    Arc radius = AXLE_TRACK (distance between wheels).

    Args:
        angle_degrees (int/float): Robot angle to turn in degrees
                                   Positive = pivot right (around right wheel)
                                   Negative = pivot left (around left wheel)
        speed (int/TurnSpeed): Motor speed in degrees/s or TurnSpeed constant
                              Default: TurnSpeed.PIVOT (80 deg/s)
                              Options:
                              - TurnSpeed.ALIGNMENT (40) - Ultra-precise pivot
                              - TurnSpeed.PRECISE (60) - High precision
                              - TurnSpeed.PIVOT (80) - Recommended for pivots
                              - TurnSpeed.STANDARD (100) - Faster pivot
                              - Numeric: Custom speed

    Returns:
        bool: True if pivot turn completed successfully

    Raises:
        TypeError: If parameters are not numeric
        ValueError: If speed is out of valid range

    Example:
        pivot_turn(90)                        # Default PIVOT speed
        pivot_turn(90, TurnSpeed.PRECISE)     # Precise pivot
        pivot_turn(-45, TurnSpeed.QUICK)      # Fast pivot

    Note:
        Pivot turns are tighter than spin turns but may be less accurate.
        Use spin_turn() for more precise angle control.
        TurnSpeed.PIVOT (80) is recommended default for best accuracy.
    """
    # Default speed
    if speed is None:
        speed = TurnSpeed.PIVOT

    # Validate inputs
    validate_angle(angle_degrees)
    validate_speed(speed)

    try:
        # Calculate arc length: s = r × θ (in radians)
        # For pivot turn, radius = AXLE_TRACK
        arc_length_mm = abs(AXLE_TRACK * angle_degrees * 3.14159 / 180)

        # Convert arc length to motor rotation degrees
        motor_degrees = int((arc_length_mm / WHEEL_CIRCUMFERENCE) * 360)

        if angle_degrees > 0:  # Pivot right (left motor moves, right motor stationary)
            left_motor.run_angle(speed, motor_degrees, wait=True)
        else:  # Pivot left (right motor moves, left motor stationary)
            right_motor.run_angle(speed, motor_degrees, wait=True)

        return True
    except Exception as e:
        print(f"pivot_turn error: {e}")
        return False

def tank_move(left_speed, right_speed, duration_ms):
    """
    Move the robot using tank-style controls.
    Speeds are in percentage (-100 to 100).
    Duration is in milliseconds.
    """
    # Calculate the drive parameters
    speed = (left_speed + right_speed) / 2
    turn_rate = (left_speed - right_speed)
    
    # Start the movement
    robot.drive(speed, turn_rate)
    
    # Wait for the specified duration
    wait(duration_ms)
    
    # Stop the robot
    robot.stop()

def move_straight_gyro(distance_mm, speed=DEFAULT_SPEED, kp=GYRO_PROPORTIONAL_GAIN):
    """
    Move straight using gyro sensor to maintain direction, even with obstacles.

    This is the BEST function for straight-line accuracy. It uses the IMU gyro
    sensor with proportional control to continuously correct heading drift,
    ensuring the robot maintains a straight path even when encountering
    obstacles or mat irregularities.

    Args:
        distance_mm (int/float): Distance to move in millimeters
                                Positive = forward, Negative = backward
        speed (int/DriveSpeed): Speed in mm/s (default: DEFAULT_SPEED=300)
                               Options:
                               - DriveSpeed.TRANSIT (700) - Fast with correction
                               - DriveSpeed.APPROACH (300) - Moderate speed
                               - DriveSpeed.PRECISE (100) - Slow, accurate
                               - Numeric: 100-900 (custom speed)
        kp (float): Proportional gain for correction (default: GYRO_PROPORTIONAL_GAIN=2.0)
                   Increase if robot doesn't correct enough (try 2.5-3.0)
                   Decrease if robot oscillates/overcorrects (try 1.0-1.5)

    Returns:
        bool: True if movement completed successfully

    Raises:
        TypeError: If parameters are not numeric
        ValueError: If parameters are out of valid range

    Example:
        move_straight_gyro(500)                            # Default speed with gyro
        move_straight_gyro(300, DriveSpeed.APPROACH, 2.5)  # Moderate speed (300 mm/s)
        move_straight_gyro(1000, DriveSpeed.TRANSIT)       # Fast transit (700 mm/s)
        move_straight_gyro(400, 600, 2.0)                  # Custom speed with custom kp

    Note:
        - Recommended for distances > 200mm where drift matters
        - Works best for FORWARD movement (backward is less reliable)
        - Update rate: 100Hz (10ms loop)
        - Typical accuracy: ±1cm at 200mm/s, ±2cm at 500mm/s
    """
    # Validate inputs
    validate_distance(distance_mm)
    validate_speed(speed)

    try:
        # Reset the heading before starting
        hub.imu.reset_heading(0)
        wait(50)  # Give IMU time to stabilize

        # Save initial motor positions
        left_start = left_motor.angle()
        right_start = right_motor.angle()

        # Calculate target motor rotation in degrees
        target_degrees = abs((distance_mm / WHEEL_CIRCUMFERENCE) * 360)

        # Keep moving until we reach the target distance
        while True:
            # Calculate average motor position
            left_pos = abs(left_motor.angle() - left_start)
            right_pos = abs(right_motor.angle() - right_start)
            avg_pos = (left_pos + right_pos) / 2

            # Check if we've reached the target distance
            if avg_pos >= target_degrees:
                robot.stop()
                break

            # Get current heading error
            heading_error = hub.imu.heading()

            # Calculate turn rate correction using proportional control
            # Negative sign to counteract drift: if robot drifts right (+heading), turn left (-)
            turn_rate = -heading_error * kp

            # Apply the correction while maintaining forward/backward motion
            robot.drive(speed if distance_mm > 0 else -speed, turn_rate)

            # Small delay to prevent overwhelming the system (100Hz update rate)
            wait(10)

        return True
    except Exception as e:
        print(f"move_straight_gyro error: {e}")
        robot.stop()
        return False

def spin_turn(target_angle, speed=None):
    """
    Make a precise spin turn using the hub's IMU sensor with proportional control.

    REFACTORED: Eliminated code duplication, added stopping tolerance, moved constants
    to module level, added error handling. Now supports TurnSpeed categories.

    Both wheels rotate in opposite directions for an in-place turn with precise
    angle control using the IMU gyro sensor and proportional feedback.

    Args:
        target_angle (int/float): Target angle to turn to (relative to current heading)
                                 Positive = right (clockwise)
                                 Negative = left (counterclockwise)
        speed (int/TurnSpeed): Base speed for IMU turn or TurnSpeed constant
                              Default: TurnSpeed.PRECISE (60 deg/s)
                              Options:
                              - TurnSpeed.ALIGNMENT (40) - Ultra-precise (±0.5°)
                              - TurnSpeed.PRECISE (60) - High precision (±1°)
                              - TurnSpeed.STANDARD (100) - Faster turn (±2°)
                              - Numeric: Custom base speed

    Returns:
        float: Final angle achieved (for verification)

    Raises:
        TypeError: If target_angle is not numeric

    Example:
        spin_turn(90)                           # Default PRECISE speed
        spin_turn(90, TurnSpeed.ALIGNMENT)      # Ultra-precise alignment
        spin_turn(-45, TurnSpeed.STANDARD)      # Faster turn
        final = spin_turn(180, TurnSpeed.PRECISE)  # Returns final angle

    Note:
        - More accurate than turn() due to IMU feedback
        - Uses proportional control: faster when far from target, slower when close
        - Stopping tolerance: ±2 degrees (SPIN_TURN_TOLERANCE)
        - Update rate: 100Hz (10ms loop)
        - Actual motor speed = base_speed + (error × SPIN_TURN_KP)
    """
    # Default speed
    if speed is None:
        speed = TurnSpeed.PRECISE

    # Validate input
    validate_angle(target_angle)

    try:
        # Use provided speed as base speed (overrides SPIN_TURN_BASE_SPEED)
        base_speed = speed

        # Reset the heading before starting the turn
        hub.imu.reset_heading(0)
        wait(50)  # Give IMU time to stabilize

        # Determine direction and target
        direction = 1 if target_angle >= 0 else -1
        target_abs = abs(target_angle)

        # Single loop for both directions (eliminates duplication)
        while True:
            current_angle = abs(hub.imu.heading())
            error = target_abs - current_angle

            # Stop if within tolerance
            if abs(error) < SPIN_TURN_TOLERANCE:
                break

            # Proportional control: speed increases with error
            adjustment = error * SPIN_TURN_KP
            motor_speed = base_speed + adjustment

            # Apply direction-adjusted speeds to motors
            left_motor.run(direction * motor_speed)
            right_motor.run(-direction * motor_speed)

            wait(10)  # 100Hz update rate

        # Stop both motors with hold for precise positioning
        left_motor.hold()
        right_motor.hold()

        # Return final angle for verification
        final_angle = hub.imu.heading()
        return final_angle

    except Exception as e:
        print(f"spin_turn error: {e}")
        left_motor.hold()
        right_motor.hold()
        return 0

# ============================================================================
# ATTACHMENT CONTROL FUNCTIONS
# ============================================================================

def run_attachment(port, degrees, speed=360):
    """
    Run an attachment motor for a specified number of degrees.

    Universal function for controlling attachment motors (arms, grippers, etc).

    Args:
        port (Port): Motor port (e.g., Port.A, Port.E)
        degrees (int/float): Degrees to rotate
                            Positive = one direction, Negative = opposite
        speed (int): Motor speed in degrees/s (default: 360)
                    Range: 0-1000 deg/s

    Returns:
        bool: True if movement completed successfully

    Raises:
        TypeError: If parameters are not valid types
        ValueError: If speed is out of range

    Example:
        run_attachment(Port.A, 90, 500)   # Rotate attachment motor 90 degrees
        run_attachment(Port.E, -180, 360) # Rotate backward 180 degrees
    """
    # Validate inputs
    validate_angle(degrees)
    if speed < 0 or speed > 1000:
        print(f"WARNING: Attachment speed {speed} out of range 0-1000")

    try:
        # Use pre-initialized motors if available, otherwise create new Motor
        motor = None
        if port == ATTACHMENT_PORT_LEFT and attachment_motor_left is not None:
            motor = attachment_motor_left
        elif port == ATTACHMENT_PORT_RIGHT and attachment_motor_right is not None:
            motor = attachment_motor_right
        else:
            # For other ports, try to create a new motor (may fail if nothing connected)
            motor = Motor(port)

        if motor is None:
            print(f"No motor connected on {port}")
            return False

        motor.run_angle(speed, degrees, wait=True)
        return True
    except Exception as e:
        print(f"run_attachment error on {port}: {e}")
        return False

def attachment_to_position(port, position, speed=360):
    """
    Move attachment motor to an absolute position.

    Useful for resetting attachments to known positions or moving to
    preset positions (e.g., home, deployed, mid-position).

    Args:
        port (Port): Motor port (e.g., Port.A, Port.E)
        position (int): Target absolute position in degrees
        speed (int): Motor speed in degrees/s (default: 360)

    Returns:
        bool: True if movement completed successfully

    Example:
        attachment_to_position(Port.A, 0, 500)    # Reset to home (0°)
        attachment_to_position(Port.E, 90, 360)   # Move to 90° position
    """
    if speed < 0 or speed > 1000:
        print(f"WARNING: Attachment speed {speed} out of range 0-1000")

    try:
        # Use pre-initialized motors if available, otherwise create new Motor
        motor = None
        if port == ATTACHMENT_PORT_LEFT and attachment_motor_left is not None:
            motor = attachment_motor_left
        elif port == ATTACHMENT_PORT_RIGHT and attachment_motor_right is not None:
            motor = attachment_motor_right
        else:
            # For other ports, try to create a new motor (may fail if nothing connected)
            motor = Motor(port)

        if motor is None:
            print(f"No motor connected on {port}")
            return False

        motor.run_target(speed, position, wait=True)
        return True
    except Exception as e:
        print(f"attachment_to_position error on {port}: {e}")
        return False

# ============================================================================
# LEFT ARM FUNCTIONS (Port A)
# ============================================================================

def left_arm_up(degrees, speed=None):
    """
    Raise the LEFT arm (Port A).

    Args:
        degrees (int): Degrees to raise (positive value)
        speed (int/ArmSpeed): Motor speed in deg/s or ArmSpeed constant
                             Default: ArmSpeed.GRAB (360 deg/s - safe, accurate)
                             Options:
                             - ArmSpeed.DELICATE (200) - Fragile objects
                             - ArmSpeed.GRAB (360) - Standard grab (recommended)
                             - ArmSpeed.COLLECT (500) - Collection missions
                             - ArmSpeed.QUICK (1000) - Fast movements

    Returns:
        bool: True if successful

    Example:
        left_arm_up(90)                      # Default GRAB speed (360)
        left_arm_up(90, ArmSpeed.DELICATE)   # Slow, precise movement
        left_arm_up(45, ArmSpeed.COLLECT)    # Faster collection speed
        left_arm_up(90, 500)                 # Custom numeric speed
    """
    if speed is None:
        speed = ArmSpeed.GRAB
    return run_attachment(ATTACHMENT_PORT_LEFT, abs(degrees), speed)

def left_arm_down(degrees, speed=None):
    """
    Lower the LEFT arm (Port A).

    Args:
        degrees (int): Degrees to lower (positive value)
        speed (int/ArmSpeed): Motor speed (default: ArmSpeed.GRAB = 360)

    Returns:
        bool: True if successful

    Example:
        left_arm_down(90)                    # Default GRAB speed
        left_arm_down(90, ArmSpeed.DELICATE) # Slow, controlled lowering
        left_arm_down(45, ArmSpeed.QUICK)    # Fast lowering
    """
    if speed is None:
        speed = ArmSpeed.GRAB
    return run_attachment(ATTACHMENT_PORT_LEFT, -abs(degrees), speed)

def left_arm_to(position, speed=None):
    """
    Move the LEFT arm (Port A) to an absolute position.

    Args:
        position (int): Target position in degrees
        speed (int/ArmSpeed): Motor speed (default: ArmSpeed.RESET = 720)
                             Use faster speed for repositioning

    Returns:
        bool: True if successful

    Example:
        left_arm_to(0)                     # Reset to home (fast)
        left_arm_to(90, ArmSpeed.GRAB)     # Move to 90° carefully
        left_arm_to(45, ArmSpeed.QUICK)    # Quick positioning
    """
    if speed is None:
        speed = ArmSpeed.RESET
    return attachment_to_position(ATTACHMENT_PORT_LEFT, position, speed)

# ============================================================================
# RIGHT ARM FUNCTIONS (Port E)
# ============================================================================

def right_arm_up(degrees, speed=None):
    """
    Raise the RIGHT arm (Port E).

    Args:
        degrees (int): Degrees to raise (positive value)
        speed (int/ArmSpeed): Motor speed (default: ArmSpeed.GRAB = 360)

    Returns:
        bool: True if successful

    Example:
        right_arm_up(90)                      # Default GRAB speed
        right_arm_up(90, ArmSpeed.DELICATE)   # Slow, precise
        right_arm_up(45, ArmSpeed.COLLECT)    # Faster collection
    """
    if speed is None:
        speed = ArmSpeed.GRAB
    return run_attachment(ATTACHMENT_PORT_RIGHT, abs(degrees), speed)

def right_arm_down(degrees, speed=None):
    """
    Lower the RIGHT arm (Port E).

    Args:
        degrees (int): Degrees to lower (positive value)
        speed (int/ArmSpeed): Motor speed (default: ArmSpeed.GRAB = 360)

    Returns:
        bool: True if successful

    Example:
        right_arm_down(90)                    # Default GRAB speed
        right_arm_down(90, ArmSpeed.DELICATE) # Slow lowering
        right_arm_down(45, ArmSpeed.QUICK)    # Fast lowering
    """
    if speed is None:
        speed = ArmSpeed.GRAB
    return run_attachment(ATTACHMENT_PORT_RIGHT, -abs(degrees), speed)

def right_arm_to(position, speed=None):
    """
    Move the RIGHT arm (Port E) to an absolute position.

    Args:
        position (int): Target position in degrees
        speed (int/ArmSpeed): Motor speed (default: ArmSpeed.RESET = 720)

    Returns:
        bool: True if successful

    Example:
        right_arm_to(0)                    # Reset to home (fast)
        right_arm_to(90, ArmSpeed.GRAB)    # Move to 90° carefully
        right_arm_to(45, ArmSpeed.QUICK)   # Quick positioning
    """
    if speed is None:
        speed = ArmSpeed.RESET
    return attachment_to_position(ATTACHMENT_PORT_RIGHT, position, speed)

# ============================================================================
# BOTH ARMS FUNCTIONS
# ============================================================================

def both_arms_up(degrees, speed=None):
    """
    Raise BOTH arms at the same time.

    Args:
        degrees (int): Degrees to raise (positive value)
        speed (int/ArmSpeed): Motor speed (default: ArmSpeed.GRAB = 360)

    Returns:
        bool: True if both arms moved successfully

    Example:
        both_arms_up(90)                      # Default GRAB speed
        both_arms_up(90, ArmSpeed.COLLECT)    # Faster collection
        both_arms_up(45, ArmSpeed.DELICATE)   # Slow, precise
    """
    if speed is None:
        speed = ArmSpeed.GRAB
    left_ok = left_arm_up(degrees, speed)
    right_ok = right_arm_up(degrees, speed)
    return left_ok and right_ok

def both_arms_down(degrees, speed=None):
    """
    Lower BOTH arms at the same time.

    Args:
        degrees (int): Degrees to lower (positive value)
        speed (int/ArmSpeed): Motor speed (default: ArmSpeed.GRAB = 360)

    Returns:
        bool: True if both arms moved successfully

    Example:
        both_arms_down(90)                    # Default GRAB speed
        both_arms_down(90, ArmSpeed.DELICATE) # Slow, controlled
        both_arms_down(45, ArmSpeed.QUICK)    # Fast lowering
    """
    if speed is None:
        speed = ArmSpeed.GRAB
    left_ok = left_arm_down(degrees, speed)
    right_ok = right_arm_down(degrees, speed)
    return left_ok and right_ok

def reset_arms(speed=None):
    """
    Reset BOTH arms to home position (0 degrees).

    Useful at the start of missions to ensure consistent starting state.

    Args:
        speed (int/ArmSpeed): Motor speed (default: ArmSpeed.RESET = 720)

    Returns:
        bool: True if both arms reset successfully

    Example:
        reset_arms()                   # Reset both arms (fast)
        reset_arms(ArmSpeed.QUICK)     # Very fast reset
        reset_arms(ArmSpeed.GRAB)      # Controlled reset
    """
    if speed is None:
        speed = ArmSpeed.RESET
    left_ok = left_arm_to(0, speed)
    right_ok = right_arm_to(0, speed)
    return left_ok and right_ok

# ============================================================================
# ADVANCED ARM CONTROL WITH LOAD SENSING
# ============================================================================

def get_arm_load(arm='left'):
    """
    Get current load on arm motor.

    Load indicates how hard the motor is working (0-100%).
    Higher load = heavier object or more resistance.

    Args:
        arm (str): Which arm ('left' or 'right')

    Returns:
        int: Load percentage (0-100), or 0 if motor not available

    Example:
        load = get_arm_load('left')
        if load > 60:
            print("Heavy object!")
    """
    try:
        if arm == 'left' and attachment_motor_left:
            return attachment_motor_left.load()
        elif arm == 'right' and attachment_motor_right:
            return attachment_motor_right.load()
        return 0
    except Exception as e:
        print(f"get_arm_load error: {e}")
        return 0

def left_arm_up_monitored(degrees, speed=None, max_load=80):
    """
    Raise left arm with load monitoring and safety cutoff.

    Stops automatically if load exceeds max_load (prevents damage).
    Useful for lifting unknown weights or detecting jams.

    Args:
        degrees (int): Degrees to raise
        speed (int/ArmSpeed): Motor speed (default: ArmSpeed.GRAB)
        max_load (int): Maximum allowed load % (default: 80)

    Returns:
        dict: {
            'success': bool,
            'initial_load': int,
            'max_load': int,
            'final_load': int
        }

    Example:
        result = left_arm_up_monitored(90, ArmSpeed.GRAB, max_load=70)
        if result['success']:
            print(f"Lifted! Max load was {result['max_load']}%")
        else:
            print("Load too high - stopped for safety")
    """
    if speed is None:
        speed = ArmSpeed.GRAB

    if attachment_motor_left is None:
        print("No motor on left arm")
        return {'success': False, 'initial_load': 0, 'max_load': 0, 'final_load': 0}

    try:
        # Record initial load
        initial_load = attachment_motor_left.load()

        # Start movement (non-blocking)
        attachment_motor_left.run_angle(speed, abs(degrees), wait=False)

        # Monitor during movement
        max_observed_load = initial_load
        while not attachment_motor_left.done():
            current_load = attachment_motor_left.load()
            max_observed_load = max(max_observed_load, current_load)

            # Safety cutoff
            if current_load > max_load:
                attachment_motor_left.hold()
                print(f"WARNING: High load detected ({current_load}%) - stopping for safety")
                return {
                    'success': False,
                    'initial_load': initial_load,
                    'max_load': max_observed_load,
                    'final_load': current_load
                }

            wait(10)

        # Completed successfully
        final_load = attachment_motor_left.load()
        return {
            'success': True,
            'initial_load': initial_load,
            'max_load': max_observed_load,
            'final_load': final_load
        }

    except Exception as e:
        print(f"left_arm_up_monitored error: {e}")
        return {'success': False, 'initial_load': 0, 'max_load': 0, 'final_load': 0}

def right_arm_up_monitored(degrees, speed=None, max_load=80):
    """
    Raise right arm with load monitoring and safety cutoff.

    Same as left_arm_up_monitored() but for right arm.
    See left_arm_up_monitored() for full documentation.
    """
    if speed is None:
        speed = ArmSpeed.GRAB

    if attachment_motor_right is None:
        print("No motor on right arm")
        return {'success': False, 'initial_load': 0, 'max_load': 0, 'final_load': 0}

    try:
        initial_load = attachment_motor_right.load()
        attachment_motor_right.run_angle(speed, abs(degrees), wait=False)

        max_observed_load = initial_load
        while not attachment_motor_right.done():
            current_load = attachment_motor_right.load()
            max_observed_load = max(max_observed_load, current_load)

            if current_load > max_load:
                attachment_motor_right.hold()
                print(f"WARNING: High load detected ({current_load}%) - stopping for safety")
                return {
                    'success': False,
                    'initial_load': initial_load,
                    'max_load': max_observed_load,
                    'final_load': current_load
                }

            wait(10)

        final_load = attachment_motor_right.load()
        return {
            'success': True,
            'initial_load': initial_load,
            'max_load': max_observed_load,
            'final_load': final_load
        }

    except Exception as e:
        print(f"right_arm_up_monitored error: {e}")
        return {'success': False, 'initial_load': 0, 'max_load': 0, 'final_load': 0}

def grab_until_load(target_load=40, max_degrees=90, speed=None, arm='left'):
    """
    Close gripper/arm until desired load reached (smart grab).

    Automatically stops when load reaches target (grabbed object)
    or after max_degrees of movement (nothing to grab).

    Perfect for grabbing objects of unknown size!

    Args:
        target_load (int): Desired grip load % (default: 40)
            - 20-30: Light grip (fragile objects)
            - 40-50: Medium grip (standard objects)
            - 60-70: Firm grip (heavy objects)
        max_degrees (int): Maximum degrees to close (default: 90)
        speed (int/ArmSpeed): Motor speed (default: ArmSpeed.DELICATE)
        arm (str): Which arm ('left' or 'right')

    Returns:
        dict: {
            'success': bool,
            'grabbed': bool,
            'final_load': int,
            'degrees_moved': int
        }

    Example:
        # Grab with light grip
        result = grab_until_load(target_load=30, arm='left')
        if result['grabbed']:
            print(f"Grabbed! Load: {result['final_load']}%")
    """
    if speed is None:
        speed = ArmSpeed.DELICATE

    motor = attachment_motor_left if arm == 'left' else attachment_motor_right

    if motor is None:
        print(f"No motor on {arm} arm")
        return {'success': False, 'grabbed': False, 'final_load': 0, 'degrees_moved': 0}

    try:
        # Start closing
        motor.run(-abs(speed))
        initial_angle = motor.angle()

        # Monitor until grabbed or max movement
        while True:
            current_angle = motor.angle()
            degrees_moved = abs(current_angle - initial_angle)
            current_load = motor.load()

            # Check if grabbed (load increased)
            if current_load >= target_load:
                motor.hold()
                print(f"Grabbed! Load: {current_load}%, Moved: {degrees_moved}°")
                return {
                    'success': True,
                    'grabbed': True,
                    'final_load': current_load,
                    'degrees_moved': degrees_moved
                }

            # Check if reached max movement
            if degrees_moved >= max_degrees:
                motor.hold()
                print(f"No object grabbed (moved {degrees_moved}°, load only {current_load}%)")
                return {
                    'success': True,
                    'grabbed': False,
                    'final_load': current_load,
                    'degrees_moved': degrees_moved
                }

            wait(10)

    except Exception as e:
        print(f"grab_until_load error: {e}")
        if motor:
            motor.hold()
        return {'success': False, 'grabbed': False, 'final_load': 0, 'degrees_moved': 0}

def lift_adaptive(degrees, min_speed=None, max_speed=None, arm='left'):
    """
    Lift arm with speed automatically adjusted for load.

    Heavy load → slow speed (more torque)
    Light load → fast speed (more efficient)

    Args:
        degrees (int): Degrees to lift (positive value)
        min_speed (int/ArmSpeed): Minimum speed for heavy loads (default: ArmSpeed.GRAB)
        max_speed (int/ArmSpeed): Maximum speed for light loads (default: ArmSpeed.COLLECT)
        arm (str): Which arm ('left' or 'right')

    Returns:
        dict: {
            'success': bool,
            'avg_load': int,
            'avg_speed': int
        }

    Example:
        # Lifts slowly if heavy, quickly if light
        result = lift_adaptive(90, arm='left')
        print(f"Lifted with avg load: {result['avg_load']}%")
    """
    if min_speed is None:
        min_speed = ArmSpeed.GRAB
    if max_speed is None:
        max_speed = ArmSpeed.COLLECT

    motor = attachment_motor_left if arm == 'left' else attachment_motor_right

    if motor is None:
        print(f"No motor on {arm} arm")
        return {'success': False, 'avg_load': 0, 'avg_speed': 0}

    try:
        target_angle = motor.angle() + abs(degrees)

        total_load = 0
        total_speed = 0
        samples = 0

        # Start moving
        motor.run(min_speed)

        while abs(motor.angle() - target_angle) > 5:
            current_load = motor.load()

            # Adjust speed based on load
            # High load (>70%) → min_speed (slow, high torque)
            # Medium load (40-70%) → medium speed
            # Low load (<40%) → max_speed (fast)
            if current_load > 70:
                speed = min_speed
            elif current_load > 40:
                # Linear interpolation between min and max
                speed = int(min_speed + (max_speed - min_speed) * (70 - current_load) / 30)
            else:
                speed = max_speed

            motor.run(speed)

            # Track statistics
            total_load += current_load
            total_speed += speed
            samples += 1

            wait(50)

        motor.hold()

        avg_load = total_load // samples if samples > 0 else 0
        avg_speed = total_speed // samples if samples > 0 else 0

        return {
            'success': True,
            'avg_load': avg_load,
            'avg_speed': avg_speed
        }

    except Exception as e:
        print(f"lift_adaptive error: {e}")
        if motor:
            motor.hold()
        return {'success': False, 'avg_load': 0, 'avg_speed': 0}

def reset_arm_to_limit(arm='left', speed=None):
    """
    Reset arm to mechanical limit using stall detection.

    Finds the mechanical "zero" position by running until motor stalls,
    then sets that position as 0°. Perfect for reliable arm calibration!

    Args:
        arm (str): Which arm ('left' or 'right')
        speed (int/ArmSpeed): Speed to approach limit (default: ArmSpeed.STALL)

    Returns:
        bool: True if successful

    Example:
        # Reset arm to known position
        if reset_arm_to_limit('left'):
            print("Left arm calibrated to mechanical zero")

    Note:
        - Uses low power (20% duty) to avoid damage
        - Backs off 10° after hitting limit
        - Sets position to 0° after calibration
    """
    if speed is None:
        speed = ArmSpeed.STALL

    motor = attachment_motor_left if arm == 'left' else attachment_motor_right

    if motor is None:
        print(f"No motor on {arm} arm")
        return False

    try:
        print(f"Calibrating {arm} arm to mechanical limit...")

        # Configure stall detection
        motor.control.stalls(
            duty_limit=20,  # Consider stalled at 20% duty
            time=100        # Must be stalled for 100ms
        )

        # Run until stalled (hits mechanical limit)
        stall_angle = motor.run_until_stalled(
            speed=-abs(speed),
            then=Stop.HOLD,
            duty_limit=20  # Use only 20% power
        )

        print(f"{arm} arm hit limit at {stall_angle}°")

        # Back off slightly from limit
        motor.run_angle(abs(speed), 10, wait=True)

        # Reset encoder to 0
        motor.reset_angle(0)

        print(f"{arm} arm calibrated! Position reset to 0°")
        return True

    except Exception as e:
        print(f"reset_arm_to_limit error: {e}")
        return False

def push_until_resistance(distance_mm, speed=None, load_threshold=75, timeout_ms=5000):
    """
    Push forward until hitting resistance (detected by motor load).

    Perfect for pushing mission models into place!
    Stops when drive motors detect high resistance.

    Args:
        distance_mm (int): Maximum distance to push
        speed (int/DriveSpeed): Push speed (default: DriveSpeed.PUSHING)
        load_threshold (int): Load % to consider "resistance" (default: 75)
        timeout_ms (int): Maximum time to push (default: 5000)

    Returns:
        dict: {
            'success': bool,
            'distance_traveled': int,
            'final_load': int,
            'stopped_reason': str  # 'resistance', 'distance', or 'timeout'
        }

    Example:
        result = push_until_resistance(200, DriveSpeed.PUSHING)
        if result['stopped_reason'] == 'resistance':
            print("Model pushed into place!")
    """
    if speed is None:
        speed = DriveSpeed.PUSHING

    try:
        print(f"Pushing until resistance (threshold: {load_threshold}%)...")

        # Start pushing forward
        robot.drive(speed, 0)

        # Track progress
        stopwatch = StopWatch()
        stopwatch.reset()
        initial_left = left_motor.angle()
        initial_right = right_motor.angle()

        while stopwatch.time() < timeout_ms:
            # Check drive motor loads
            left_load = left_motor.load()
            right_load = right_motor.load()
            avg_load = (left_load + right_load) / 2

            # Calculate distance traveled
            left_degrees = abs(left_motor.angle() - initial_left)
            right_degrees = abs(right_motor.angle() - initial_right)
            avg_degrees = (left_degrees + right_degrees) / 2
            distance_traveled = int((avg_degrees / 360) * WHEEL_CIRCUMFERENCE)

            # Check if hit resistance
            if avg_load >= load_threshold:
                robot.stop()
                print(f"Resistance detected! Load: {avg_load}%, Distance: {distance_traveled}mm")
                return {
                    'success': True,
                    'distance_traveled': distance_traveled,
                    'final_load': int(avg_load),
                    'stopped_reason': 'resistance'
                }

            # Check if reached max distance
            if distance_traveled >= distance_mm:
                robot.stop()
                print(f"Max distance reached: {distance_traveled}mm")
                return {
                    'success': True,
                    'distance_traveled': distance_traveled,
                    'final_load': int(avg_load),
                    'stopped_reason': 'distance'
                }

            wait(10)

        # Timeout
        robot.stop()
        left_degrees = abs(left_motor.angle() - initial_left)
        right_degrees = abs(right_motor.angle() - initial_right)
        avg_degrees = (left_degrees + right_degrees) / 2
        distance_traveled = int((avg_degrees / 360) * WHEEL_CIRCUMFERENCE)

        print(f"Push timeout after {distance_traveled}mm")
        return {
            'success': False,
            'distance_traveled': distance_traveled,
            'final_load': int((left_motor.load() + right_motor.load()) / 2),
            'stopped_reason': 'timeout'
        }

    except Exception as e:
        print(f"push_until_resistance error: {e}")
        robot.stop()
        return {'success': False, 'distance_traveled': 0, 'final_load': 0, 'stopped_reason': 'error'}

# ============================================================================
# SENSOR-BASED MOVEMENT FUNCTIONS
# ============================================================================

def move_until_line(speed=DEFAULT_SPEED, sensor_port=Port.E,
                   target_reflection=20, timeout_ms=5000):
    """
    Move forward until color sensor detects a line (dark surface).

    Uses reflection value to detect when robot crosses from light to dark surface.
    Includes timeout protection to prevent infinite loops.

    Args:
        speed (int): Movement speed in mm/s (default: DEFAULT_SPEED=200)
        sensor_port (Port): Color sensor port (default: Port.E)
        target_reflection (int): Reflection threshold (0-100, default: 20)
                                Values below this indicate dark line
        timeout_ms (int): Maximum time to search in milliseconds (default: 5000)

    Returns:
        bool: True if line detected, False if timeout

    Example:
        move_until_line(200)                    # Move until black line
        move_until_line(150, Port.F, 30, 3000)  # Custom sensor and threshold

    Note:
        - Calibrate target_reflection on your mat (typically 15-25 for black)
        - White mat typically reads 90-100
        - Requires ColorSensor connected to specified port
    """
    try:
        sensor = ColorSensor(sensor_port)
        robot.drive(speed, 0)

        stopwatch = StopWatch()
        stopwatch.reset()

        while stopwatch.time() < timeout_ms:
            if sensor.reflection() < target_reflection:
                robot.stop()
                return True
            wait(10)

        # Timeout reached
        robot.stop()
        print(f"move_until_line timeout after {timeout_ms}ms")
        return False

    except Exception as e:
        print(f"move_until_line error: {e}")
        robot.stop()
        return False

def move_until_distance(speed=DEFAULT_SPEED, sensor_port=Port.F,
                       target_distance_mm=50, timeout_ms=5000):
    """
    Move forward until distance sensor detects object within range.

    Args:
        speed (int): Movement speed in mm/s (default: DEFAULT_SPEED=200)
        sensor_port (Port): Ultrasonic sensor port (default: Port.F)
        target_distance_mm (int): Stop distance in mm (default: 50)
        timeout_ms (int): Maximum time to search in milliseconds (default: 5000)

    Returns:
        bool: True if object detected, False if timeout

    Example:
        move_until_distance(200, Port.F, 100)  # Move until 10cm from object
    """
    try:
        sensor = UltrasonicSensor(sensor_port)
        robot.drive(speed, 0)

        stopwatch = StopWatch()
        stopwatch.reset()

        while stopwatch.time() < timeout_ms:
            distance = sensor.distance()
            if distance <= target_distance_mm:
                robot.stop()
                return True
            wait(10)

        # Timeout reached
        robot.stop()
        print(f"move_until_distance timeout after {timeout_ms}ms")
        return False

    except Exception as e:
        print(f"move_until_distance error: {e}")
        robot.stop()
        return False

# ============================================================================
# ADVANCED UTILITY FUNCTIONS
# ============================================================================

def safe_move_with_retry(move_function, *args, max_retries=2, **kwargs):
    """
    Execute a movement function with automatic retry on failure.

    Wrapper function that adds error recovery to any movement function.

    Args:
        move_function: Function to call (e.g., move_straight, turn)
        *args: Positional arguments for the function
        max_retries (int): Maximum retry attempts (default: 2)
        **kwargs: Keyword arguments for the function

    Returns:
        bool: True if movement succeeded (possibly after retry)

    Example:
        safe_move_with_retry(move_straight, 500, max_retries=3)
        safe_move_with_retry(spin_turn, 90, speed=200)

    Note:
        Adds 500ms delay between retry attempts
    """
    for attempt in range(max_retries + 1):
        try:
            result = move_function(*args, **kwargs)
            if result:  # If function returns True, success
                return True
            # If function returns False but didn't raise exception
            if attempt < max_retries:
                print(f"Retry {attempt + 1}/{max_retries}...")
                wait(500)
                robot.stop()  # Ensure stopped before retry
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries:
                wait(500)
                robot.stop()
            else:
                return False

    return False

def check_battery():
    """
    Check battery voltage and warn if low.

    Returns:
        tuple: (voltage_mv, is_ok) where voltage is in millivolts
               and is_ok is True if voltage is acceptable

    Example:
        voltage, ok = check_battery()
        if not ok:
            print("Battery low! Charge before competition.")
    """
    MIN_SAFE_VOLTAGE = 4400  # mV 7800

    voltage = hub.battery.voltage()
    is_ok = voltage >= MIN_SAFE_VOLTAGE

    if not is_ok:
        print(f"WARNING: Battery low ({voltage}mV, min: {MIN_SAFE_VOLTAGE}mV)")
        hub.light.on(Color.RED)
    else:
        print(f"Battery OK: {voltage}mV")

    return voltage, is_ok

def calibrate_gyro():
    """
    Calibrate gyro sensor (must be on flat, stable surface).

    Call this at the start of each competition run to ensure
    accurate gyro readings. Robot must not be touched during calibration.

    Returns:
        bool: True if calibration successful

    Example:
        print("Place robot on flat surface. Do not touch.")
        wait(1000)
        if calibrate_gyro():
            print("Calibration complete!")
    """
    try:
        print("Calibrating gyro... DO NOT MOVE ROBOT")
        hub.imu.reset_heading(0)
        wait(1000)  # Allow gyro to stabilize

        # Check if gyro is stable (should be near 0)
        heading = hub.imu.heading()
        if abs(heading) > 5:
            print(f"WARNING: Gyro unstable (heading: {heading})")
            return False

        print("Gyro calibration complete")
        return True

    except Exception as e:
        print(f"calibrate_gyro error: {e}")
        return False

def get_robot_status():
    """
    Print comprehensive robot status for diagnostics.

    Useful for pre-competition checks and debugging.

    Returns:
        dict: Status information
    """
    status = {}

    try:
        # Battery
        voltage = hub.battery.voltage()
        status['battery_mv'] = voltage
        status['battery_ok'] = voltage >= 4800 # original 7800

        # Gyro
        status['heading'] = hub.imu.heading()
        status['gyro_ok'] = abs(hub.imu.heading()) < 5

        # Motors
        status['left_motor_angle'] = left_motor.angle()
        status['right_motor_angle'] = right_motor.angle()

        # Print summary
        print("=== ROBOT STATUS ===")
        print(f"Battery: {voltage}mV {'✓' if status['battery_ok'] else '✗ LOW'}")
        print(f"Heading: {status['heading']}° {'✓' if status['gyro_ok'] else '✗ UNSTABLE'}")
        print(f"Left motor: {status['left_motor_angle']}°")
        print(f"Right motor: {status['right_motor_angle']}°")
        print("===================")

        return status

    except Exception as e:
        print(f"get_robot_status error: {e}")
        return {}

# ============================================================================
# SPEED PRESET HELPER FUNCTION
# ============================================================================

def list_speed_presets():
    """
    Print all available speed presets with their values and use cases.

    Useful for reference during mission programming.
    """
    print("=" * 70)
    print("AVAILABLE SPEED PRESETS")
    print("=" * 70)
    print(f"{'Speed Constant':<25} {'Value':<10} {'Use Case'}")
    print("-" * 70)
    print(f"{'DriveSpeed.PRECISE':<25} {DriveSpeed.PRECISE:<10} Final positioning")
    print(f"{'DriveSpeed.APPROACH':<25} {DriveSpeed.APPROACH:<10} Approaching models")
    print(f"{'DriveSpeed.COLLECTION':<25} {DriveSpeed.COLLECTION:<10} Object collection")
    print(f"{'DriveSpeed.TRANSIT':<25} {DriveSpeed.TRANSIT:<10} Moving between areas")
    print(f"{'DriveSpeed.RETURN':<25} {DriveSpeed.RETURN:<10} Returning to base")
    print(f"{'DriveSpeed.PUSHING':<25} {DriveSpeed.PUSHING:<10} Pushing objects")
    print("=" * 70)
    print("\nUsage examples:")
    print("  move_straight(300, DriveSpeed.TRANSIT)")
    print("  move_straight_gyro(500, DriveSpeed.APPROACH)")
    print("  move_straight(100, DriveSpeed.PRECISE)")
    print("  move_straight(400, 650)  # Custom numeric speed")

# ============================================================================
# EXAMPLE USAGE AND TESTING
# ============================================================================

def test_movements():
    """
    Test all basic movement functions.

    Run this to verify robot is working correctly after configuration changes.
    Comment out sections as needed for focused testing.
    """
    print("=== Testing Basic Movements ===")

    # Test 1: Basic straight movement
    print("Test 1: Forward 200mm")
    move_straight(200)
    wait(1000)

    # Test 2: Turn
    print("Test 2: Turn right 90°")
    turn(90)
    wait(1000)

    # Test 3: Backward movement
    print("Test 3: Backward 100mm")
    move_straight(-100)
    wait(1000)

    # Test 4: Turn opposite direction
    print("Test 4: Turn left 90°")
    turn(-90)
    wait(1000)

    # Test 5: Pivot turn
    print("Test 5: Pivot turn right 45°")
    pivot_turn(45)
    wait(1000)

    # Test 6: Gyro-corrected movement
    print("Test 6: Gyro-corrected 300mm")
    move_straight_gyro(300)
    wait(1000)

    # Test 7: Precise spin turn
    print("Test 7: Spin turn 90°")
    spin_turn(90)
    wait(1000)

    print("=== Movement tests complete ===")

def test_attachments():
    """
    Test attachment motor functions.

    Requires attachment motors connected to ATTACHMENT_PORT_1 and ATTACHMENT_PORT_2.
    """
    print("=== Testing Attachments ===")

    # Test arm up/down
    print("Test 1: Arm up 90°")
    arm_up(90)
    wait(1000)

    print("Test 2: Arm down 90°")
    arm_down(90)
    wait(1000)

    # Test reset
    print("Test 3: Reset attachments")
    reset_attachments()
    wait(1000)

    print("=== Attachment tests complete ===")

def calibration_test():
    """
    Quick calibration and accuracy test.

    Tests movement accuracy over known distances.
    Measure actual distance traveled and compare to expected.
    """
    print("=== Calibration Test ===")

    # Check battery
    voltage, ok = check_battery()
    if not ok:
        print("WARNING: Battery too low for accurate testing")
        return

    # Calibrate gyro
    print("\nCalibrating gyro...")
    if not calibrate_gyro():
        print("Gyro calibration failed")
        return

    # Test straight accuracy (measure this manually)
    print("\n--- Testing 300mm forward ---")
    print("Mark starting position. Press button to continue.")
    # Wait for button press (implement based on your needs)
    wait(2000)

    move_straight_gyro(300, speed=200)
    print("Measure actual distance traveled. Should be 300mm ±5mm")
    wait(3000)

    # Return to start
    move_straight_gyro(-300, speed=200)
    wait(2000)

    # Test turn accuracy
    print("\n--- Testing 90° turn ---")
    print("Mark starting angle. Press button to continue.")
    wait(2000)

    spin_turn(90)
    print("Check if robot turned exactly 90°. Should be within ±2°")
    wait(3000)

    print("\n=== Calibration test complete ===")

def competition_ready_check():
    """
    Comprehensive pre-competition check.

    Run this before each competition round to ensure robot is ready.
    """
    print("=" * 40)
    print("COMPETITION READINESS CHECK")
    print("=" * 40)

    # Check 1: Robot status
    print("\n1. Checking robot status...")
    status = get_robot_status()

    if not status.get('battery_ok', False):
        print("FAIL: Battery voltage too low")
        return False

    if not status.get('gyro_ok', False):
        print("WARNING: Gyro reading unusual (may need recalibration)")

    # Check 2: Calibrate gyro
    print("\n2. Calibrating gyro...")
    if not calibrate_gyro():
        print("FAIL: Gyro calibration failed")
        return False

    # Check 3: Quick movement test
    print("\n3. Testing basic movement...")
    try:
        # Small movements to verify motors work
        result = move_straight(50)
        if not result:
            print("FAIL: Forward movement failed")
            return False

        result = move_straight(-50)
        if not result:
            print("FAIL: Backward movement failed")
            return False

        result = spin_turn(45)
        if result == 0:  # Error return
            print("FAIL: Turn failed")
            return False

        spin_turn(-45)  # Return to start angle

    except Exception as e:
        print(f"FAIL: Movement test error: {e}")
        return False

    # All checks passed
    print("\n" + "=" * 40)
    print("✓ ROBOT READY FOR COMPETITION")
    print("=" * 40)
    hub.light.on(Color.GREEN)
    return True

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    """
    Main execution block.

    Uncomment the function you want to run, or create your own mission code here.
    """

    # Pre-competition check (recommended before each round)
    # competition_ready_check()

    # Test basic movements
    test_movements()

    # Test attachments
    # test_attachments()

    # Calibration test
    # calibration_test()

    # Example: Single movement test
    # move_straight_gyro(500, speed=200)

    # Example: Spin turn test
    # spin_turn(90)

    # Example: Check robot status
    get_robot_status()

    # Example: List speed presets
    # list_speed_presets()

    # Example mission using speed presets
    # move_straight_gyro(600, DriveSpeed.TRANSIT)   # Fast transit (type-safe!)
    # spin_turn(90)
    #move_straight(-200, DriveSpeed.APPROACH)       # Approach mission
    # move_straight(50, DriveSpeed.PRECISE)         # Final positioning
    # arm_down(90)
    # move_straight(-250, DriveSpeed.RETURN)        # Fast return

    print("\nRobot initialized and ready!")
    print("Edit __main__ section to run your code.")
    print("\nDriveSpeed presets available:")
    print("  DriveSpeed.PRECISE    - 100 mm/s  (high accuracy)")
    print("  DriveSpeed.APPROACH   - 300 mm/s  (moderate speed)")
    print("  DriveSpeed.COLLECTION - 500 mm/s  (good balance)")
    print("  DriveSpeed.TRANSIT    - 700 mm/s  (fast movement)")
    print("  DriveSpeed.RETURN     - 900 mm/s  (maximum speed)")
    print("  DriveSpeed.PUSHING    - 600 mm/s  (high power)")
