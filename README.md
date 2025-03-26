# Hand-Gesture-Based-Virtual-Mouse-using-OpenCV-MediaPipe
## Introduction
This project implements an AI-powered Virtual Mouse that allows users to control their computer using hand gestures instead of a physical mouse. The system utilizes MediaPipe Hands for real-time hand tracking and OpenCV for video processing.

🎯 Key Features

✅ Move Cursor – Move your index finger to control the pointer.

✅ Left Click – Touch the thumb and index finger together.

✅ Right Click – Touch the thumb and ring finger together.

✅ Drag – Keep the thumb and index finger close while moving.

✅ Scrolling – Move index and middle fingers up/down.

✅ Swipe – Move the hand left/right for tab switching.

✅ Zoom In – Thumb up.

✅ Zoom Out – Thumb down.

---
 Installation & Setup
1️⃣ Clone the Repository
```
git clone https://github.com/your-username/ai-virtual-mouse.git
cd ai-virtual-mouse
```
2️⃣ Install Required Dependencies
Ensure you have Python 3.x installed, then run:
```
pip install -r requirements.txt
```
3️⃣ Run the Project
```
python src/main.py
```
4️⃣ Exit the Program
Press 'q' to quit the application.

---


🛠️ ## Technologies Used

1. Python – Programming language

2. OpenCV – Computer vision library for video processing

3. MediaPipe – Real-time hand tracking

4. NumPy – Numerical operations

5. pynput – Mouse event simulation

---





 How It Works?
 
🖐️ The system captures hand movements via a webcam and uses MediaPipe Hands to detect finger positions. Based on predefined gestures, the program translates these hand movements into mouse actions.

🖱️ Gesture Mapping
Gesture	Action

Move Index Finger	Cursor Movement

Thumb + Index Touch	     ---> Left Click

Thumb + Ring Touch	      ---> Right Click

Thumb + Index	           ---> Close	Drag

Index + Middle Up/Down	  ---> Scroll

Hand Left/Right         	---> Swipe

Thumb Up	                ---> Zoom In

Thumb Down	              ---> Zoom Out

---

📜 License
This project is licensed under the MIT License.








