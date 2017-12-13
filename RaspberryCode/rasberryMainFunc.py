from time import gmtime, strftime
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

x=3

def pushed_left(event):
    global x
    if event.action != ACTION_RELEASED:
        print('LEFT')

def pushed_right(event):
    global x
    if event.action != ACTION_RELEASED:
        print('RIGHT')

sense = SenseHat()

############ Joystick listner##########
sense.stick.direction_left = pushed_left
sense.stick.direction_right = pushed_right

while True:
    t = strftime("%H:%M", gmtime())
    message = 'Time:' + t

    sense.show_message(message, scroll_speed=(0.08), text_colour=[176, 224, 230], back_colour=[0, 0, 0])
    sense.clear()

    temp = sense.get_temperature()
    message = 'Temp: %.2f ' % (temp)

    sense.show_message(message, scroll_speed=(0.08), text_colour=[200, 0, 200], back_colour=[0, 0, 0])
    sense.clear()





