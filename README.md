# Smart Home IoT System

Smart home IoT system using Arduino hardware, Python integration, sensor automation, and ThingSpeak cloud monitoring.

---

## Features

- Smart lighting system
- Temperature monitoring
- Motion detection simulation
- Garage door automation
- Ventilation control
- Emergency mode
- Sensor automation
- ThingSpeak cloud integration
- Email command control system
- Real Arduino hardware communication

---

## Hardware Components

- Arduino board
- LM35 temperature sensor
- Ultrasonic sensor
- Servo motor
- LEDs
- Breadboard
- Jumper wires

---

## Technologies Used

- Arduino C/C++
- Python
- ThingSpeak
- Embedded Systems
- IoT Automation

---

## Project Structure

```bash
arduinoKitCode.ino
smart_home_email_control.py
screenshots/
README.md
```

---

## Functionality

The system automatically controls lighting, ventilation, garage access, and emergency states using sensor data and automation logic.

Sensor data is uploaded to ThingSpeak cloud services for monitoring and analytics.

The Python integration enables:
- email command processing
- automation control
- daily reports
- cloud communication
- alarm notifications

---

## Motion Detection Simulation

The Arduino kit used for this project did not include a dedicated PIR motion sensor.

To simulate motion detection functionality, a custom software-based solution was implemented using the keyword:

```text
MOTION
```

When motion is triggered through the simulation logic, the system activates a dedicated LED indicator representing detected movement inside the smart home environment.

This approach allowed the project to demonstrate motion detection workflows, alarm logic, and automation behavior even without a physical PIR module.

---

## Hardware Setup

The project was implemented using real Arduino hardware components connected through a breadboard setup.

### Components Used
- Arduino board
- Ultrasonic sensor
- Servo motor
- LEDs
- Temperature sensor
- Breadboard and jumper wires

---

## Screenshots

### Hardware Prototype

![Hardware Setup](screenshots/hardware_setup.jpeg)

---

## Learning Outcomes

Through this project, I improved my understanding of:

- IoT systems
- Embedded programming
- Sensor communication
- Hardware-software integration
- Arduino development
- Automation systems
- Real-time monitoring
- Cloud-based IoT platforms
- Python-Arduino communication

---

## Author

Sara Zivkovic
