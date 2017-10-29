

def checkCustomCommandName(name):
    name = str(name)

    if len(name) > 20:
        return False

    elif len(name) < 1:
        return False

    else:
        return True

def checkResponse(response):
    response = str(response)

    if len(response) > 1000:
        return False

    elif len(response) < 1:
        return False

    else:
        return True
