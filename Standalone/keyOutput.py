#!/usr/bin/env python3
import time

# import GPIOSimulator as GPIO
import  RPi.GPIO as GPIO
import time

NULL_CHAR = chr(0)
pressed = False;


GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN,pull_up_down=GPIO.PUD_UP)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())


def null_report():
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write((NULL_CHAR*8).encode())


testMessage=['windows','s','s','h',' ','r','a','s','p','b','e','r','r','y','p','i','.','l','o','c','a','l','return']


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



#        match key:
#            case 'windows':
#                output.append(chr(227)+NULL_CHAR*7)
#            case ' ':
#                output.append(NULL_CHAR*2+chr(44)+NULL_CHAR*5)
#            case '.':
#                output.append(NULL_CHAR*2+chr(55)+NULL_CHAR*5)
#            case 'return':
#                output.append(NULL_CHAR*2+chr(40)+NULL_CHAR*5)
#            case _:
#                output.append(NULL_CHAR*2+chr(ord(key) - 93)+NULL_CHAR*5)
#        output.append(NULL_CHAR*8)


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









while True:
#    inputValue = GPIO.input(26)
#    if (inputValue == True):
#        write_report(NULL_CHAR * 8)
#        pressed = False
#    else:
#        if not pressed:
#            for command in commandToOutput(testMessage):
#                if command == NULL_CHAR*2+chr(40)+NULL_CHAR*5:
#                    time.sleep(1)
#
#                write_report(command)
#                print(command)
#
#                if command == chr(8)+NULL_CHAR*7:
#                    time.sleep(1)
#        pressed= True
#   
#    time.sleep(0.1)
    macroButton(26,testMessage)
    time.sleep(0.1)

