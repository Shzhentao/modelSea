import os
from subprocess import call
import time

def imgMultidownloader(pdfurl, localPdfName):
    IDM = "C:\\Program Files (x86)\\Internet Download Manager\\IDMan.exe"
    call([IDM, '/d', pdfurl, '/p', os.path.abspath(localPdfName), '/f', os.path.basename(localPdfName), '/a'])
    call([IDM, '/s'])


if __name__ == "__main__":
    lines = open("download.txt", "r", encoding="utf-8").readlines()
    for line in lines:
        url = line.strip().split(" ")[-1]
        dirsss = line.strip().split(" ")[-2].replace("$DLFOLDER", "amicorpus")
        name = url.split("audio/")[-1]
        target = dirsss + "/" + name
        os.makedirs(dirsss, exist_ok=True)
        if os.path.exists(target):
            continue
        imgMultidownloader(url, target)
        while True:
            time.sleep(1)
            if os.path.exists(target):
                break