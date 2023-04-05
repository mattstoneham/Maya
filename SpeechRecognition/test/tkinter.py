from Tkinter import *



# run a loop in tkinter
root = Tk()

def task():
    print("hello")
    root.after(2000, task)  # reschedule event in 2 seconds

root.after(2000, task)
root.mainloop()



# tkinter not in a loop
from Tkinter import *

ROOT = Tk()
LABEL = Label(ROOT, text="Hello, world!")
LABEL.pack()
LOOP_ACTIVE = True
while LOOP_ACTIVE:
    ROOT.update()
    USER_INPUT = raw_input("Give me your command! Just type \"exit\" to close: ")
    if USER_INPUT == "exit":
        ROOT.quit()
        LOOP_ACTIVE = False
    else:
        LABEL = Label(ROOT, text=USER_INPUT)
        LABEL.pack()




import Tkinter as tk

window = tk.Tk()
greeting = tk.Label(window, text="Hello, Tkinter")
greeting.pack()

'''
def main(): # main program code

    while True:
        


if __name__ == '__main__':
    main()
'''


from Tkinter import *

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()