# FLL ROBOT CONTROL - API REFERENCE
**Complete Reference for SPIKE Prime Robot Control**

---

## Table of Contents
1. [Speed Constants](#speed-constants)
   - DriveSpeed
   - TurnSpeed
   - ArmSpeed
2. [Movement Functions](#movement-functions)
   - move_straight(), move_straight_gyro()
   - turn(), spin_turn(), pivot_turn()
   - tank_move()
3. [Arm Control Functions](#arm-control-functions)
   - Left/Right Arm Functions
   - Both Arms Functions
   - Advanced Load Sensing Functions
4. [Sensor-Based Movement](#sensor-based-movement)
5. [Utility Functions](#utility-functions)
6. [Configuration Constants](#configuration-constants)
7. [Complete Examples](#complete-examples)

---

## Speed Constants

### DriveSpeed - Robot Movement Speeds
Used for driving, turning, and robot movement (units: mm/s)

```python
from robot import DriveSpeed

DriveSpeed.PRECISE      # 100 mm/s - Final positioning (±0.5cm accuracy)
DriveSpeed.APPROACH     # 300 mm/s - Approaching models (±1cm accuracy)
DriveSpeed.COLLECTION   # 500 mm/s - Object collection (±2cm accuracy)
DriveSpeed.TRANSIT      # 700 mm/s - Moving between areas (±3cm accuracy)
DriveSpeed.RETURN       # 900 mm/s - Returning to base (±4cm accuracy)
DriveSpeed.PUSHING      # 600 mm/s - Pushing heavy objects (high power)
```

**When to use:**
- **PRECISE**: Within 5cm of target, final alignment
- **APPROACH**: 5-20cm from target, moderate precision
- **COLLECTION**: Object collection, balanced speed/accuracy
- **TRANSIT**: Long straight runs (>50cm), speed priority
- **RETURN**: Going home, maximum speed, precision not critical
- **PUSHING**: Heavy objects, ramps, need extra torque

### TurnSpeed - Turn/Rotation Speeds
Used for turning and rotation control (units: deg/s)

```python
from robot import TurnSpeed

# PRECISE TURNS (40-80 deg/s) - Highest accuracy
TurnSpeed.ALIGNMENT     # 40 deg/s  - Ultra-precise (±0.5° accuracy)
TurnSpeed.PRECISE       # 60 deg/s  - High precision (±1° accuracy)

# STANDARD TURNS (80-120 deg/s) - Good balance
TurnSpeed.STANDARD      # 100 deg/s - Default balanced (±2° accuracy)
TurnSpeed.APPROACH      # 120 deg/s - Fast approach (±3° accuracy)

# FAST TURNS (150-200 deg/s) - Speed priority
TurnSpeed.QUICK         # 150 deg/s - Quick reposition (±4° accuracy)
TurnSpeed.REPOSITION    # 200 deg/s - Maximum speed (±5° accuracy)

# SPECIALIZED TURNS
TurnSpeed.PIVOT         # 80 deg/s  - Pivot turns (one wheel stationary)
TurnSpeed.CURVE         # 60 deg/s  - Curved paths (continuous turning)
```

**When to use:**
- **ALIGNMENT**: Final docking, critical angle positioning (< 1° error)
- **PRECISE**: Default for spin_turn(), IMU-based turns (< 2° error)
- **STANDARD**: Default for turn(), general purpose (< 3° error)
- **APPROACH**: Fast transitions between mission areas
- **QUICK**: Time-saving turns, mid-mission repositioning
- **REPOSITION**: Return to base, maximum safe turn speed
- **PIVOT**: Space-constrained environments, tight corners
- **CURVE**: Following curved paths, arc movements

**Turn Method Selection:**
- `spin_turn()` → Use TurnSpeed.PRECISE (IMU feedback, most accurate)
- `turn()` → Use TurnSpeed.STANDARD (open-loop, faster)
- `pivot_turn()` → Use TurnSpeed.PIVOT (tightest radius)

### ArmSpeed - Arm/Attachment Speeds
Used for attachment motors and arm control (units: deg/s)

```python
from robot import ArmSpeed

ArmSpeed.DELICATE   # 200 deg/s - Fragile objects, precise placement
ArmSpeed.GRAB       # 360 deg/s - Standard grab (most common, safest)
ArmSpeed.COLLECT    # 500 deg/s - Collection missions
ArmSpeed.MODERATE   # 640 deg/s - Faster collections
ArmSpeed.RESET      # 720 deg/s - Repositioning, resets
ArmSpeed.QUICK      # 1000 deg/s - Maximum safe speed
ArmSpeed.PUSH       # 400 deg/s - Pushing objects, force operations
ArmSpeed.STALL      # 200 deg/s - Stall detection
```

**When to use:**
- **DELICATE**: Fragile objects, precise coral placement
- **GRAB**: Standard grabbing (default, most reliable)
- **COLLECT**: Fast collection sequences
- **MODERATE**: Time-critical collections
- **RESET**: Quick repositioning between missions
- **QUICK**: Emergency operations, fast release
- **PUSH**: Applying force, pushing structures
- **STALL**: Detecting mechanical limits

---

## Movement Functions

### move_straight()
Move robot straight for a given distance (open-loop, no gyro correction)

```python
move_straight(distance_mm, speed=DEFAULT_SPEED)
```

**Parameters:**
- `distance_mm` (int/float): Distance in millimeters
  - Positive = forward
  - Negative = backward
- `speed` (int/DriveSpeed): Speed in mm/s (default: 300)

**Returns:** `bool` - True if successful

**Examples:**
```python
move_straight(300)                          # Forward 300mm at default speed
move_straight(500, DriveSpeed.TRANSIT)      # Fast forward movement
move_straight(-200, DriveSpeed.PRECISE)     # Backward slowly
move_straight(400, 650)                     # Custom speed 650 mm/s
```

**Notes:**
- May drift without gyro correction on long distances
- Use `move_straight_gyro()` for better accuracy

---

### move_straight_gyro()
Move straight with gyro correction for maximum accuracy

```python
move_straight_gyro(distance_mm, speed=DEFAULT_SPEED, kp=GYRO_PROPORTIONAL_GAIN)
```

**Parameters:**
- `distance_mm` (int/float): Distance in millimeters
- `speed` (int/DriveSpeed): Speed in mm/s (default: 300)
- `kp` (float): Proportional gain for correction (default: 2.0)
  - Increase (2.5-3.0) if robot doesn't correct enough
  - Decrease (1.0-1.5) if robot oscillates

**Returns:** `bool` - True if successful

**Examples:**
```python
move_straight_gyro(500)                            # Default speed with gyro
move_straight_gyro(800, DriveSpeed.TRANSIT)        # Fast with correction
move_straight_gyro(300, DriveSpeed.APPROACH, 2.5)  # Custom correction gain
```

**Notes:**
- **Best function for accuracy** - uses IMU feedback
- Recommended for distances > 200mm
- Update rate: 100Hz (10ms loop)
- Typical accuracy: ±1cm at 300mm/s, ±2cm at 700mm/s

---

### turn()
Turn robot by specified angle (open-loop, both wheels opposite directions)

```python
turn(angle_degrees, speed=None)
```

**Parameters:**
- `angle_degrees` (int/float): Angle to turn
  - Positive = right (clockwise)
  - Negative = left (counterclockwise)
- `speed` (int/TurnSpeed): Turn rate in deg/s or TurnSpeed constant
  - **Default:** TurnSpeed.STANDARD (100 deg/s)
  - Options: TurnSpeed.ALIGNMENT, PRECISE, STANDARD, APPROACH, QUICK, REPOSITION
  - Or numeric: Custom turn rate

**Returns:** `bool` - True if successful

**Examples:**
```python
turn(90)                           # Default STANDARD speed (100 deg/s)
turn(90, TurnSpeed.QUICK)          # Fast turn (150 deg/s)
turn(-45, TurnSpeed.PRECISE)       # Slower, more accurate (60 deg/s)
turn(180, TurnSpeed.REPOSITION)    # Maximum speed (200 deg/s)
turn(90, 150)                      # Custom numeric speed
```

**Notes:**
- Open-loop (no gyro feedback) - faster but less accurate
- Use `spin_turn()` for precise angle control with IMU feedback
- Default TurnSpeed.STANDARD provides good balance (±2° accuracy)

---

### spin_turn()
Precise spin turn using IMU sensor with proportional control

```python
spin_turn(target_angle, speed=None)
```

**Parameters:**
- `target_angle` (int/float): Target angle (relative to current heading)
  - Positive = right (clockwise)
  - Negative = left (counterclockwise)
- `speed` (int/TurnSpeed): Base speed for IMU turn or TurnSpeed constant
  - **Default:** TurnSpeed.PRECISE (60 deg/s)
  - Options: TurnSpeed.ALIGNMENT (40), PRECISE (60), STANDARD (100)
  - Or numeric: Custom base speed

**Returns:** `float` - Final angle achieved

**Examples:**
```python
spin_turn(90)                           # Default PRECISE speed (60 deg/s)
spin_turn(90, TurnSpeed.ALIGNMENT)      # Ultra-precise (40 deg/s, ±0.5°)
spin_turn(-45, TurnSpeed.STANDARD)      # Faster turn (100 deg/s, ±2°)
final = spin_turn(180, TurnSpeed.PRECISE)  # Returns final angle for verification
```

**Notes:**
- **Most accurate turning function** - uses IMU feedback
- Stopping tolerance: ±2 degrees
- Uses proportional control: `motor_speed = base_speed + (error × Kp)`
- Faster when far from target, slower when close
- Update rate: 100Hz (10ms loop)
- Recommended for angle-critical missions

---

### pivot_turn()
Pivot turn around one stationary wheel (tighter turn than spin turn)

```python
pivot_turn(angle_degrees, speed=None)
```

**Parameters:**
- `angle_degrees` (int/float): Robot angle to turn
  - Positive = pivot right (around right wheel)
  - Negative = pivot left (around left wheel)
- `speed` (int/TurnSpeed): Motor speed or TurnSpeed constant
  - **Default:** TurnSpeed.PIVOT (80 deg/s)
  - Options: TurnSpeed.ALIGNMENT, PRECISE, PIVOT, STANDARD
  - Or numeric: Custom speed

**Returns:** `bool` - True if successful

**Examples:**
```python
pivot_turn(90)                        # Default PIVOT speed (80 deg/s)
pivot_turn(90, TurnSpeed.PRECISE)     # Slower, more accurate (60 deg/s)
pivot_turn(-45, TurnSpeed.QUICK)      # Faster pivot (150 deg/s)
```

**Notes:**
- Tightest radius (~50% less space than spin turn)
- One wheel stationary, other moves in arc
- May be less accurate than spin turn
- TurnSpeed.PIVOT (80) recommended for best accuracy
- Perfect for space-constrained environments

---

### tank_move()
Tank-style controls with independent left/right speeds

```python
tank_move(left_speed, right_speed, duration_ms)
```

**Parameters:**
- `left_speed` (int): Left wheel speed (-100 to 100)
- `right_speed` (int): Right wheel speed (-100 to 100)
- `duration_ms` (int): Duration in milliseconds

**Examples:**
```python
tank_move(50, 50, 2000)     # Forward for 2 seconds
tank_move(50, -50, 1000)    # Spin right for 1 second
tank_move(80, 20, 1500)     # Curve right for 1.5 seconds
```

---

## Arm Control Functions

### Left Arm (Port A)

#### left_arm_up()
Raise the left arm

```python
left_arm_up(degrees, speed=None)
```

**Parameters:**
- `degrees` (int): Degrees to raise (positive value)
- `speed` (int/ArmSpeed): Motor speed (default: ArmSpeed.GRAB = 360)

**Returns:** `bool` - True if successful

**Examples:**
```python
left_arm_up(90)                      # Default GRAB speed
left_arm_up(90, ArmSpeed.DELICATE)   # Slow, precise
left_arm_up(45, ArmSpeed.QUICK)      # Fast movement
left_arm_up(90, 500)                 # Custom speed
```

---

#### left_arm_down()
Lower the left arm

```python
left_arm_down(degrees, speed=None)
```

**Parameters:**
- `degrees` (int): Degrees to lower (positive value)
- `speed` (int/ArmSpeed): Motor speed (default: ArmSpeed.GRAB = 360)

**Returns:** `bool` - True if successful

**Examples:**
```python
left_arm_down(90)                    # Default GRAB speed
left_arm_down(90, ArmSpeed.COLLECT)  # Faster collection
```

---

#### left_arm_to()
Move left arm to absolute position

```python
left_arm_to(position, speed=None)
```

**Parameters:**
- `position` (int): Target position in degrees
- `speed` (int/ArmSpeed): Motor speed (default: ArmSpeed.RESET = 720)

**Returns:** `bool` - True if successful

**Examples:**
```python
left_arm_to(0)                     # Reset to home (fast)
left_arm_to(90, ArmSpeed.GRAB)     # Move to 90° carefully
```

---

### Right Arm (Port E)

#### right_arm_up()
Raise the right arm

```python
right_arm_up(degrees, speed=None)
```

**Parameters:** Same as `left_arm_up()`

**Examples:**
```python
right_arm_up(90)                      # Default GRAB speed
right_arm_up(90, ArmSpeed.DELICATE)   # Slow, precise
```

---

#### right_arm_down()
Lower the right arm

```python
right_arm_down(degrees, speed=None)
```

**Parameters:** Same as `left_arm_down()`

**Examples:**
```python
right_arm_down(90)                    # Default GRAB speed
right_arm_down(45, ArmSpeed.QUICK)    # Fast lowering
```

---

#### right_arm_to()
Move right arm to absolute position

```python
right_arm_to(position, speed=None)
```

**Parameters:** Same as `left_arm_to()`

**Examples:**
```python
right_arm_to(0)                    # Reset to home
right_arm_to(45, ArmSpeed.GRAB)    # Move to 45°
```

---

### Both Arms

#### both_arms_up()
Raise both arms simultaneously

```python
both_arms_up(degrees, speed=None)
```

**Parameters:**
- `degrees` (int): Degrees to raise (positive value)
- `speed` (int/ArmSpeed): Motor speed (default: ArmSpeed.GRAB = 360)

**Returns:** `bool` - True if both successful

**Examples:**
```python
both_arms_up(90)                      # Default GRAB speed
both_arms_up(90, ArmSpeed.COLLECT)    # Faster collection
```

---

#### both_arms_down()
Lower both arms simultaneously

```python
both_arms_down(degrees, speed=None)
```

**Parameters:** Same as `both_arms_up()`

**Examples:**
```python
both_arms_down(90)                    # Default GRAB speed
both_arms_down(45, ArmSpeed.DELICATE) # Slow, controlled
```

---

#### reset_arms()
Reset both arms to home position (0 degrees)

```python
reset_arms(speed=None)
```

**Parameters:**
- `speed` (int/ArmSpeed): Motor speed (default: ArmSpeed.RESET = 720)

**Returns:** `bool` - True if both successful

**Examples:**
```python
reset_arms()                   # Fast reset (default)
reset_arms(ArmSpeed.QUICK)     # Very fast
reset_arms(ArmSpeed.GRAB)      # Controlled reset
```

**Notes:**
- Call at start of missions for consistent state
- Fast default speed for efficiency

---

### Advanced Arm Control with Load Sensing

The robot supports intelligent arm control with load sensing for adaptive behavior and safety monitoring.

#### get_arm_load()
Get current motor load (0-100% torque/effort)

```python
get_arm_load(arm='left')
```

**Parameters:**
- `arm` (str): Which arm ('left' or 'right')

**Returns:** `int` - Load percentage (0-100)

**Examples:**
```python
load = get_arm_load('left')
if load > 60:
    print("Heavy object!")
elif load < 20:
    print("Light object or empty")
```

**Notes:**
- 0% = No load (free movement)
- 20-40% = Light object
- 40-60% = Medium object
- 60-80% = Heavy object
- 80-100% = Very heavy or stalled

---

#### left_arm_up_monitored() / right_arm_up_monitored()
Lift arm with safety monitoring and load cutoff

```python
left_arm_up_monitored(degrees, speed=None, max_load=80)
right_arm_up_monitored(degrees, speed=None, max_load=80)
```

**Parameters:**
- `degrees` (int): Degrees to lift
- `speed` (int/ArmSpeed): Motor speed (default: ArmSpeed.GRAB)
- `max_load` (int): Maximum allowed load % (default: 80)

**Returns:** `dict` with keys:
- `success` (bool): True if completed without stopping
- `initial_load` (int): Load at start
- `max_load` (int): Maximum load observed during movement
- `final_load` (int): Load at end

**Examples:**
```python
result = left_arm_up_monitored(90, ArmSpeed.GRAB, max_load=70)
if result['success']:
    print(f"Lifted! Max load was {result['max_load']}%")
else:
    print("Load too high - stopped for safety")
```

**Notes:**
- Automatically stops if load exceeds `max_load`
- Prevents motor damage from overloading
- Use lower `max_load` for fragile objects
- Use higher `max_load` (85-90) for heavy objects

---

#### grab_until_load()
Smart grab - closes until desired load reached

```python
grab_until_load(target_load=40, max_degrees=90, speed=None, arm='left')
```

**Parameters:**
- `target_load` (int): Desired grip load % (default: 40)
  - 20-30: Light grip (fragile objects)
  - 40-50: Medium grip (standard objects)
  - 60-70: Firm grip (heavy objects)
- `max_degrees` (int): Maximum closing distance (default: 90)
- `speed` (int/ArmSpeed): Motor speed (default: ArmSpeed.DELICATE)
- `arm` (str): Which arm ('left' or 'right')

**Returns:** `dict` with keys:
- `success` (bool): True if operation completed
- `grabbed` (bool): True if object grabbed (load reached target)
- `final_load` (int): Final load percentage
- `degrees_moved` (int): How far arm moved

**Examples:**
```python
# Grab with light grip
result = grab_until_load(target_load=30, arm='left')
if result['grabbed']:
    print(f"Grabbed! Load: {result['final_load']}%")
    print(f"Closed {result['degrees_moved']}°")
else:
    print("Nothing to grab")
```

**Notes:**
- Perfect for unknown object sizes
- Automatically stops when object detected
- Prevents crushing fragile objects
- Returns False if nothing grabbed after max_degrees

---

#### lift_adaptive()
Adaptive lifting - speed automatically adjusts to weight

```python
lift_adaptive(degrees, min_speed=None, max_speed=None, arm='left')
```

**Parameters:**
- `degrees` (int): Degrees to lift (positive value)
- `min_speed` (int/ArmSpeed): Minimum speed for heavy loads (default: ArmSpeed.GRAB)
- `max_speed` (int/ArmSpeed): Maximum speed for light loads (default: ArmSpeed.COLLECT)
- `arm` (str): Which arm ('left' or 'right')

**Returns:** `dict` with keys:
- `success` (bool): True if completed
- `avg_load` (int): Average load during movement
- `avg_speed` (int): Average speed used

**Examples:**
```python
# Lifts slowly if heavy, quickly if light
result = lift_adaptive(90, arm='left')
print(f"Lifted with avg load: {result['avg_load']}%")
```

**Notes:**
- Heavy load (>70%) → uses min_speed (more torque)
- Medium load (40-70%) → interpolated speed
- Light load (<40%) → uses max_speed (efficient)
- Automatically optimizes for efficiency

---

#### reset_arm_to_limit()
Auto-calibration using stall detection

```python
reset_arm_to_limit(arm='left', speed=None)
```

**Parameters:**
- `arm` (str): Which arm ('left' or 'right')
- `speed` (int/ArmSpeed): Approach speed (default: ArmSpeed.STALL)

**Returns:** `bool` - True if successful

**Examples:**
```python
# Reset arm to known position
if reset_arm_to_limit('left'):
    print("Left arm calibrated to mechanical zero")
```

**Notes:**
- Finds mechanical "zero" position automatically
- Uses only 20% duty (safe, low power)
- Backs off 10° after hitting limit
- Sets position to 0° after calibration
- Perfect for reliable arm initialization

---

#### push_until_resistance()
Push forward until hitting resistance (drive motors)

```python
push_until_resistance(distance_mm, speed=None, load_threshold=75, timeout_ms=5000)
```

**Parameters:**
- `distance_mm` (int): Maximum distance to push
- `speed` (int/DriveSpeed): Push speed (default: DriveSpeed.PUSHING)
- `load_threshold` (int): Load % to consider "resistance" (default: 75)
- `timeout_ms` (int): Maximum time to push (default: 5000)

**Returns:** `dict` with keys:
- `success` (bool): True if operation completed
- `distance_traveled` (int): Distance traveled in mm
- `final_load` (int): Final drive motor load
- `stopped_reason` (str): 'resistance', 'distance', or 'timeout'

**Examples:**
```python
result = push_until_resistance(200, DriveSpeed.PUSHING)
if result['stopped_reason'] == 'resistance':
    print("Model pushed into place!")
    print(f"Pushed {result['distance_traveled']}mm")
```

**Notes:**
- Perfect for pushing mission models into position
- Monitors left and right drive motor loads
- Stops automatically when resistance detected
- Use for applying consistent force

---

## Sensor-Based Movement

### move_until_line()
Move forward until color sensor detects dark line

```python
move_until_line(speed=DEFAULT_SPEED, sensor_port=Port.E,
                target_reflection=20, timeout_ms=5000)
```

**Parameters:**
- `speed` (int): Movement speed in mm/s (default: 300)
- `sensor_port` (Port): Color sensor port (default: Port.E)
- `target_reflection` (int): Reflection threshold 0-100 (default: 20)
- `timeout_ms` (int): Maximum search time (default: 5000)

**Returns:** `bool` - True if line detected, False if timeout

**Examples:**
```python
move_until_line(200)                        # Default settings
move_until_line(150, Port.F, 30, 3000)      # Custom sensor and threshold
```

**Notes:**
- Calibrate `target_reflection` on your mat
- Black line typically: 15-25
- White mat typically: 90-100
- Includes timeout protection

---

### move_until_distance()
Move forward until ultrasonic sensor detects object

```python
move_until_distance(speed=DEFAULT_SPEED, sensor_port=Port.F,
                    target_distance_mm=50, timeout_ms=5000)
```

**Parameters:**
- `speed` (int): Movement speed in mm/s (default: 300)
- `sensor_port` (Port): Ultrasonic sensor port (default: Port.F)
- `target_distance_mm` (int): Stop distance in mm (default: 50)
- `timeout_ms` (int): Maximum search time (default: 5000)

**Returns:** `bool` - True if object detected, False if timeout

**Examples:**
```python
move_until_distance(200, Port.F, 100)  # Stop at 10cm from object
```

**Notes:**
- Requires UltrasonicSensor connected
- Includes timeout protection

---

## Utility Functions

### check_battery()
Check battery voltage and warn if low

```python
check_battery()
```

**Returns:** `tuple` - (voltage_mv, is_ok)
- `voltage_mv` (int): Battery voltage in millivolts
- `is_ok` (bool): True if voltage acceptable (>4400mV)

**Examples:**
```python
voltage, ok = check_battery()
if not ok:
    print("Battery low! Charge before competition.")
```

**Notes:**
- Minimum safe voltage: 4400mV
- Hub light turns RED if low
- Run before each competition round

---

### calibrate_gyro()
Calibrate IMU gyro sensor (robot must be stationary)

```python
calibrate_gyro()
```

**Returns:** `bool` - True if calibration successful

**Examples:**
```python
print("Place robot on flat surface. Do not touch.")
wait(1000)
if calibrate_gyro():
    print("Calibration complete!")
```

**Notes:**
- Robot must be on flat, stable surface
- Do not touch robot during calibration
- Takes ~1 second
- Run at start of each competition run

---

### get_robot_status()
Get comprehensive robot diagnostics

```python
get_robot_status()
```

**Returns:** `dict` - Status information
- `battery_mv`: Battery voltage
- `battery_ok`: Battery acceptable (>4800mV)
- `heading`: Current IMU heading
- `gyro_ok`: Gyro stable (<5° drift)
- `left_motor_angle`: Left motor position
- `right_motor_angle`: Right motor position

**Examples:**
```python
status = get_robot_status()
print(f"Battery: {status['battery_mv']}mV")
print(f"Heading: {status['heading']}°")
```

**Notes:**
- Useful for pre-competition checks
- Prints formatted status to console

---

### competition_ready_check()
Comprehensive pre-competition verification

```python
competition_ready_check()
```

**Returns:** `bool` - True if all checks pass

**Checks:**
1. Battery voltage (>4800mV)
2. Gyro calibration
3. Basic movement test
4. Turn test

**Examples:**
```python
if competition_ready_check():
    print("Robot ready!")
    # Run mission
else:
    print("Robot not ready - fix issues")
```

**Notes:**
- Run before each competition round
- Hub light turns GREEN if ready
- Includes small test movements

---

### safe_move_with_retry()
Execute movement function with automatic retry on failure

```python
safe_move_with_retry(move_function, *args, max_retries=2, **kwargs)
```

**Parameters:**
- `move_function`: Function to call (e.g., move_straight, turn)
- `*args`: Positional arguments for function
- `max_retries` (int): Maximum retry attempts (default: 2)
- `**kwargs`: Keyword arguments for function

**Returns:** `bool` - True if succeeded (possibly after retry)

**Examples:**
```python
safe_move_with_retry(move_straight, 500, max_retries=3)
safe_move_with_retry(spin_turn, 90, speed=200)
```

**Notes:**
- 500ms delay between retries
- Stops robot before retry
- Useful for competition reliability

---

## Configuration Constants

### Physical Robot Measurements
```python
WHEEL_DIAMETER = 56      # mm - SPIKE Prime small wheels
AXLE_TRACK = 126         # mm - distance between wheel centers
```

**Important:** Measure your specific robot and update these values!

### Default Performance Settings
```python
DEFAULT_SPEED = 300              # mm/s - straight movement
DEFAULT_TURN_SPEED = 100         # deg/s - turning
DEFAULT_ACCELERATION = 500       # mm/s² - straight acceleration
DEFAULT_TURN_ACCELERATION = 200  # deg/s² - turn acceleration
GYRO_PROPORTIONAL_GAIN = 2.0     # Gyro correction gain
```

### Port Assignments
```python
LEFT_MOTOR_PORT = Port.B
RIGHT_MOTOR_PORT = Port.F
ATTACHMENT_PORT_LEFT = Port.A      # Left arm
ATTACHMENT_PORT_RIGHT = Port.E     # Right arm
```

**Important:** Update these to match your robot's wiring!

### Validation Limits
```python
MAX_DISTANCE = 2000      # mm - maximum single movement
MAX_SPEED = 1000         # mm/s - maximum safe speed
MAX_TURN_RATE = 500      # deg/s - maximum turn rate
```

---

## Complete Examples

### Example 1: Simple Mission
```python
#!/usr/bin/env pybricks-micropython
from robot import *

if __name__ == "__main__":
    # Check battery
    check_battery()

    # Reset arms
    reset_arms()
    wait(500)

    # Drive to target
    move_straight_gyro(600, DriveSpeed.TRANSIT)
    spin_turn(45)
    move_straight(200, DriveSpeed.APPROACH)

    # Operate arm
    left_arm_down(90, ArmSpeed.GRAB)
    wait(500)
    left_arm_up(90, ArmSpeed.GRAB)

    # Return home
    spin_turn(-45)
    move_straight_gyro(-800, DriveSpeed.RETURN)
```

### Example 2: Object Collection
```python
from robot import *

def collect_objects():
    """Collect multiple objects"""
    # Approach area
    move_straight_gyro(500, DriveSpeed.APPROACH)

    # Collect first object
    left_arm_down(90, ArmSpeed.COLLECT)
    wait(300)
    left_arm_up(90, ArmSpeed.COLLECT)

    # Move to second object
    move_straight(150, DriveSpeed.COLLECTION)

    # Collect second object
    right_arm_down(90, ArmSpeed.COLLECT)
    wait(300)
    right_arm_up(90, ArmSpeed.COLLECT)

    # Return
    move_straight(-650, DriveSpeed.RETURN)

if __name__ == "__main__":
    competition_ready_check()
    collect_objects()
```

### Example 3: Precise Placement
```python
from robot import *

def precise_placement():
    """Precise object placement mission"""
    # Open arms
    both_arms_up(90, ArmSpeed.DELICATE)
    wait(500)

    # Approach carefully
    move_straight(250, DriveSpeed.APPROACH)
    move_straight(50, DriveSpeed.PRECISE)

    # Grab object gently
    both_arms_down(90, ArmSpeed.GRAB)
    wait(1000)

    # Lift
    both_arms_up(30, ArmSpeed.GRAB)
    wait(500)

    # Transport
    move_straight_gyro(400, DriveSpeed.COLLECTION)
    spin_turn(90)

    # Final precise approach
    move_straight(100, DriveSpeed.APPROACH)
    move_straight(30, DriveSpeed.PRECISE)

    # Release gently
    both_arms_down(45, ArmSpeed.DELICATE)
    wait(500)
    both_arms_up(10, ArmSpeed.DELICATE)

    # Back away
    move_straight(-130, DriveSpeed.PRECISE)

    # Reset
    reset_arms(ArmSpeed.QUICK)

if __name__ == "__main__":
    if competition_ready_check():
        precise_placement()
```

### Example 4: Using Sensors
```python
from robot import *

def sensor_navigation():
    """Navigate using sensors"""
    # Move until black line
    if move_until_line(200, Port.E, 20, 5000):
        print("Line found!")

        # Align with line
        move_straight(20, DriveSpeed.PRECISE)

        # Turn along line
        spin_turn(90)
    else:
        print("Line not found!")
        return False

    # Move until object detected
    if move_until_distance(200, Port.F, 100, 5000):
        print("Object detected!")

        # Stop 5cm away
        move_straight(-50, DriveSpeed.PRECISE)
    else:
        print("No object found!")
        return False

    return True

if __name__ == "__main__":
    sensor_navigation()
```

### Example 5: Intelligent Turning with TurnSpeed
```python
from robot import *

def multi_phase_mission():
    """Mission showing intelligent turn speed selection"""
    # Check battery
    check_battery()

    # === Phase 1: Fast Transit ===
    move_straight_gyro(600, DriveSpeed.TRANSIT)
    turn(90, TurnSpeed.APPROACH)  # Fast approach turn (±3°)
    wait(500)

    # === Phase 2: Approach Mission ===
    move_straight_gyro(400, DriveSpeed.APPROACH)
    spin_turn(45, TurnSpeed.PRECISE)  # Precise turn (±1°)
    wait(500)

    # === Phase 3: Final Alignment ===
    move_straight(150, DriveSpeed.PRECISE)
    spin_turn(30, TurnSpeed.ALIGNMENT)  # Ultra-precise (±0.5°)
    wait(500)

    # === Phase 4: Execute Mission ===
    left_arm_down(90, ArmSpeed.GRAB)
    wait(500)
    left_arm_up(90, ArmSpeed.GRAB)

    # === Phase 5: Navigate Tight Space ===
    move_straight(-100, DriveSpeed.PRECISE)
    pivot_turn(90, TurnSpeed.PIVOT)  # Tight turn (±3°)
    move_straight(200, DriveSpeed.COLLECTION)

    # === Phase 6: Quick Reposition ===
    turn(180, TurnSpeed.QUICK)  # Fast turn (±4°)
    move_straight(300, DriveSpeed.COLLECTION)

    # === Phase 7: Return Home ===
    turn(90, TurnSpeed.REPOSITION)  # Max speed! (±5°)
    move_straight_gyro(-1200, DriveSpeed.RETURN)

if __name__ == "__main__":
    multi_phase_mission()
```

### Example 6: Adaptive Arm Control with Load Sensing
```python
from robot import *

def intelligent_collection():
    """Collect objects with adaptive arm control"""
    # Check battery and calibrate
    check_battery()
    calibrate_gyro()

    # Calibrate arm to mechanical zero
    if reset_arm_to_limit('left'):
        print("Arm calibrated!")

    # Approach object
    move_straight_gyro(400, DriveSpeed.APPROACH)
    spin_turn(45, TurnSpeed.PRECISE)

    # Smart grab - automatically detects object
    result = grab_until_load(target_load=40, max_degrees=90, arm='left')
    if result['grabbed']:
        print(f"Grabbed! Load: {result['final_load']}%")
        print(f"Closed {result['degrees_moved']}°")

        # Adaptive lift - speed adjusts to weight
        lift_result = lift_adaptive(90, arm='left')
        print(f"Lifted with avg load: {lift_result['avg_load']}%")

        # Transport object
        move_straight_gyro(500, DriveSpeed.COLLECTION)
        spin_turn(90, TurnSpeed.STANDARD)

        # Release gently
        left_arm_down(90, ArmSpeed.DELICATE)
    else:
        print("Nothing to grab")

    # Return home
    turn(180, TurnSpeed.REPOSITION)
    move_straight_gyro(-900, DriveSpeed.RETURN)

if __name__ == "__main__":
    intelligent_collection()
```

### Example 7: Push with Load Sensing
```python
from robot import *

def push_mission_model():
    """Push heavy mission model into place"""
    # Approach model
    move_straight_gyro(300, DriveSpeed.APPROACH)
    spin_turn(45, TurnSpeed.PRECISE)

    # Position arms for pushing
    both_arms_down(45, ArmSpeed.GRAB)

    # Push until resistance detected
    result = push_until_resistance(
        distance_mm=250,
        speed=DriveSpeed.PUSHING,
        load_threshold=75,
        timeout_ms=5000
    )

    if result['stopped_reason'] == 'resistance':
        print(f"Model pushed into place!")
        print(f"Pushed {result['distance_traveled']}mm")
        print(f"Final load: {result['final_load']}%")
    elif result['stopped_reason'] == 'distance':
        print("Reached max distance (no resistance)")
    else:
        print("Push timeout")

    # Back away
    move_straight(-100, DriveSpeed.PRECISE)

    # Reset arms
    reset_arms()

if __name__ == "__main__":
    push_mission_model()
```

---

## Tips and Best Practices

### Speed Selection
1. **Start fast, end slow**: Use TRANSIT for long runs, APPROACH for getting closer, PRECISE for final positioning
2. **Match speed to mission**: Precision missions use slower speeds, collection missions use moderate speeds
3. **Use gyro for long runs**: Always use `move_straight_gyro()` for distances >200mm
4. **Custom speeds ok**: Don't hesitate to use numeric values if presets don't fit

### Turn Speed Selection
1. **Match turn speed to mission phase**: Fast transit → TurnSpeed.APPROACH, Precise positioning → TurnSpeed.ALIGNMENT
2. **Use spin_turn() for precision**: Always use `spin_turn()` with TurnSpeed.PRECISE or ALIGNMENT for angle-critical missions
3. **Use turn() for speed**: Use `turn()` with TurnSpeed.STANDARD or QUICK when speed matters more than precision
4. **Pivot for tight spaces**: Use `pivot_turn()` with TurnSpeed.PIVOT when space is constrained (<20cm clearance)
5. **Progressive precision**: Start with APPROACH/QUICK, then STANDARD, finally PRECISE/ALIGNMENT as you approach target

### Arm Control
1. **Reset at start**: Always call `reset_arms()` at the beginning of missions
2. **Use GRAB as default**: ArmSpeed.GRAB (360) is the safest, most reliable speed
3. **Slow for fragile**: Use DELICATE for fragile objects or precise placement
4. **Fast for resets**: Use RESET or QUICK when repositioning between missions
5. **Use load sensing for unknowns**: Use `grab_until_load()` when object size is uncertain
6. **Monitor heavy lifts**: Use `left_arm_up_monitored()` with max_load=70 for safety
7. **Adaptive lifting**: Use `lift_adaptive()` to automatically optimize speed based on weight

### Load Sensing Best Practices
1. **Calibrate arms first**: Use `reset_arm_to_limit()` for consistent starting positions
2. **Smart grabbing**: Use `grab_until_load()` instead of fixed angles when object size varies
3. **Safety thresholds**: Set `max_load=70-75` for most operations, lower (60-65) for delicate work
4. **Check load after grab**: Always verify `result['grabbed']` is True before proceeding
5. **Adaptive speed**: Use `lift_adaptive()` for unknown weights to optimize for both speed and safety
6. **Push with feedback**: Use `push_until_resistance()` instead of fixed distances when pushing models

### Competition Prep
1. **Always check battery**: Run `check_battery()` before each round
2. **Calibrate gyro**: Call `calibrate_gyro()` at start of each run
3. **Use pre_mission_check**: Run `pre_mission_check.py` before competition rounds
4. **Test with retry**: Use `safe_move_with_retry()` for critical movements
5. **Calibrate arms**: Run `reset_arm_to_limit()` before first mission if using load sensing

### Debugging
1. **Check return values**: All functions return True/False or dict for success detection
2. **Use get_robot_status()**: Quick diagnostic between runs
3. **Print statements**: Add print statements to track mission progress
4. **Test incrementally**: Test each movement individually before combining
5. **Monitor loads**: Print load values during development to tune thresholds
6. **Check turn accuracy**: Use test functions from demo_turn_speeds.py to verify turn precision

---

**Created:** 2025-10-19
**For:** FLL 2025 Season
**Version:** 1.0
