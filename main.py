from kivy.app import App
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy import platform
from kivy.uix.label import Label
import os
import random

class BlockTouchWidget(Widget):
    def on_touch_down(self, touch):
        # Display the overlay image
        overlay_image = Image(source="/storage/emulated/0/Pictures/xtreme.png", allow_stretch=True)
        overlay_image.size = (min(self.width, self.height), min(self.width, self.height))
        overlay_image.pos = (self.width / 2 - overlay_image.width / 2, self.height / 2 - overlay_image.height / 2)
        self.add_widget(overlay_image)

        # Schedule the removal of the message and overlay image after 3 seconds
        def remove_message(dt):
            self.remove_widget(overlay_image)

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
        Clock.schedule_once(self.next_image, 1.0)  # Display first image for 1 second

        return self.root

    def on_start(self):
        if platform == 'android':
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            activity.setRequestedOrientation(0)  # 0 corresponds to SCREEN_ORIENTATION_LANDSCAPE

    def randomize_order(self):
        random.shuffle(self.image_files)

    def show_current_image(self):
        if 0 <= self.current_image_index < len(self.image_files):
            image_path = os.path.join(self.pictures_folder, self.image_files[self.current_image_index])
            self.image.source = image_path

            # Get the screen size and set the image's size accordingly
            window_width, window_height = Window.size
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
