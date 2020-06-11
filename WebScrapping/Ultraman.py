import requests
from bs4 import BeautifulSoup

url = 'http://www.scifijapan.com/articles/2015/10/04/bandai-ultraman-ultra-500-figure-list/' # url yang akan discrap

data = requests.get(url) # request url 

page_soup = BeautifulSoup(data.text, 'html.parser') # memasukkan page dalam bentuk html ke dalam variabel page_soup

storage = []    # memilah page dalam bentuk html yg berawalan <p> dan <strong> dan memasukkannya ke dalam storage
for p in page_soup.find_all('p'):
    for strong in p.find_all('strong'):
        storage.append(strong.text)

ultraman_dirty = storage[0:(storage.index('Ultra Monster 500/ ウルトラ怪獣５００'))] #slicing ultraman berdasarkan kalimat yang memisahkan ultraman dan monster yaitu Ultra Monster 500/ ウルトラ怪獣５００ 
monster_dirty = storage[(storage.index('Ultra Monster 500/ ウルトラ怪獣５００')):] #slicing monster

#Cleaning Data

ultraman = ultraman_dirty[2:]
monster = monster_dirty[1:monster_dirty.index('73 Judah Spectre')+1]

#Make it Prettier

ultraman_pretty = "" # agar tiap item dalam list ditampilkan di baris baru
monster_pretty = "" # agar tiap item dalam list ditampilkan di baris baru

for i in ultraman:
    ultraman_pretty+=f'{i} \n'

for j in monster:
    monster_pretty+=f'{j} \n'  

print(" ")
print(r" | |  | | | |                                  ")
print(r" | |  | | | |_ _ __ __ _ _ __ ___   __ _ _ __  ")
print(r" | |  | | | __| '__/ _` | '_ ` _ \ / _` | '_ \ ")
print(r" | |__| | | |_| | | (_| | | | | | | (_| | | | |")
print(r"  \____/|_|\__|_|  \__,_|_| |_| |_|\__,_|_| |_|")
print(ultraman_pretty) # dalam bentuk list
print("")
print("")
print(r" |  \/  |               | |           ")
print(r" | \  / | ___  _ __  ___| |_ ___ _ __ ")
print(r" | |\/| |/ _ \| '_ \/ __| __/ _ \ '__|")
print(r" | |  | | (_) | | | \__ \ ||  __/ |   ")
print(r" |_|  |_|\___/|_| |_|___/\__\___|_    ")
print(monster_pretty) # dalam bentuk list
print(" ")
            

