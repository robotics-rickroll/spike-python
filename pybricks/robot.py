#!/usr/bin/env pybricks-micropython
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# Robot Constants
WHEEL_DIAMETER = 56  # diameter in mm (SPIKE Prime small wheels)
AXLE_TRACK = 126    # distance between wheels in mm
WHEEL_CIRCUMFERENCE = 3.14159 * WHEEL_DIAMETER  # circumference in mm

# Movement Constants
DEFAULT_SPEED = 200         # Default straight movement speed (mm/s)
DEFAULT_TURN_SPEED = 100    # Default turning speed (deg/s)
GYRO_PROPORTIONAL_GAIN = 2.0  # Gain for gyro-based movement correction

# Initialize the hub
hub = PrimeHub()

# Initialize the motors
# If robot spins instead of going straight, swap CLOCKWISE/COUNTERCLOCKWISE
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.F, Direction.CLOCKWISE)

# Set the yaw angle to 0 at the start
hub.imu.reset_heading(0)

# Initialize the drive base
robot = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)

def move_straight(distance_mm, speed=DEFAULT_SPEED):
    """
    Move the robot straight for a given distance in millimeters.
    Positive distance moves forward, negative distance moves backward.
    Speed is in mm/s (default: DEFAULT_SPEED)
    """
    robot.straight(distance_mm)

def turn(angle_degrees, speed=DEFAULT_TURN_SPEED):
    """
    Turn the robot by a specified angle in degrees.
    Positive angle turns right, negative angle turns left.
    Speed is in degrees/s (default: DEFAULT_TURN_SPEED)
    """
    robot.turn(angle_degrees)

def pivot_turn(angle_degrees, speed=DEFAULT_TURN_SPEED):
    """
    Make a pivot turn around one wheel.
    Positive angle turns right (around right wheel), 
    negative angle turns left (around left wheel).
    Speed is in degrees/s (default: DEFAULT_TURN_SPEED)
    """
    if angle_degrees > 0:  # Turn right
        left_motor.run_angle(speed, angle_degrees)
    else:  # Turn left
        right_motor.run_angle(speed, -angle_degrees)

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

def move_straight_gyro(distance_mm, speed=DEFAULT_SPEED):
    """
    Move straight using gyro sensor to maintain direction, even with obstacles.
    Uses proportional control for straight line motion.

    Args:
        distance_mm (int): Distance to move in millimeters (positive=forward, negative=backward)
        speed (int): Speed in mm/s (default: DEFAULT_SPEED)
    """
    # Reset the heading before starting
    hub.imu.reset_heading(0)

    # Use the global proportional constant
    KP = GYRO_PROPORTIONAL_GAIN

    # Save initial motor positions
    left_start = left_motor.angle()
    right_start = right_motor.angle()

    # Calculate target angle in degrees using wheel circumference
    target_degrees = (distance_mm / WHEEL_CIRCUMFERENCE) * 360

    # Keep moving until we reach the target distance
    while True:
        # Calculate average motor position
        left_pos = abs(left_motor.angle() - left_start)
        right_pos = abs(right_motor.angle() - right_start)
        avg_pos = (left_pos + right_pos) / 2

        # Check if we've reached the target distance
        if avg_pos >= abs(target_degrees):
            robot.stop()
            break

        # Get current heading error
        heading_error = hub.imu.heading()

        # Calculate turn rate correction using proportional control
        # Negative sign to counteract drift: if robot drifts right (+heading), turn left (-)
        turn_rate = -heading_error * KP

        # Apply the correction while maintaining forward/backward motion
        robot.drive(speed if distance_mm > 0 else -speed, turn_rate)

        # Small delay to prevent overwhelming the system
        wait(10)

def spin_turn(target_angle, speed=DEFAULT_TURN_SPEED):
    """
    Make a precise spin turn using the hub's IMU sensor with proportional control.
    Uses the difference between current and target angles to adjust motor speeds.
    
    Args:
        target_angle: The target angle to turn to (not relative, but absolute)
        speed: Base speed for the turn (default: DEFAULT_TURN_SPEED)
    """
    # Reset the heading before starting the turn
    current_angle = hub.imu.heading()
    
    # Proportional control constants
    BASE_SPEED = 60  # Base motor speed
    KP = 9          # Proportional gain factor
    
    if target_angle >= current_angle:
        # Turning right (positive)
        while current_angle <= target_angle:
            current_angle = hub.imu.heading()
            # Calculate speeds using proportional control
            error = target_angle - current_angle
            adjustment = error * KP
            
            # Apply speeds to motors
            left_motor.run(BASE_SPEED + adjustment)
            right_motor.run(-BASE_SPEED - adjustment)
            wait(10)
    else:
        # Turning left (negative)
        while current_angle >= target_angle:
            current_angle = hub.imu.heading()
            # Calculate speeds using proportional control
            error = target_angle - current_angle
            adjustment = error * KP
            
            # Apply speeds to motors
            left_motor.run(BASE_SPEED + adjustment)
            right_motor.run(-BASE_SPEED - adjustment)
            wait(10)
    
    # Stop both motors with hold
    left_motor.hold()
    right_motor.hold()# Example usage
def test_movements():
    # Move forward 200mm
    move_straight(200)
    wait(1000)  # Wait 1 second
    
    # Turn right 90 degrees
    turn(90)
    wait(1000)
    
    # Move backward 100mm
    move_straight(-100)
    wait(1000)
    
    # Turn left 90 degrees
    turn(-90)
    wait(1000)
    
    # Make a pivot turn right 45 degrees
    pivot_turn(45)
    wait(1000)
    
    # Tank move: forward arc (faster on right side)
    tank_move(50, 80, 2000)

if __name__ == "__main__":
    # Run the test movements
    #test_movements()
    #move_straight(200)
    spin_turn(90, speed=150)  # Example spin turn
    #move_straight_gyro(1200,speed=400)
