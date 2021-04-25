#sKarthika Thiruvallur 

from socket import * 
import os
import sys
import struct
import time 
import select 
import binascii
ICMP_ECHO_REQUEST = 8

def checksum(string): 
    string = bytearray(string)
    ctotal= 0
    countTo = (len(string) // 2) * 2 
    for count in range(0, countTo, 2):
        thisVal = string[count + 1] * 256 + string[count]
        ctotal = ctotal + thisVal
        ctotal = ctotal & 0xffffffff
    
    if countTo < len(string):
        ctotal = ctotal + string[-1]
        ctotal = ctotal & 0xffffffff

    ctotal = (ctotal >> 16) + (ctotal & 0xffff)
    ctotal = ctotal + (ctotal >> 16)
    answer = ~ctotal 
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer



def receiveOnePing(mySocket, ID, timeout, destAddr): 
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft) 
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:
            return "Request timed out."
        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
     
        icmpHeader = recPacket[20:28]
        icmpType, code, mychecksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
    
        if type != 8 and packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent  
      
        timeLeft = timeLeft - howLongInSelect 
        if timeLeft <= 0:
            return "Request timed out."



        
def sendOnePing(mySocket, destAddr, ID):
  
    myChecksum = 0
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1) 
    data = struct.pack("d", time.time())

    myChecksum = checksum(header + data)
    
    if sys.platform == 'darwin':
      
        myChecksum = htons(myChecksum) & 0xffff 
    else:
        myChecksum = htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1) 
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1)) 
   
def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
   
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF #
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close() 
    return delay



def ping(host, timeout=1):

    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")

        delay = doOnePing(dest, timeout) 
        print(delay)
        time.sleep(1)
    return delay

ping("www.google.com")
