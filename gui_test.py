from kivy.app import App

from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.label     import Label
from kivy.uix.widget    import Widget
from kivy.uix.button    import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup     import Popup
from kivy.uix.settings  import (Settings, 
                                SettingsWithSidebar,
                                SettingsWithSpinner,
                                SettingsWithTabbedPanel)
                               
from kivy.properties import OptionProperty, ObjectProperty

from kivy.lang import Builder

root = Builder.load_file("accordion.kv")

class AccordionApp(App):
    def build(self):
        return root


if __name__ == '__main__':
    AccordionApp().run()
