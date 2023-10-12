import requests
import json
import PySimpleGUI as psg
import os
import os.path

file_exists = os.path.exists('./ntfy-gui/config.json')

if file_exists == False:
    defaultConfig = {
        "ntfy_server": "",
        "ntfy_topic": "",
        "ntfy_title": "",
        "ntfy_priority": "",
        "ntfy_access_token": ""
    }
    path = './ntfy-gui'
    os.mkdir(path)
    with open('./ntfy-gui/config.json', 'w') as f:
        defaultConfigJson = json.dumps(defaultConfig)
        f.write(defaultConfigJson)

    psg.theme("DarkBlue15")
    layout = [[psg.Text("A directory named \"ntfy-gui\" has been created in this directory. It contains a json configuration file for quicker message sending.")], [psg.Button("OK")]]

    # Create the window
    window = psg.Window("Notification", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == psg.WIN_CLOSED:
            break

    window.close()

with open("./ntfy-gui/config.json", "r") as f:
        config = json.load(f)
        defaultServer = config["ntfy_server"]
        defaultTopic = config["ntfy_topic"]
        defaultTitle = config["ntfy_title"]
        defaultPriority = config["ntfy_priority"]
        defaultAccessToken = config["ntfy_access_token"]


serverText = psg.Text('Input the server here. Ensure to include \"https://\".', expand_x=True, justification='center')
server = psg.Input(defaultServer, key='-SERVER-', expand_x=True, justification='center')
topicText = psg.Text('What topic do you want to post to?', expand_x=True, justification='center')
topic = psg.Input(defaultTopic, key='-TOPIC-', expand_x=True, justification='center')
titleText = psg.Text('What do you want the title to be?', expand_x=True, justification='center')
title = psg.Input(defaultTitle, key='-TITLE-', expand_x=True, justification='center')
priorityText = psg.Text('What do you want the priority to be? Answer with a number 1-5.', expand_x=True, justification='center')
priority = psg.Input(defaultPriority, key='-PRIORITY-', expand_x=True, justification='center')
accessTokenText = psg.Text('If using a topic behind authentication, enter your access token here.', expand_x=True, justification='center')
accessToken = psg.Input(defaultAccessToken, key='-ACCESS_TOKEN-', expand_x=True, justification='center')
messageText = psg.Text('What would you like the message to be?', expand_x=True, justification='center')
message = psg.Input('', key='-MESSAGE-', expand_x=True, justification='center')
send = psg.Button('Send', key='-SEND-')

psg.theme("DarkBlue15")
layout = [[serverText], [server], [topicText], [topic], [titleText], [title], [priorityText], [priority], [accessTokenText], [accessToken], [messageText], [message], [send]]
window = psg.Window('ntfy GUI', layout, size=(1000,500))

while True:
    event, values = window.read()
    print(event, values)
    if event == '-SEND-':
        if values['-PRIORITY-'] not in ('12345'):
            psg.popup("Only digits 1-5 are allowed as the priority")
            window['-PRIORITY-'].update(values['-PRIORITY-'][:-1])
        elif values['-PRIORITY-'] in ('12345'):
            server = values['-SERVER-']
            topic = values['-TOPIC-']
            title = values['-TITLE-']
            priority = values['-PRIORITY-']
            message = values['-MESSAGE-']
            accessToken = values['-ACCESS_TOKEN-']
            # bearerAuth = "Bearer" + accessToken
            url = server + '/' + topic
            requests.post(url, data=message, headers={"Title":title,"Priority":priority,"Authorization": "Bearer " + accessToken})
            break
    if event == psg.WIN_CLOSED or event == 'Exit':
        break