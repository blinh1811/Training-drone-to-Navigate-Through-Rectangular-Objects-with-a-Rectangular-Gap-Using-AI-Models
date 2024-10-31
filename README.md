# Drone Training to Navigate Circular Obstacles Using AI

## Overview
This project involves training an unmanned aerial vehicle (UAV), specifically the DJI Tello drone, to autonomously navigate through circular obstacles with a central opening. By integrating a Convolutional Neural Network (CNN) model, the drone is able to recognize obstacles and determine the correct path through them, reducing collision risks and enhancing autonomous capabilities. The project showcases the application of machine learning and computer vision in real-time UAV navigation.

## Project Objectives
- **Develop an autonomous navigation model** for drones to detect and pass through circular obstacles with high accuracy.
- **Implement CNN for image classification**, enabling the drone to recognize obstacle shapes and decide the appropriate direction.
- **Optimize real-time obstacle detection** and path planning for safe navigation in indoor environments.

## Features
- **Obstacle Detection**: Identifies circular obstacles with a hole in the center using computer vision.
- **Path Planning**: Determines the best path for the drone to navigate through obstacles.
- **6-Direction Movement**: Trained model enables the drone to move in six directions (up, down, left, right, forward, backward) based on obstacle positions.
- **Real-Time Decision Making**: Allows the drone to make autonomous navigation decisions based on CNN model predictions.

![image](https://github.com/user-attachments/assets/5ebc473c-2bdd-4660-89c8-b0aa6b02aadf)

## Project Structure
### 1. Data Collection
   - Created a custom dataset of circular obstacles with RGB colors (red, green, blue) for model training.
   - Each image contains variations in size and position to enhance model accuracy.

![image](https://github.com/user-attachments/assets/0a190323-ef92-4632-a188-8b9eefc9123b)

### 2. Model Development
   - **CNN Architecture**: Developed using TensorFlow/Keras for image recognition.
   - **Training & Evaluation**: Trained the model on labeled obstacle data with up to 99% accuracy for training and 98% for testing.

![image](https://github.com/user-attachments/assets/0f66bf9e-c94a-4ef8-bf50-ec3de84256d3)

### 3. Drone Control and Integration
   - **Programming**: Used Python and the DJI Tello SDK to control drone movements.
   - **Integration**: Combined CNN output with drone commands for autonomous obstacle navigation.

## Requirements
- **Hardware**: DJI Tello Drone
- **Software**: 
  - Python 3.x
  - TensorFlow/Keras for model training
  - OpenCV for image processing
  - `djitellopy` library for DJI Tello control
