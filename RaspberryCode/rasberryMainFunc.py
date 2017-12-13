from sense_hat import SenseHat
from time import gmtime, strftime
sense = SenseHat()

############ Joystick listner##########
from time import sleep

while True:
    t = strftime("%H:%M", gmtime())
    message = 'Time:' + t

    sense.show_message(message, scroll_speed=(0.08), text_colour=[176, 224, 230], back_colour=[0, 0, 0])
    sense.clear()

    temp = sense.get_temperature()
    message = 'Temp: %.2f ' % (temp)

    sense.show_message(message, scroll_speed=(0.08), text_colour=[200, 0, 200], back_colour=[0, 0, 0])
    sense.clear()

    #TODO wait a bit to check for the
    for event in sense.stick.get_events():
        message = 'Joystick got move'
        sense.show_message(message, scroll_speed=(0.08), text_colour=[176, 224, 230], back_colour=[0, 0, 0])
        print("The joystick was {} {}".format(event.action, event.direction))

# PUSH - send to server the direction and the local temp
#


