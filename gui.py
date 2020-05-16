from tkinter import *

root = Tk()


output_frame = LabelFrame(root, height=350)
output_frame.pack(fill=X)
output_frame.pack_propagate(0)

mylabel = Label(output_frame, text='hello')
mylabel.pack(anchor=NW)

root.mainloop()