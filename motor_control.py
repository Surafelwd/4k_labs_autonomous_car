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
        
        GPIO.setmode(GPIO.BCM) ##bcm pin numbering
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

    def speed(self, speed):
        # Set speed for Motor A (0 to 100%)
        self.pwmA.ChangeDutyCycle(speed)
        #Motor A
    def forward(self):
        GPIO.output(self.In1A, GPIO.HIGH)
        GPIO.output(self.In2A, GPIO.LOW)
       ## Motor A
    def backward(self):
        GPIO.output(self.In1A, GPIO.LOW)
        GPIO.output(self.In2A, GPIO.HIGH)
        ##Motor B
    def left(self):
        GPIO.output(self.In1B, GPIO.HIGH)
        GPIO.output(self.In2B, GPIO.LOW)
        ##Motor B
    def right(self):
        GPIO.output(self.In1B, GPIO.LOW)
        GPIO.output(self.In2B, GPIO.HIGH)
        ##Motor A &b   
    def stop(self):
        # Stop both motors
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        GPIO.output(self.In1A, GPIO.LOW)
        GPIO.output(self.In2A, GPIO.LOW)
        GPIO.output(self.In1B, GPIO.LOW)
        GPIO.output(self.In2B, GPIO.LOW)
    def gradual_stop(self ,delay = 0.1):
        for  c in  range(100,-1,-10):
            self.pwmA.ChangeDutyCycle(c)
            time.sleep(delay)
        self.pwmA.ChangeDutyCycle(0)
        GPIO.output(self.In1A,GPIO.LOW)
        GPIO.output(self.In2A,GPIO.LOW)
class Sensor:
    def __init__(self, trig, echo, car, stop_distance=30):
        self.trig = trig
        self.echo = echo
        self.car = car
        self.stop_distance = stop_distance
        ## pin setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def measure_distance(self):
        GPIO.output(self.trig, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(self.trig, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trig, GPIO.LOW)
        ## waiting echo signal to start
        while GPIO.input(self.echo) == GPIO.LOW:
            start = time.time()
        ## waiting echo signal to end
        while GPIO.input(self.echo) == GPIO.HIGH:
            end = time.time()
        ## converting time(second) to distance(centiMeter)
        duration = end - start
        distance = duration * 17150
        distance = round(distance, 2)
        
        return distance
    ##condition to stop the car
    def avoidance(self):
        while True:
            distance = self.measure_distance()
            if distance <= self.stop_distance:
                
                self.car.gradual_stop()
                print(f"Obstacle detected at {distance} cm. Stopping gradually.")
            else:
                self.car.move_forward()
                self.car.set_speed(50)  # Example speed
                print(f"Moving forward. Distance: {distance} cm.")
            
            time.sleep(0.5)