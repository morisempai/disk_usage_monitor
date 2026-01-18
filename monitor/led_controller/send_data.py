import serial
import time
from dataclasses import dataclass
import shutil


serial_port_name = 'COM3'
baud_rate = 115200
# ---------------------

@dataclass
class ledData():
    x: int
    y: int
    red: int
    green: int
    blue: int

def send_data(serial_obj: serial.Serial, data: list[ledData]):
    led_num = len(data)
    output = [led_num]
    for led in data:
        output.append(led.x)
        output.append(led.y)
        output.append(led.red)
        output.append(led.green)
        output.append(led.blue)

    ser.write(bytes(output))
    ser.flush()
    time.sleep(0.1)
    print(f"Sent: {output!r}")

try:
    # Open the serial port with a timeout
    ser = serial.Serial(serial_port_name, baud_rate, timeout=1)
    time.sleep(0.5)
    print(f"Serial port {serial_port_name} opened successfully at {baud_rate} baud.")

    leds = [
        ledData(0, 0, 128, 0, 0),
        ledData(1, 1, 0, 128, 0),
        ledData(2, 2, 0, 0, 128),
        ledData(3, 3, 40, 40, 40),
        ]

    while (True):
        usage = shutil.disk_usage("C:\Users\moris\led")
        
        usage_percent = usage.used/usage.total

        for led in leds:
            led.x = (led.x + 1) % 4
            leds[0].red = (leds[0].red + 1) % 10 + 10 
            leds[1].green = (leds[1].green + 1) % 10 + 10
            leds[2].blue = (leds[2].blue + 1) % 10 + 10
            leds[3].red = (leds[3].red + 1) % 10 + 10
            leds[3].green = (leds[3].green + 1) % 10 + 10 
            leds[3].blue = (leds[3].blue + 1) % 10 + 10
        send_data(ser, leds)


except Exception as e:
    print(f"Error: {e}")
    print(f"Please check if {serial_port_name} is the correct port and if it is not in use by another program.")

finally:
    # Close the serial port
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")