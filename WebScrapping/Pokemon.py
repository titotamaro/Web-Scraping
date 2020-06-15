import requests

user_input = input("Masukkan nama pokemon: ").lower() # user input lowercase

host = "https://pokeapi.co/api/v2/" # pokemon API host
pokemon_name = f"pokemon/{user_input}" # pokemon name
url = host + pokemon_name # complete url

data = requests.get(url) # requests to get url
data = data.json() # change to json 

HP = data["stats"][0]["base_stat"] # HP
Attack = data["stats"][0]["base_stat"] # Attack
Defense = data["stats"][0]["base_stat"] # Defense
Speed = data["stats"][0]["base_stat"] # Speed
Type = data["types"][0]["type"]["name"] # Type

print(" ") # User output
print(f"Nama: {user_input.capitalize()}") # User output
print(f"Attack: {Attack}") # User output
print(f"Defense: {Defense}") # User output
print("Abilities : ") # User output
num = 1
for i in data ['abilities']:
    print(f"{num}. {i['ability']['name']}")
    num += 1
    print(f"Type : {data['types'][0]['type']['name']}")
print(f"Speed: {Speed}") # User output
