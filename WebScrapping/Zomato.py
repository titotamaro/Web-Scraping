import requests

user_key = "95175c79b787c7dd4265272c6271ae8b" # api_keys

print("1. Cari Restoran") # input untuk mencari resto
print("2. Daily Menu") # input untuk daily menu (hanya tersedia di Prague)
pilih = input("Masukkan pilihan: ")

headInfo = {'user-key':user_key} # headinfo untuk isi headers, bila tidak ada ini maka response akan error

if pilih == "1":
    try:
        user_input = input("Masukkan nama kota: ").lower() # nama kota menggunakan lowercase
        if user_input.replace(" ","").isalpha() == True: # Error Handling
            host = "https://developers.zomato.com/api/v2.1/" # host dari api url
            city = "cities?q=" # pemanggilan API untuk cities
            headInfo = {'user-key':user_key} # headinfo untuk isi headers, bila tidak ada ini maka response akan error
            
            url = host + city + user_input # url secara lengkap untuk cities 
            data = requests.get(url, headers=headInfo) #pemanggilan dari zomato dan dimasukkan dalam variabel data
            data = data.json() # data diubah menjadi bentuk json
        
            id_cities = data["location_suggestions"][0]["id"] # pemanggilan id_cities dari API
            search = f"search?entity_id={id_cities}&entity_type=city" #pemanggilan search dari API menggunakan id_cities sebagai komponen url
            url_jumlah_resto = host + search # url untuk mencari jumlah resto
            data_jml = requests.get(url_jumlah_resto, headers=headInfo) # pemanggilan dari zomato dan dimasukkan dalam variabel data2
            data_jml = data_jml.json() # data diubah menjadi bentuk json


            url2 = f"https://developers.zomato.com/api/v2.1/location_details?entity_id={id_cities}&entity_type=city"
            data2 = requests.get(url2, headers=headInfo) # pemanggilan dari zomato dan dimasukkan dalam variabel data2
            data2 = data2.json() # data diubah menjadi bentuk json

            jumlah_resto = data_jml["results_found"] #jumlah resto
            if jumlah_resto > 0: # pengecekan jumlah restoran
                print(f"Jumlah restoran di kota tersebut adalah: {jumlah_resto}") #user output
                display = int(input("Jumlah Restaurant yang akan ditampilkan: "))
                temp = 1
                for i in data2['best_rated_restaurant']:
                    if temp < jumlah_resto:
                        print(f"Nama Restoran:      {i['restaurant']['name']}") #user output
                        print(f"Jenis Restoran:     {i['restaurant']['establishment'][0]}")#user output
                        print(f"Cuisines:           {i['restaurant']['cuisines']}")#user output
                        print(f"Alamat:             {i['restaurant']['location']['address']}") #user output
                        print(f"Rating:             {i['restaurant']['user_rating']['aggregate_rating']}") #user output
                        print(f"Nomor Telepon:      {i['restaurant']['phone_numbers']}") #user output
                        print(" ")
                        temp += 1
        else: # apabila jumlah resto 0
            print("Tidak ada restoran Zomato di daerah ini") # Error Output
    except:
        print("Invalid Input!") # Error Output   

elif pilih == "2":
    nama_resto = input("Masukkan Nama Resto : ").lower() # input nama resto
    nama_kota_resto = input("Masukkan Nama Kota : ").lower() # input kota resto
    url_kota_resto = f"https://developers.zomato.com/api/v2.1/locations?query={nama_kota_resto}&count=1" # url kota resto
    
    data_kota_resto = requests.get(url_kota_resto, headers=headInfo) # pemanggilan data menggunakan API
    data_kota_resto = data_kota_resto.json() # mengubah data menjadi json

    entity_type_resto = data_kota_resto['location_suggestions'][0]['entity_type'] # untuk entity type
    id_cities_resto = data_kota_resto['location_suggestions'][0]['entity_id'] # untuk city id
    url_resto_daily = f"https://developers.zomato.com/api/v2.1/location_details?entity_id={id_cities_resto}&entity_type={entity_type_resto}" # url lengkap

    data_resto_daily = requests.get(url_resto_daily, headers=headInfo) # pemanggilan data untuk daily menu
    data_resto_daily = data_resto_daily.json() # mengubah data menjadi json
    restoran = False
    for i in data_resto_daily['best_rated_restaurant']: # pengecekan Restoran sesuai input nama resto dan kota
        if i['restaurant']['name'].lower() == nama_resto:
            id_resto = i['restaurant']['R']['res_id']
            restoran = True
            break

    if restoran == True:
        url_daily = f"https://developers.zomato.com/api/v2.1/dailymenu?res_id={id_resto}" # url untuk daily menu
        data_daily = requests.get(url_daily, headers=headInfo) # pemanggilan API
        data_daily = data_daily.json() # mengubah data menjadi json
        print("Menu yang tersedia:") # user output
        try:
            for i in data_daily['daily_menus'][0]['daily_menu']['dishes']:
                print(f"- {i['dish']['name']}") # user output
        except:
            print(f"{data_daily['message']}") # user output 
    elif restoran == False:
        print("Nama Resto Tidak Tersedia") # Error Output

else:
    print('Invalid Input!') #Error Output



