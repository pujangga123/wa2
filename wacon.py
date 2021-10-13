import time

from ext_wa import Wa

wa = Wa(verbose=True) # verbose = True : untuk debug mode
wa.open()


if not wa.send_message_to('628156083740',"percobaan"):
    print("Fail 1")

if not wa.send_message_to('083921830128',"kjflsjkflaksjd"):
    print("Fail 2")
    