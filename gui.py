from tkinter import *

root = Tk()

def search(input, output):
    res = input.get()
    Label(output, text=res).pack(anchor=NW)
    input.delete(0, END)

output_frame = LabelFrame(root, height=450)
output_frame.pack(fill=X, pady=30)
output_frame.pack_propagate(0)

input = Entry(root, width=35)
input.pack(pady=5)

search_button = Button(root, text='Search', command=lambda : search(input, output_frame))
search_button.pack(pady=5)

search_options = LabelFrame(root, bd=0)
search_options.pack(pady=5)
def_button = Button(search_options, text='Definition')
syn_button = Button(search_options, text='Synonym')
def_button.pack(side=LEFT, padx=5)
syn_button.pack(side=LEFT, padx=5)


root.bind('<Return>', (lambda event: search(input, output_frame)))
root.mainloop()
