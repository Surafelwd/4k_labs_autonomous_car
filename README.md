# Autonomous Car with Ultrasonic Sensor and Lane Detection

This project implements an autonomous vehicle using a Raspberry Pi, equipped with an ultrasonic sensor for obstacle avoidance and a camera for lane detection using OpenCV.

## Project Structure

### Files
- ultrasonic.py: Contains the Sensor class that manages the ultrasonic sensor for distance measurement and obstacle avoidance.
- motor_control.py: Contains the Car class that manages motor control, including speed and directional commands.

## Features

1. Ultrasonic Sensor for Obstacle Detection:
   - Continuously measures the distance to the nearest object.
   - Stops the car if an obstacle is detected within a defined range.

2. Lane Detection with OpenCV:
   - Processes video input to detect lane markings.
   - Guides the car to maintain its path based on lane detection results.

## Installation

### Prerequisites
- Raspberry Pi with GPIO support
- Python 3.x
- OpenCV library
- RPi.GPIO library

### Installation Steps
1. Clone the repository:
   `bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
