from machine import Pin, UART
from time import sleep_ms

class RYLR896:
    def __init__(self, port_num, baud_rate=115200, tx_pin=None, rx_pin=None):
        if tx_pin is None and rx_pin is None:
            self._uart = UART(port_num, baudrate=baud_rate)  
        else:
            self._uart = UART(port_num, baudrate=baud_rate, tx=tx_pin, rx=rx_pin) 
                
    def cmd(self, lora_cmd):
        self._uart.write('{}\r\n'.format(lora_cmd))
        sleep_ms(50)
        while(self._uart.any()==0):
            pass
        reply = self._uart.readline()
        print(reply.decode().strip('\r\n'))
    
    def test(self):
        self._uart.write('AT\r\n')
        sleep_ms(50)
        while(self._uart.any()==0):
            pass
        reply = self._uart.readline()
        print(reply.decode().strip('\r\n'))

    def set_addr(self, addr):
        self._uart.write('AT+ADDRESS={}\r\n'.format(addr))
        sleep_ms(50)
        while(self._uart.any()==0):
            pass
        reply = self._uart.readline()
        print(reply.decode().strip('\r\n'))
        print('Address set to: {}\r\n'.format(addr))


    def send_msg(self, addr, msg):
        self._uart.write('AT+SEND={},{},{}\r\n'.format(addr,len(msg),msg))
        sleep_ms(1000)
        while(self._uart.any()==0):
            pass
        reply = self._uart.readline()
        print(reply.decode().strip('\r\n'))
        
    def read_msg(self):
        if self._uart.any()==0:
            print('No Messages.')
        else:
            msg = ''
            while(self._uart.any()):
                msg = msg + self._uart.read(self._uart.any()).decode()
                sleep_ms(10)
                
            msg = msg.strip('\r\n')
            clean_msg = msg.replace("+RCV=", "")
            parts = clean_msg.split(',')
    
            addr_recv_from = parts[0]  
            msg_len = parts[1]  
            msg_str = parts[2]  
            msg_RSSI = parts[3]  
            msg_SNR = parts[4]
            
            print("Rcv from Addr: {}\r\nMsg Length: {}\r\nRSSI: {}\r\nSNR: {}\r\nMsg: {}\r\n".format(addr_recv_from,msg_len,msg_RSSI,msg_SNR,msg_str))

    
# led = Pin(25, Pin.OUT)
# 
# for x in range(5):
#     sleep_ms(1000)
#     led.toggle()
    

# uart1 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
# uart1.write("Just popping in")
# sleep_ms(1)
# data = uart1.read()
# 
# 
# if data:
#     print(data.decode('utf-8'))
# else:
#     print("No data received")

lora = RYLR896(0, baud_rate=115200, tx_pin=Pin(0), rx_pin=Pin(1)) 
sleep_ms(1000)
lora.set_addr(2)  


