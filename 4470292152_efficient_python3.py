import sys
import timeit

from memory_profiler import memory_usage

delta = 30

def processInputFile():
    stringX = ""
    stringY = ""

    if len(sys.argv) == 1:
        print("You forgot to list the input file as an argument (see project instructions)!")
    else:
        input_file_path = str(sys.argv[1].strip())

    with open(input_file_path) as inputFile:
        for line in inputFile:
            if line.strip().isalpha() and stringX == "":
                stringX = line.strip()
            elif line.strip().isalpha() and not stringX == "":
                stringY = line.strip()
            elif not stringX == "" and stringY == "":
                index_to_add_to = int(line.strip())
                stringX = stringX[:index_to_add_to+1] + stringX + stringX[index_to_add_to+1:]
                #print("working_string X: " + str(stringX))
            else:
                index_to_add_to = int(line.strip())
                stringY = stringY[:index_to_add_to+1] + stringY + stringY[index_to_add_to+1:]
                #print("working_string Y: " + str(stringY))

    return stringX, stringY


def getMismatchCost(stringX_char, stringY_char):
    mismatch_cost = 0

    #print("stringX_char: " + str(stringX_char))
    #print("stringY_char: " + str(stringY_char))
    if (stringX_char == "A" and stringY_char == "C") or (stringX_char == "C" and stringY_char == "A"):
        mismatch_cost = 110
    elif (stringX_char == "A" and stringY_char == "G") or (stringX_char == "G" and stringY_char == "A"):
        mismatch_cost = 48
    elif (stringX_char == "A" and stringY_char == "T") or (stringX_char == "T" and stringY_char == "A"):
        mismatch_cost = 94
    elif (stringX_char == "G" and stringY_char == "C") or (stringX_char == "C" and stringY_char == "G"):
        mismatch_cost = 118
    elif (stringX_char == "T" and stringY_char == "G") or (stringX_char == "G" and stringY_char == "T"):
        mismatch_cost = 110
    elif (stringX_char == "T" and stringY_char == "C") or (stringX_char == "C" and stringY_char == "T"):
        mismatch_cost = 48

    return mismatch_cost

def getAlignmentValuesWithInputString(stringX, stringY):
    M_array = []
    for k in range(0, (len(stringY) + 1)):
        empty_row = [0] * (len(stringX) + 1)
        M_array.append(empty_row)

    for i in range(1, len(stringX) + 1):
        M_array[0][i] = delta * i
    for j in range(1, len(stringY) + 1):
        M_array[j][0] = delta * j

    for y in range(1, len(stringY) + 1):
        for x in range(1, len(stringX) + 1):
            stringY_char = stringY[y - 1]
            stringX_char = stringX[x - 1]

            mismatch_cost = getMismatchCost(stringX_char, stringY_char)

            # print("matched: " + str(mismatch_cost + M_array[y-1][x-1]))
            # print("no_match_x: " + str(delta + M_array[y][x-1]))
            # print("no_match_y: " + str(delta + M_array[y-1][x]))

            min_val = min(mismatch_cost + M_array[y - 1][x - 1], delta + M_array[y][x - 1], delta + M_array[y - 1][x])
            # print("min_val: " + str(min_val))
            M_array[y][x] = min_val

    resulting_coords = []
    x = len(stringX)
    y = len(stringY)

    resulting_coords.append((x, y))

    while x >= 1 or y >= 1:
        #print("i: " + str(i))

        stringY_char = "_"
        if y > 0:
            stringY_char = stringY[y - 1]

        stringX_char = "_"
        if x > 0:
            stringX_char = stringX[x - 1]

        mismatch_cost = getMismatchCost(stringX_char, stringY_char)

        matched = 99999999999
        no_match_x = 99999999999
        no_match_y = 99999999999

        if x > 0 and y > 0:
            matched = mismatch_cost + M_array[y - 1][x - 1]
        if x > 0:
            no_match_x = delta + M_array[y][x - 1]
        if y > 0:
            no_match_y = delta + M_array[y - 1][x]

        #print("HAVE: matched: " + str(matched))
        #print("HAVE: no_match_x: " + str(no_match_x))
        #print("HAVE: no_match_y: " + str(no_match_y))

        if matched <= no_match_x and matched <= no_match_y:
            #print("MATCH")
            resulting_coords.append((x-1,y-1))
            x = x - 1
            y = y - 1
        elif no_match_x <= matched and no_match_x <= no_match_y:
            #print("X MATCHES Y GAP")
            resulting_coords.append((x - 1, y))
            x = x - 1
        elif no_match_y <= matched and no_match_y <= no_match_x:
            #print("Y MATCHES X GAP")
            resulting_coords.append((x, y - 1))
            y = y - 1

    return resulting_coords

def writeAlignmentValues_MemoryEfficient():
    stringX, stringY = processInputFile()
    #print("stringX: " + str(stringX))
    #print("stringY: " + str(stringY))

    Plist = [(0, 0), (len(stringX), len(stringY))]
    Plist = dc_align(stringX, stringY, Plist, 1, 1)

    #sort by x then y coord
    nodesToVisit = sorted(set(Plist), key=lambda node: (node[0], node[1]))

    x_solution = ""
    y_solution = ""

    for node_index in range(1, len(nodesToVisit)):
        prev_node = node = nodesToVisit[node_index-1]
        node = nodesToVisit[node_index]

        if prev_node[0] == node[0]-1 and prev_node[1] == node[1]-1:
            #then first char matched
            x_solution = x_solution + stringX[node[0]-1]
            y_solution = y_solution + stringY[node[1]-1]
        elif prev_node[0] == node[0]-1:
            x_solution = x_solution + stringX[node[0]-1]
            y_solution = y_solution + "_"
        elif prev_node[1] == node[1]-1:
            x_solution = x_solution + "_"
            y_solution = y_solution + stringY[node[1]-1]

    #print(str(set(Plist)))
    #print("x_solution: " + x_solution)
    #print("y_solution: " + y_solution)
    global xToWrite
    global yToWrite
    if len(x_solution) >= 50:
        xToWrite = x_solution[:50] + " " + x_solution[len(x_solution)-50:]
    else:
        xToWrite = x_solution + " " + x_solution

    if len(y_solution) >= 50:
        yToWrite = y_solution[:50] + " " + y_solution[len(y_solution)-50:]
    else:
        yToWrite = y_solution + " " + y_solution

def space_efficient_align(stringX, stringY):
    M_array = []
    for k in range(0, len(stringY) + 1):
        empty_row = [0] * 2
        M_array.append(empty_row)


    for j in range(1, len(stringY) + 1):
        M_array[j][0] = delta * j

    for x in range(1, len(stringX) + 1):
        M_array[0][1] = delta * x
        stringX_char = stringX[x - 1]
        for y in range(1, len(stringY) + 1):
            stringY_char = stringY[y-1]

            mismatch_cost = getMismatchCost(stringX_char, stringY_char)

            min_val = min(mismatch_cost + M_array[y - 1][0], delta + M_array[y][0], delta + M_array[y - 1][1])
            #print("min_val: " + str(min_val))
            M_array[y][1] = min_val

        #Update Columns
        if x != len(stringX):
            for row in M_array:
                row[0] = row[1]

    return M_array

def dc_align(stringX, stringY, Plist, base_x, base_y):
    m = len(stringX)
    n = len(stringY)

    #print("TESTstringX: " + stringX)
    #print("TESTstringY: " + stringY)

    if m <= 2 or n <= 2:
        coords = getAlignmentValuesWithInputString(stringX, stringY)
        new_coords = []
        for pair in coords:
            newX = pair[0] + base_x - 1
            newY = pair[1] + base_y - 1
            new_coords.append((newX,newY))
        Plist = Plist + new_coords
        return Plist


    forwardX = stringX[:m//2]
    forward_align = space_efficient_align(forwardX, stringY)
    reversedY = stringY[::-1]
    second_half_x = stringX[m//2: m]
    reversedX = second_half_x[::-1]
    backward_align = space_efficient_align(reversedX, reversedY)

    min_index = 0
    min_value = 99999999999999999999999999
    for i in range(0, n+1):
        check_value = forward_align[i][1] + backward_align[n-i][1]
        if check_value <= min_value:
            min_value = check_value
            min_index = i

    #list in x,y format
    Plist.append((m//2 + base_x, min_index + base_y))

    #print("aeppending: " + str((m//2 + base_x, min_index + base_y)))
    #print("firstX: " + str(stringX[:m//2]))
    #("secondY: " + str(stringY[:min_index]))
    #print("thirdX: " + str(stringX[m//2 + 1:]))
    #print("fourthY: " + str(stringY[min_index + 1:]))

    Plist = dc_align(stringX[:m//2], stringY[:min_index], Plist, base_x, base_y)
    #new_x_base = min(m//2 + 1 + base_x, len(stringX)+1)
    new_x_base = m // 2 + 1 + base_x
    #new_y_base = min(min_index + 1 + base_y, len(stringY)+1)
    new_y_base = min_index + 1 + base_y
    Plist = dc_align(stringX[m//2 + 1:], stringY[min_index + 1:], Plist, new_x_base, new_y_base)

    return Plist


if __name__ == '__main__':
    xToWrite = ""
    yToWrite = ""

    with open("output.txt", "w+") as outputFile:
        checkpoint_1 = timeit.default_timer()
        efficient_mem_usage = memory_usage(writeAlignmentValues_MemoryEfficient)
        checkpoint_2 = timeit.default_timer()

        time_taken = checkpoint_2 - checkpoint_1
        outputFile.write(xToWrite + "\n")
        outputFile.write(yToWrite+ "\n")
        outputFile.write(str(time_taken)+ "\n")
        outputFile.write(str(max(efficient_mem_usage) * 1000))

    print("Enjoy your winter break!")
