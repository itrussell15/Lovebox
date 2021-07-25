import gpiozero as gpio
import time

class GPIO_Handler:
    
    def __init__(self, led, light):
        self.led = gpio.PWMLED(led)
        self.light = gpio.LightSensor(light, charge_time_limit = 0.3)
        self.led.off()
        
    def flash_light(self):
        self.led.blink(1, 1, 1, 1)
        
    def light_detected(self):
        self.led.off()
    
#gpio = GPIO_Handler(led = 18, light = 4)
#while True:
#    print("Waiting for dark -> {:.2f}".format(gpio.light.value))
#    gpio.light.wait_for_dark()
#    print("dark")
#    time.sleep(0.5)
    