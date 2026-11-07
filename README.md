# reinforcement-learning-racing-game
<H1>How to run</H1>
Still work in progress

<H1>Step 1: Make an easy testing map</H1>
<img width="1762" height="1030" alt="image" src="https://github.com/user-attachments/assets/3f0cf0e6-5655-4c91-86f1-74e4f348cb10" />
I created an easy map using Tiled.

<H1>Step 2: Make a hard map</H1>
<img width="1592" height="1062" alt="image" src="https://github.com/user-attachments/assets/c98be540-0498-4ff0-8e75-bd3cde9bb250" />
I made a harder map with tighter turns for the final map the trained model should complete.

<h1>Step 3: Make the car basics</h1>
<img width="1906" height="1130" alt="image" src="https://github.com/user-attachments/assets/f5adab8a-3174-4d21-be7f-72c371fe8298" />
The first goal was to make the car move around the map, rotate the car 90 degrees when it turns direction and implement simple out-of-bounds checks. However after implementing this I felt the game felt too clunky. It would be hard to train a model without smooth turns around corners, so I had to change how it turns.

<h1>Step 4: Make a smooth turning mechanic</h1>
<img width="1877" height="1082" alt="image" src="https://github.com/user-attachments/assets/1fbf9a15-c000-421e-943a-d866b0867e81" />
Using some trigonometry, ...

<h1>Step 5: Add smooth collisions</h1>
<img width="1821" height="967" alt="image" src="https://github.com/user-attachments/assets/52bbd7f1-1c77-4419-a9c1-dacec5da5030" />

<h1>Step 6: Make a smoother racing map</h1>
<img width="1167" height="1086" alt="image" src="https://github.com/user-attachments/assets/73c51c36-0386-4c45-85b9-e4134ed5fd77" />
As my old map had rugged track borders, I decided to change it to something with smoother borders. Using some stock images online, I compiled together a new training map.

