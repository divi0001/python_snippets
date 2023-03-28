from logging import exception
from operator import is_
import struct
import binascii
from sys import argv
from urllib import response
import lossy_UDP_socket as socket



def main():
    # read parameters
    if len(argv) != 3:
        print(f'Usage: {argv[0]} [<hostname> [<port>]]\n')
        
    hostname: str = argv[1] if len(argv) > 1 else 'localhost'
    port: int = int(argv[2]) if len(argv) > 2 else 64000
    
    addr = (hostname, port)
     
    
    # read in data
    data = bytearray()
    while True:
        line = input()
        if not line:
            # line is empty
            break
        line_data = bytes.fromhex(line)
        data += line_data
    daList = []
    ii = 1
    for da in range(len(data)//7):
        
        daList += [data[ii:ii+7]]
        ii = ii+7
    #print(daList)
    #print(data)
    
    bit = 1
    #socket try-with-ressources
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        
        for h in daList:
            
            
            try:
                
                d = build_message(bit,h)
                sock.sendto(d,addr) 
                
                response = sock.recv(128)
                #print(d)
                if is_ack(bit,response):
                    
                    bit = flipI(bit)
                
                else:
                    j = 0
                    while j < 32:
                        try:
                            
                            sock.settimeout(0.1)
                            sock.sendto(d,addr)
                            resp = sock.recv(128)
                            if is_ack(bit,resp):
                                j = 33
                                
                        
                        except socket.timeout:
                            #print("timeout")
                            j += 1           
                
            
            except socket.timeout:
                j = 0
                while j < 32:
                        try:
                            
                            sock.settimeout(0.1)
                            sock.sendto(d,addr)
                            resp = sock.recv(128)
                            #print("nak-ed")
                            if is_ack(bit,resp):
    
                                break
                        
                        except socket.timeout:
                            #print("timeout")
                            j += 1           
            
            # TODO: implement the rdt3.0 logic.
            # remember to set a timeout and to handle the timeout exception
        bit = flipI(bit)
        finalsend = struct.pack('<I',0)
        finalcountdown = build_message(bit,finalsend)
        
        while True:
            try:
                
                sock.sendto(finalcountdown,addr)
                sock.settimeout(0.1)
                recPckg = sock.recv(128)
                if is_ack(bit,recPckg):
                    break
            except:
                pass
        
def flipI(bit):
    if bit == 0:
        return 1
    else:
        return 0
    
def build_message(sequence_number: int, body : bytes) -> bytes:
      
    
    back = struct.pack('<II8s', sequence_number, 0x6E634E43, body)
    bin_asc = binascii.crc32(back)
    msg = struct.pack('<II8s', sequence_number, bin_asc, body)
    return msg

def is_ack(expected_sequence_number: int, acknowledgement: bytes) -> bool:
    
    ack_chk = struct.unpack('<II',acknowledgement)
    if expected_sequence_number == ack_chk[0]:
        ch = struct.pack('<II', expected_sequence_number, 0x6E634E43)
        ch1 = binascii.crc32(ch)
        if ch1 == ack_chk[1]:
            return True
        else:
            return False
    else:
        return False
    
if __name__ == '__main__':
    main()