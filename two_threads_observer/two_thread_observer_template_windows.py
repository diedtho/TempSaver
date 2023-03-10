import os
import shutil
from datetime import datetime
import re
import threading
import time
from pathlib import Path

from pynput import mouse
from PIL import ImageGrab
from screeninfo import get_monitors

class CommonUtilities:

    def __init__(self):
        print('CommonUtilities initializing!')
        self.count = 0
        self.src_dir = r'D:\Temp'
        self.dest_dir = r'D:\Backup'
        self.file_path = r'D:\Temp\INSCommand.ini'
        self.dest_folder = "temp"
        self.tmp_folder = os.path.join(self.dest_dir, self.dest_folder)
        self.path_to_save = self.tmp_folder
        self.path_to_screenshots = os.path.join(self.dest_dir, 'Screenshots')
        self.cmd_timestamp_prelast = time.time()
        self.cmd_timestamp_last = time.time()
        self.initialize()

    def initialize(self):
        self.clean_src_dir()
        self.clean_dest_dir()
        Path(self.path_to_save).mkdir(parents=True, exist_ok=True)
        Path(self.path_to_screenshots).mkdir(parents=True, exist_ok=True)

    def clean_src_dir(self):
        if os.path.isdir(self.src_dir):
            for f in os.listdir(self.src_dir):
                if os.path.isfile(f):
                    try:
                        os.remove(os.path.join(self.src_dir, f))
                    except Exception as e:
                        print(f'Error deleting file:\n{e}')

    def clean_dest_dir(self):
        if os.path.isdir(self.dest_dir):
            for f in os.listdir(self.dest_dir):
                if os.path.isfile(f):
                    try:
                        os.remove(os.path.join(self.dest_dir, f))
                    except Exception as e:
                        print(f'Error deleting file:\n{e}')
                if os.path.isdir(f):
                    try:
                        shutil.rmtree(os.path.join(self.dest_dir, f))
                    except Exception as e:
                        print(f'Error deleting directory:\n{e}')

class MouseListener:

    def __init__(self, common_utils):
        self.common_utils = common_utils
        print('MouseListener started!')
        self.running = True


    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            self.take_screenshot(x, y)


    def start(self):
        with mouse.Listener(on_click=self.on_click) as listener:
            while self.running:
                time.sleep(1)
                if not listener.running:
                    self.running = False

    def take_screenshot(self, x, y):
        m = get_monitors()
        print(m)
        screen_width, screen_height = m[0].width, m[0].height
        # Größe des Bereichs, der aufgenommen werden soll
        width, height = 1200, 1200
        # Berechnung der Koordinaten des Bereichs
        x1 = max(0, x - width // 2)
        y1 = max(0, y - height // 2)
        x2 = min(screen_width, x + width // 2)
        y2 = min(screen_height, y + height // 2)
        im = ImageGrab.grab(bbox=(x1, y1, x2, y2), xdisplay=None)  # xdisplay="" if x11 else xdisplay=None
        print(f'path to save: {self.common_utils.path_to_save}')
        filename = f"screenshot_{self.common_utils.count}.png"
        filepath = os.path.join(self.common_utils.path_to_screenshots, filename)
        im.save(filepath)
        print('Screenshot was taken.')
        self.second_thread = "screenshot it!"
        self.common_utils.count += 1


class FileChangeObserver:

    def __init__(self, common_utils):
        self.common_utils = common_utils
        print('FileChange-Observer started!')
        self.running = True

    def start(self):
        while self.running:
            time.sleep(2)
            self.check_file_change()
    def check_file_change(self):
        if os.path.isfile(self.common_utils.file_path):
            cmd_timestamp_new = os.path.getmtime(self.common_utils.file_path)
        else:
            cmd_timestamp_new = 0
        if self.common_utils.cmd_timestamp_last != cmd_timestamp_new:
            print(f'timestamp new: {cmd_timestamp_new}')
            print(f'timestamp old: {self.common_utils.cmd_timestamp_last}')


class ThreadOperations:

    def __init__(self):
        self.common_utils = CommonUtilities()
        self.first_thread = ''
        self.second_thread = ''

    def do_first_thread(self):
        m = MouseListener(self.common_utils)
        m.start()

    def do_second_thread(self):
        fco = FileChangeObserver(self.common_utils)
        fco.start()

    def run(self):
        t1 = threading.Thread(target=self.do_first_thread)
        t2 = threading.Thread(target=self.do_second_thread)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print(self.first_thread, self.second_thread)


if __name__ == '__main__':
    tt = ThreadOperations()
    tt.run()
