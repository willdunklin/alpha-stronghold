from collections import namedtuple


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