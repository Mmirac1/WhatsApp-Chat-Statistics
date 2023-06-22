names = {}
def calculate(file):
    try:
        with open(file, "r", encoding="utf-8") as dosya:

            #if dosya.readline().find(": ") == -1: dosya.seek(0)   # Grup ilk açıldığında oluşan sistem bildirimi var mı

            for msg in dosya.readlines():
                try:
                    if not msg.find(' - ') == -1 and not msg.find(': ') == -1 and msg.find("‎")  == -1:   # Sistem bildirimlerini çıkartır
                        if not msg[16:21].find('+') == -1: noName = True    # İsim mi yoksa numara mı diye kontrol eder
                        else: noName = False

                        info = msg[0:msg.find(': ')].split()    # Mesajdan önceki info kısmı
                        text = (len(msg[msg.find(': '):].split()) - 1)  # Mesajdaki kelime sayısı

                        day, month, year, time = info[0], info[1], info[2], info[3]

                        if noName:  name = str(msg[(msg.find('+')-1):msg.find(': ')])   # İsim numaraysa name = numara olur
                        elif len(info) > 6 :    name = str(info[5]) +' '+ str(info[6])  # İsim 2 kelimeden oluşuyorsa
                        else:   name = str(info[5])
                        
                        if name in names:   
                            names[name]["messages"] += 1
                            names[name]["words"] += text
                        else:   names[name]={"messages":1, "words":text}     # Kişinin adı listede yoksa(İlk mesajı ise) kaydeder

                    else: continue
                except: continue
        return names
    except: return "eror"