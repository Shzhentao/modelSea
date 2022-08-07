import os
from subprocess import call


def imgMultidownloader(pdfurl, localPdfName):
    IDM = "C:\\Program Files (x86)\\Internet Download Manager\\IDMan.exe"
    call([IDM, '/d', pdfurl, '/p', os.path.abspath(localPdfName), '/f', os.path.basename(localPdfName), '/a'])
    call([IDM, '/s'])


if __name__ == "__main__":
    lines = open("download.txt", "r", encoding="utf-8").readlines()
    for line in lines:
        url = line.strip().split(" ")[-1]
        dirsss = line.strip().split(" ")[-2].replace("$DLFOLDER", "amicorpus")
        os.makedirs(dirsss, exist_ok=True)
        imgMultidownloader(url, dirsss)