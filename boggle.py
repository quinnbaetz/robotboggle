"""Simple 5x5 Boggle game solver.

Free to use under the New BSD License:
http://opensource.org/licenses/BSD-3-Clause

"""


import random

MIN_LENGTH = 2
DICTIONARY = set()
PREFIXES = {}
WIDTH = 5
HEIGHT = 5
OFFSETS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
CUBES = [s.lower().split() for s in [
    'S N S U S E',
    'A R Y I F S',
    'O H H L R D',
    'T E T M O T',
    'J K B X Q Z',
    'T E T I I I',
    'E T P S C I',
    'E E E E M A',
    'S A R A I F',
    'F R Y S I P',
    'E A E A E E',
    'N D N A N E',
    'N T D H H O',
    'Y I R P R H',
    'N R L D D O',
    'L I T C E P',
    'H D R O L N',
    'N N E M G A',
    'W U N T O O',
    'A A A F R S',
    'C C W N T S',
    'O T O U T O',
    'L I T C E I',
    'O V W R R G',
    'M E A G E U',
]]

def load_dictionary():
    global DICTIONARY
    global PREFIXES

    DICTIONARY = set()
    with open('words.txt') as f:
        for line in f:
            word = line.strip()
            if len(word) >= MIN_LENGTH and word.isalpha():
                DICTIONARY.add(word.lower())

    PREFIXES = {}
    for word in sorted(DICTIONARY):
        node = PREFIXES
        for letter in word:
            if letter not in node:
                node[letter] = {}
            node = node[letter]

    print len(DICTIONARY), 'words loaded'
    print '----'

def is_prefix(prefix):
    node = PREFIXES
    for letter in prefix:
        if letter not in node:
            return False
        node = node[letter]
    return True


def toNumber(pos):
    return str(pos[0] + pos[1]*WIDTH)

def find_words(board, positions_used, prefix, pos, buildup="", locMap={}):
    current = prefix + board[pos]
    add = ","
    if buildup is "":
        add = ""
    buildup = buildup + add +toNumber(pos)
    if not is_prefix(current):
        # No words with this as a prefix
        return set(), locMap

    found = set()
    if current in DICTIONARY:
        found.add(current)
        locMap[current] = buildup
    positions_used.add(pos)

    for offset in OFFSETS:
        new_pos = (pos[0] + offset[0], pos[1] + offset[1])
        if new_pos in positions_used:
            continue
        if not (0 <= new_pos[0] < WIDTH and 0 <= new_pos[1] < HEIGHT):
            continue

        newFound, newMap = find_words(board, positions_used, current, new_pos, buildup, locMap)
        found.update(newFound)
        locMap.update(newMap)

    positions_used.remove(pos)
    return found, locMap

def solve(board):
    words = set()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            found, locmap = find_words(board, set(), '', (x, y))
            words.update(found)
    return words, locmap

def make_board(width=4, height=4, letters=None):
    global WIDTH, HEIGHT
    WIDTH = width
    HEIGHT = height
    if letters is None:
        cubes = list(CUBES)
        random.shuffle(cubes)
        letters = ' '.join(random.choice(cube) for cube in cubes)
    board = {}
    y = 0
    x = 0
    for letter in letters.split():
        board[x, y] = letter.lower()
        x += 1
        if x >= WIDTH:
            x = 0
            y += 1
    return board

def print_board(board):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            letter = board[x, y]
            letter = letter.upper()
            print letter,
        print
    print
    for y in range(HEIGHT):
        for x in range(WIDTH):
            print toNumber((x, y)),
        print



