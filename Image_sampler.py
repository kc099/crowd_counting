import cv2
import os

# from the tkinter library
#from fileinput import filename
#from lib2to3.pgen2.tokenize import _Coord
from tkinter import *

# import filedialog module
from tkinter import filedialog
from PIL import ImageTk,Image

# importing the module
#from email.mime import image
images = []
def load_images_from_folder():
   
    # folder_selected = filedialog.askdirectory()
    # for filename in os.listdir(folder_selected):
    #     img = ImageTk.PhotoImage(Image.open(os.path.join(folder_selected,filename)))
    #     print(os.path.join(folder_selected,filename))
    #     if img is not None:
    #         images.append(img)
    
    top = Toplevel()
    top.title('image window')
    #my_label = Label(top, image=images[0])

    #my_label.grid(row=0, column=0,columnspan=4)


    button_back=Button(top,text="<<")
    button_sample=Button(top,text="Mark image")
    button_forward=Button(top,text=">>")
    button_exit = Button(top,text="exit", command=top.withdraw())

    button_back.grid(row=1,column=1)
    button_sample.grid(row=1,column=2)
    button_forward.grid(row=1,column=3)
    button_exit.grid(row=1,column=4)

    # 
    # 


#Create the root window
window = Tk()

# Set window title
window.title('File Explorer')

# Set window size
window.geometry("500x500")

#Set window background color
window.config(background = "white")



# Create a File Explorer label
label_file_explorer = Label(window,
							text = "File Explorer using Tkinter",
							width = 100, height = 4,
							fg = "blue")


button_explore = Button(window,
						text = "Select the Images folder",
						command = load_images_from_folder)

button_exit = Button(window,
					text = "Exit",
					command = exit)

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column = 1, row = 1)

button_explore.grid(column = 1, row = 2)

button_exit.grid(column = 1,row = 3)

# Let the window wait for any events
window.mainloop()

