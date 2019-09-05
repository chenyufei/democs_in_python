import socket
import threading
import json
import time
import Info
import calculate_challenge

global_appeui = ''
global_appkey = ''
global_ip = ''
global_port = 0

cmdseq=0
NoError = True
iRecvHeartBeatNumber = 0
NoExit = True

client = object() #socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def timeout():
    global  timer
    global iRecvHeartBeatNumber
    global NoExit
    print("heartbeatnumber="+iRecvHeartBeatNumber)
    iRecvHeartBeatNumber = iRecvHeartBeatNumber + 1
    if NoExit:
        if iRecvHeartBeatNumber >= 3:
            disconnect_service()
            start_join_service(global_ip, global_port, global_appeui, global_appkey)
        else:
            start_heart_watch()

timer = object()

def start_heart_watch():
    print("start_heart_watch")
    global timer
    timer = threading.Timer(60 + 10, timeout)
    timer.start()

def stop_heart_watch():
    print("stop_heart_watch")
    global timer, iRecvHeartBeatNumber
    iRecvHeartBeatNumber = 0
    if type(timer) != type(object()):
        timer.cancel()

def start_connect_service(ip, port):
    print("start_connect_service")
    global NoError, client
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
    except Exception as e:
        NoError = False
        print('start connect error',e)

def disconnect_service():
    global  client
    client.close()

def  deal_cmd(jdict):
    cmd = jdict["cmd"]
    print("cmd=" + cmd)
    if "join_ack" == cmd:
        stop_heart_watch()
        start_heart_watch()
    elif "updata" == cmd:
        stop_heart_watch()
        start_heart_watch()
    elif "forced_quit" == cmd or "quit_ack" == cmd:
        stop_heart_watch()
        disconnect_service()
        start_join_service(global_ip, global_port, global_appeui, global_appkey)
    elif "heartbeat" == cmd:
        stop_heart_watch()
        send_heart_ack()
        start_heart_watch()
    else:
        print(jdict)

def parse_recv_data(data):
    global iRecvHeartBeatNumber
    jdict = object()
    try:
        data = data.decode('utf-8')
        jdict = json.loads(data)
    except Exception as e:
        print("parse json fail")
        print('Error', e)
        return
    deal_cmd(jdict)


def recv_data_from_service():
    global NoError, client
    while NoError:
        try:
            data = client.recv(1024)
            data = data[5:len(data)-1] #5:delete the message head; len(data)-1: to delete the last 0x00
            print(data)
            parse_recv_data(data)
        except Exception as e:
            NoError = False
            print('Error', e)
        finally:
            if NoError:
                print("recv success")
            else:
                client.close()
                start_join_service(global_ip, global_port, global_appeui, global_appkey)

def start_send(sendString):
    global NoError, client
    print(sendString)
    try:
        length = (len(sendString) + 1) & 0xFFFF
        hvalue = length >> 8
        lvalue = length & 0xFF
        datahead = bytearray()
        datahead.append(0x0a)
        datahead.append(1)
        datahead.append(2)
        datahead.append(hvalue)
        datahead.append(lvalue)
        data = datahead.decode() + sendString + "\0"
        # for i in data:
        #    print('%#x'%ord(i))
        client.send(data.encode())
    except Exception as e:
        NoError = False
        print('start_send-Error', e)
    finally:
        if not NoError:
            client.close()


def getcmdseq():
    global cmdseq
    cmdseq += 2
    return cmdseq

def start_join_service(ip, port, appeui, appkey):
    global global_appeui
    global global_appkey
    global global_ip
    global global_port
    global NoError
    global iRecvHeartBeatNumber

    global_appeui = appeui
    global_appkey = appkey
    global_ip = ip
    global_port = port
    NoError = True
    iRecvHeartBeatNumber = 0
    print("###############################")
    print(ip)
    print(port)
    print(appeui)
    print(appkey)
    print("###############################")
    try:
        start_connect_service(ip, port)
        join_service(appeui, appkey)
        start_recv_thread()
    except Exception as e:
        NoError = False
        print('Error', e)
    finally:
        if NoError:
            print("success")
        else:
            global  client
            client.close()
            print("error,so close socket")
            time.sleep(100)
            start_join_service(global_ip, global_port, global_appeui, global_appkey)

def join_service(appeui, appkey):
    print("======================")
    appnonce = Info.get_appnonce()
    #appnonce = 1537598872
    challenge = calculate_challenge.get_challenge(appeui,appkey,appnonce)
    joindata = '{\"cmd\":\"join\",\"cmdseq\":%d,\"appeui\":\"%s\",\"appnonce\":%d,\"challenge\":\"%s\"}' % (getcmdseq(), appeui, appnonce, challenge)
    start_send(joindata)
    print("======================")


def send_heart_ack():
    print("**********************")
    heartack = '{\"cmd\":\"heartbeat_ack\"}'
    start_send(heartack)
    print("**********************")


def recv_thread_func():
    recv_data_from_service()

def start_recv_thread():
    recvthread = threading.Thread(target=recv_thread_func)
    recvthread.setDaemon(True)
    recvthread.start()
    recvthread.join()
