from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.widget import Widget
import os
import random
from kivy.config import Config

# Set the window to run in fullscreen mode
Config.set('graphics', 'fullscreen', 'auto')

class BlockTouchWidget(Widget):
    def on_touch_down(self, touch):
        # Display "Don't Touch" message
        dont_touch_label = Label(
            text="PLEASE, Don't Touch!",
            font_size=100,
            color= ('yellow'),
            pos=(self.width / 2 - 100, self.height / 2 - 25)
        )
        self.add_widget(dont_touch_label)

        # Schedule the removal of the message after 3 seconds
        def remove_message(dt):
            self.remove_widget(dont_touch_label)

        Clock.schedule_once(remove_message, 3)
        return True

class SlideshowApp(App):
    min_display_time = 10  # Minimum display time (seconds)
    max_display_time = 15  # Maximum display time (seconds)
    pictures_folder = "/storage/emulated/0/Pictures"  # Updated picture folder path

    def build(self):
        # Check if the specified folder exists
        if not os.path.exists(self.pictures_folder):
            print("Pictures folder not found. Please ensure your pictures are in the specified folder.")
            return

        self.image_files = [f for f in os.listdir(self.pictures_folder) if f.lower().endswith('.jpg')]
        self.randomize_order()
        self.current_image_index = 0

        self.image = Image(allow_stretch=True)
        self.root = BlockTouchWidget()
        self.root.add_widget(self.image)

        # Schedule the initial display
        self.show_current_image()
        Clock.schedule_once(self.next_image, random.uniform(self.min_display_time, self.max_display_time))

        return self.root

    def randomize_order(self):
        random.shuffle(self.image_files)

    def show_current_image(self):
        if 0 <= self.current_image_index < len(self.image_files):
            image_path = os.path.join(self.pictures_folder, self.image_files[self.current_image_index])
            self.image.source = image_path

            # Get the screen size and set the image's size accordingly
            window_width, window_height = self.root.size
            self.image.size = (window_width, window_height)

            # Create an animation for the fade-in effect
            self.image.opacity = 0
            fade_in_animation = Animation(opacity=1, duration=1.0)
            fade_in_animation.start(self.image)

    def next_image(self, dt):
        # Create an animation for the fade-out effect
        fade_out_animation = Animation(opacity=0, duration=1.0)
        fade_out_animation.bind(on_complete=self.load_next_image)
        fade_out_animation.start(self.image)

    def load_next_image(self, *args):
        # Display the next image and schedule the following image
        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
        self.show_current_image()
        self.randomize_order()
        Clock.schedule_once(self.next_image, random.uniform(self.min_display_time, self.max_display_time))

if __name__ == '__main__':
    SlideshowApp().run()
