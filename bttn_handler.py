import machine
from time import sleep_ms

class LORA:
    def __init__(self, port_num, baud_rate=115200, tx_pin=None, rx_pin=None):
        if tx_pin is None and rx_pin is None:
            self._uart = machine.UART(port_num, baudrate=baud_rate)  
        else:
            self._uart = machine.UART(port_num, baudrate=baud_rate, tx=tx_pin, rx=rx_pin) 
    
    def test(self):
        self._uart.write('AT\r\n')
        sleep_ms(50)
        while(self._uart.any() == 0):
            pass
        reply = self._uart.readline()
        print(reply.decode().strip('\r\n'))

    def set_addr(self, addr):
        self._uart.write('AT+ADDRESS={}\r\n'.format(addr))

    def send_msg(self, addr, msg):
        self._uart.write('AT+SEND={},{},{}\r\n'.format(addr, len(msg), msg))
        sleep_ms(50)
        while(self._uart.any() == 0):
            pass
        reply = self._uart.readline()
        print(reply.decode().strip())

# Debounce duration (in milliseconds)
debounce_time = 200
debounce_timer = machine.Timer(-1)

# Flag to prevent repeated presses within debounce period
debounced = False

def button_handler(pin):
    global debounced
    if not debounced:
        print('MSG SENT')
        lora.send_msg(2, '1')
        debounced = True
        debounce_timer.init(period=debounce_time, mode=machine.Timer.ONE_SHOT, callback=reset_debounce)

def reset_debounce(timer):
    global debounced
    debounced = False
    


# LoRa configuration
lora = LORA(0, baud_rate=115200, tx_pin=machine.Pin(0), rx_pin=machine.Pin(1))
sleep_ms(1000)
lora.set_addr(1)

# Button configuration with IRQ
button = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_DOWN)
button.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)

# Main loop
while True:
    machine.idle()
    #machine.lightsleep(60000)
