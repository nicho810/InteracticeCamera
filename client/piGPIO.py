import RPi.GPIO as GPIO


def pinSetup(triggerPin, fanPin, lightPin):
    # 配置GPIO
    GPIO.setmode(GPIO.BOARD)  # 设置为board IO模式
    GPIO.setup(triggerPin, GPIO.IN)
    GPIO.setup(fanPin, GPIO.OUT)
    GPIO.setup(lightPin, GPIO.OUT)


def readPin(pin):
    return GPIO.input(pin)


def setPin(pin):
    GPIO.output(pin, True)
    return 0


def resetPin(pin):
    GPIO.output(pin, False)
    return 0
