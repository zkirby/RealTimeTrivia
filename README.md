# Race Car Trivia Game (Arduino/Python)
# About
This application was developed as the second half of a trivia game meant to be played by two players. The program has a GUI built in pygame (hopefully moved to GTK+3 one day) that flashes trivia questions. If the player gets the question right, a car controlled by an Arduino Uno moves forward and flashes green lights. If the player answers 10 questions correctly they win. To play the game you can rase the clock or set up two computers to race against a friend. I constructed this a long time ago for a club rush in high school for the robotics team.

# How It Works
The GUI in Pygame uses the Pyserial python module to push single letter commands (either an R or W) to an open serial port running on the Arduino. The data is then read in a continuous loop by the Arduino script until it receives something. It then executes some commands based on which letter was passed to the script. 
