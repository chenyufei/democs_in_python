import ctypes
def get_challenge(appeui, appkey, appnonce):
    appeui = ctypes.c_char_p(appeui.encode('utf-8'))
    appkey = ctypes.c_char_p(appkey.encode('utf-8'))
    ll = ctypes.cdll.LoadLibrary
    lib = ll("./libchallenge.so")

    p = ctypes.create_string_buffer(32)
    lib.get_challenge(appkey, appeui, appnonce, p)
    challenge = p.raw
    print(challenge)
    return challenge.decode('utf-8')

