# wa2

**Project WA2** adalah program untuk WA Blast.
_Blast/Mass broadcast WA_ sendiri adalah sesuatu yang tidak didukung oleh WA bahkan berusaha dibatasi, oleh sebab itu program _WA blast_ selalu berubah. Setiap update dilakukan oleh WA memerlukan update pada script ini juga.

### Prasyarat:
- Instalasi Google Chrome. Pada versi ini (2021-10-22) digunakan chrome driver 94 
- Pastikan chrome driver sudah terpasang di folder drivers
- Instalasi Python. Pada saat dikembangkan, digunakan Python 3.7
- Install package yang diperlukan menggunakan ```pip install -r requirements.txt```

### penggunaan:
1.  Lewat CLI
    ```python wagui2.pyw```
2.  Lewat GUI:
    Double klik ```wagui2.pyw```, atau Anda bisa membuat shortcut ke file ini.

### Maintenance:
- Sewaktu-waktu WhatsApp akan melakukan update para yang menyebabkan perubahan struktur tag HTML nya. Jika itu terjadi, update file ```xpath.json```
- Jika ada pembaharuan Chrome maka pembaharuan Chrome Driver perlu dilakukan. Download Chrome Driver di https://chromedriver.chromium.org/downloads, extract file zip, simpan di folder drivers.
