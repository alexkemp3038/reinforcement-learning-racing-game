# reinforcement-learning-racing-game
<H1>How to run</H1>
Still work in progress

<H1>Making The Game</H1>
<H2>Step 1: Make an easy testing map</H2>
<img width="1762" height="1030" alt="image" src="https://github.com/user-attachments/assets/3f0cf0e6-5655-4c91-86f1-74e4f348cb10" />
I created an easy map using Tiled.

<H2>Step 2: Make a hard map</H2>
<img width="1592" height="1062" alt="image" src="https://github.com/user-attachments/assets/c98be540-0498-4ff0-8e75-bd3cde9bb250" />
I made a harder map with tighter turns for the final map the trained model should complete.

<h2>Step 3: Make the car basics</h2>
<img width="1906" height="1130" alt="image" src="https://github.com/user-attachments/assets/f5adab8a-3174-4d21-be7f-72c371fe8298" />
The first goal was to make the car move around the map, rotate the car 90 degrees when it turns direction and implement simple out-of-bounds checks. However after implementing this I felt the game felt too clunky. It would be hard to train a model without smooth turns around corners, so I had to change how it turns.

<h2>Step 4: Make a smooth turning mechanic</h2>
<img width="1877" height="1082" alt="image" src="https://github.com/user-attachments/assets/1fbf9a15-c000-421e-943a-d866b0867e81" />
Using some trigonometry, ...

<h2>Step 5: Add smooth collisions</h2>
<img width="1821" height="967" alt="image" src="https://github.com/user-attachments/assets/52bbd7f1-1c77-4419-a9c1-dacec5da5030" />

<h2>Step 6: Make a smoother racing map</h2>
<img width="1167" height="1086" alt="image" src="https://github.com/user-attachments/assets/73c51c36-0386-4c45-85b9-e4134ed5fd77" />
As my old map had rugged track borders, I decided to change it to something with smoother borders. Using some stock images online, I compiled together a new training map.

<H1>Making The Model</H1>
<H2>Step 1: Add raycasting values</H2>
<img width="1570" height="1101" alt="image" src="https://github.com/user-attachments/assets/0105b3cd-f07a-4201-9651-9b8ecc7715f8" />
To pass the values of the cars distance to the wall to the model for it to train steering I decided to use raycasting as its an effective method for a task like this with little performance overhead, meaning training wont take as long. I made a separate file for a sensor class, which is a sensor that sends out rays from the center of the car and uses angle dependant bounding box calculations combined with raycasting to determine the value from each ray to the track border, which is stored as a value between 0.0 and 1.0. It ranges from touching the wall (0.0), to the ray not detecting anything within its full maximum length (1.0).

<H2>Making Neural Network Skeleton</H2>
<img width="1207" height="987" alt="image" src="https://github.com/user-attachments/assets/0764197d-982f-4dfd-a380-9e3982853f00" />
Created a seperate file for the network, with two objects: NeuralNetwork and Level. Every NeuralNetwork has a list of levels. Each level is made up of inputs, outputs, biases and weights. feedForwards passes inputs through a process and gives each value to the mapped output. In this case, all inputs are times by its weight, then summed together. This is then compared to its bias, which is the threshold for whether the neuron should turn on or off. If the sum is greater than its bias the output is turned on (set to 1), otherwise its turned off (set to 0).
