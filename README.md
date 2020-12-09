# alpha-stronghold

This project is meant to correctly traverse the randomly generated Stronghold structure in Minecraft. 
The current iteration uses a simple classifier for any given room but will eventually be an LSTM based maze-traversal-like algorithm.

## To get data
Generate ```data.txt``` and ```labels.txt``` with ```parser.py``` using ```strongholds.txt``` (https://drive.google.com/file/d/1PswZeVVz8Q7iLcRnCDr5geRqcid8kZQb/view?usp=sharing).

## To train the classifier
Run ```classifier.py``` and it will generate a model. Tweak the number of epochs to get different training results, or figure out how loading models back in works.

## To test a room with classifier
Run ```test.py```. You will be asked to input a json style list that contains pertinent data.

The general formate is as follows:

```[depth, "PreviousRoom", "CurrentRoom", ["Child", "Rooms", "In", "Order", "None"]]```

A empty format can will be supplied by typing ```?``` into the prompt.

#### Note: only run the algorithm on rooms with choices (Corridor, FiveWayCrossing, SquareRoom) and in all other choices advance forward into the next available room.

The list of rooms can be found on ```line 1``` of ```test.py``` but are also listed below:

```
Corridor
PrisonHall
LeftTurn
RightTurn
SquareRoom
Stairs
SpiralStaircase
FiveWayCrossing
ChestCorridor
Library
PortalRoom
SmallCorridor
Start
None
```
