
#!/usr/bin/env python3
import time

# import GPIOSimulator as GPIO
import  RPi.GPIO as GPIO
import time

NULL_CHAR = chr(0)

GPIO.setmode(GPIO.BCM)


def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def null_report():
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write((NULL_CHAR*8).encode())

def pinSetup(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)

def commandToOutput(inputList):
    output=[]
    for key in inputList:

        if key == 'windows':
            output.append(chr(8)+NULL_CHAR*7)
        elif key == ' ':
            output.append(NULL_CHAR*2+chr(44)+NULL_CHAR*5)
        elif key == '.':
            output.append(NULL_CHAR*2+chr(55)+NULL_CHAR*5)
        elif key == 'return':
            output.append(NULL_CHAR*2+chr(40)+NULL_CHAR*5)
        else:
            output.append(NULL_CHAR*2+chr(ord(key) - 93)+NULL_CHAR*5)
        output.append(NULL_CHAR*8)
    return output

def macroButton(pin, strokeOrder):
    inputValue = GPIO.input(pin)
    pressed = False

    if (inputValue == True):
        write_report(NULL_CHAR * 8)
        pressed = False

    else:
        if not pressed:
            for command in commandToOutput(strokeOrder):
                if command == NULL_CHAR*2+chr(40)+NULL_CHAR*5:
                    time.sleep(1)

                write_report(command)

                if command == chr(8)+NULL_CHAR*7:
                    null_report()
                    time.sleep(1)
        pressed= True