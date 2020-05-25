from tkinter import *
import dictionary

root = Tk()
root.geometry('600x600')



def search(input, output):
    res = input.get()
    output.set(res)
    input.delete(0, END)

def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox('all'))

def frame_size(event):
    output_canvas.itemconfig(canvas_frame, width=event.width)

main_frame = Frame(root, height=400, bg='black')
main_frame.pack(fill=X)

output_canvas = Canvas(main_frame, height=400, bd=1, relief=SUNKEN)
scroll = Scrollbar(main_frame, command=output_canvas.yview)
scroll.pack(side=RIGHT, fill=Y)
output_canvas.pack(side=TOP, fill=X)

output_frame = Frame(output_canvas)
output_canvas.configure(yscrollcommand=scroll.set)
canvas_frame = output_canvas.create_window((0,0), window=output_frame, anchor="nw")

output = StringVar()
outmessage = Message(output_frame, textvariable=output, anchor=NW, width=580).pack(anchor=NW, fill=X)



input = Entry(root, width=35)
input.pack(pady=5)
search_button = Button(root, text='Search', command=lambda : search(input, output))
search_button.pack(pady=5)

search_options = Frame(root, bd=0)
search_options.pack(side=TOP, pady=5)
def_button = Button(search_options, text='Definition')
syn_button = Button(search_options, text='Synonym')
def_button.pack(side=LEFT, padx=5)
syn_button.pack(side=LEFT, padx=5)


root.bind('<Return>', (lambda event: search(input, output)))
output_frame.bind("<Configure>", lambda event: on_frame_configure(output_canvas))
output_canvas.bind("<Configure>", frame_size)

root.mainloop()
outmessage['width'] = output_frame.winfo_width()