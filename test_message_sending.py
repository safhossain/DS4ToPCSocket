import socket
import random

PORT = 5050 #random port not being used
HOST = "172.19.254.109" 
#HOST = socket.gethostbyname(socket.gethostname()) #dynamically gets the ip address of the server

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def send(msg):
    message = msg.encode("utf-8") #gotta encode message before sending that shii    
    client_socket.send(message)

# PWM values for the rover movement motors (range 0-255, neutral = 127 or 128)
    # leftWheelX: Turns the respective left wheel clockwise and counterclockwise
#assigning random PWM values in 0-255 range for testing purposes
leftWheelX_pwm_val = random.randint(0, 255)
leftWheel1 = leftWheelX_pwm_val
leftWheel2 = leftWheelX_pwm_val
leftWheel3 = leftWheelX_pwm_val
    # rightWheelX: Turns the respective right wheel clockwise and counterclockwise
rightWheelX_pwm_val = random.randint(0, 255)
rightWheel1 = rightWheelX_pwm_val
rightWheel2 = rightWheelX_pwm_val
rightWheel3 = rightWheelX_pwm_val

# PWM values for the arm motors (range 0-255)
shoulder = random.randint(0, 255) # Moves up and down
wristright = random.randint(0, 255) # Controls the right motor of the diff joint
wristleft = random.randint(0, 255) # Controls the left motor of the diff joint
claw = random.randint(0, 255) # Open value > 127 and close value < 127
gantry = random.randint(0, 255) # Moves the entire arm up and down; Up value > 127 and down value < 127
spin = random.randint(0, 255) # Spins the entire arm  360 degrees vertically

#camx: #neutral 90, range 0-180
cam1x = random.randint(0, 180)
cam1y = random.randint(0, 180)
cam2x = random.randint(0, 180)
cam2y = random.randint(0, 180)

string_to_send = str()

wheels_or_arm = random.randint(0, 1) # 0 for wheels, 1 for arm
if wheels_or_arm == 0:
    string_to_send=f"D_{leftWheel1}_{leftWheel2}_{leftWheel3}_{rightWheel1}_{rightWheel2}_{rightWheel3}"
else:
    string_to_send=f"A_{shoulder}_{wristright}_{wristleft}_{claw}_{gantry}_{spin}_{cam1x}_{cam1y}_{cam2x}_{cam2y}"

send(string_to_send)
print(client_socket.recv(1024).decode("utf-8"))