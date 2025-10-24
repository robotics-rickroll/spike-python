# 🤖 FLL ROBOT - QUICK REFERENCE CARD
**Print this and keep it next to your computer!**

---

## 📦 IMPORTS

```python
from robot import *
```

---

## 🚗 MOVEMENT

### Basic Movement
```python
move_straight(300, DriveSpeed.APPROACH)      # Forward 300mm
move_straight(-200, DriveSpeed.PRECISE)      # Backward 200mm
```

### With Gyro (More Accurate!)
```python
move_straight_gyro(500, DriveSpeed.TRANSIT)  # Gyro-corrected forward
move_straight_gyro(-300, DriveSpeed.RETURN)  # Gyro-corrected backward
```

### Turning
```python
turn(90)                              # Simple turn right
turn(-45, TurnSpeed.QUICK)            # Fast turn left
spin_turn(90)                         # Precise turn right (with gyro!)
spin_turn(-45, TurnSpeed.ALIGNMENT)   # Ultra-precise turn (with gyro!)
pivot_turn(90, TurnSpeed.PIVOT)       # Tight turn (less space)
```

---

## 💪 ARMS

### Left Arm (Port A)
```python
left_arm_up(90)           # Raise left arm
left_arm_down(90)         # Lower left arm
left_arm_to(0)            # Move to position
```

### Right Arm (Port E)
```python
right_arm_up(90)          # Raise right arm
right_arm_down(90)        # Lower right arm
right_arm_to(0)           # Move to position
```

### Both Arms
```python
both_arms_up(90)          # Raise both
both_arms_down(90)        # Lower both
reset_arms()              # Reset to home (0°)
```

---

## ⚡ DRIVESPEED - For Movement

```python
DriveSpeed.PRECISE      # 100  - Very slow, very accurate
DriveSpeed.APPROACH     # 300  - Medium speed (MOST COMMON)
DriveSpeed.COLLECTION   # 500  - Faster
DriveSpeed.TRANSIT      # 700  - Long runs
DriveSpeed.RETURN       # 900  - Going home (maximum speed)
DriveSpeed.PUSHING      # 600  - Heavy objects
```

**When to use:**
- **PRECISE** → Final positioning, close to models
- **APPROACH** → Most missions (good balance!)
- **COLLECTION** → Collecting objects
- **TRANSIT** → Long straight runs
- **RETURN** → Going back to base
- **PUSHING** → Heavy objects, ramps

---

## ⚡ TURNSPEED - For Turning

```python
TurnSpeed.ALIGNMENT     # 40  - Ultra-precise (±0.5°)
TurnSpeed.PRECISE       # 60  - High precision (±1°)
TurnSpeed.STANDARD      # 100 - Balanced (COMMON!)
TurnSpeed.APPROACH      # 120 - Fast approach
TurnSpeed.QUICK         # 150 - Quick reposition
TurnSpeed.REPOSITION    # 200 - Maximum speed
TurnSpeed.PIVOT         # 80  - Pivot turns
```

**When to use:**
- **ALIGNMENT** → Final docking, critical angle
- **PRECISE** → Most spin_turn() (best balance!)
- **STANDARD** → Most turn() (default)
- **QUICK/REPOSITION** → Fast turns, going home
- **PIVOT** → Tight spaces

---

## ⚡ ARMSPEED - For Arms

```python
ArmSpeed.DELICATE   # 200  - Very slow, fragile objects
ArmSpeed.GRAB       # 360  - Standard (SAFE DEFAULT!)
ArmSpeed.COLLECT    # 500  - Collection missions
ArmSpeed.MODERATE   # 640  - Faster collections
ArmSpeed.RESET      # 720  - Repositioning
ArmSpeed.QUICK      # 1000 - Maximum speed
ArmSpeed.PUSH       # 400  - Pushing objects
```

**When to use:**
- **DELICATE** → Fragile objects, precise placement
- **GRAB** → Most missions (safest!)
- **COLLECT** → Fast collections
- **RESET** → Repositioning arms
- **QUICK** → Emergency, fast release

---

## 🎯 QUICK PATTERNS

### Grab and Lift
```python
both_arms_down(90, ArmSpeed.GRAB)    # Grab
wait(500)
both_arms_up(30, ArmSpeed.GRAB)      # Lift
```

### Drive to Target
```python
move_straight_gyro(600, DriveSpeed.TRANSIT)    # Fast
spin_turn(45)
move_straight(200, DriveSpeed.APPROACH)        # Slow down
move_straight(50, DriveSpeed.PRECISE)          # Final position
```

### Complete Sequence
```python
reset_arms()                                    # Reset
wait(500)
move_straight_gyro(500, DriveSpeed.APPROACH)   # Drive
left_arm_down(90, ArmSpeed.GRAB)               # Grab
wait(500)
left_arm_up(90, ArmSpeed.GRAB)                 # Lift
move_straight(-500, DriveSpeed.RETURN)         # Return
```

---

## 🔧 UTILITIES

### Check Battery
```python
voltage, ok = check_battery()
if not ok:
    print("Battery low!")
```

### Calibrate Gyro
```python
calibrate_gyro()          # Do this at start of each run!
```

### Pre-Competition Check
```python
competition_ready_check()  # Run before EVERY round!
```

### Wait
```python
wait(1000)                # Wait 1 second (1000 milliseconds)
wait(500)                 # Wait 0.5 seconds
```

---

## 📋 MISSION TEMPLATE

```python
#!/usr/bin/env pybricks-micropython
from robot import *

if __name__ == "__main__":
    # 1. Check robot ready
    check_battery()

    # 2. Reset arms
    reset_arms()
    wait(500)

    # 3. Your mission here
    move_straight_gyro(500, DriveSpeed.APPROACH)
    spin_turn(45)
    left_arm_down(90, ArmSpeed.GRAB)
    wait(500)
    left_arm_up(90, ArmSpeed.GRAB)

    # 4. Return home
    spin_turn(-45)
    move_straight_gyro(-500, DriveSpeed.RETURN)

    # 5. Reset
    reset_arms()
```

---

## 🚨 COMMON MISTAKES

### ❌ WRONG
```python
left_arm_up(90, 360)              # Hard to remember what 360 means
move_straight(300, 700)           # Hard to remember what 700 means
```

### ✅ CORRECT
```python
left_arm_up(90, ArmSpeed.GRAB)              # Clear!
move_straight(300, DriveSpeed.TRANSIT)      # Clear!
```

---

## 💡 PRO TIPS

1. **Always reset arms first**: `reset_arms()` at start of mission
2. **Use gyro for long runs**: `move_straight_gyro()` > 200mm
3. **Check battery every round**: `check_battery()`
4. **Start fast, end slow**: TRANSIT → APPROACH → PRECISE
5. **Use spin_turn() for precision**: More accurate than turn()
6. **Match turn speed to phase**: Fast transit → APPROACH/QUICK, Final → ALIGNMENT
7. **When in doubt**: Use `ArmSpeed.GRAB`, `DriveSpeed.APPROACH`, `TurnSpeed.PRECISE`

---

## 🎮 SPEED SELECTION GUIDE

### For Movement:
```
Super Accurate? → DriveSpeed.PRECISE
Most Missions?  → DriveSpeed.APPROACH ⭐
Long Runs?      → DriveSpeed.TRANSIT
Going Home?     → DriveSpeed.RETURN
```

### For Turns:
```
Final Docking?  → TurnSpeed.ALIGNMENT (spin_turn)
Most Missions?  → TurnSpeed.PRECISE (spin_turn) ⭐
General Turn?   → TurnSpeed.STANDARD (turn)
Fast Transit?   → TurnSpeed.QUICK (turn)
Tight Space?    → TurnSpeed.PIVOT (pivot_turn)
```

### For Arms:
```
Fragile Object? → ArmSpeed.DELICATE
Most Missions?  → ArmSpeed.GRAB ⭐
Fast Collection?→ ArmSpeed.COLLECT
Repositioning?  → ArmSpeed.RESET
```

---

## 🔍 PORTS

```
Left Motor:  Port.B
Right Motor: Port.F
Left Arm:    Port.A
Right Arm:   Port.E
```

---

## 📞 HELP

**Can't remember a speed?**
```python
# Just use a number!
move_straight(300, 400)      # Custom 400 mm/s
left_arm_up(90, 500)         # Custom 500 deg/s
```

**Want to see all speeds?**
```python
list_speed_presets()         # Prints all available speeds
```

**Robot status?**
```python
get_robot_status()           # Shows battery, gyro, motors
```

---

## ⚡ SUPER QUICK REFERENCE

```python
# MOVEMENT
move_straight_gyro(500, DriveSpeed.APPROACH)
spin_turn(90, TurnSpeed.PRECISE)
turn(90, TurnSpeed.STANDARD)
pivot_turn(90, TurnSpeed.PIVOT)

# ARMS
left_arm_down(90, ArmSpeed.GRAB)
right_arm_up(90, ArmSpeed.GRAB)
both_arms_up(90, ArmSpeed.GRAB)
reset_arms()

# LOAD SENSING
grab_until_load(target_load=40, arm='left')
lift_adaptive(90, arm='left')
push_until_resistance(200, DriveSpeed.PUSHING)

# UTILITIES
check_battery()
calibrate_gyro()
wait(1000)
```

---

## 🏆 COMPETITION DAY CHECKLIST

Before each round:
- [ ] Charge battery (>4.4V)
- [ ] Run `competition_ready_check()`
- [ ] Wait for GREEN light
- [ ] Upload mission code
- [ ] Place robot on mat
- [ ] Press button to start!

---

**Print Me! Keep Me Handy! Code Awesome Robots! 🤖**

**Version:** 1.0 | **Created:** 2025-10-19 | **For:** FLL 2025
