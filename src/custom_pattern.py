import time
import numpy as np


class CustomPattern(object):
    def __init__(self, show):
        self.basis = np.array(
            [0, 0, 0, 1,  # top
             0, 0.7, 0, 0,  # right
             1, 0.7, 0, 0,  # right
             0, 0.7, 0, 0,  # right
             0, 0.7, 1, 0,  # bot
             0, 0.7, 1, 0,  # bot
             0, 0.7, 1, 0,  # bot
             0, 0, 1, 0,  # left
             0, 0, 1, 0,  # left
             0, 0, 1, 0,  # left
             0, 0, 0, 1,  # top
             0, 0, 0, 1])  # top
        self.pixels = self.basis * 250

        if not callable(show):
            raise ValueError('show parameter is not callable')

        self.show = show
        self.stop = False

    def wakeup(self, direction=0):
        pixels = self.basis * 2
        step = 5
        brigthness = 50
        for i in range(len(pixels) // 16):
            brigthness = 50
            sp_i = i + 10
            if sp_i > 11:
                sp_i = 0
            while brigthness < 240:
                brigthness += step
                pixels[sp_i * 4:sp_i * 4 + 4] = self.basis[sp_i * 4:sp_i * 4 + 4] * brigthness
                pixels[(i + 1) * 4:(i + 1) * 4 + 4] = self.basis[(i + 1) * 4:(i + 1) * 4 + 4] * brigthness
                pixels[(i + 4) * 4:(i + 4) * 4 + 4] = self.basis[(i + 4) * 4:(i + 4) * 4 + 4] * brigthness
                pixels[(i + 7) * 4:(i + 7) * 4 + 4] = self.basis[(i + 7) * 4:(i + 7) * 4 + 4] * brigthness
                self.print_pixels(pixels)
                self.show(pixels)
                time.sleep(0.01)

            # if i > 0:
            #     while brigthness < 220:
            #         brigthness += step
            #         print(brigthness)
            #         pixels[0:i-1 * 4 + 4] = pixels[0:i-1 * 4 + 4] + (self.basis[0:i-1 * 4 + 4] * brigthness)
            #         self.print_pixels(pixels)
            #         self.show(pixels)
            #         time.sleep(0.02)
        self.pixels = pixels

    def speak(self):
        pixels = self.pixels
        for i in range(1, 25):
            self.show([(v * i / 24) for v in pixels])
            time.sleep(0.01)

    def think(self):
        while not self.stop:
            self.pixels = np.roll(self.pixels, 4)
            self.print_pixels(self.pixels)
            self.show(self.pixels)
            time.sleep(0.05)

    def listen(self):
        pixels = self.basis
        step = 6

        low = 120
        high = 220
        brightness = low
        while not self.stop:
            new_pixels = [(v * brightness) for v in self.basis]
            self.show(new_pixels)
            time.sleep(0.01)
            self.print_pixels(new_pixels)
            if brightness < low:
                step = 6
                # time.sleep(0.4)
            elif brightness > (high - step):
                step = -1
                # time.sleep(0.4)

            brightness += step

    def off(self):
        self.show([0] * 4 * 12)

    @staticmethod
    def print_pixels(pixels):
        if __name__ == '__main__':
            print("-----------------")
            for i in range(len(pixels) // 4):
                four_pix = pixels[i * 4], pixels[i * 4 + 1], pixels[i * 4 + 2], pixels[i * 4 + 3]
                print("[{:2d}]: {:5.1f} {:5.1f} {:5.1f} {:5.1f}".format(i, *four_pix))
            print("-----------------")


if __name__ == '__main__':
    from pixel_ring import pixel_ring
    from gpiozero import LED

    power = LED(5)
    power.on()
    pixel_ring.set_brightness(20)
    pixel_ring.pattern = CustomPattern(pixel_ring.show)
    while True:
        try:
            pixel_ring.wakeup()
            time.sleep(9)
            # pixel_ring.think()
            # time.sleep(3)
            # pixel_ring.listen()
            # time.sleep(6)
            # pixel_ring.speak()
            # time.sleep(6)
        except KeyboardInterrupt:
            break

    pixel_ring.off()
    time.sleep(1)
