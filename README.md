This project uses computer vision to trace the path of the finger or user’s particular action. The user can draw using different coloured objects which are detected using the camera input.


The dependencies and libraries required to run this project are specified in the requirements.txt file. They can be installed by running the following command in the project directory:
	pip install -r requirements.txt


After this step, the code can be executed using:
	python AirCanvas.py


Before running the code, ensure that camera access is enabled. When the code starts executing, the 4 windows with the following titles wil be opened up:
	1. Tracking
	2. Color detectors
	3. Paint
	4. mask


The functions of each of these windows are explained below:

- Tracking: This is the window where the user can see themselves in the camera input and they can also see what is being drawn by them. 

- Color detectors: This is where the user can adjust the colour of the object being detected as a marker. Objects of a variety of colours can be detected by altering the values of Upper Hue, Upper Saturation, Upper Value, Lower Hue, Lower Saturation and Lower Value.

- Paint: This is the area where the user can see what they drew on a plain white background.

- mask: This window shows the where the colour of the object is being detected. When a object is detected, it marks the object as white on a black background and the user can view how detection takes place in realtime.


To exit from the application, the user can do so by pressing 'Q' on the keyboard.
