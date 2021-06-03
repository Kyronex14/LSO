# Creating and removing swap space in Linux operating system. Please respect the effort
# Linux işletim sisteminde swap alanı oluşturup kaldırmak. Lütfen verilen emeğe sayı gösterin.

import os
import sys
import time


def has_swap():
    with open("/etc/fstab", "r") as reader:
        if reader.read().find("swap") != -1:
            return True
        return False


def delete_swap():
    satir = 0
    try:
        os.system("sudo swapoff -v /swapfile")
        os.system("sudo rm /swapfile")

        def sil(satir):
            f.seek(0)
            satirlar = f.readlines()
            satirlar.pop(satir)
            os.remove("/etc/fstab")
            nf = open("/etc/fstab", "w")
            for line2 in satirlar:
                nf.write(line2)

        with open("/etc/fstab") as f:
            for line in f.readlines():
                satir += 1
                if("swap" in line):
                    sil(satir - 1)

    except Exception as e:
        return 'ERROR'
    return 'SUCCESS'


def add_swap(size):
    try:
        os.system("sudo fallocate -l {}M /swapfile".format(size))
        os.system("sudo chmod 600 /swapfile")
        os.system("sudo mkswap /swapfile")
        os.system("sudo swapon /swapfile")

        with open("/etc/fstab", "a") as writer:
            writer.write("/swapfile none swap defaults 0 0")
    except Exception as e:
        return 'ERROR'
    return 'SUCCESS'