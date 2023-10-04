import socket

PORT = 5050
#HOST = "172.19.254.109"
HOST = socket.gethostbyname(socket.gethostname()) #dynamically gets the ip address of the server
DISCONNECT_MESSAGE = "quit()" 

# binding socket to port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

def parse_message(msg):
    parts = msg.split('_') # since message is guaranteed to be in the format #"D_leftWheel1_rightWheel1_leftWheel2_rightWheel2_leftWheel3_rightWheel3" or “A_shoulder_wristright_wristleft_claw_gantry_spin_cam1x_cam1y_cam2x_cam2y”
    if parts[0] == "D":
        return {
            "Drive_Command": {
                "left_wheel1": parts[1],
                "left_wheel2": parts[2],
                "left_wheel3": parts[3],
                "right_wheel1": parts[4],
                "right_wheel2": parts[5],
                "right_wheel3": parts[6]
            }
        }

    elif parts[0] == "A":
        return {
            "Arm_Command": {
                "shoulder": parts[1],
                "wrist_right": parts[2],
                "wrist_left": parts[3],
                "claw": parts[4],
                "gantry": parts[5],
                "spin": parts[6]
            },
            "Camera_position": {
                "cam1x": parts[7],
                "cam1y": parts[8],
                "cam2x": parts[9],
                "cam2y": parts[10]
            }
        }
    else:
        return {"Error": "Invalid message type"}

def start():
    server_socket.listen() 
    print(f"[LISTENING] Server is listening on {HOST}")
    while True:
        communication_socket, addr_client = server_socket.accept()
        print(f"[NEW CONNECTION] {addr_client} connected.")
        
        while True:
            message = communication_socket.recv(1024).decode("utf-8")        
            if not message:
                break
            print(parse_message(message))
            communication_socket.send("Message received".encode("utf-8"))
    #communication_socket.close()
    #print(f"[DISCONNECTED] {addr_client} disconnected.")

print("[STARTING] server is starting...")
start()