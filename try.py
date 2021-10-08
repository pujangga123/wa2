import time

from ext_wa import Wa

wa = Wa()
wa.open()

# nomor telepon diawali 2 digit kode negara + no HP tanpa "0" di depan
wa.send_message_to("628156083740", "Percobaan")
time.sleep(wa.delay_wa_load)
wa.send_message_to("628156083740", "Percobaan 2")