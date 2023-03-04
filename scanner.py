import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import sys
from scapy.all import sr1,sr,IP,TCP

def scanner(target,startport,endport):
    print(f"Scanning {target} for open TCP Ports from {startport} to {endport}\n")

    if startport == endport:
        endport+=1

    open = 0
    for x in range(startport,endport):
        packet = IP(dst=target)/TCP(dport=x,flags="S")
        try:
            response = sr1(packet,timeout=0.5,verbose=0)
            if response.haslayer(TCP) and response.getlayer(TCP).flags==0x12:
                print(f"Port {x} is open!")
                open+=1
            sr(IP(dst=target)/TCP(dport=response.sport,flags='R'),timeout=0.5,verbose=0)
        except(AttributeError):
            pass

    print(f"Scan is Complete! {open} ports open in {target}!")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} target startport endport")
        sys.exit(0)

    target = str(sys.argv[1])
    startport = int(sys.argv[2])
    endport = int(sys.argv[3])

    scanner(target,startport,endport)