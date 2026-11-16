# reinforcement-learning-racing-game
<H1>Repository Structure</H1>
'racing_game.py' is the main file structure connecting components together and has the main game loop.This is the file that should be ran.<br>
'utils.py' has functions that is used in the main file, but is put in here for readability. The lerp() function is also used in other files.<br>
'car.py' is the file containing the AbstractCar class and its methods.<br>
'checkpoint.py' is the file containing the checkpoint class.<br>
'network.py' is the file containing the NeuralNetwork and Level classes. This is the main structure of the network allowing the model to learn.<br>
'sensor.py' is the file containing the Sensor class. This is used for ray casting values as inputs.<br>

<br>
<H1>Overview of the Logic</H1>
<H2>The Game</H2>
The map itself was made by combining assets found online.<br>
The game uses 'test_map_border_png' as a mask which is compared to the car hitbox to check for collisions.<br>
Car rotation is calculated using trigonometry to find where it should go diagonally.<br>
The cars speed, rotational speed and acceleration can be configured by changing MAX_SPEED, MAX_ROT_SPEED and ACCELERATION respectively.<br>
Each car has a defined sensor using the Sensor object, which uses raycasting to store a list of 9 values between 0 and 1 to represent how close that ray is to a wall.<br>

<H2>The Training Model</H2>
The neural network is made by defining a NeuralNetwork class which is made up of a list of Levels, with the first one in the list being the input layer and the last being the output layer.<br>
The network uses neuroevolution and mutation to get better.<br>
Neuroevolution is used by creating a defined number of cars, all with random brains, and selecting the best performing cars and variating them with the goal of improving them. Variation is done by mutation, this slightly tweaks the values of each brain with the goal of improving them. <br>
Every level object is essentially a pair of layers, as every level has a list of inputs(current layer) and outputs(next layer). It also has a list of biases and weights, which are initially randomised. <br>
The amount of neurons in the input layer is the amount of values stored in the sensor, by default this is 9.<br>
The amount of neurons in the output layer is 4, with each representing forward, backward, left and right respectively.<br>
By default, 1 hidden layer is defined, with 20 neurons.<br>
Running inputs through the network is done using the feedForward method in the NeuralNetwork class, where its feeds forward (runs values and calcuations through) every Level.<br> 
It is a fully connected network, where every connection is multiplied by its weight, they are then all summed up and compared to its bias. This is then ran through the tanh activation function, which is used to ensure smooth steering and to keep values close together and ensure non-linearity. If its the output layer and its greater than its bias, its considered important enough, and turned on. Otherwise, its turned off.<br>
To avoid overfitting: INITIAL_MUTATION (25% by default) is the mutation level used for generations 1-14 and 36-49, and REFINING_MUTATION (%5 by default) is used for generations 15-35 and over 50. This is done to ensure the model can handle randomness and allow for more obscure variations with the hope of them being faster, and then improving them with a more refined value.<br>

<H2>Average Case Example</H2>
For the first 1 or 2 generations, none of the cars might be able to even make the first turn. This is okay as they are randomised until a car reaches the first checkpoint (around the corner). Once a car reaches the first checkpoint, it is then saved as the champion car. Any cars that finish with the same number of checkpoints, will then be saved based on whoever reached the last checkpoint the fastest. The highest score is 17 as this is the number of checkpoints. The cars that will now spawn each generation will be a slightly altered version of the champion car, with more random and less random variations depending on what number of generation it is (25% for generations 1-14 and 36-49, and 5% for generations 15-35 and over 50). Once a car finishes the track, the best time will be updated and the time should get better the more they train.<br>

<H1>How to run</H1>
<H2>VSCode</H2>
1. Open the 'racing_game.py' file in your VSCode application.<br>
2. Make sure that python is installed on your computer. This can be done by clicking the 3 lines on the top left -> Terminal -> New Terminal -> and typing 'python --version'. If it does not pop up with a python version, you need to install python.<br>
3. Click 'run python file' on the top right, or right click anywhere in the file and click 'Run Python File'.<br>
4. If its your first time running it, the program should run after step 3. If a champion car file is generated after you've already ran it, follow the instructions prompted in the terminal.<br>
<br>
<H2>Command Prompt</H2>
1. Navigate to the directory 'racing_game.py' is in by using the 'cd ' command. To check if you are in the correct directory, type 'ls' and it should show its name.<br>
2. Type and enter 'python racing_game.py' in the terminal to run the program.<br>
3. If its your first time running it, the program should run after step 3. If a champion car file is generated after you've already ran it, follow the instructions prompted in the terminal.<br><br>
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

<H2>Step 2: Making Neural Network Skeleton</H2>
<img width="1207" height="987" alt="image" src="https://github.com/user-attachments/assets/0764197d-982f-4dfd-a380-9e3982853f00" />
Created a seperate file for the network, with two objects: NeuralNetwork and Level. Every NeuralNetwork has a list of levels. Each level is made up of inputs, outputs, biases and weights. feedForwards passes inputs through a process and gives each value to the mapped output. In this case, all inputs are times by its weight, then summed together. This is then compared to its bias, which is the threshold for whether the neuron should turn on or off. If the sum is greater than its bias the output is turned on (set to 1), otherwise its turned off (set to 0).

<H2>Step 3: Mapping outputs to controls</H2>
<img width="1840" height="842" alt="image" src="https://github.com/user-attachments/assets/35c66fa2-4c76-4799-8974-c0a630fb99a4" />
I then mapped these outputs to a newly created move_ai function which can now move the cars by itself. I then added a generate_cars(n) function that generates n amount of cars and the game loop has been altered to handle multiple cars. Once a car touches a border, the car is classified as dead (alive = false) and it can no longer move. To minimise visual clutter, I also added a feature where dead cars change transparency level.

<H2>Step 4: Deciding how to reward the agent</H2>
<img width="1560" height="782" alt="image" src="https://github.com/user-attachments/assets/ca2fd67c-cd2d-449a-b85b-886b4d567315" />
To save the best cars and mutate them, we need to define "best" and decide which car to save. To do this we need to reward the car for doing a correct action and the car with the most correct actions will be decided as the "best". Here are all the reward systems i considered and why I did/didn't pick it:
- Distance driven - This can work but cars the drive in circles or wiggling forward and back can be considered the best.
- Time alive - This only considers the alive state and doesnt actually consider progess within the race track.
- Lap time - Can be used to optimise lap time but wont help in early training as cars will not finish at first, may come back to this later..
- Checkpoints - This is the method I decided to use. It created checkpoints along the track and each car will keep track of each checkpoint it gets past.

<H2>Step 5: Implementing a save and load feature</H2>
<img width="637" height="551" alt="image" src="https://github.com/user-attachments/assets/1bd77e8f-6ce9-4d05-9d54-085e4c6f3224" />
To save the champion car, we need to save the best car object into a file and be able to load it back into memory. This can be done with three different ways in Python:
- JSON - Best for readable, secure objects. However, it doesnt support python objects, functions or NumPy Arrays (natively).
- NPZ - Best for ML datasets and numbers in a compressed format. However, its primarily used for NumPy ecosystem, not for rgeneral objects.
- Pickle - Great python supported file type for converts any Python Object into a byte stream. However, it isnt very secure, its only for python and mismatched versions is a common issue. It will also crash if something is changed in the object class and then it tries to be loaded.

After weighing all the pros and cons, I decided to go with Pickle. This is the easiest of the three to implement and security isn't a concern as it does not store confidential data and is a locally sourced project. The last issue is a concern, but shouldn't be an issue in the final version as it will be fully complete and the car class shouldn't be altered if its fully working.  

It only saves the brain as we want the car to begin at the beginning when the car is loaded and the brain stores the part we care about - the best brain out of all the cars.

<H2>Step 6: Putting it all together</H2>
<img width="997" height="952" alt="image" src="https://github.com/user-attachments/assets/56d3b787-b6d9-4ce8-b998-c1934318b0d7" />
Firstly, I created an HUD which displays generation number, times and scores. I also made a function that changes the mutation level based on what generation it is, to avoid overfitting (please read "The training model" for more info. on this).<br>

<img width="1197" height="815" alt="image" src="https://github.com/user-attachments/assets/7526d159-75ce-41aa-a9bc-c4ebfb95c5f9" />
I then added a user prompt in the terminal so the user can switch from restarting training, watching the best car in the champion car file or continue training the champion car.

<img width="1187" height="575" alt="image" src="https://github.com/user-attachments/assets/004a81d4-a91f-45d7-94eb-e11299062873" />
I had to update the way the cars are generated based on what the user prompts.

<img width="1177" height="252" alt="image" src="https://github.com/user-attachments/assets/b036453b-c11e-4b5e-8bd3-18c47b67ee07" />
Here I added a feature where the user can press the space bar, this ends training and goes into the mode for watching the champion car race by itself.

<img width="1207" height="822" alt="image" src="https://github.com/user-attachments/assets/1017236b-9118-4d9d-835b-6b5393c26fbf" />
<img width="1202" height="567" alt="image" src="https://github.com/user-attachments/assets/54fd94b7-6ee3-4480-926b-f7897129183f" />
This is main logic handling how new generations are handled and saved. A generation is over once either a timeout occurs, a car finished a lap or all cars are declared dead. Once a generation is over, a champion is set if there is a new one. The second image is for handling the visual for watching the champion car (endlessly drives around the track and is reset to start position each time).



