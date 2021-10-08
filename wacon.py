import time

from ext_wa import Wa

wa = Wa(verbose=True) # verbose = True : untuk debug mode
wa.open()
# programm akan lanjut setelah user scan QR WhatsApp

#time.sleep(wa.delay_wa_load) # waktu tunggu WA terbuka
#while not wa.is_ready(wa.path_msg):
#    time.sleep(10)

# nomor telepon diawali 2 digit kode negara + no HP tanpa "0" di depan
nomor = "628156083742" # nomor dummy, ganti dengan nomor valid.
wa.send_message_to(nomor, "Percobaan")
time.sleep(wa.delay_wa_load)
wa.send_message_to(nomor, "Percobaan 2")