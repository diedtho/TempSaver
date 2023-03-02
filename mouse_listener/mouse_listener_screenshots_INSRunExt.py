import os
import shutil
from datetime import datetime
import re
import threading
import time
from pathlib import Path

from pynput import mouse
import pyscreenshot
from screeninfo import get_monitors

class CommonUtilities:

    def __init__(self):
        print('CommonUtilities initializing!')
        self.count = 0
        self.root = r'D:\Temp'
        self.dest_dir = r'D:\Backup'
        self.cmd_path = r'D:\Temp\INSCommand.ini'
        self.tmp_folder = os.path.join(self.dest_dir, "tmp")
        self.dest_folder = "tmp"
        self.path_to_save = os.path.join(self.dest_dir, self.dest_folder)
        Path(self.path_to_save).mkdir(parents=True, exist_ok=True)
        self.cmd_timestamp_prelast = os.path.getmtime(self.cmd_path)
        self.cmd_timestamp_last = os.path.getmtime(self.cmd_path)


class MouseListener:

    def __init__(self):
        print('MouseListener started!')
        self.running = True
        self.common_utils = CommonUtilities()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            d = ThreadOperations(x, y, self.common_utils)
            d.run()
            self.check_command_change()

    def start(self):
        with mouse.Listener(on_click=self.on_click) as listener:
            while self.running:
                time.sleep(1)
                if not listener.running:
                    self.running = False

    def check_command_change(self):
        cmd_timestamp_new = os.path.getmtime(self.common_utils.cmd_path)
        print(f'timestamp new: {cmd_timestamp_new}')
        print(f'timestamp old: {self.common_utils.cmd_timestamp_last}')
        if self.common_utils.cmd_timestamp_last != cmd_timestamp_new:
            print(f'old path to save: {self.common_utils.path_to_save}')
            #self.save_all_files()
            self.common_utils.cmd_mtime_str = datetime.fromtimestamp(cmd_timestamp_new).strftime("%H_%M_%S")
            cmd_new = None
            with open(self.common_utils.cmd_path, 'r', encoding='utf8') as fr:
                for line in fr.readlines():
                    if line.startswith('Command='):
                        cmd_new = re.sub(r'^Command=(.*)\n$', r'\1', line)
            new_folder_name = self.common_utils.cmd_mtime_str + "_" + cmd_new
            self.common_utils.path_to_save = os.path.join(self.common_utils.dest_dir, new_folder_name)
            print(f'new path to save: {self.common_utils.path_to_save}')
            Path(self.common_utils.path_to_save).mkdir(parents=True, exist_ok=True)
            self.common_utils.cmd_timestamp_prelast = self.common_utils.cmd_timestamp_last
            self.save_all_files()
            self.common_utils.cmd_timestamp_last = cmd_timestamp_new
            try:
                shutil.copy(self.common_utils.cmd_path, self.common_utils.path_to_save)
            except shutil.SameFileError:
                pass

    def save_all_files(self):
        for filename in os.listdir(self.common_utils.root):
            f = os.path.join(self.common_utils.root, filename)
            # checking if it is a file
            if os.path.isfile(f):
                timestamp = os.path.getmtime(f)
                if timestamp >= self.common_utils.cmd_timestamp_prelast and '.tmp' not in filename:
                    try:
                        shutil.copy(f, os.path.join(self.common_utils.path_to_save, filename))
                    except shutil.SameFileError:
                        pass


class ThreadOperations:

    def __init__(self, mouse_x, mouse_y, common_utils):
        self.first_thread = ''
        self.second_thread = ''
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.common_utils = common_utils


    def do_first_thread(self):
        pass

    def do_second_thread(self):
        m = get_monitors()
        print(m)
        screen_width, screen_height = m[0].width, m[0].height
        # Größe des Bereichs, der aufgenommen werden soll
        width, height = 1200, 1200
        # Berechnung der Koordinaten des Bereichs
        x1 = max(0, self.mouse_x - width // 2)
        y1 = max(0, self.mouse_y - height // 2)
        x2 = min(screen_width, self.mouse_x + width // 2)
        y2 = min(screen_height, self.mouse_y + height // 2)
        im = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
        print(f'path to save: {self.common_utils.path_to_save}')
        filename = f"screenshot_{self.common_utils.count}.png"
        filepath = os.path.join(self.common_utils.path_to_save, filename)
        im.save(filepath)
        print('Screenshot was taken.')
        self.second_thread = "screenshot it!"
        self.common_utils.count += 1



    def run(self):
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
