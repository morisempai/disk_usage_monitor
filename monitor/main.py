from simpler_drop import BallDropEngine, Canvas, LedController, TerminalCanvas
import time
import shutil
import os
import argparse

parser = argparse.ArgumentParser(
     prog="filesystemMonitor",
     description="display fs utilization using COM port"
)
parser.add_argument('--path')
parser.add_argument('--port')
parser.add_argument('--style', choices=['sand'], default="sand")


class LedCanvas(Canvas):
    def __init__(self, port_name, fps=10, filling_frames=10):
        super().__init__(fps)
        self.led_controller = LedController(port_name=port_name)
        self.old_matrix = []
        self.filling_frames = filling_frames

    def draw(self, pixel_matrix):
        if not self.old_matrix:
            self.led_controller.load_matrix(self.rotate(pixel_matrix))
            self.led_controller.update()
            self.old_matrix = pixel_matrix
            time.sleep(1/self.fps)
        else:
            for frame in range(self.filling_frames):
                self.led_controller.load_matrix_with_transition(self.rotate(self.old_matrix), self.rotate(pixel_matrix), frame/self.filling_frames)
                self.led_controller.update()
                time.sleep(1/self.fps/self.filling_frames)
            self.old_matrix = pixel_matrix
    
    def rotate(self, pixels):
        new_list = []
        column_len = len(pixels)//2
        row_len = len(pixels[0])//2

        for y in range(column_len):
            new_row = []
            for x in range(row_len):
                new_row.append(pixels[y+x][len(pixels[0])//2+x-y])
            new_list.append(new_row)
        return new_list


class DiskUsageGauge(BallDropEngine):
    def __init__(self, width=9, height=8):
        super().__init__(width, height)
        self._monitoring_path = ""

    @property
    def monitoring_path(self):
        return self._monitor_path
    
    @monitoring_path.setter
    def monitoring_path(self, path):
        if os.path.exists(path=path):
            self._monitoring_path = path
        else:
            raise ValueError("Path does't exist")


    def start(self):
        offset = 0
        for y in range(self.height//2, self.height):
            self.pixels[y][offset] = self.OBSTICLE
            self.pixels[y][offset+1] = self.OBSTICLE
            self.pixels[y][-offset-1] = self.OBSTICLE
            self.pixels[y][-offset-2] = self.OBSTICLE
            offset += 1
        
        self.usage = shutil.disk_usage(path=self._monitoring_path)
        self.gauge = self.usage.used*self.width*self.height/self.usage.total
        self.displayed_gauge = 0
        self.counter = 0
    
    def loop(self):
        self.usage = shutil.disk_usage(path=self._monitoring_path)
        self.gauge = self.usage.used*25//self.usage.total
        self.counter += 1
        if self.counter%7 == 0:
            if self.displayed_gauge<self.gauge:
                self.add_particle(0, self.width//2)
                self.displayed_gauge += 1
            elif self.displayed_gauge>self.gauge and self.pixels[-3][self.width//2]:
                self.pixels[-2][self.width//2] = self.EMPTY
                self.displayed_gauge -= 1 
        # # for dynamic behavor
        elif self.counter%15 == 0 and self.pixels[-3][self.width//2]: 
            self.pixels[-2][self.width//2] = self.EMPTY
            self.displayed_gauge -= 1

if __name__ == "__main__":
    args = parser.parse_args()
    if args.style == "sand":
        engine = DiskUsageGauge()
    else:
        raise ValueError("unknown style name")
    engine.monitoring_path = args.path
    engine.add_canvas(LedCanvas(port_name=args.port, fps=4))
    # engine.add_canvas(TerminalCanvas(fps=4))
    engine.run()

