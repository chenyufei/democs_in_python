import ctypes
import socket

CmdSeq=0

py_appeui = raw_input("input the appeui:")
print(py_appeui)
appeui=ctypes.c_char_p(py_appeui.encode('utf-8'))

py_appkey = raw_input("input the appkey:")
print(py_appkey)
appkey=ctypes.c_char_p(py_appkey.encode('utf-8'))

py_appnonce = raw_input("input the appnonce:")
print(py_appnonce)
appnonce=long(py_appnonce)

ll=ctypes.cdll.LoadLibrary
lib = ll("./libchallenge.so")

p=ctypes.create_string_buffer(32)

lib.get_challenge(appkey,appeui,appnonce,p);
challenge = p.raw
print (challenge)


def StartSend(sendString):
	try
		int length = (sendString.Length + 1) & 0xFFFF
		byte[] senddata = new byte[length + 5]

		int hValue = length >> 8
		int lValue = length & 0xFF
		byte[] arr = new byte[] { (byte)'\n', (byte)1, (byte)2, (byte)hValue, (byte)lValue }
		arr.CopyTo(senddata, 0)

		byte[] str = UTF8Encoding.UTF8.GetBytes(sendString)
		Buffer.BlockCopy(str, 0, senddata, 5, sendString.Length)

		senddata[sendString.Length + 5] = UTF8Encoding.UTF8.GetBytes("\0")[0]
		if(m_nkStream.CanWrite)
			m_nkStream.Write(senddata, 0, senddata.Length)
			return true
		else
			return false
	catch (Exception)
		return false

def getCmdSeq():
	return CmdSeq += CmdSeq + 2

