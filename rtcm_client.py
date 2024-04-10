import socket
import base64

SERVER_HOST = 'geortk.jp'
SERVER_PORT = 2101
#MOUNT_POINT = 'lm_siddique0'
MOUNT_POINT = 'kfarm'
#OUNT_POINT = 'kaname'

#SERVER_HOST = 'rtk2go.com'
#SERVER_PORT = 2104
#MOUNT_POINT = 'AKASAKI-JF'
#MOUNT_POINT = "Sonnano_Naiyo"

#SERVER_HOST = 'rtk2go.com'
#SERVER_PORT = 2104
#MOUNT_POINT = "KOIL_FACTORY_PRO"

#SERVER_HOST = 'rtk2go.com'
#SERVER_PORT = 2101
#MOUNT_POINT = 'ACACU'

AGENT_NAME  = 'test agent/0.1'
USER_EMAIL  = base64.b64encode("Tomonobu.Saito@sony.com:password".encode('utf-8')).decode('utf-8')

BUFFER_SIZE = 1024

# protocol
rev = 2      # 1 or 2
auth = True # Trune or False

try:
    # Connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    print(f"RTK Connected: {SERVER_HOST}:{SERVER_PORT}/{MOUNT_POINT}")
    print(f"RTK protocol : rev {rev} / auth {auth}")
    print(f"email(base64): {USER_EMAIL}")

    # Send HTTP request
    if 2 == rev:
        if True == auth:
            header = (f"GET /{MOUNT_POINT} HTTP/1.1\r\n"
                      f"Host: {SERVER_HOST}:{SERVER_PORT}\r\n"
                      f"Ntrip-Version: Ntrip/2.0\r\n"
                      f"User-Agent: NTRIP {AGENT_NAME}\r\n"
                      f"Authorization: Basic {USER_EMAIL}\r\n"
                      f"Accept: */*\r\n"
                      f"Connection: close\r\n\r\n")
        else:
            header = (f"GET /{MOUNT_POINT} HTTP/1.1\r\n"
                      f"Host: {SERVER_HOST}:{SERVER_PORT}\r\n"
                      f"Ntrip-Version: Ntrip/2.0\r\n"
                      f"User-Agent: NTRIP {AGENT_NAME}\r\n"
                      f"Accept: */*\r\n"
                      f"Connection: close\r\n\r\n")
    else:
        if True == auth:
            header = (f"GET /{MOUNT_POINT} HTTP/1.0\r\n"
                      f"User-Agent: NTRIP {AGENT_NAME}\r\n"
                      f"Authorization: Basic {USER_EMAIL}\r\n"
                      f"Accept: */*\r\n"
                      f"Connection: close\r\n\r\n")
        else:
            header = (f"GET /{MOUNT_POINT} HTTP/1.0\r\n"
                      f"User-Agent: NTRIP {AGENT_NAME}\r\n"
                      f"Accept: */*\r\n"
                      f"Connection: close\r\n\r\n")
            
    sock.send(header.encode('utf-8'))
    #socket.send(header.encode('ascii'))
    
    # Receive response
    response = sock.recv(BUFFER_SIZE).decode('utf-8').strip()
    print(f"Response: {response}")  # Should be "ICY 200 OK"

    # Continuously receive data
    while True:
        buf = sock.recv(BUFFER_SIZE)
        if not buf:
            break

        # Process received data (base64 encoding as per Java code)
        encoded_data = base64.b64encode(buf).decode('utf-8')
        print("----------")
        print(f"BASE64: {encoded_data}")
        print("----------")
        print(f"RAW: {buf}")
    
    print("==========")
    print(f"Header: {header}")  # Should be "ICY 200 OK"
    
    print("==========")
    print(f"Response: {response}")  # Should be "ICY 200 OK"

except Exception as e:
    print(f"TCP Thread stop: {e}")
finally:
    sock.close()
