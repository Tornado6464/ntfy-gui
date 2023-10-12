import requests
import json
import PySimpleGUI as psg

#GUI below here

with open("config.json", "r") as f:
        config = json.load(f)
        defaultServer = config["ntfy_server"]
        defaultTopic = config["ntfy_topic"]
        defaultTitle = config["ntfy_title"]
        defaultPriority = config["ntfy_priority"]


serverText = psg.Text('Input the server here. Ensure to include \"https://\".', expand_x=True, justification='center')
server = psg.Input(defaultServer, key='-SERVER-', expand_x=True, justification='center')
topicText = psg.Text('What topic do you want to post to?', expand_x=True, justification='center')
topic = psg.Input(defaultTopic, key='-TOPIC-', expand_x=True, justification='center')
titleText = psg.Text('What do you want the title to be?', expand_x=True, justification='center')
title = psg.Input(defaultTitle, key='-TITLE-', expand_x=True, justification='center')
priorityText = psg.Text('What do you want the priority to be? Answer with a number 1-5.', expand_x=True, justification='center')
priority = psg.Input(defaultPriority, key='-PRIORITY-', expand_x=True, justification='center')
messageText = psg.Text('What would you like the message to be?', expand_x=True, justification='center')
message = psg.Input('', key='-MESSAGE-', expand_x=True, justification='center')
send = psg.Button('Send', key='-SEND-')

layout = [[serverText], [server], [topicText], [topic], [titleText], [title], [priorityText], [priority], [messageText], [message], [send]]
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
            url = server + '/' + topic
            requests.post(url, data=message, headers={"Title":title,"Priority":priority})
            break
    if event == psg.WIN_CLOSED or event == 'Exit':
        break