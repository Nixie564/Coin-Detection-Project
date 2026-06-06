# Coin-Detection-Project
The Coin Detection System project is a comprehensive electronics engineering endeavor that demonstrates the real-world application of image recognition integrated with a physical actuator system.

The system utilizes a computer vision approach to perform object detection operating in Python Programming utilizing the YOLOv8 and OpenCV library, specifically identifying coins with different objects present. This visual intelligence is bridged to physical hardware by a serial communication link using the PySerial library, enabling the Python script to transmit detection data to an Arduino Uno microcontroller , which acts as the intermediary between the software logic and the physical components. The core of the hardware integration is the use of the AC Light Dimmer Module as an actuator. This module regulates the power delivered to an AC-powered lamp by utilizing Pulse Width Modulation (PWM) signals sent from the Arduino. The brightness of the lamp is dynamically adjusted based on the specific number of coins detected by the YOLOv8 algorithm, where the power delivered is scaled relative to the coin count. This setup effectively displays how complex digital image processing can be translated into precise, automated physical actions

## Technologies Used

- Python
- YOLOv8 (Ultralytics)
- OpenCV
- Supervision
- Tkinter
- PySerial
- PyWin32
- Arduino
