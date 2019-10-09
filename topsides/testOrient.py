import orient_API as API
import keyboard
import time

if __name__ == '__main__':

    while 1:
        get_key = input("Enter directin: ")
        if(get_key == 'w'):
            API.sway(0.2)
        if(get_key == 'z'):
            API.sway(0)
        time.sleep(1)
