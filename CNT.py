# -*- coding: utf-8 -*-
from psychopy import visual, event, core, data, gui
import pandas as pd
import random
from fileHandling import *

# Define colors (12 colors) in RGB255 format
colors = {
    "black": (0, 0, 0),
    "blue": (0, 0, 255),
    "brown": (105, 51, 0),
    "cyan": (0, 255, 255),
    "green": (0, 255, 0),
    "lightblue": (0, 102, 255),
    "magenta": (255, 0, 255),
    "orange": (255, 153, 0),
    "red": (255, 0, 0),
    "skyblue": (153, 204, 255),
    "white": (255, 255, 255),
    "yellow": (255, 255, 0)
}

class Experiment:
    def __init__(self, win_color, txt_color):
        self.stimuli_positions = [[-.4, 0], [.4, 0], [0, 0]]
        self.win_color = win_color
        self.txt_color = txt_color

    # def create_window(self, color=(1, 1, 1)):
    #     # type: (object, object) -> object
    #     color = self.win_color
    #     win = visual.Window(monitor="testMonitor",
    #                         color=color, fullscr=True)
    #     return win



    def settings(self):
       experiment_info = {'Subid': '', 'Age': '', 'Experiment Version': 1,
                       'Sex': ['Male', 'Female'],
                       'Language': ['English', 'Swedish', 'Russian'], u'date':
                           data.getDateStr(format="%Y-%m-%d_%H:%M"),'Inversion':['No', 'Yes']}

       info_dialog = gui.DlgFromDict(title='Color Naming Test', dictionary=experiment_info,
                                  fixed=['Experiment Version'])
       experiment_info[u'DataFile'] = u'Data' + os.path.sep + u'stroop.csv'

       if info_dialog.OK:
        return experiment_info
       else:
        core.quit()
       return 'Cancelled'
def get_colour_opposite(colorname):
      opposite = {
        "red"     : "cyan", # R
        "yellow"  : "blue", # Y
        "green"   : "magenta", # G
        "blue"    : "yellow", # B
        "magenta" : "green", # 
        "skyblue" : "brown", # 
        "brown"   : "skyblue", # noncanonical
     "lightblue"  : "orange", # noncanonical
        "orange"  : "lightblue", # dark orange
        "cyan"    : "red", # 
        "black"   : "white", # 
        "white"   : "black",
        "Silver"  : "Silver"}
      return opposite[colorname]

if __name__ == "__main__":
    background = "Gray"
    back_color = (0, 0, 0)
    textColor = "Silver"
    experiment = Experiment(win_color=background , txt_color=textColor)
    settings = experiment.settings()
    #language = settings['Language']
    inversion = settings['Inversion']
    
    # Create a window
    win = visual.Window(fullscr=True, color=(255, 255, 255), colorSpace='rgb255')

    # Create a list to store results
    results = []

    # Main test loop
    for _ in range(100):  # 50 repetitions
        # Randomly select a color
        color_name, color_value = random.choice(list(colors.items()))
    
        # Set the background color to the stimulus color in RGB format
        if inversion == "No" : 
            win.color = [c for c in color_value]
            print("win.color", win.color)
        else  : win.color = get_colour_opposite(list(colors.keys())[list(colors.values()).index(color_value)])
    
        # Display the color on the screen
        win.flip()
    
        # Start timing
        start_time = core.getTime()
    
        # Display buttons with gray text
        buttons = {}
        button_positions = [(0.2, 0.5), (0.2, 0), (0.2, -0.5), 
                        (-0.2, 0.5), (-0.2, 0), (-0.2, -0.5),
                        (0.5, 0.5), (0.5, 0), (0.5, -0.5), 
                        (-0.5, 0.5), (-0.5, 0), (-0.5, -0.5)]
    
        for i, button_color_name in enumerate(colors.keys()):
              button = visual.TextStim(win, text=button_color_name,
                                 pos=button_positions[i],
                                 color=(0.5, 0.5, 0.5), height=0.1)  
              button.draw()
    
        # Wait for selection
        win.flip()
    
        selected_color = None
        while selected_color is None:
            mouse = event.Mouse(visible=True, win=win)
            if mouse.getPressed()[0]:  
                x, y = mouse.getPos()
                for i, button_color_name in enumerate(colors.keys()):
                    button_position = button_positions[i]
                    if button_position[0] - 0.2 < x < button_position[0] + 0.2 and button_position[1] - 0.2 < y < button_position[1] + 0.2:
                        selected_color = button_color_name
                        break

            if 'escape' in event.getKeys():  
                win.close()
                core.quit()

        reaction_time = core.getTime() - start_time

        # Determine correctness of selection
        correct_choice = int(selected_color == color_name)

        # Save the result
        results.append({
            "presentedcolor": color_name,
            "selection": selected_color,
            "Accuracy": correct_choice,
            "RT": reaction_time,
            "inversion":  settings['Inversion'],
            'subid': settings['Subid'],
            'age': settings['Age'],
            'sex': settings['Sex'],
            "date": settings['date']
        })

        # Clear the screen before the next stimulus
        win.flip()
        core.wait(1)

# Close the window and save results to a CSV file
win.close()

# Create DataFrame and save to CSV
df = pd.DataFrame(results)
df.to_csv('color_selection_results.csv', index=False)
print("Results saved to color_selection_results.csv")