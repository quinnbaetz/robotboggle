import finger
import boggle
import optparse


WIDTH = 4
HEIGHT = 4
offsetTop = .25
offsetBottom = .15
offsetLeft = .05
offsetRight = .05
padHeight = 1 - (offsetTop + offsetBottom)
padWidth = 1 - (offsetLeft + offsetRight)

def bylength(word1, word2):
        return len(word2) - len(word1)

def toCoords(num):
    return (int(num)%WIDTH, int(int(num)/WIDTH))


def convertToCoordinates(num):
    x, y = toCoords(num)
    percX = (padWidth/WIDTH)*x + offsetTop
    percY = (padHeight/HEIGHT)*y + offsetLeft
    return (percX, percY)



def main():
    boggle.load_dictionary()

    usage = """Usage: %prog [board_letters]

Example: %prog  T N N H  I G N E  S G E I  C A H N"""

    parser = optparse.OptionParser(usage=usage)
    options, args = parser.parse_args()
    print args
    if args:
        board = boggle.make_board(width=WIDTH, height=HEIGHT, letters=' '.join(args))
    else:
        board = boggle.make_board(width=WIDTH, height=HEIGHT)

    boggle.print_board(board)
    print '----'
    #precalculate word list, optimize by doing robot while building this up
    words, locmap = boggle.solve(board)
    wordList = list(words)
    wordList.sort(cmp=bylength)
    for i in wordList:
        print "( %s -> %s )" % (i, locmap[i])
        locs = locmap[i].split(",")
        finger.down(*convertToCoordinates(locs[0]))
        for loc in locs[1:]:
            finger.drag(*convertToCoordinates(loc))
        finger.up()
        print





if __name__ == '__main__':
    main()
