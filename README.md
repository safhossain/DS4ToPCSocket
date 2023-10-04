To run:
1. Plug in a DualShock4 Playstation Controller and plug to USB.
2. Have two instances of the terminal of your choice open.
3. Run `receiver.py`. This is the "host" of the server and will be "listening" after it's run indefinitely. Unfortunately it doesn't quit gracefuly unless interupprted externally either by closing the terminal or occasionally a ctrl+C
4. Run `ds4_values.py`. This will open a pygame window which will be a black 400x400 screen. You have click on this window for the DS4 values to be registered to the program.
5. Play around with the DS4 buttons and analogue sticks/triggers. 
a) The terminal instance running `ds4_values.py` will be printing out debugging info but will send the correct format to the reciever file.
b) the terminal instance running  `receiver.py` will be printing out the PWM values for either rover movement or arm movement commands in the correct format
