'''
    Terminal interface
    
    Written by Laurent Fournier, October 2016

    To-do :
    - 
'''

import npyscreen

class GuiTerminal(npyscreen.NPSApp):
    def main(self):
        F  = npyscreen.Form(name = "\\a.gus\\",)
        
        t   = F.add(npyscreen.TitleText,          name = "Text:",)
        fn  = F.add(npyscreen.TitleFilename,      name = "Filename:")
        fn2 = F.add(npyscreen.TitleFilenameCombo, name = "Filename2:")
        dt  = F.add(npyscreen.TitleDateCombo,     name = "Date:")
        s   = F.add(npyscreen.TitleSlider,        name = "Slider",     out_of = 12)
        ml  = F.add(npyscreen.MultiLineEdit,                           max_height =  5, value = """Text zone!\nMutiline, press ^R to reformat.\n""", rely = 9)
        ms  = F.add(npyscreen.TitleSelectOne,     name="Pick One",     max_height =  4, value = [1,], values = ["Option1","Option2","Option3"], scroll_exit=True)
        ms2 = F.add(npyscreen.TitleMultiSelect,   name="Pick Several", max_height = -2, value = [1,], values = ["Option1","Option2","Option3"], scroll_exit=True)

        # This lets the user interact with the Form.
        F.edit()
        print(ms.get_selected_objects())

if (__name__ == "__main__"):
    App = GuiTerminal()
    App.run()
