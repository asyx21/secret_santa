# Secret Santa random drawing

Secret Santa is random drawing assigning one person to be responsible to offer a gift to another one.  
It is particularly usefull for big Christmas parties to simplify and limit the number of gifts each others are giving.  

This programs makes the drawing pseudo-randomly taking into account potential exclusion in between two or more players.

The results are written in separate files and are sent by email provided that player's have one.

## scripts

- `random_drawing.py`

## How to use

1. Prepare the participant file with details of the players. Use example participant.example.txt
2. Install libraries with `pip install -r requirements.txt`
3. Run `python random_drawing.py players.example.txt` giving the participant file to generate the drawing results
