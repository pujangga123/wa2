import time

from ext_wa import Wa

wa = Wa()
wa.open()

#time.sleep(wa.delay_wa_load) # waktu tunggu WA terbuka
#while not wa.is_ready(wa.path_msg):
#    time.sleep(10)

# nomor telepon diawali 2 digit kode negara + no HP tanpa "0" di depan
wa.send_message_to("628156083740", "Percobaan")
time.sleep(wa.delay_wa_load)
wa.send_message_to("628156083740", "Percobaan 2")