# Python program to create
# a file explorer in Tkinter

# import all components
# from the tkinter library
from fileinput import filename
#from lib2to3.pgen2.tokenize import _Coord
from tkinter import *

# import filedialog module
from tkinter import filedialog
from PIL import ImageTk,Image

# importing the module
from email.mime import image
import cv2
import glob

path = '/home/dokka/Desktop/testcv/images/photos/images_part4/*.jpg'

image_list = []
for name in glob.glob(path):
	image_list.append(name)


coord =[]

# Function for opening the
# file explorer window
def browseFiles():
    global my_img
    global file_name
    file_name = filedialog.askopenfilename(initialdir = "/",
										title = "Select a File",
										filetypes = (("Text files",
														"*.txt*"),
													("all files",
														"*.*")))
	
	# Change label contents
    label_file_explorer.configure(text="File Opened: "+file_name)

    
    top = Toplevel()
    top.title('image window')
    my_img = ImageTk.PhotoImage(Image.open(file_name))
    #my_img = ImageTk.PhotoImage(Image.open(file_name))
    my_label = Label(top, image=my_img).pack()
    csv = Entry(top,width=50).pack()
	#btn0 = Button(top, text="Enter the name", command=save).pack()
    btn1 = Button(top, text="Mark Coordinates", command=coordinates).pack()
    btn2= Button(top, text="Save Coordinates", command=savecoord).pack()
    btn3 = Button(top, text="close window", command=top.destroy).pack()
	



def savecoord():
	csvname = input(print("Enter the name you want to save"))
	#textfile = open("a_file.txt", "w")
	with open(csvname +'.txt','w+') as f:
		for item in coord:
			f.write("( %s , %s)\n" %(item[0] , item[1]))
			#print(item)


		f.close()

	coord.clear()

	#for element in coord:
	#	textfile.write(element + "\n")
	#	textfile.close()
    
def coordinates():
    
    if __name__=="__main__":

	  #csvname=input(print("enter the csv name"))

     	# reading the image
        img = cv2.imread(file_name, 1)

	  # displaying the image
        cv2.imshow("image",img)

	  # setting mouse handler for the image
	 # and calling the click_event() function
        cv2.setMouseCallback('image', click_event)

	 # wait for a key to be pressed to exit
        cv2.waitKey(0)

	 #if key == ord('s'):
	 #	write_file

	 # close the window
        cv2.destroyAllWindows()
	

def click_event(event, x, y, flags, params):
	

	# checking for left mouse clicks
	if event == cv2.EVENT_LBUTTONDOWN:

		# displaying the coordinates
		# on the Shell
		print(x, ' ', y)
		coord.append([x,y])
		print(coord)

		# displaying the coordinates
		# on the image window-+
		#font = cv2.FONT_HERSHEY_SIMPLEX
		#cv2.putText(img, str(x) + ',' +
		#			str(y), (x,y), font,
		#			1, (255, 0, 0), 2)
		#cv2.imshow("image", img)

	# checking for right mouse clicks	
	if event==cv2.EVENT_RBUTTONDOWN:

		# displaying the coordinates
		# on the Shell
		print(x, ' ', y)

		# displaying the coordinates
		# on the image window
		font = cv2.FONT_HERSHEY_SIMPLEX
		b = img[y, x, 0]
		g = img[y, x, 1]
		r = img[y, x, 2]
		cv2.putText(img, str(b) + ',' +
					str(g) + ',' + str(r),
					(x,y), font, 1,
					(255, 255, 0), 2)
		cv2.imshow("image", img)

																								
# Create the root window
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
						text = "Browse Files",
						command = browseFiles)

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


# driver function
