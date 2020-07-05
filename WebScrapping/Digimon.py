# Web Scraping menggunakan BeautifulSoup dan input hasil scraping ke dalam mySQL menggunakan mysql.connector

import requests
import mysql.connector
from bs4 import BeautifulSoup
from mysql.connector import errorcode


url = 'http://digidb.io/digimon-list/' # url yang akan discrap

data = requests.get(url) # menyimpan isi dari url ke dalam variabel data
soup = BeautifulSoup(data.text, 'html.parser') # memasukkan data bentuk html ke variabel soup

# FINDING ALL DIGIMON
storage = []
for a in soup.find_all('a'):
    storage.append(a.text)
# print(storage) --> Checking result

# CLEANING DATA DIGIMON

digimon = storage[storage.index('Kuramon'):storage.index('Gallantmon NX')+1] #slicing dari Kuramon ke Gallantmon NX    
# print(digimon) --> Checking result
# print(len(digimon)) --> Checking if total digimon is 341 which is true

# FINDING IMAGE OF ALL DIGIMON
storage_img = []
for img in soup.find_all('img'):
    storage_img.append(img['src']) #memunculkan isi '<img src=' dari html
# print(storage_img) --> Checking result

# CLEANING DATA IMAGE OF ALL DIGIMON

image = storage_img[storage_img.index('http://digidb.io/images/dot/dot629.png'):storage_img.index('http://digidb.io/images/dot/dot905.png')+1] #slicing dari image Kuramon ke image Gallantmon NX
# print(image) --> Checking result
# print(len(image)) --> Checking if total digimon is 341 which is true

# STAGE, TYPE, ATTRIBUTE ALL DIGIMON
storage_stage = []
for stage in soup.find_all('tr'):
    temp = []
    for j in stage.find_all('td'):
        temp.append(j.text)
    storage_stage.append(temp)    
# print(storage_stage) #--> Checking result
# print(len(storage_stage))
storage_stage = storage_stage[1:] 

# CLEANING DATA STAGE, TYPE, ATTRIBUTE, DLL ALL DIGIMON
for i in range(len(storage_stage)):
    storage_stage[i].pop(0)
for j in range(len(storage_stage)):
    storage_stage[j].pop(0)     
# print(storage_stage) #--> Checking result      
# print(len(storage_stage))

# PENOMOROAN UNTUK TABEL
nomor = [i for i in range(1,342)] # banyaknya nomor sesuai dengan jumlah digimon

value_to_insert = [] # Merge nomor, digimon, link_image, attribut,dll
for i in range (0,341):
    temp = []
    temp.append(nomor[i])
    temp.append(digimon[i])
    temp.append(image[i])
    temp.extend(storage_stage[i])
    value_to_insert.append(temp)

value_to_insert_tuple = [tuple(l) for l in value_to_insert] # mengubah nested list menjadi tuple

# print(value_to_insert_tuple) #--> Checking value to insert 

# Akses mySQL
namaDB = {
    'user' : 'root',
    'password' : 'cherryblossomtime',
    'host' : 'localhost',
    'database' : 'digimon' #database sudah dibuat lewat command prompt
}

try: # try dan except untuk mengecek koneksi ke server mySQL
    conn = mysql.connector.connect(**namaDB)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Username salah atau Password salah!")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database tidak ditemukan!")
    else:
        print("Gagal koneksi ke database!")
else:
    print("Connected")

    kursor = conn.cursor()

    query1 = "create table digital_monster (nomor int, digimon char(50), link_image char(100), stage char(20), type char(20), attribute char(20), memory int, equip_slots int, HP int, SP int, atk int, def int, intelligence int, spd int)"        
    kursor.execute(query1) #--> Making table digimon
    conn.commit()

    query2 = "insert into digital_monster (nomor,digimon,link_image,stage,type,attribute,memory,equip_slots,HP,SP,atk,def,intelligence,spd) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    value = value_to_insert_tuple # variabel yang akan dimasukkan dalam table dan bentuk datal list
    kursor.executemany(query2,value) # execute many data
    conn.commit() # commit untuk melakukan update etc.
    print(kursor.rowcount, "Data Tersimpan") # jumlah row yang berhasil disimpan


