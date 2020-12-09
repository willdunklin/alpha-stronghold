room_to_vector = {
    'Corridor':         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'PrisonHall':       [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'LeftTurn':         [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'RightTurn':        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'SquareRoom':       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'Stairs':           [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    'SpiralStaircase':  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    'FiveWayCrossing':  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    'ChestCorridor':    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    'Library':          [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    'PortalRoom':       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    'SmallCorridor':    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    'Start':            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    'None':             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
}

from collections import namedtuple
from tensorflow import keras
from numpy import asarray
import json

Room = namedtuple('Room', 'type children has_portal')

def get_room_from_line(line, current_stronghold_list):
    stuff = line.rstrip('\n').split(" ")
    c_indices = stuff[1::]
    children = []
    has_portal = stuff[0] == "PortalRoom"
    for child in c_indices:
        if int(child) == -1:
            children.append(Room("None", [], False))
        else:
            children.append(current_stronghold_list[int(child)])
            if current_stronghold_list[int(child)].has_portal:
                has_portal = True
    return Room(stuff[0], children, has_portal)

def parse_file(path):
    f = open(path, "r")
    while True:
        line = f.readline()
        if not line:
            break
        if 'START' in line:
            f.readline()
            line = f.readline()
            stronghold = []
            last_room = None
            while 'END' not in line:
                last_room = get_room_from_line(line, stronghold)
                stronghold.append(last_room)
                line = f.readline()
            yield last_room

# depth: depth of room, last: name of last room, current: name of current room, children: list of child names
def create_data(depth, last, current, children):
    for _ in range(5 - len(children)):
        children.append('None')

    lists = [depth]
    lists += room_to_vector[last] + room_to_vector[current]
    for child in children:
        lists += room_to_vector[child]

    return lists

def get_input():
    s = input('Input for current room: ')
    if s == '?':
        print('format: [, "", "", ["", "", "", "", ""]]')
        return get_input()
    params = json.loads(s)

    return create_data(params[0], params[1], params[2], params[3])

model = keras.models.load_model("model5.keras")

while True:
    data = [asarray(get_input())]
    data = asarray(data)
    print(model.predict(data))