import time

from ext_wa import Wa

wa = Wa(verbose=True) # verbose = True : untuk debug mode
wa.open()

if not wa.send_message_to('62853149286580',"Percobaan"):
    print("Fail 0")

if not wa.send_message_to('6281560837400',"barbie cantik"):
    print("Fail 1")

if not wa.send_message_to('0839218301280',"kjflsjkflaksjd"):
    print("Fail 2")

if not wa.send_message_to('62853149286580',"percobaan 2"):
    print("Fail 3")
    