import time

from ext_wa import Wa

wa = Wa(verbose=True, path_driver="drivers\\chromedriver94.exe")
wa.open()  # open WA for device link

# nomor telepon diawali 2 digit kode negara + no HP tanpa "0" di depan
wa.send_message_to("628156083740", "Percobaan",paste=True)

