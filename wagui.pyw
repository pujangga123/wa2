from tkinter import *
from ext_wa import Wa
from threading import Thread

force_stop = False

class SendMessages(Thread):    
    def run(self):
        force_stop = False
        content = target.get("1.0",END)

        rows = content.split("\n")
        n = 1
        log("Prep session & linking device...")
        
        wa = Wa()
        wa.open()
        berhasil = 0
        gagal = 0
        for row in rows:
            if row != "":
                try:
                    arow = row.split("\t")
                    number = arow[0]
                    msg = arow[1]
                    if number=="" or msg =="":
                        raise ValueError()                
                    log("sending to "+number+": "+msg)
                    if wa.send_message_to(number,msg):
                        log("✔ message sent to "+number )
                        berhasil += 1
                    else:
                        log("❌ cannot send to "+number)
                        gagal += 1
                except Exception as e:
                    log("invalid data on row "+str(n))
            n += 1
            if force_stop:
                log("Force Stop")
                return 
        log("======= Pengiriman selesai =======")
        log(" Terkirim = "+str(berhasil))
        log(" Gagal = "+str(gagal))
        log("==================================")

def log(text):
    from datetime import datetime
    now = datetime.now()
    result.insert(END,now.strftime("%H:%M:%S")+" > "+text+"\n")
    result.see("end")
    

def send_messages():
    sm = SendMessages()
    sm.start()

def stop_click():
    force_stop = True

win = Tk()
win.title("WA2 GUI")
win.geometry("500x600")
f1 = Frame(win)
f1.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)

target = Text(f1, height=15)
target.pack()
btn = Button(f1, text="Proses", command=send_messages)
btn.pack(fill=X)
stop_button = Button(f1, text="Stop", command=stop_click)
stop_button.pack(fill=X)

result = Text(f1,height=15, foreground="white", background="black")
result.pack(pady=10)

win.mainloop()