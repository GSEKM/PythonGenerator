from tkinter import *
from tkinter import ttk


methods = ['Y(int x)', 'Turn(float x)', 'Stop()']
methodsLib = ['Servo();\n', 'uint8_t attach(int pin, int min, int max); ', 'void write(int value); ', 'int read();', 'bool attached(); ']
libraries = ['Servo,','Servo,','Servo,']


root = Tk()
root.configure(background='grey')

root.style = ttk.Style()

#('clam', 'alt', 'default', 'classic')
root.style.theme_use("alt")

label1 = Label(text = 'Arduino Model Driven Development',font=("Arial Bold", 20))
label1.grid(row = 0, column = 0)
# label1.pack()

# entry1 = Entry(font=("Arial Bold", 20))
# entry1.grid(row = 1, column = 0)

btn = Button(text="Pack", bg="blue", fg="red")
btn.grid(row = 2, column = 0)

for method in methods: #Rows
    for j in range(2): #Columns
        print(method)
        print(methods.index(method)+1)
        # b = Entry(root, text="")
        if j == 0:
            b = Label(text = method,font=("Arial", 20))
            b.grid(row=methods.index(method)+1, column=j+1)
        elif j == 1:

            variable = StringVar(root)
            variable.set("          ") # default value

            b = OptionMenu(*(root, variable) + tuple(methodsLib))
            # b = Label(text = "method",font=("Arial", 20))
            b.grid(row=methods.index(method)+1, column=j+1)
            




# height = 5
# width = 5
# for i in range(5): #Rows
#     for j in range(5): #Columns
#         b = Entry(root, text="")
#         b.grid(row=i+10, column=j+1)



mainloop()# root.mainloop()

