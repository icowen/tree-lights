from neopixel import Neopixel
import rp2
import random
import uasyncio as asyncio
from primitives import Pushbutton
from machine import Pin



from Rgb import RGB

class Sparkle:
    NUM_UPDATES = 20
    HALF_UPDATES = NUM_UPDATES // 2
    MAX_BRIGHT = 255
    BRIGHTNESS_STEP = MAX_BRIGHT / HALF_UPDATES
    
    def __init__(self, pixel, lights):
        self.pixel = pixel
        self.lights = lights
        self.brightness = 0
        self.update_num = 0
        
    def update(self):
        self.update_num += 1
        
        if self.update_num >= Sparkle.NUM_UPDATES:
            return True
        
        step_direction = -abs(self.update_num - Sparkle.HALF_UPDATES) + Sparkle.HALF_UPDATES
        self.brightness = Sparkle.BRIGHTNESS_STEP * step_direction
        self.lights.brightness(self.brightness)
        self.lights.set_pixel(self.pixel, RGB.WHITE)
        self.lights.show()

        return False
        
    def reset(self, pixel):
        self.pixel = pixel
        self.brightness = 0
        self.update_num = 0
            
            
class Sparkles:
    DEFAULT_BRIGHTNESS = 100
    SLEEP = 0.05
    NUM_SPARKLES = 10
    
    def __init__(self, lights, color=RGB.GREEN):
        self.color = color
        self.lights = lights
        
        self.lights.brightness(Sparkles.DEFAULT_BRIGHTNESS)
        self.lights.fill(color)
        
        self.sparkles = []
            
    def get_pixel(self):
        current = [s.pixel for s in self.sparkles]
        
        while True:
            pixel = int(random.random() * self.lights.num_leds)
            if pixel not in current:
                return pixel
    
    def init_sparkles(self):
        for sparkle_num in range(Sparkles.NUM_SPARKLES):
            sparkle = Sparkle(self.get_pixel(), self.lights)
            
            for update_num in range(sparkle_num * 2):
                sparkle.update()
            
            self.sparkles.append(sparkle)
        
    async def run(self):
        self.init_sparkles()
        while True:
            await asyncio.sleep(Sparkles.SLEEP)
            for sparkle in self.sparkles:
                if sparkle.update():
                    self.lights.brightness(Sparkles.DEFAULT_BRIGHTNESS)
                    self.lights.set_pixel(sparkle.pixel, self.color)
                    self.lights.show()
                    sparkle.reset(self.get_pixel())
                
                
class Controller:
    NUM_LIGHTS = 100

    def __init__(self):
        for _ in range(2):
            try:
                self.lights = Neopixel(Controller.NUM_LIGHTS, 0, 28, "RGB")
            except OSError as e:
                rp2.PIO(0).remove_program()
        
        self.init_button()
        self.display = self.display_generator()
        self.task = asyncio.create_task(next(self.display)())
        
    def init_button(self):
        button = Pushbutton(Pin(27, Pin.IN, Pin.PULL_UP), suppress=True)
        button.release_func(self.next_display)
        button.long_func(self.off)
        
    def display_generator(self):
        displays = [self.candy_cane, self.color_fade, self.icicles, self.sparkles]
        while True:
            for display in displays:
                yield display
        
    def next_display(self):
        print("Button Pressed")

        self.task.cancel()
        self.task = asyncio.create_task(next(self.display)())
        
    async def no_op(self):
        await asyncio.Event().wait()
        
    def off(self):
        print("Off")

        self.task.cancel()
        self.task = asyncio.create_task(self.turn_off())
        
    async def turn_off(self):
        self.lights.fill(RGB.RED)
        
        for brightness in range(255, 0, -2):
            self.lights.brightness(brightness)
            self.lights.fill(RGB.RED)
            await asyncio.sleep(0.01)
            self.lights.show()
        
        self.lights.fill(RGB.OFF)
        self.lights.show()
        
        self.task = asyncio.create_task(self.no_op())
                
    async def candy_cane(self):
        print("Candy cane")

        self.lights.brightness(100)
        self.lights.fill(RGB.RED)
        
        for i in [0, 30, 60]:
            self.lights.set_pixel_line(i, i + 10, RGB.WHITE)
        
        while True:
            self.lights.show()
            self.lights.rotate_right(1)
            await asyncio.sleep(0.05)
            
    async def color_fade(self):
        print("Color Fade")

        colors = [RGB.RED, RGB.GREEN, RGB.BLUE, RGB.PURPLE]
        full_bright, half_bright = 255, 255 // 2
        
        while True:
            for color in colors:
                self.lights.brightness(0)
                self.lights.fill(color)
                self.lights.show()
                
                for brightness_step in range(full_bright):
                    brightness = -abs(brightness_step - half_bright) + half_bright
                    self.lights.brightness(brightness)
                    self.lights.fill(color)
                    await asyncio.sleep(0.01)        
                    self.lights.show()
    
    async def icicles(self):
        print("Icicles")

        self.lights.fill(RGB.OFF)
        
        for _ in range(10):
            self.lights.brightness(_ * 25)
            self.lights.set_pixel(_, RGB.BLUE)
            self.lights.set_pixel(Controller.NUM_LIGHTS // 2 + _, RGB.WHITE)
        self.lights.show()
        
        while True:
            self.lights.rotate_right(1)
            await asyncio.sleep(0.1)
            self.lights.show()
            
    async def sparkles(self):
        print("Sparkles")

        await Sparkles(self.lights).run()
                
    async def run(self):
        try:
            while True:
                try:
                    await self.task
                except asyncio.CancelledError:
                    continue
        except Exception as e:
            raise e
        finally:
            if self.lights is not None:
                self.lights.fill(RGB.OFF)
                self.lights.show()

    
if __name__ == "__main__":
    asyncio.run(Controller().run())