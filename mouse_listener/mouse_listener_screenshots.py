import threading
import time
from pynput import mouse
import pyscreenshot


class MouseListener:

    def __init__(self):
        print('MouseListener started!')
        self.running = True

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            d = ThreadOperations(x, y)
            d.run()

    def start(self):
        with mouse.Listener(on_click=self.on_click) as listener:
            while self.running:
                time.sleep(1)
                if not listener.running:
                    self.running = False


class ThreadOperations:

    def __init__(self, mouse_x, mouse_y):
        self.first_thread = ''
        self.second_thread = ''
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

    def do_first_thread(self):
        for i in range(5):
            self.first_thread += chr(i)
            time.sleep(2)
            self.first_thread += self.second_thread

    def do_second_thread(self):
        print(f'x: {self.mouse_x}')
        print(f'y: {self.mouse_y}')
        x0 = 50
        y0 = 50
        x1 = self.mouse_x
        y1 = self.mouse_y
        im = pyscreenshot.grab(bbox=(x0, y0, x1, y1))
        im.save("screenshot.png")
        print('Screenshot was taken.')
        self.second_thread = "screenshot it!"

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
