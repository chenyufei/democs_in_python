import Info
import json
import deal_socket
import calculate_challenge
import sys

def main():

	if len(sys.argv) < 5:
		print('python %s ip port appeui appkey' % (sys.argv[0]))
		print('example: python %s 127.0.0.1 3003 ffffffffffffffff 00112233445566778899aabbccddeeff' % (sys.argv[0]))
		return

	try:
		ip = sys.argv[1]
		port = int(sys.argv[2])
		appeui = sys.argv[3]
		appkey = sys.argv[4]
		'''
		print("======================")
		ip = Info.get_ip()
		port = Info.get_port()
		appeui = Info.get_appeui()
		appkey = Info.get_appkey()
		print("======================")
		
		print("**********************")
		print(ip)
		print(port)
		print(appeui)
		print(appkey)
		print("**********************")
		'''
		deal_socket.start_join_service(ip, port, appeui, appkey)

	except Exception as e:
		print('Error', e)
	finally:
		print("close the socket")
main()
