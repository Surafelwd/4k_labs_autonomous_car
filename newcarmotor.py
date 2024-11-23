import time
import RPi.GPIO as GPIO

class Car:
    def __init__(self, EnaA, In1A, In2A, EnaB, In1B, In2B):
        # Motor A (Speed and Forward/Backward)
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        
        # Motor B (Left/Right)
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B
        
        GPIO.setmode(GPIO.BCM)  # BCM pin numbering
        GPIO.setup(self.EnaA, GPIO.OUT)
        GPIO.setup(self.In1A, GPIO.OUT)
        GPIO.setup(self.In2A, GPIO.OUT)
        
        GPIO.setup(self.EnaB, GPIO.OUT)
        GPIO.setup(self.In1B, GPIO.OUT)
        GPIO.setup(self.In2B, GPIO.OUT)
        
        # Initialize PWM for Motor A
        self.pwmA = GPIO.PWM(self.EnaA, 100)  # 100 Hz frequency
        self.pwmA.start(0)  # Start with 0% duty cycle
        
        # Initialize PWM for Motor B
        self.pwmB = GPIO.PWM(self.EnaB, 100)  # 100 Hz frequency
        self.pwmB.start(0)  # Start with 0% duty cycle
    
    def set_speed(self, speed):
        # Clamp speed between 0 and 100
        speed = max(0, min(100, speed))
        self.pwmA.ChangeDutyCycle(speed)
    
    def forward(self, speed):
        self.set_speed(speed)
        GPIO.output(self.In1A, GPIO.HIGH)
        GPIO.output(self.In2A, GPIO.LOW)
    
    def backward(self, speed):
        self.set_speed(speed)
        GPIO.output(self.In1A, GPIO.LOW)
        GPIO.output(self.In2A, GPIO.HIGH)
    
    def left(self, speed):
        self.set_speed(speed)
        GPIO.output(self.In1B, GPIO.HIGH)
        GPIO.output(self.In2B, GPIO.LOW)
        self.pwmB.ChangeDutyCycle(speed)
    
    def right(self, speed):
        self.set_speed(speed)
        GPIO.output(self.In1B, GPIO.LOW)
        GPIO.output(self.In2B, GPIO.HIGH)
        self.pwmB.ChangeDutyCycle(speed)
    
    def center(self):
        GPIO.output(self.In1B, GPIO.LOW)
        GPIO.output(self.In2B, GPIO.LOW)
        self.pwmB.ChangeDutyCycle(0)
    
    def stop(self):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        GPIO.output(self.In1A, GPIO.LOW)
        GPIO.output(self.In2A, GPIO.LOW)
        GPIO.output(self.In1B, GPIO.LOW)
        GPIO.output(self.In2B, GPIO.LOW)
    
    def gradual_stop(self, delay=0.1):
        for c in range(100, -1, -10):
            self.pwmA.ChangeDutyCycle(c)
            time.sleep(delay)
        self.stop()  # Ensure motors are fully stopped

    def cleanup(self):
        self.stop()
        GPIO.cleanup()
    

# Ultrasonic sensor pins
TRIG = 18
ECHO = 27

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Function to measure distance
def measure_distance():
    # Trigger the ultrasonic pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Measure the time the pulse takes to return
    start_time = time.time()
    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    end_time = time.time()
    while GPIO.input(ECHO) == 1:
        end_time = time.time()

    # Calculate distance based on the time difference
    elapsed_time = end_time - start_time
    distance = (elapsed_time * 34300) / 2  # Speed of sound in cm/s

    return distance

try:
    car = Car(12, 16, 20, 21, 19, 26)
    # Example usage:
    car.forward(50)
    time.sleep(2)
    car.stop()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    car.cleanup()
