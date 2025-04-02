#battle bear Prototype 1
import RPi.GPIO as GPIO
import time

# Pin Definitions
in1 = 24
in2 = 23
enA = 25
in3 = 22
in4 = 27
enB = 17
# Pin for line tracking sensor
RIGHT_SENSOR, MIDDLE_SENSOR, LEFT_SENSOR = 20, 18, 16

# Pin for Left Ultra Sound sensor
LEFT_TRI = 14 
LEFT_ECHO = 15
# Pin for Right Ultra Sound sensor
RIGHT_TRI = 5
RIGHT_ECHO = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup line tracking sensor pins
GPIO.setup(RIGHT_SENSOR, GPIO.IN)
GPIO.setup(MIDDLE_SENSOR, GPIO.IN)
GPIO.setup(LEFT_SENSOR, GPIO.IN)

# Setup LEFT ultrasonic sensor pins
GPIO.setup(LEFT_TRI, GPIO.OUT)
GPIO.setup(LEFT_ECHO, GPIO.IN)
GPIO.output(LEFT_TRI, False)
# Setup RIGHT ultrasonic sensor pins
GPIO.setup(RIGHT_TRI, GPIO.OUT)
GPIO.setup(RIGHT_ECHO, GPIO.IN)
GPIO.output(RIGHT_TRI, False)

# Setup motor control pins as OUTPUT
for pin in [in1, in2, in3, in4, enA, enB]:
    GPIO.setup(pin, GPIO.OUT)

# Initialize all motor pins to LOW
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

# Setup PWM for motor control
pA = GPIO.PWM(enA, 1000)  # Enable A (Left Motors)
pB = GPIO.PWM(enB, 1000)  # Enable B (Right Motors)
pA.start(0)
pB.start(0)

previousMove = None
move_num = 1

# The moves of BattleBear
def forward():
    print("Forward")
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    
def stop():
    print("Stop")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    
def backward():
    print("Backward")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW) 
    GPIO.output(in4, GPIO.HIGH)
    
def right():
    print("Turn Right")
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

def left():
    print("Turn Left")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

def rightBackward():
    print("Turn Right / right backward")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    
def leftBackward():
    print("Turn Left / left backward")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    
def leftForward():
    print("Turn left / right forward")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

def rightForward():
    print("Turn Right / left forward")
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    
def decodeCommand(keyword):
    global previousMove
    if keyword == 'f':
        pA.ChangeDutyCycle(30)
        pB.ChangeDutyCycle(30)
        forward()
    elif keyword == "hf":
        pA.ChangeDutyCycle(80)
        pB.ChangeDutyCycle(80)
        forward()
    elif keyword == "mf":
        pA.ChangeDutyCycle(100)
        pB.ChangeDutyCycle(100)
        forward()
    elif keyword == 's':
        stop()
    elif keyword == 'b':
        pA.ChangeDutyCycle(80)
        pB.ChangeDutyCycle(80)
        backward()
    elif keyword == 'r':
        pA.ChangeDutyCycle(50)
        pB.ChangeDutyCycle(50)
        right()
    elif keyword == 'l':
        pA.ChangeDutyCycle(50)
        pB.ChangeDutyCycle(50)
        left()
    elif keyword == "rb":
        pA.ChangeDutyCycle(75)
        pB.ChangeDutyCycle(75)
        rightBackward()
    elif keyword == "lb":
        pA.ChangeDutyCycle(75)
        pB.ChangeDutyCycle(75)
        leftBackward()
    elif keyword == "rf":
        pA.ChangeDutyCycle(75)
        pB.ChangeDutyCycle(75)
        rightForward()
    elif keyword == "lf":
        pA.ChangeDutyCycle(75)
        pB.ChangeDutyCycle(75)
        leftForward()
    elif keyword == "hrf":
        pA.ChangeDutyCycle(100)
        pB.ChangeDutyCycle(100)
        rightForward()
    elif keyword == "hlf":
        pA.ChangeDutyCycle(100)
        pB.ChangeDutyCycle(100)
        leftForward()
    previousMove = keyword

# Return the left, center, right sensor values (line tracking)
def lineTracking():
    return [GPIO.input(LEFT_SENSOR), GPIO.input(MIDDLE_SENSOR), GPIO.input(RIGHT_SENSOR)]

# Calculate distance for LEFT HC-SR04 sensor in centimeters
def measure_left_distance():
    GPIO.output(LEFT_TRI, True)
    time.sleep(0.00001)
    GPIO.output(LEFT_TRI, False)
    pulse_start = time.time()
    timeout = pulse_start + 0.04
    while GPIO.input(LEFT_ECHO) == 0 and time.time() < timeout:
        pulse_start = time.time()
    pulse_end = time.time()
    timeout = pulse_end + 0.04
    while GPIO.input(LEFT_ECHO) == 1 and time.time() < timeout:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

# Calculate distance for RIGHT HC-SR04 sensor in centimeters
def measure_right_distance():
    GPIO.output(RIGHT_TRI, True)
    time.sleep(0.00001)
    GPIO.output(RIGHT_TRI, False)
    pulse_start = time.time()
    timeout = pulse_start + 0.04
    while GPIO.input(RIGHT_ECHO) == 0 and time.time() < timeout:
        pulse_start = time.time()
    pulse_end = time.time()
    timeout = pulse_end + 0.04
    while GPIO.input(RIGHT_ECHO) == 1 and time.time() < timeout:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

# Sequentially get ultrasonic distances to reduce interference.
def get_ultrasonic_distances():
    left_distance = measure_left_distance()
    time.sleep(0.05)
    right_distance = measure_right_distance()
    return left_distance, right_distance

# Helper: Turn for a given duration while checking enemy distance.
# If enemy detected (distance <= threshold), return True immediately.
def turn_with_enemy_check(turn_command, duration, enemy_threshold=30):
    start_time = time.time()
    decodeCommand(turn_command)
    while (time.time() - start_time) < duration:
        left_dist, right_dist = get_ultrasonic_distances()
        if left_dist <= enemy_threshold or right_dist <= enemy_threshold:
            print("Enemy detected during turn!")
            return True
        time.sleep(0.05)
    return False

def battleMode():
    global move_num
    
    sensorValues = lineTracking()
    # initial move on first iteration
    if move_num == 1:
        decodeCommand('r')
        pA.ChangeDutyCycle(100)
        pB.ChangeDutyCycle(100)
        time.sleep(0.65)
        pA.ChangeDutyCycle(0)
        pB.ChangeDutyCycle(0)
        time.sleep(0.2)

    # Edge detection takes highest priority.
    if sensorValues != [1, 1, 1]:
        # detect white on left => steer right
        if GPIO.input(LEFT_SENSOR) == 0 and GPIO.input(RIGHT_SENSOR) == 1:
            print("running case [0,1,1] or [0,0,1]")
            decodeCommand('b')
            time.sleep(0.65)
            # While turning right, check enemy distance.
            if turn_with_enemy_check('rb', 0.35):
                decodeCommand('f')
        # detect white on right => steer left
        elif GPIO.input(RIGHT_SENSOR) == 0 and GPIO.input(LEFT_SENSOR) == 1:
            print("running case [1,1,0] or [1,0,0]")
            decodeCommand('b')
            time.sleep(0.65)
            if turn_with_enemy_check('lb', 0.35):
                decodeCommand('f')
        # case: white detected on all sensors
        elif sensorValues == [0, 0, 0]:
            print("running case [0,0,0]")
            decodeCommand('b')
            time.sleep(0.7)
            decodeCommand('r')
            time.sleep(1)
        # for weird or ambiguous cases:
        else:
            print("running weird case")
            decodeCommand('s')
            time.sleep(0.2)
            # Double-check sensors
            if GPIO.input(LEFT_SENSOR) == 0 and GPIO.input(RIGHT_SENSOR) == 1:
                decodeCommand('b')
                time.sleep(0.5)
                if turn_with_enemy_check('rb', 0.35):
                    decodeCommand('f')
            elif GPIO.input(RIGHT_SENSOR) == 0 and GPIO.input(LEFT_SENSOR) == 1:
                decodeCommand('b')
                time.sleep(0.5)
                if turn_with_enemy_check('lb', 0.35):
                    decodeCommand('f')
            else:
                decodeCommand('rf')
                time.sleep(0.30)
                decodeCommand('lf')
                time.sleep(0.60)
    # Normal enemy tracking when no white line avoidance is required.
    else:
        decodeCommand('f')
        
    # Get ultrasonic distances for enemy detection.
    left_distance, right_distance = get_ultrasonic_distances()
    print(f"move_num = {move_num} sensorsValue = {lineTracking()}")
    print(f"LEFT DISTANCE = {left_distance} cm / RIGHT DISTANCE = {right_distance} cm")
    
    leftActive = left_distance <= 30
    rightActive = right_distance <= 30
    
    leftCloseActive = left_distance <= 5
    rightCloseActive = right_distance <= 5
    
    if leftActive and rightActive:
        print("\033[31m ENEMY AT FRONT!\033[0m")
        if sensorValues != [1, 1, 1]:
            decodeCommand('s')
        elif leftCloseActive and rightCloseActive:
            decodeCommand('mf')
        else:
            decodeCommand('hf')
    elif leftActive and not rightActive:
        print("\033[31m ENEMY AT LEFT!\033[0m")
        decodeCommand('hlf')
        time.sleep(0.1)
    elif rightActive and not leftActive:
        print("\033[31m ENEMY AT RIGHT!\033[0m")
        decodeCommand('hrf')
        time.sleep(0.1)
    else:
        print("\033[31m NOT FOUND ENEMY\033[0m")
        decodeCommand('f')
        
    move_num += 1
            
try:
    while True:
        battleMode()
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\n Measurement stopped by User")
finally:
    stop()
    GPIO.cleanup()
