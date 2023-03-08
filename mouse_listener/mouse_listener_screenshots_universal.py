import os
import threading
import time
from pathlib import Path

from pynput import mouse

class CommonUtilities:

    def __init__(self):
        print('CommonUtilities initializing!')
        self.count = 0
        self.source_root = r'D:\Temp'
        self.dest_root = r'D:\Backup'
        self.cmd_path = os.path.join(self.root_dest, 'XyzCommand.ini')
        self.tmp_folder_dest = os.path.join(self.dest_dir, "tmp")
        self.path_to_save = os.path.join(self.root_dest, self.tmp_folder_dest)
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
        pass

    def save_all_files(self):
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
        pass

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
