from tkinter import *
import dictionary

root = Tk()
root.geometry('600x600')

def search(input, output):
    res = input.get()
    Label(output, text=res).pack(anchor=NW)
    input.delete(0, END)

def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox('all'))

main_frame = Frame(root, height=400, bg='black')
main_frame.pack(fill=X)

output_canvas = Canvas(main_frame, height=400, bd=1, relief=SUNKEN)
scroll = Scrollbar(main_frame, command=output_canvas.yview)
scroll.pack(side=RIGHT, fill=Y)
output_canvas.pack(side=TOP, fill=X)

output_frame = Frame(output_canvas)
output_canvas.configure(yscrollcommand=scroll.set)
output_canvas.create_window((0,0), window=output_frame, anchor="nw")

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
