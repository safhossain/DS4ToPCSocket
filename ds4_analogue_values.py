import pygame
import json
import math

# leftwheel X + rightwheel X : left joystick
# Shoulder
# Wrist Right
# Wrist Left
# Claw: Open value > 127 and close value < 127: 
# Gantry: Moves the entire arm up and down Up value > 127 and down value < 127. probably okay just to use d-pad up/down
# Spin: Spins the entire arm 360 degrees vertically : analogue left/right L2/R2
# cam1x: Camera tile Neutral 90 range 180
# cam1y: Camera tile Neutral 90 range 180
# cam2x: Camera tile Neutral 90 range 180
# cam2y: Camera tile Neutral 90 range 180

def map_analogue_to_PWM(x_axis, y_axis):
    # first scale {-1, ..., +1} belongs to "real numbers" (kinda)
    # second scale {0, ..., 255} belongs to integers
    # we can approximate this mapping with the function floor[f(a)] = floor[127.5*a + 127.5] where a is the analogue value
    def scale_analogue_to_PWM(analogue_value):
        return int(127.5 * analogue_value + 127.5)
    
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

pygame.init()
pygame.joystick.init()

with open('ds4_button_mapping.json', 'r') as file:
    button_mappings = json.load(file)

# minimum threshold in joystick analogue values to be considered as a movement
X_AXIS_THRESHOLD = 0.13 # actual: 0.12939453125
Y_AXIS_THRESHOLD = 0.08 # actual: 0.074493408203125
Z_AXIS_THRESHOLD = 0.05 # actual: 0.027435302734375

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
        for button_name, button_index in button_mappings.items():
            if joystick.get_button(button_index):
                print(button_name)
        x_axis = joystick.get_axis(0)
        y_axis = joystick.get_axis(1)
        z_axis = joystick.get_axis(2)
        
        if (abs(x_axis) > X_AXIS_THRESHOLD) or (abs(y_axis) > Y_AXIS_THRESHOLD):
            print(f"({x_axis if abs(x_axis) > X_AXIS_THRESHOLD else 0}," f"{y_axis if abs(y_axis) > Y_AXIS_THRESHOLD else 0})")
            PWM_left, PWM_right = map_analogue_to_PWM(x_axis, y_axis)
            print(f"PWM_left: {PWM_left}, PWM_right: {PWM_right}")
        if abs(z_axis) > Z_AXIS_THRESHOLD:
            print(f"z_axis: {z_axis}")
            
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