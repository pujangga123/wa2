from tkinter import *

win = Tk()
win.title("WA2 GUI")
win.geometry("500x600")
f1 = Frame(win)
f1.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)

target = Text(f1, height=15)
target.pack()
btn = Button(f1, text="Proses")
btn.pack(fill=X)

result = Text(f1,height=15, foreground="white", background="black")
result.pack(pady=10)

win.mainloop()