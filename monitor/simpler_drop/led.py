import serial
from dataclasses import dataclass

#TODO redo
from .utils import Particle

@dataclass
class ledData():
    x: int
    y: int
    red: int
    green: int
    blue: int

class LedController:
    def __init__(self, width=4, height=4, port_name="COM3"):
        self.width = width
        self.height = height
        self.serial =  serial.Serial(port_name, 115200, timeout=1)
        self.data: list[ledData] = []

    def clear(self):
        self.data = []

    # def load_monocolour_matrix(self, data: list[list], colour=(10,10,10)):
    #     self.data = []
    #     for y in range(len(data)):
    #         for x in range(len(data[y])):
    #             if data[y][x]:
    #                 self.data.append(ledData(x, y, colour[0], colour[1], colour[2]))
    def load_matrix(self, data: list[list]):
        self.data = []
        for y in range(len(data)):
            for x in range(len(data[y])):
                if isinstance(data[y][x], Particle):
                    self.data.append(ledData(x, y, data[y][x].red, data[y][x].green , data[y][x].blue))
    
    def load_matrix_with_transition(self, data_old: list[list], data_new: list[list], transition_stage: int): # transition_stage 0-1
        self.data = []
        for y in range(len(data_old)):
            for x in range(len(data_old[y])):
                red, green, blue = 0, 0, 0
                if isinstance(data_old[y][x], Particle):
                    red += int(data_old[y][x].red*(1-transition_stage))
                    green += int(data_old[y][x].green*(1-transition_stage))
                    blue += int(data_old[y][x].blue*(1-transition_stage))
                if isinstance(data_new[y][x], Particle):
                    red += int(data_new[y][x].red*(transition_stage))
                    green += int(data_new[y][x].green*(transition_stage))
                    blue += int(data_new[y][x].blue*(transition_stage))
                self.data.append(ledData(x, y, red, green , blue))

    

    def update(self):
        led_num = len(self.data)
        output = [led_num]
        for led in self.data:
            output.append(led.x)
            output.append(led.y)
            output.append(led.red)
            output.append(led.green)
            output.append(led.blue)

        self.serial.write(bytes(output))
        self.serial.flush()
