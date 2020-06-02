from tkinter import *
import dictionary
import threading
import time

root = Tk()
root.geometry('600x600')
mode = 'definitions'
num_of_results = 1

def concatenate(word, list_of_lines):
    ret = mode + ' of ' + word + '\n\n'
    for s in list_of_lines:
        ret += s
        ret += '\n'
    if ret[-1] == '\n': ret = ret[:-1]
    return ret

def search(input, output):
    global num_of_results
    word = input.get()
    input.delete(0, END)
    output.set('searching for ' + mode + ' of "' + word + '"...')

    if mode == 'definitions': lines = dictionary.definition(word, 5, num_of_results)
    else: lines = dictionary.synonym(word, num_of_results)

    s = concatenate(word, lines)
    output.set(s)

def set_num_of_results(label, slider):
    global num_of_results
    num_of_results = slider.get()
    label.config(text="Number of Results: " + str(num_of_results))

def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox('all'))

def frame_size(event):
    output_canvas.itemconfig(canvas_frame, width=event.width)
    out_message.configure(width=event.width-scroll.winfo_width())

def synonym_mode(def_button, syn_button):
    global mode
    mode = 'synonyms'
    def_button['state'] = 'normal'
    syn_button['state'] = 'disabled'

def definition_mode(def_button, syn_button):
    global mode
    mode = 'definitions'
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
search_button = Button(root, text='Search', command=threading.Thread(target=search, args=(input, output)).start)
search_button.pack(pady=5)

search_options = Frame(root, bd=0)
search_options.pack(side=TOP, pady=5)

def_button, syn_button = None, None
def_button = Button(search_options, text='Definition', command=lambda : definition_mode(def_button, syn_button), state='disabled')
syn_button = Button(search_options, text='Synonym', command=lambda: synonym_mode(def_button, syn_button))
def_button.pack(side=LEFT, padx=5)
syn_button.pack(side=LEFT, padx=5)

results_num_label = Label(root, text="Number of Results: 1")
results_num_label.pack(pady=2)
results_num_slider = Scale(root, from_=1, to=5, orient=HORIZONTAL, showvalue=0, \
    command=lambda event: set_num_of_results(results_num_label, results_num_slider))
results_num_slider.pack()

root.bind('<Return>', (lambda event: threading.Thread(target=search, args=(input, output)).start()))
output_frame.bind("<Configure>", lambda event: on_frame_configure(output_canvas))
output_canvas.bind("<Configure>", frame_size)



dictionary.initialize()
root.mainloop()