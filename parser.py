from collections import namedtuple

Room = namedtuple('Room', 'type children has_portal')

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

data = open('data.txt', 'w')
labels = open('labels.txt', 'w')

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

def get_good_child(children):
    for i, child in enumerate(children):
        if child.has_portal:
            return child, i

# Print a sequence of rooms to the portal room
def get_good_children(stronghold, depth=1, last='Start'):
    child, _ = get_good_child(stronghold.children)

    # If the child has no children, you found the portal room
    if len(child.children) == 0:
        return

    if child.type not in ['FiveWayCrossing', 'SquareRoom', 'Corridor']:
        get_good_children(child, depth+1, child.type)
        return
    
    for room in child.children:
        if room.type == 'PortalRoom':
            return

    if len([x for x in child.children if x.type != 'None' and x.type != 'Library' and x.type != 'SmallCorridor']) <= 1:
        get_good_children(child, depth+1, child.type)
        return

    print_result(depth, last, child.type, [x.type for x in child.children], get_good_child(child.children)[1])
    get_good_children(child, depth+1, child.type)

def print_result(depth, last, current, children, label):
    for _ in range(5 - len(children)):
        children.append('None')

    lists = [depth]
    lists += room_to_vector[last] + room_to_vector[current]
    for child in children:
        lists += room_to_vector[child]
    
    data.write(str(lists) + '\n')
    labels.write(str([label]) + '\n')

    
# Create 
gen = parse_file('strongholds.txt')

for _ in range(100000):
    stronghold = next(gen)
    if stronghold == None:
        break

    get_good_children(stronghold)
    # data.flush()
    # data.flush()