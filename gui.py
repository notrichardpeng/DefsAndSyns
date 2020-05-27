from tkinter import *
import dictionary

root = Tk()
root.geometry('600x600')
mode = 'definition'


def concatenate(word, list_of_lines):
    ret = 'definitions of ' + word + '\n\n' if mode == 'definition' else 'synonyms of ' + word + '\n\n'
    for s in list_of_lines:
        ret += s
        ret += '\n'
    if ret[-1] == '\n': ret = ret[:-1]
    return ret

def search(input, output):
    word = input.get()
    strs = dictionary.definition(word, 2, 2) if mode == 'definition' else dictionary.synonym(word, 2)

    s = concatenate(word, strs)

    output.set(s)
    input.delete(0, END)

def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox('all'))

def frame_size(event):
    output_canvas.itemconfig(canvas_frame, width=event.width)
    out_message.configure(width=event.width-scroll.winfo_width())

def synonym_mode(def_button, syn_button):
    global mode
    mode = 'synonym'
    def_button['state'] = 'normal'
    syn_button['state'] = 'disabled'

def definition_mode(def_button, syn_button):
    global mode
    mode = 'definition'
    def_button['state'] = 'disabled'
    syn_button['state'] = 'normal'



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
out_message = Message(output_frame, textvariable=output, anchor=NW)
out_message.pack(anchor=NW, fill=X)



input = Entry(root, width=35)
input.pack(pady=5)
search_button = Button(root, text='Search', command=lambda : search(input, output))
search_button.pack(pady=5)

search_options = Frame(root, bd=0)
search_options.pack(side=TOP, pady=5)

def_button, syn_button = None, None
def_button = Button(search_options, text='Definition', command=lambda : definition_mode(def_button, syn_button), state='disabled')
syn_button = Button(search_options, text='Synonym', command=lambda : synonym_mode(def_button, syn_button))
def_button.pack(side=LEFT, padx=5)
syn_button.pack(side=LEFT, padx=5)


root.bind('<Return>', (lambda event: search(input, output)))
output_frame.bind("<Configure>", lambda event: on_frame_configure(output_canvas))
output_canvas.bind("<Configure>", frame_size)



dictionary.initialize()
root.mainloop()