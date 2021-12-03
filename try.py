import time

from ext_wa import Wa

# driver disesuaikan dengan versi yang digunakan
driver = "drivers\\chromedriver96.exe"

wa = Wa(verbose=True, path_driver=driver)
wa.open()  # open WA for device link

# nomor telepon diawali 2 digit kode negara + no HP tanpa "0" di depan
wa.send_message_to("628156083740", "Percobaan")

