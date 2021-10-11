import time

from ext_wa import Wa

wa = Wa(verbose=True)
wa.open()  # open WA for device link

# nomor telepon diawali 2 digit kode negara + no HP tanpa "0" di depan
wa.send_message_to("628156083740", "Percobaan")
wa.send_message_to("628156083740", "Percobaan 2")

