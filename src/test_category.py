import numpy as np
import string

panjang = 0
tinggi = 0
status = "Status"

print("Panjang/Tinggi: ")
param = input()

if(string.capwords(param) == "Panjang"):
    print("Masukkan panjang anak: ")
    panjang = float(input())
elif(string.capwords(param) == "Tinggi"):
    print("Masukkan tinggi anak: ")
    tinggi = float(input())
else:
    print("Data not found!")

print("Masukkan jenis kelamin: ")
gender = input()
print("Masukkan umur: ")
umur = int(input())

"""
keterangan:
    th1 = -3SD
    th2 = -2SD
    th3 = -1SD
    th4 = median
    th5 = +1SD
    th6 = +2SD
    th7 = +3SD
"""

if(string.capwords(gender) == "Laki-laki"):
    if(umur>=0 and umur <=24 and string.capwords(param) == "Panjang"):
        print("Penggolongan Panjang Badan (Laki-laki => 0-24)")
        th1 = (0.0031*((umur+1)**3)) - (0.1685*((umur+1)**2)) + (3.7408*(umur+1)) + 41.996
        th2 = (0.0031*((umur+1)**3)) - (0.1680*((umur+1)**2)) + (3.7738*(umur+1)) + 43.864
        th3 = (0.0032*((umur+1)**3)) - (0.1678*((umur+1)**2)) + (3.8046*(umur+1)) + 45.782
        th4 = (0.0032*((umur+1)**3)) - (0.1678*((umur+1)**2)) + (3.8395*(umur+1)) + 47.651
        th5 = (0.0032*((umur+1)**3)) - (0.1674*((umur+1)**2)) + (3.8701*(umur+1)) + 49.566
        th6 = (0.0029*((umur+1)**3)) - (0.1582*((umur+1)**2)) + (3.8297*(umur+1)) + 51.565
        th7 = (0.0032*((umur+1)**3)) - (0.1659*((umur+1)**2)) + (3.9249*(umur+1)) + 53.358
    elif(umur>=24 and umur <=60 and string.capwords(param) == "Tinggi"):
        print("Penggolongan Tinggi Badan (Laki-laki => 24-60)")
        th1 = (0.4932*(umur-24)) + 78.265
        th2 = (0.5361*(umur-24)) + 81.368
        th3 = (0.5784*(umur-24)) + 84.491
        th4 = (0.6213*(umur-24)) + 87.597
        th5 = (0.6634*(umur-24)) + 90.717
        th6 = (0.7063*(umur-24)) + 93.826
        th7 = (0.7500*(umur-24)) + 96.918
    else:
        print("Data not found!")

elif(string.capwords(gender) == "Perempuan"):
    if(umur>=0 and umur <=24 and string.capwords(param) == "Panjang"):
        print("Penggolongan Panjang Badan (Perempuan => 0-24)")
        th1 = (0.0026*((umur+1)**3)) - (0.1390*((umur+1)**2)) + (3.2942*(umur+1)) + 41.667
        th2 = (0.0026*((umur+1)**3)) - (0.1415*((umur+1)**2)) + (3.3779*(umur+1)) + 43.453
        th3 = (0.0026*((umur+1)**3)) - (0.1422*((umur+1)**2)) + (3.4457*(umur+1)) + 45.262
        th4 = (0.0027*((umur+1)**3)) - (0.1430*((umur+1)**2)) + (3.5099*(umur+1)) + 47.099
        th5 = (0.0027*((umur+1)**3)) - (0.1451*((umur+1)**2)) + (3.5895*(umur+1)) + 48.898
        th6 = (0.0028*((umur+1)**3)) - (0.1471*((umur+1)**2)) + (3.6650*(umur+1)) + 50.724
        th7 = (0.0028*((umur+1)**3)) - (0.1481*((umur+1)**2)) + (3.7327*(umur+1)) + 52.533
    elif(umur>=24 and umur <=60 and string.capwords(param) == "Tinggi"):
        print("Penggolongan Tinggi Badan (Perempuan => 24-60)")
        th1 = (0.5237*(umur-24)) + 76.477
        th2 = (0.5664*(umur-24)) + 79.696
        th3 = (0.6087*(umur-24)) + 82.945
        th4 = (0.6502*(umur-24)) + 86.181
        th5 = (0.6922*(umur-24)) + 89.431
        th6 = (0.7340*(umur-24)) + 92.673
        th7 = (0.7770*(umur-24)) + 95.896
    else:
        print("Data not found!")

else:
    print("Data not found!")

print(th1, th2, th3, th4, th5, th6, th7)

if(string.capwords(param) == "Panjang"):
    print("PB/U")
    if(panjang<th1):
        status = "severely_stunted"
    elif(panjang>=th1 and panjang<th2):
        status = "stunted"
    elif(panjang>=th2 and panjang<=th7):
        status = "normal"
    elif(panjang>th7):
        status = "tinggi"

elif(string.capwords(param) == "Tinggi"):
    print("TB/U")
    if(tinggi<th1):
        status = "severely_stunted"
    elif(tinggi>=th1 and tinggi<th2):
        status = "stunted"
    elif(tinggi>=th2 and tinggi<=th7):
        status = "normal"
    elif(tinggi>th7):
        status = "tinggi"

else:
    print("Data not found!")

print("Status anak: ", status)