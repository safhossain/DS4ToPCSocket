import pygame
import json
import math
import socket

PORT = 5050
#HOST = "172.19.254.109"
HOST = socket.gethostbyname(socket.gethostname())
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #UNCOMMENT
client_socket.connect((HOST, PORT)) #UNCOMMENT

def send(msg):
    message = msg.encode("utf-8") #gotta encode message before sending that shii    
    client_socket.send(message)

# leftwheel X + rightwheel X : [x and y axis]
# Shoulder [z-axis]
# Wrist Right [d-pad right]
# Wrist Left [d-pad left]
# Claw: Open value > 127 [cross] and close value < 127 [circle]
# Gantry: Moves the entire arm up and down Up value > 127 and down value < 127. probably okay just to use [d-pad up/down]
# Spin: Spins the entire arm 360 degrees vertically : analogue left/right [L2/R2]
# cam1x: Camera tile Neutral 90 range 180
# cam1y: Camera tile Neutral 90 range 180
# cam2x: Camera tile Neutral 90 range 180
# cam2y: Camera tile Neutral 90 range 180

def scale_analogue_to_PWM(analogue_value):
        return int(127.5 * analogue_value + 127.5)

def map_x_and_y_analogue_to_PWM_wheels(x_axis, y_axis):
    # first scale {-1, ..., +1} belongs to "real numbers" (kinda)
    # second scale {0, ..., 255} belongs to integers
    # we can approximate this mapping with the function floor[f(a)] = floor[127.5*a + 127.5] where a is the analogue value
    #forward_or_backward = 1 if y_axis > Y_AXIS_THRESHOLD else -1 #<--- yee this is bullshit
    if x_axis > X_AXIS_THRESHOLD: # turn right, so left wheel goes forward, right wheel stays still
        # unfortunately, the joystick calibration is not perfect. so it is possible for math.sqrt(x_axis**2 + y_axis**2) > 1
        # this will result in PWM values > 255
        PWM_left = scale_analogue_to_PWM(math.sqrt(x_axis**2 + y_axis**2))
        PWM_right = 127
    elif x_axis < -X_AXIS_THRESHOLD: # turn left, so right wheel goes forward, left wheel stays still
        PWM_left = 127
        PWM_right = scale_analogue_to_PWM(math.sqrt(x_axis**2 + y_axis**2))
    else: # go straight
        PWM_left = scale_analogue_to_PWM(y_axis)
        PWM_right = scale_analogue_to_PWM(y_axis)
    return PWM_left, PWM_right

def map_to_PWM_arms(L2_anal, R2_anal, z_axis, cross_state, circle_state, d_pad_up_state, d_pad_down_state, d_pad_right_state, d_pad_left_state):
    PWM_wrist_right = 255 if d_pad_right_state else 0
    PWM_wrist_left = 255 if d_pad_left_state else 0
    PWM_claw = 255 if cross_state else (0 if circle_state else 127)
    PWM_gantry = 255 if d_pad_up_state else (0 if d_pad_down_state else 127)
    PWM_shoulder = scale_analogue_to_PWM(z_axis) #this is probably not right
    PWM_spin = scale_analogue_to_PWM(L2_anal - R2_anal) #this is also probably not right
    return PWM_shoulder, PWM_wrist_right, PWM_wrist_left, PWM_claw, PWM_gantry, PWM_spin, 90, 90, 90, 90 # the spin values are definitely not right


pygame.init()
pygame.joystick.init()

with open('ds4_button_mapping.json', 'r') as file:
    button_mappings = json.load(file)

# minimum threshold in joystick analogue values to be considered as a movement
X_AXIS_THRESHOLD = 0.13 # actual: 0.12939453125
Y_AXIS_THRESHOLD = 0.08 # actual: 0.074493408203125
Z_AXIS_THRESHOLD = 0.05 # actual: 0.027435302734375
L2_AXIS_THRESHOLD = -0.05 #
R2_AXIS_THRESHOLD = -0.05 #

# window
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
screen =  pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Testing DS4 Events")

# clock for game frame rate
clock = pygame.time.Clock()
FPS = 60

joysticks = []

# GAME LOOP
running = True
while running:
    clock.tick(FPS)

    for joystick in joysticks:
        # for button_name, button_index in button_mappings.items():
        #     if joystick.get_button(button_index):
        #         print(button_name)

        x_axis = joystick.get_axis(0)
        y_axis = joystick.get_axis(1)
        z_axis = joystick.get_axis(2)
        L2_axis = joystick.get_axis(4)
        R2_axis = joystick.get_axis(5)
        
        
        if (abs(x_axis) > X_AXIS_THRESHOLD) or (abs(y_axis) > Y_AXIS_THRESHOLD):
            #print(f"({x_axis if abs(x_axis) > X_AXIS_THRESHOLD else 0}," f"{y_axis if abs(y_axis) > Y_AXIS_THRESHOLD else 0})")            
            PWM_left, PWM_right = map_x_and_y_analogue_to_PWM_wheels(x_axis, y_axis)
            print(f"PWM_left: {PWM_left}, PWM_right: {PWM_right}")
            send(f"D_{PWM_left}_{PWM_left}_{PWM_left}_{PWM_right}_{PWM_right}_{PWM_right}")  #UNCOMMENT
       
        if abs(z_axis) > Z_AXIS_THRESHOLD or L2_axis > L2_AXIS_THRESHOLD or R2_axis > R2_AXIS_THRESHOLD or joystick.get_button(0) or joystick.get_button(1) or joystick.get_button(11) or joystick.get_button(12) or joystick.get_button(13) or joystick.get_button(14):
            PWM_shoulder, PWM_wrist_right, PWM_wrist_left, PWM_claw, PWM_gantry, PWM_spin, cam1x, cam1y, cam2x, cam2y = map_to_PWM_arms(L2_axis, R2_axis, z_axis, joystick.get_button(0), joystick.get_button(1), joystick.get_button(11), joystick.get_button(12), joystick.get_button(14), joystick.get_button(13))
            print(f"PWM_shoulder: {PWM_shoulder}, PWM_wrist_right: {PWM_wrist_right}, PWM_wrist_left: {PWM_wrist_left}, PWM_claw: {PWM_claw}, PWM_gantry: {PWM_gantry}, PWM_spin: {PWM_spin}, cam1x: {cam1x}, cam1y: {cam1y}, cam2x: {cam2x}, cam2y: {cam2y}")
            send(f"A_{PWM_shoulder}_{PWM_wrist_right}_{PWM_wrist_left}_{PWM_claw}_{PWM_gantry}_{PWM_spin}_{cam1x}_{cam1y}_{cam2x}_{cam2y}") #UNCOMMENT        

    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            print(event)
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joy)
            print(joy.get_name())
            print(joy.get_numaxes())
            print(joy.get_power_level())
        if event.type == pygame.QUIT:
            running = False