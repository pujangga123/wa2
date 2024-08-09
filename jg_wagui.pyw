from tkinter import *
from tkinter import messagebox, ttk
from ext_wa import Wa, download_xpath_definition
from threading import Thread
import os, fnmatch
import random, csv, time, datetime

force_stop = False
sm = None  # send message thread

class SendMessages(Thread):    
    """
        thread yang bertugas mengirimkan pesan berdasarkan data dan template yang sudah ditentukan.
        ketika SendMessage dijalankan, pastikan data sudah tervalidasi sebelumnya
        pastikan:
        1. content sudah terisi
        2. template sudah terisi
    """
    def run(self):
        force_stop = False
        content = target.get("1.0",END)

        rows = content.split("\n")
        tmp_text = template.get("1.0",END)
        log("Prep session & linking device...")

        drivers = optVariable.get()
        att_file = var_image.get()
        if att_file[0] == "*":
            att_file = ""
        wa = Wa(verbose=True, logging = True,path_driver="drivers\\"+drivers)
        if wa is None:
            log("Chrome driver: incompatible")
            return
        wa.open()
        berhasil = 0
        gagal = 0
        n = 0
        
        #var 20 message
        x = 0
        for row in rows:
            n += 1 #counter pengiriman
            if row != "":
                try:
                    arow = row.split("\t")
                    if len(arow)<1:
                        raise ValueError()
                    number = arow[0] # nomor selalu pada kolom pertama
                    
                    # cek number jika bukan +62
                    if(number[0]=="0"):
                        number = "62"+number[1:]                   
              
                    msg = parse_text(tmp_text, arow)
                    log(str(n)+"# sending to "+number+": "+msg)
                    ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    arow.insert(0, ct)
                    if wa.send_message_to(number,msg,att_file):
                        log("✔ message sent to "+number )
                        berhasil += 1
                        f2 = open('success.csv', 'a+', newline='')
                        writer2 = csv.writer(f2, delimiter=';')
                        writer2.writerow(arow)
                        f2.close()
                    else:
                        log("❌ cannot send to "+number)
                        gagal += 1
                        #jika gagal tulis ke csv
                        f = open('error.csv', 'a+', newline='')
                        writer = csv.writer(f, delimiter=';')
                        writer.writerow(arow)
                        f.close()                    
                except Exception as e:
                    log("invalid data on row "+str(n))

            #antar pengiriman jeda 20 - 60 detik
            delay_rdm = random.randint(20, 60)
            log("tunggu "+str(delay_rdm)+" secs")
            time.sleep(delay_rdm)

            #pengiriman 20 pesan jeda 2 - 5 menit
            x += 1
            if x >= 20:
                delay_rdm2 = random.randint(120, 300)
                log("===== Tunggu "+str(delay_rdm2)+" detik ======")
                time.sleep(delay_rdm2)
                x = 0
                    
            if force_stop:
                log("Force Stop")
                return 

            
        log("======= Pengiriman selesai =======")
        log(" Terkirim = "+str(berhasil))
        log(" Gagal = "+str(gagal))
        log("==================================")

def log(text):
    """
        fungsi menambahkan tulisan pada result
    """
    from datetime import datetime
    now = datetime.now()
    result.insert(END,now.strftime("%H:%M:%S")+" > "+text+"\n")
    result.see("end")
    
def parse_text(tmp_text, datas):
    """
        fungsi untuk parse template (tmp_text) dengan memasukan data (datas)
        datas berupa list
        list[0] adalah {NUMBER}
        list[1] adalah {V1}
        list[2] adalah {V2}
        dst
    """
    n = 0
    for v in datas:
        if n==0:
            tmp_text = tmp_text.replace("{NUMBER}",v)
        else:
            tmp_text = tmp_text.replace("{V"+str(n)+"}",v)
        n += 1
    return tmp_text

def insert_num():
    template.insert(END,"{NUMBER}")

def insert_v1():
    template.insert(END,"{V1}")

def insert_v2():
    template.insert(END,"{V2}")

def insert_v3():
    template.insert(END,"{V3}")

def insert_v4():
    template.insert(END,"{V4}")

def preview_click():
    """
        preview pesan, tampilan template dan di parse dengan variabel
        dengan contoh data baris ke-1
    """
    target_text = target.get("1.0",END).split("\n") # not good, but it works
    datas = target_text[0].split("\t")

    t = template.get("1.0", END)
    parsed = parse_text(t,datas)
    messagebox.showinfo("Preview", parsed )

def send_messages():
    # validasi
    target_text = target.get("1.0",END)
    if len(target_text)<=1:
        messagebox.showerror("Error", "Anda belum menyiapkan data kontak yang akan dikirim")
        return
    
    t = template.get("1.0", END)
    if len(t) <=1 :
        messagebox.showerror("Error", "Anda menyiapkan template text")
        return


    sm = SendMessages()
    sm.start()

def stop_click(): 
    """
        fungsi untuk stop proses
        masih belum berfungsi dengan baik, perlu diperbaiki.
    """
    #force_stop = True
    sm.stop()
    sm.join()

def show_xpath():
    try:
        with open("xpath.json") as f:
            contents = f.read()
        contents = contents.replace("{","")
        contents = contents.replace("}","")
        contents = contents.replace("\n","\n\n")
        contents = contents.replace("  ","")
        messagebox.showinfo("xpath.json",contents)
    except:
        messagebox.showerror("xpath.json", "Definition not found")

def update_xpath():
    """
        Fungsi untuk download xpath dari server
        ini diperlukan kalau ada perubahan struktur di web WhatsApp,
        tentu sebelumnya xpath.json nya harus diupdate dulu (manual)
    """
    download_xpath_definition("https://insite3.jgmmotor.co.id/remote/wa2/xpath.json")
    messagebox.showinfo("","Done")

def open_folder():
    os.system("explorer D:\WA2\images")

def attach_file():
    from tkinter import filedialog as fd
    import shutil

    filetypes = (
        ('jpg', '*.jpg'),
        ('jpeg', '*.jpeg'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Attach Image',
        initialdir='D:\\WA2\\images',
        filetypes=filetypes)

    f = os.path.basename(filename)
    d = os.path.dirname(filename)

    print(filename)
    if filename!="":
        shutil.copyfile(filename, "D:\\WA2\\images\\"+f)
        imglist = fnmatch.filter(os.listdir('images'), '*.jpg') + fnmatch.filter(os.listdir('images'), '*.jpeg')
        imglist.insert(0,"* TANPA GAMBAR *")
        opt_image['values'] = imglist

    

####################################################
# inisialisasi mulai
####################################################

win = Tk()
win.title("WA2 GUI (JG) v240131.1")
win.iconbitmap("wa2.ico")
win.geometry("500x550")
f1 = Frame(win)
f1.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)

"""
    target berisi data yang antar kolomnya dipisah tanda TAB (\t)
    kolom pertama harus nomor telepon, diawali "62"
"""
Label(f1, text="1. Data: antar data dipisah oleh TAB. Kolom pertama harus No WA").pack(fill=X,anchor=W)
target = Text(f1, height=6) 
target.pack()

Label(f1,text="2. Buat template").pack(fill=X,anchor=W)
template = Text(f1, height=8)
template.pack()
f4 = Frame(f1)
f4.pack(fill=X)
attach = Button(f4, text="Attach", command=attach_file)
attach.pack(side=RIGHT)
imglist = fnmatch.filter(os.listdir('images'), '*.jpg') + fnmatch.filter(os.listdir('images'), '*.jpeg')
imglist.insert(0,"* TANPA GAMBAR *")
var_image = StringVar(win)
var_image.set("* TANPA GAMBAR *") # default value
opt_image = ttk.Combobox(f4, textvariable=var_image)
opt_image['values'] = imglist
opt_image.pack(side=RIGHT)
btn_openfolder = Button(f4, text="Open Folder", command=open_folder)
btn_openfolder.pack(side=RIGHT)


f3 = Frame(f1) # panel tombol untuk insert vars
f3.pack(fill=X)
insert_tno = Button(f3, text="Nomor", command=insert_num)
insert_tno.pack(side=LEFT)
insert_tv1 = Button(f3,text="V1", command=insert_v1)
insert_tv1.pack(side=LEFT)
insert_tv2 = Button(f3,text="V2", command=insert_v2)
insert_tv2.pack(side=LEFT)
insert_tv3 = Button(f3,text="V3", command=insert_v3)
insert_tv3.pack(side=LEFT)
insert_tv4 = Button(f3,text="V4", command=insert_v4)
insert_tv4.pack(side=LEFT)
preview = Button(f3, text="Preview", command = preview_click)
preview.pack(side=LEFT)

f2 = Frame(f1) # panel drivers & tombol untuk definisi (show & update)
f2.pack(fill=X, pady=5)
# prep drivers dropdown
Label(f2, text="Driver : ").pack(side=LEFT)
flist = fnmatch.filter(os.listdir('drivers'), '*.exe')
optVariable = StringVar(win)
optVariable.set(flist[0]) # default value
optFiles = OptionMenu(f2, optVariable,*flist)
optFiles.pack(side=LEFT)

showxpath = Button(f2, text="Show Def", command=show_xpath)
showxpath.pack(side=RIGHT)
updatexpath = Button(f2, text="Update Def", command=update_xpath)
updatexpath.pack(side=RIGHT)

f3 = Frame(f1) # panel tombol proses & stop
f3.pack(fill=X)
btn = Button(f3, text="Proses", command=send_messages, background='lightgreen')
btn.pack(fill=X,side=LEFT)
stop_button = Button(f3, text="Stop", command=stop_click)
stop_button.pack(fill=X,side=LEFT)

# result box
result = Text(f1,height=20, foreground="white", background="black")
result.pack()

win.mainloop()