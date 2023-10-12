import requests
import json

configUse = input("Enter a 1 to use the config file values and a 0 to use new values:\n")

if configUse == "1":
    with open("config.json", "r") as f:
        config = json.load(f)
    server = config["ntfy_server"]
    topic = config["ntfy_topic"]
    title = config["ntfy_title"]
    priority = ["ntfy_priority"]

    url = server + "/" + topic

elif configUse == "0":
    server = input("What server do you want to use? Ensure to include \"https://\" or \"http://\".\n")
    topic = input("What topic do you want to post to?\n")
    url = server + "/" + topic
    title = input("What do you want the title to be?\n")
    priority = input("What do you want the priority to be? Answer with a number 1-5.\n")


message = input('What would you like the message to be?\n')

requests.post(url, data=message, headers={"Title":title,"Priority":priority})