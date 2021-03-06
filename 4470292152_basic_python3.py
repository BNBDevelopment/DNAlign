import datetime
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

def writeAlignmentValues():
    stringX, stringY = processInputFile()

    #print("stringX: " + str(stringX))
    #print("stringY: " + str(stringY))

    M_array =[]
    for k in range(0, (len(stringY) + 1)):
        empty_row = [0] * (len(stringX) + 1)
        M_array.append(empty_row)

    for i in range(1, len(stringX) + 1):
        M_array[0][i] = delta * i
    for j in range(1, len(stringY) + 1):
        M_array[j][0] = delta * j


    for y in range(1, len(stringY) + 1):
        for x in range(1, len(stringX) + 1):
            stringY_char = stringY[y-1]
            stringX_char = stringX[x-1]

            mismatch_cost = getMismatchCost(stringX_char, stringY_char)

            #print("matched: " + str(mismatch_cost + M_array[y-1][x-1]))
            #print("no_match_x: " + str(delta + M_array[y][x-1]))
            #print("no_match_y: " + str(delta + M_array[y-1][x]))

            min_val = min(mismatch_cost + M_array[y-1][x-1], delta + M_array[y][x-1], delta + M_array[y-1][x])
            #print("min_val: " + str(min_val))
            M_array[y][x] = min_val

    #Work back to get solution:

    x = len(stringX)
    y = len(stringY)

    x_answer = ""
    y_answer = ""

    while x >= 1 or y >= 1:
        #print("i: " + str(i))

        stringY_char = stringY[y - 1]
        stringX_char = stringX[x - 1]
        mismatch_cost = getMismatchCost(stringX_char, stringY_char)

        matched = mismatch_cost + M_array[y - 1][x - 1]
        no_match_x = delta + M_array[y][x - 1]
        no_match_y = delta + M_array[y - 1][x]

        #print("HAVE: matched: " + str(matched))
        #print("HAVE: no_match_x: " + str(no_match_x))
        #print("HAVE: no_match_y: " + str(no_match_y))

        if matched <= no_match_x and matched <= no_match_y:
            #print("MATCH")
            x_answer = stringX[x-1] + x_answer
            y_answer = stringY[y-1] + y_answer
            x = x - 1
            y = y - 1
        elif no_match_x <= matched and no_match_x <= no_match_y:
            #print("X MATCHES Y GAP")
            y_answer = "_" + y_answer
            x_answer = stringX[x-1] + x_answer
            x = x - 1
        elif no_match_y <= matched and no_match_y <= no_match_x:
            #print("Y MATCHES X GAP")
            x_answer = "_" + x_answer
            y_answer = stringY[y - 1] + y_answer
            y = y - 1

    #TODO: WRITE TO OUTPUT.TXT AND CONFIRM THESE ARE CORRECT
    #print("x_answer: " + x_answer)
    #print("y_answer: " + y_answer)
    global xToWrite
    global yToWrite
    if len(x_answer) >= 50:
        xToWrite = x_answer[:50] + " " + x_answer[len(x_answer)-50:]
    else:
        xToWrite = x_answer + " " + x_answer

    if len(y_answer) >= 50:
        yToWrite = y_answer[:50] + " " + y_answer[len(x_answer)-50:]
    else:
        yToWrite = y_answer + " " + y_answer





if __name__ == '__main__':
    xToWrite = ""
    yToWrite = ""

    with open("output.txt", "w+") as outputFile:
        checkpoint_1 = timeit.default_timer()
        inefficient_mem_usage = memory_usage((writeAlignmentValues))
        checkpoint_2 = timeit.default_timer()

        time_taken = checkpoint_2 - checkpoint_1
        outputFile.write(xToWrite + "\n")
        outputFile.write(yToWrite+ "\n")
        outputFile.write(str(time_taken)+ "\n")
        outputFile.write(str(max(inefficient_mem_usage) * 1000))

    print("Enjoy your winter break!")


