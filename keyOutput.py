
#!/usr/bin/env python3
from os import write
import time

# import GPIOSimulator as GPIO
import  RPi.GPIO as GPIO
import time

NULL_CHAR = chr(0)

GPIO.setmode(GPIO.BCM)

RMETA=128
RALT=64
RSHIFT=32
RCTRL=16
LMETA=8
LALT=4
LSHIFT=2
LCTRL=1





def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def null_report():
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write((NULL_CHAR*8).encode())

def pinSetup(pins):
    for category in pins:
        for pin in category:
            GPIO.setup(pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)






def commandToOutput(inputList):
    output=[]
    print(inputList)
    
    for keys in inputList:
        temp=''
        keyCount=0
        modifierKeys = 0
        for key in keys:
            if key == 'rmeta':
                modifierKeys += RMETA
            elif key == '`ralt':
                modifierKeys += RALT
            elif key == 'rshift':
                modifierKeys += RSHIFT
            elif key == 'rctrl':
                modifierKeys += RCTRL
            elif key == 'lmeta' or key == 'windows':
                modifierKeys += LMETA
            elif key == 'lalt':
                modifierKeys += LALT
            elif key == 'lshift':
                modifierKeys += LSHIFT
            elif key == 'lctrl':
                modifierKeys += LCTRL
            elif key == ' ':
                temp += chr(44)
                keyCount += 1
            elif key == '.':
                temp += chr(55)
                keyCount += 1
            elif key == 'return':
                temp+=chr(40)
                keyCount += 1
            else:
                temp += chr(ord(key) - 93)
                keyCount += 1
        output.append(chr(modifierKeys)+NULL_CHAR+temp+NULL_CHAR*(6-keyCount))
        output.append(NULL_CHAR*8)
        print("keys: "+str(keys)+" output:"+str(output[-1]))
        
                
        


    return output







def macroButton(pin, strokeOrder, previousState):

    inputValue = GPIO.input(pin)


    if isinstance(strokeOrder,str):
        file=open(strokeOrder,'r')
        strokeOrder=[]
        for line in file:
            strokeOrder.append(list(filter(None,line.strip('\n').split(','))))

    if (inputValue == False and previousState == True):
        commandList=commandToOutput(strokeOrder)
        for command in commandList:
            if command == NULL_CHAR*2+chr(40)+NULL_CHAR*5:
                time.sleep(1)
                print("return sleep")
                    

            write_report(command)

            if command == chr(8)+NULL_CHAR*7:
                null_report()
                time.sleep(1)
                print("windows sleep")
        else:
            write_report(NULL_CHAR*8)
    return inputValue


def funcMacroButton(pin, previousState, function, args=''):

    inputValue = GPIO.input(pin)
    if (inputValue == False and previousState == True):
        function(*args)
    return inputValue