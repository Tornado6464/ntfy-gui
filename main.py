import requests
import json
import PySimpleGUI as psg
import os
import os.path
import typing

version = "v1.1.0"


# Check if the config.json exists, if it does not, create it.
file_exists = os.path.exists('./ntfy-gui/config.json')

if not file_exists:
    defaultConfig = {
        "ntfy_server": "",
        "ntfy_topic": "",
        "ntfy_title": "",
        "ntfy_priority": "",
        "ntfy_access_token": ""
    }
    path:str = './ntfy-gui'
    try:
        os.rmdir(path)
    except:
        os.mkdir(path)
    else:
        os.mkdir(path)
    with open('./ntfy-gui/config.json', 'w') as f:
        defaultConfigJson = json.dumps(defaultConfig)
        f.write(defaultConfigJson)

    # Notify the user that a new directory and config.json have been generated.
    psg.theme_global("DarkBlue15")
    psg.popup_ok("A directory named \"ntfy-gui\" has been created in this directory. It contains a json configuration file for quicker message sending.")

with open("./ntfy-gui/config.json", "r") as f:
        config:dict[str, int] = json.load(f)
        defaultServer:str = config["ntfy_server"]
        defaultTopic:str = config["ntfy_topic"]
        defaultTitle:str = config["ntfy_title"]
        defaultPriority:str = config["ntfy_priority"]
        defaultAccessToken:str = config["ntfy_access_token"]

# Basic set up for GUI
headerText = psg.Text('Welcome! You are currently using ' + version + '\n', expand_x=True, justification='center')
serverText = psg.Text('Input the server here. Ensure to include \"https://\".', expand_x=True, justification='center')
server = psg.Input(defaultServer, key='-SERVER-', expand_x=True, justification='center')
topicText = psg.Text('What topic do you want to post to?', expand_x=True, justification='center')
topic = psg.Input(defaultTopic, key='-TOPIC-', expand_x=True, justification='center')
titleText = psg.Text('What do you want the title to be? (Optional)', expand_x=True, justification='center')
title = psg.Input(defaultTitle, key='-TITLE-', expand_x=True, justification='center')
priorityText = psg.Text('What do you want the priority to be? Answer with a number 1-5. (Optional)', expand_x=True, justification='center')
priority = psg.Input(defaultPriority, key='-PRIORITY-', expand_x=True, justification='center')
accessTokenText = psg.Text('If using a topic behind authentication, enter your access token here. (Optional)', expand_x=True, justification='center')
accessToken = psg.Input(defaultAccessToken, key='-ACCESS_TOKEN-', expand_x=True, justification='center')
emailText = psg.Text('If you would like to send an email containing this message, enter the email address here. Enter no more than one email address. (Optional)', expand_x=True, justification='center')
email = psg.Input('', key='-EMAIL-', expand_x=True, justification='center')
phoneText = psg.Text('Send to notification to a phone number. Requires the authentication field to be filled out. (Optional)', expand_x=True, justification='center')
phone = psg.Input('', key='-PHONE-', expand_x=True, justification='center')
messageText = psg.Text('What would you like the message to be?', expand_x=True, justification='center')
message = psg.Input('', key='-MESSAGE-', expand_x=True, justification='center')
send = psg.Button('Send', key='-SEND-')
save = psg.Button('Save', key='-SAVE-')

psg.theme_global("DarkBlue15")
layout = [[headerText], [serverText], [server], [topicText], [topic], [titleText], [title], [priorityText], [priority], [accessTokenText], [accessToken], [emailText], [email], [phoneText], [phone], [messageText], [message], [[send],[save]]]
window = psg.Window('ntfy GUI', layout, size=(1000,600))

# GUI
while True:
    event, values = window.read()
    print(event, values)
    if event == '-SEND-':
        if values['-PRIORITY-'] not in ('12345'):
            psg.popup("Only digits 1-5 are allowed as the priority")
            window['-PRIORITY-']('')
        if "https://" not in values['-SERVER-']:
            psg.popup("You must include \"https://\" in the server field.")
            window['-SERVER-']('')
        else:
            server = values['-SERVER-']
            topic = values['-TOPIC-']
            title = values['-TITLE-']
            priority = values['-PRIORITY-']
            accessToken = values['-ACCESS_TOKEN-']
            email = values['-EMAIL-']
            phone = values['-PHONE-']
            message = values['-MESSAGE-']
            url = server + '/' + topic
            requests.post(url, data=message, headers={"Title":title,"Priority":priority,"Authorization": "Bearer " + accessToken, "Email": email, 'Call': phone})
            psg.popup_ok("Message sent.")

    if event =='-SAVE-':
        server = values['-SERVER-']
        topic = values['-TOPIC-']
        title = values['-TITLE-']
        priority = values['-PRIORITY-']
        message = values['-MESSAGE-']
        accessToken = values['-ACCESS_TOKEN-']

        saveConfig = {
            "ntfy_server": server,
            "ntfy_topic": topic,
            "ntfy_title": title,
            "ntfy_priority": priority,
            "ntfy_access_token": accessToken
        }
        path = './ntfy-gui'
        os.remove('./ntfy-gui/config.json')
        os.removedirs(path)
        os.mkdir(path)
        with open('./ntfy-gui/config.json', 'w') as f:
            saveConfigJson = json.dumps(saveConfig)
            f.write(saveConfigJson)
        psg.theme("DarkBlue15")
        psg.popup_ok("Configuration saved")

    if event == psg.WIN_CLOSED or event == '-EXIT-':
        break