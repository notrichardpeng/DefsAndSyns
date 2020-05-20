from tkinter import *


root = Tk()
root.geometry('600x600')

def search(input, output):
    res = input.get()
    Label(output, text=res).pack(anchor=NW)
    input.delete(0, END)

def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox('all'))

output_canvas = Canvas(root, height=400, bd=1, relief=SUNKEN)
output_frame = Frame(output_canvas)
scroll = Scrollbar(root, command=output_canvas.yview)
output_canvas.configure(yscrollcommand=scroll.set)

scroll.pack(side=RIGHT, fill=Y)
output_canvas.pack(side=TOP, fill=X)
output_canvas.create_window((4,4), window=output_frame, anchor="nw")



input = Entry(root, width=35)
input.pack(pady=5)
search_button = Button(root, text='Search', command=lambda : search(input, output_frame))
search_button.pack(pady=5)

search_options = Frame(root, bd=0)
search_options.pack(side=TOP, pady=5)
def_button = Button(search_options, text='Definition')
syn_button = Button(search_options, text='Synonym')
def_button.pack(side=LEFT, padx=5)
syn_button.pack(side=LEFT, padx=5)


root.bind('<Return>', (lambda event: search(input, output_frame)))
output_frame.bind("<Configure>", lambda event: on_frame_configure(output_canvas))

root.mainloop()
