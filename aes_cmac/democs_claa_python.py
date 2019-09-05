import ctypes
import socket
import threading
from time import ctime,sleep

cmdseq=0
py_appeui=''
py_appkey=''
py_appnonce=''
challenge=''
ip=''
port=0
NoError = True

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def get_challenge():
    global py_appeui
    py_appeui = input("input the appeui:")
    print(py_appeui)
    appeui=ctypes.c_char_p(py_appeui.encode('utf-8'))
    global py_appkey
    py_appkey = input("input the appkey:")
    print(py_appkey)
    appkey=ctypes.c_char_p(py_appkey.encode('utf-8'))
    
    global py_appnonce
    py_appnonce = input("input the appnonce:")
    print(py_appnonce)
    appnonce=long(py_appnonce)

    ll=ctypes.cdll.LoadLibrary
    lib = ll("./libchallenge.so")

    p=ctypes.create_string_buffer(32)

    lib.get_challenge(appkey,appeui,appnonce,p)
    challenge = p.raw
    print (challenge)
    return challenge

def get_ip_port():
    global ip
    ip = input("input the ip:")
    global port
    port = int(input("intput the port:"))

def start_connect_service(ip,port):
    global NoError
    global client
    try:
	print("*********************")
	print(ip)
	print(port)
	print("*********************")
        client.connect((ip,port))
	print("connect ok")
    except Exception as e:
	NoError = False    

def recv_data_from_service():
    global NoError
    while NoError:
	try:
            data = client.recv(1024)
            print(data.decode("utf8"))
	except Exception as e:
            NoError = False
	    print('Error',e)
	finally:
	    print("");

def start_send(sendString):
    global NoError
    try:
        length = (len(sendString) + 1) & 0xFFFF
        hValue = length >> 8
        lValue = length & 0xFF
        datahead = bytearray()
	datahead.append('\n')
	datahead.append(1)
	datahead.append(2) 
	datahead.append(hValue)
	datahead.append(lValue)
	data = datahead.decode() + sendString + "\0";
#for i in data:
#    print('%#x'%ord(i))
	client.send(data)

	recv_data_from_service()
        #
    except Exception as e:
        NoError = False
	print('chen-Error',e)
    finally:
            print('finally...')

def getcmdseq():
    global cmdseq
    cmdseq += 2
    return cmdseq

def join_service():
    print("^^^^^^^^^^^^^^^^^^^^^")
    joindata = '{\"cmd\":\"join\",\"cmdseq\":%d,\"appeui\":\"%s\",\"appnonce\":%d,\"challenge\":\"%s\"}' % (getcmdseq(), py_appeui,long(py_appnonce),challenge)
    start_send(joindata)
    print("^^^^^^^^^^^^^^^^^^^^^")

def send_heart_ack():
    print("^^^^^^^^^^^^^^^^^^^^^")
    heartack = '{\"cmd\":\"heartbeat_ack\"}'
    start_send(heartack)
    print("^^^^^^^^^^^^^^^^^^^^^")
    



def main():
    global ip
    global port
    try:
	print("======================")
        get_ip_port()
	print(ip)
	print(port)
	print("======================\r\n")

	global challenge
        challenge = get_challenge()
	print("======================")
        print(py_appeui)
        print(py_appkey)
        print(py_appnonce)
        print(challenge)
	print("======================\r\n")

	print("begin connect")
        start_connect_service(ip,port)	
	join_service()
	
	#recvthread.join()
	#sendthread.join()
    except Exception as e:
	print("**********************")
        print('Error:', e)
	print("**********************")
    finally:
        print('release the socket')

main()
