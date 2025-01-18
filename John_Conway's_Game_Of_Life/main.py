isValidR = False
isValidC = False

while isValidR == False:
    rowNum = int(input("Please enter the number (integer) of rows in the grid: "))
    if rowNum > 0:
        isValidR = True
    else:
        print("Please enter a positive integer for the number of rows.")

while isValidC == False:
    colNum = int(input("Please enter the number (integer) of columns in the grid: "))
    if colNum > 0:
        isValidC = True
    else:
        print("Please enter a positive integer for the number of columns.")

print("\nHere is your grid: ")

startingList = [[i + 1 + j * colNum for i in range(colNum)] for j in range(rowNum)]

longestElement = len(str(rowNum * colNum))

print("|", end="")
for k in range(((longestElement + 3) * colNum) - 1):
    print("-", end="")
print("|")

for l in startingList:
    for m in l:
        print("| ", end="")
        print(m, end="")
        for l in range(longestElement - len(str(m))):
            print(" ", end="")
        print(" ", end="")
        
        if m % colNum == 0:
            print("|")
            print("|", end="")
            for n in range(((longestElement + 3) * colNum) - 1):
                print("-", end="")
            print("|")

stopAdding = False
aliveNums = []
print()
print("The program will ask you for the corresponding cell numbers (integers) that you would like to activate as alive. Please enter the numbers one at a time.")

while stopAdding == False:
    addAlive = input("Please either enter one number (integer) or type 'Stop' to continue the program: ")
    if addAlive == "stop" or addAlive == "Stop" or addAlive == "q":
        stopAdding = True
    elif int(addAlive) not in range(1, rowNum * colNum + 1):
        print("Please enter a valid input. ")
    else:
        aliveNums.append(int(addAlive))

isValidG = False
while not isValidG:
    genNum = int(input("Please enter the number (integer) of generations you want to carry out: "))
    if genNum > 0:
        isValidG = True
    else:
        print("Please enter a positive integer for the number of generations.")

grid = [[num for num in row] for row in startingList]

for o in range(rowNum):
    for p in range(colNum):
        if grid[o][p] in aliveNums:
            grid[o][p] = "@"

print()
print("Generation 0: ")
print("|", end="")
for q in range(((longestElement + 3) * colNum) - 1):
    print("-", end="")
print("|")

counter1 = 0
for r in grid:
    for s in r:
        print("| ", end="")
        print(s, end="")
        for t in range(longestElement - len(str(s))):
            print(" ", end="")
        print(" ", end="")
        counter1 += 1
        
        if counter1 % colNum == 0:
            print("|")
            print("|", end="")
            for u in range(((longestElement + 3) * colNum) - 1):
                print("-", end="")
            print("|")

def neighbourNum(grid, rowNum, colNum, rowNumber, colNumber):
    '''
    Returns the number of neighbours a given element in the grid has
    '''
    liveNeighbors = 0
    for aroundR in range(max(0, rowNum - 1), min(rowNumber, rowNum + 2)):
        for aroundC in range(max(0, colNum - 1), min(colNumber, colNum + 2)):
            if (aroundR, aroundC) != (rowNum, colNum) and grid[aroundR][aroundC] == "@":
                liveNeighbors += 1
    return liveNeighbors


neighbourList = [[0] * colNum for v in range(rowNum)]

underpopulation = []
overpopulation = []
breeding = []
justRight = []

for w in range(1, genNum):
    
    for x in range(rowNum):
        for y in range(colNum):
            neighbourList[x][y] = neighbourNum(grid, x, y, rowNum, colNum)
    
    for z in range(rowNum):
        for a in range(colNum):
            if neighbourList[z][a] < 2 and grid[z][a] == "@":
                grid[z][a] = startingList[z][a]
                underpopulation.append(startingList[z][a])
            elif grid[z][a] == "@" and neighbourList[z][a] in range(2,4):
                grid[z][a] = "@"
                justRight.append(startingList[z][a])
            elif grid[z][a] != "@" and neighbourList[z][a] == 3:
                grid[z][a] = "@"
                breeding.append(startingList[z][a])
            elif neighbourList[z][a] > 3:
                grid[z][a] = startingList[z][a]
                overpopulation.append(startingList[z][a])

    print()
    print("Generation: ", w)
    print()
    
    print("Underpopulation: ", end="")
    for b in underpopulation:
        if b == underpopulation[-1]:
            print(b)
        else:
            print(b, end=", ")
    print()
    print("Just Right: ", end="")
    for c in justRight:
        if c == justRight[-1]:
            print(c)
        else:
            print(c, end=", ")
    print()
    print("Overpopulation: ", end="")
    for d in overpopulation:
        if d == overpopulation[-1]:
            print(d)
        else:
            print(d, end=", ")
    print()
    print("Breeding: ", end="")
    for e in breeding:
        if e == breeding[-1]:
            print(e)
        else:
            print(e, end=", ")
    
    counter2 = 0
    print()
    print("|", end="")
    for b in range(((longestElement + 3) * colNum) - 1):
        print("-", end="")
    print("|")
    for c in grid:
        for d in c:
            print("| ", end="")
            print(d, end="")
            for e in range(longestElement - len(str(d))):
                print(" ", end="")
            print(" ", end="")
            counter2 += 1
            
            if counter2 % colNum == 0:
                print("|")
                print("|", end="")
                for d in range(((longestElement + 3) * colNum) - 1):
                    print("-", end="")
                print("|")
    overpopulation = []
    breeding = []
    underpopulation = []
    justRight = []
