import os
from datetime import datetime
import re
import threading
import time
from pathlib import Path

from pynput import mouse
import pyscreenshot
from screeninfo import get_monitors



class MouseListener:

    def __init__(self):
        print('MouseListener started!')
        self.running = True
        self.count = 0
        self.folder_list = ['start']

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            d = ThreadOperations(x, y, self.count, self.folder_list)
            d.run()
            self.count += 1

    def start(self):
        with mouse.Listener(on_click=self.on_click) as listener:
            while self.running:
                time.sleep(1)
                if not listener.running:
                    self.running = False

    def update_folder_list(self):
        folder_new = None
        with open(r'D:\Temp\INSCommand.ini', 'r', encoding='utf8') as fr:
            for line in fr.readlines():
                if line.startswith('Command='):
                    folder_new = re.sub(r'^Command=(.*)\n$', r'\1', line)
        # now = datetime.now()
        # current_time = now.strftime("%H_%M_%S")
        file_modtime = os.path.getctime(r'D:\Temp\INSCommand.ini')
        mod_time = datetime.fromtimestamp(file_modtime).strftime("%H_%M_%S")
        folder_new = mod_time + "_" + folder_new
        if folder_new not in self.folder_list:
            self.folder_list.append(folder_new)

class ThreadOperations:

    def __init__(self, mouse_x, mouse_y, count, folder_list):
        self.first_thread = ''
        self.second_thread = ''
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.count = count
        self.root = r'D:\Screenshots'
        self.folder_list = folder_list
        self.path_to_save = None

    def do_first_thread(self):
        if self.count == 0:
            self.count = 1

    def do_second_thread(self):
        m = get_monitors()
        print(m)
        screen_width, screen_height = m[0].width, m[0].height
        # Größe des Bereichs, der aufgenommen werden soll
        width, height = 800, 800
        # Berechnung der Koordinaten des Bereichs
        x1 = max(0, self.mouse_x - width // 2)
        y1 = max(0, self.mouse_y - height // 2)
        x2 = min(screen_width, self.mouse_x + width // 2)
        y2 = min(screen_height, self.mouse_y + height // 2)
        im = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
        self.update_path()
        im.save(f"{self.path_to_save}/screenshot_{self.count}.png")
        print('Screenshot was taken.')
        self.second_thread = "screenshot it!"
        self.count += 1

    def set_path(self):
        self.path_to_save = self.root + "/" + self.folder_list[-1]
        Path(self.path_to_save).mkdir(parents=True, exist_ok=True)

    def update_path(self):
        with open(r'D:\Temp\INSCommand.ini', 'r', encoding='utf8') as fr:
            for line in fr.readlines():
                if line.startswith('Command='):
                    command_new = re.sub(r'^Command=(.*)\n$', r'\1', line)
        #now = datetime.now()
        #current_time = now.strftime("%H_%M_%S")
        file_modtime = os.path.getctime(r'D:\Temp\INSCommand.ini')
        mod_time = datetime.fromtimestamp(file_modtime).strftime("%H_%M_%S")
        self.path_to_save = self.root + "/" + mod_time + "_" + command_new
        Path(self.path_to_save).mkdir(parents=True, exist_ok=True)

    def run(self):
        self.set_path()
        t1 = threading.Thread(target=self.do_first_thread)
        t2 = threading.Thread(target=self.do_second_thread)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print(self.first_thread, self.second_thread)


if __name__ == '__main__':
    m = MouseListener()
    m.start()
