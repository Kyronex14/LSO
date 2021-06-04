# Creating and removing swap space in Linux operating system. Please respect the effort
# Linux işletim sisteminde swap alanı oluşturup kaldırmak. Lütfen verilen emeğe sayı gösterin.

import os
import sys
import time

# * a control function for swap


def has_swap():
    with open("/etc/fstab", "r") as reader:
        if reader.read().find("swap") != -1:
            return True
        return False

# * function to delelete swap



def delete_swap():
    satir = 0
    try:
        os.system("sudo swapoff -v /swapfile")
        os.system("sudo rm /swapfile")

        def sil(satir):
            f.seek(0)
            satirlar = f.readlines()
            satirlar.pop(satir)
            print(satirlar)
            os.remove("/etc/fstab")
            nf = open("/etc/fstab","w")
            for line2 in satirlar:
               nf.write(line2)


        with open("/etc/fstab") as f:
               for line in f.readlines():
                   satir+=1
                   if("swap" in line):
                       sil(satir - 1)

    except Exception as e:
        if language == '1':
            print('There was an error while deleting the swap.')
            print('Error description:', e)
        else:
            print('Swap silinirken bir hata çıktı.')
            print('Hata açıklaması:', e)

    if language == "1":
        print('Swap deleted succesfully!')
    else:
        print('Swap silindi!')

# * function to add swap


def add_swap(size):
    try:
        os.system("sudo fallocate -l {}M /swapfile".format(size))
        os.system("sudo chmod 600 /swapfile")
        os.system("sudo mkswap /swapfile")
        os.system("sudo swapon /swapfile")

        with open("/etc/fstab", "a") as writer:
            writer.write("/swapfile none swap defaults 0 0")
    except Exception as e:
        if language == '1':
            print('There was an error while deleting the swap.')
            print('Error description:', e)
        else:
            print('Swap silinirken bir hata çıktı.')
            print('Hata açıklaması:', e)

    if language == "1":
        print('Swap added succesfully.')
    else:
        print("Swap alanı başarıyla eklendi!")


print("Swap Area Transactions\n")
print('Swap Alanı Kontrolcüsü')
print("Choose a language/Bir dil seçiniz.\n")

language = input("1-Türkçe/2-English\n")

if (language == "1"):

    print("Hangi işlemi yapmak istiyorsunuz?\n")

    process = input("1-Swap alanı oluşturma/2-Swap alanı silme\n")
    if (process == "1"):
        if has_swap():
            print("Swap alanı zaten mevcut!")
            sys.exit()

        size = int(
            input("Kaç GB alan ayırmak istiyorsunuz? (1-2 GB şeklinde...)")) * 1024
        print('Ayırılacak alan:', size, type(size))

        print("İşlemler başlıyor..\n")
        time.sleep(3)
        add_swap(size)

        do_reboot = input("Sistem yeninden başlatılsın mı?  e/h\n")
        if (do_reboot == "e"):
            os.system("reboot")
        else:
            sys.exit()

    if (process == "2"):
        do_continue = input(
            "Bu işlem, Swap alanı sonradan oluşturulmamış ise hatalarla sonuçlanabilir, devam etmek istiyor musunuz?  e/h")

        if (do_continue == "e"):
            print("İşlemler başlıyor..")
            time.sleep(3)

            if not has_swap():
                print("Swap alanı zaten mevcut değil!")
                sys.exit()

            delete_swap()

if (language == "2"):
    print("What action do you want to take?\n")

    process = input("1-Creating a swap area/2-Deleting a swap area\n")
    if (process == "1"):
        if has_swap():
            print("Swap space already exists!")
            sys.exit()

        size = int(input(
            "How many GB of space do you want to allocate? (in the form of 1-2 GB...)")) * 1024
        print('Size to allocate (mb):', size, type(size))
        print("Process is starting...\n")
        time.sleep(3)

        add_swap(size)

        end = input("Reboot the system? y/n\n")
        if (end == "y"):
            os.system("reboot")
        else:
            sys.exit()

    if (process == "2"):
        do_continue = input(
            "This operation may cause minor errors if the swap space is not created afterwards, do you want to continue?  y/n")

        if (do_continue == "e"):
            print("Operations begin..")
            time.sleep(3)

            if not has_swap():
                print("Swap space already does not exist!")
                sys.exit()

            delete_swap()
