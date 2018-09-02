# -*- coding: utf-8 -*
import  Adafruit_Thermal as Thermal
import random
printer = Thermal.Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

printer.println("--------------------------------")
printer.justify('C')
printer.inverseOn()
printer.setSize('L')
printer.println("SeeedStudio")
printer.inverseOff()
printer.println()
printer.println()
printer.setSize('M')
printer.println("The score of your photo style is")
score = 99+ random.random()
printer.println(score)
printer.println()
# 这里添加二维码打印代码
printer.println()
printer.println()
printer.println("--------------------------------")
printer.println()
printer.println()


