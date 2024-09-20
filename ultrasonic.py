import time
import RPi.GPIO as GPIO
from motor_control import Car  # Import Car class from motor_control.py

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
