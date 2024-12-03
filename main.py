from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from plyer import notification
import time

class NotificationApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        notify_button = Button(
            text="Send Notification",
            size_hint=(1, 0.2),
            on_press=self.send_notification
        )
        
        layout.add_widget(notify_button)
        return layout

    def send_notification(self, instance):
        """
        Trigger a local notification on Android.
        """
        notification.notify(
            title="Local Notification",
            message="This is your push notification!",
            app_name="My Kivy App",
            timeout=5  # Duration the notification stays visible
        )
        print("Notification Sent!")

if __name__ == '__main__':
    NotificationApp().run()
