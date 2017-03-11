# Tool Module:
# Functions that make life easier
"""

Functions List:
isIntTOOL
giveMeanOfListTOOL
giveListInOrderTOOL

"""

# Return TRUE if INT else FALSE
def isIntTOOL(number):
    try:
        int(number)
        return True
    except ValueError:
        return False

# !!!LIST MUST BE MADE OF SAME DATA TYPE OR BOOLEANS AND NON STRING!!! RETURN MEAN as an INT
def giveMeanOfListTOOL(list):
    size = len(list)
    valuelist = []

    # Turn VALUES from LIST to make a VALUELIST of NUMBERS or a VALUELIST of STRINGS
    for value in list:
        if isIntTOOL(value) == True:
            valuelist.append(value)

        elif value == True:
            valuelist.append(1)

        elif value == False:
            valuelist.append(0)

        elif value == "null" or value == "":
            valuelist.append(0)

        else:
            return "!!!DOESN'T SUPPORT " + str(value) + "!!!"

    # PROCESS the DATA
    if isIntTOOL(valuelist[0]) == True:  # If DATA is MADE of NUMBERS
        total = 0.0

        for number in valuelist:
            total += number

        return total / size  # MEDIAN formula total(all)/len(all)

    else:  # If DATA is MADE of NON NUMBER
        return "!!!DOESN'T SUPPORT THE FOLLOWING!!!\n" + str(valuelist)

# !!!LIST MUST BE MADE OF SAME STRINGS!!! RETURNS LIST sorting STRINGS from those who REPEAT MOST to those who REPEAT LEAST. [1(first biggest value) : XXXXX, 2(second biggest value) : XXXXX, etc..]
def giveListInOrderTOOL(list):
    stringdictionary = {}  # DICTIONARY made of ALL POSSIBLE STRINGS

    if isIntTOOL(list[0]) == True:
        return "!!!DOESN'T SUPPORT " + str(list[0]) + "!!!"

    for value in list:  # ADDING STRINGS to the STRINGDICTIONARY
        if value in stringdictionary:  # To PREVENT any GLITCHES
            pass
        else:  # ADDS STRING to the VALUE DICTIONARY ONCE
            stringdictionary[str(value)] = 0

    for string in stringdictionary:  # ADD to the VALUE of a STRING for EACH INSTANCE of that STRING in LIST
        stringdictionary[str(string)] = list.count(str(string))

    sort = sorted(stringdictionary.values())  # LIST of the ORDER of the VALUES

    result = []
    for position in sort:
        for key, value in stringdictionary.items():
            if value == position:
                if key in result:
                    pass
                else:
                    result.append(str(key))
                    break

    result.reverse()

    return result
