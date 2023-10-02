import socket

PORT = 5050
HOST = "172.19.254.109"
#HOST = socket.gethostbyname(socket.gethostname()) #dynamically gets the ip address of the server
DISCONNECT_MESSAGE = "quit()" 

# binding socket to port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

def start():
    server_socket.listen() 
    print(f"[LISTENING] Server is listening on {HOST}")
    while True:
        communication_socket, addr_client = server_socket.accept()
        print(f"[NEW CONNECTION] {addr_client} connected.")
        message = communication_socket.recv(1024).decode("utf-8")
        print(f"Message received from client: {message}")
        communication_socket.send("Message received".encode("utf-8"))
        communication_socket.close()
        print(f"[DISCONNECTED] {addr_client} disconnected.")

print("[STARTING] server is starting...")
start()