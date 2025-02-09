questsion_number = 0
response = "봇이지뭐"

def questsion_number_grant(x):
    global questsion_number
    response_date = {
        "text": x,
        "number": questsion_number
    }
    print(response_date)
    questsion_number = questsion_number + 1

questsion_number_grant(response)
questsion_number_grant(response)
questsion_number_grant(response)
questsion_number_grant(response)
