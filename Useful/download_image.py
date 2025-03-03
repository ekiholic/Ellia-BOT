import requests
import json
import os
import csv
import urllib

from sqlalchemy import false

fields = ["name", "image_filename"]

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def main():
    img = "https://swarfarm.com/static/herders/images/monsters/"
    path = "assets/Monsters/"
    light_3 = "https://swarfarm.com/api/v2/monsters/?page_size=30&natural_stars=3&element=light&awaken_level=1&can_awaken=true"
    dark_3 = "https://swarfarm.com/api/v2/monsters/?page_size=30&natural_stars=3&element=dark&awaken_level=1&can_awaken=true"
    fire_4 = "https://swarfarm.com/api/v2/monsters/?page_size=30&natural_stars=4&element=fire&awaken_level=1&can_awaken=true"
    water_4 = "https://swarfarm.com/api/v2/monsters/?page_size=30&natural_stars=4&element=water&awaken_level=1&can_awaken=true"
    wind_4 = "https://swarfarm.com/api/v2/monsters/?page_size=30&natural_stars=4&element=wind&awaken_level=1&can_awaken=true"
    light_4 = "https://swarfarm.com/api/v2/monsters/?page_size=30&natural_stars=4&element=light&awaken_level=1&can_awaken=true"
    dark_4 = "https://swarfarm.com/api/v2/monsters/?page_size=30&natural_stars=4&element=dark&awaken_level=1&can_awaken=true"
    fire_5 = "https://swarfarm.com/api/v2/monsters/?page_size=30&natural_stars=5&element=fire&awaken_level=1&can_awaken=true"
    water_5 = "https://swarfarm.com/api/v2/monsters/?page_size=30&natural_stars=5&element=water&awaken_level=1&can_awaken=true"
    wind_5 = "https://swarfarm.com/api/v2/monsters/?page_size=30&natural_stars=5&element=wind&awaken_level=1&can_awaken=true"
    dark_5 = "https://swarfarm.com/api/v2/monsters/?page_size=30&natural_stars=5&element=dark&awaken_level=1&can_awaken=true"
    light_5 = "https://swarfarm.com/api/v2/monsters/?page_size=30&natural_stars=5&element=light&awaken_level=1&can_awaken=true"

    f = open('Unit_by_element.txt', 'w+')

    f.write("[Light]\n")

    res = []
    res = raw_data_to_monster_list(get_all_monster(light_3))
    print("Sorting mob by element...")
    for monster in res:
        f.write(monster[0] + "\n")
    print("Done !\n")

    res = []
    res = raw_data_to_monster_list(get_all_monster(light_4))
    print("Sorting mob by element...")
    for monster in res:
        f.write(monster[0] + "\n")
    print("Done !\n")

    res = []
    res = raw_data_to_monster_list(get_all_monster(light_5))
    print("Sorting mob by element...")
    for monster in res:
        f.write(monster[0] + "\n")
    print("Done !\n")

    f.write("[Dark]\n")
    res = []
    res = raw_data_to_monster_list(get_all_monster(dark_3))
    print("Sorting mob by element...")
    for monster in res:
        f.write(monster[0] + "\n")
    print("Done !\n")

    res = []
    res = raw_data_to_monster_list(get_all_monster(dark_4))
    print("Sorting mob by element...")
    for monster in res:
        f.write(monster[0] + "\n")
    print("Done !\n")

    res = []
    res = raw_data_to_monster_list(get_all_monster(dark_5))
    print("Sorting mob by element...")
    for monster in res:
        f.write(monster[0] + "\n")
    print("Done !\n")

    f.write("[Fire]\n")
    res = []
    res = raw_data_to_monster_list(get_all_monster(fire_4))
    print("Sorting mob by element...")
    for monster in res:
        f.write(monster[0] + "\n")
    print("Done !\n")

    res = []
    res = raw_data_to_monster_list(get_all_monster(fire_5))
    print("Sorting mob by element...")
    for monster in res:
        f.write(monster[0] + "\n")
    print("Done !\n")

    f.write("[Water]\n")
    res = []
    res = raw_data_to_monster_list(get_all_monster(water_4))
    print("Sorting mob by element...")
    for monster in res:
        f.write(monster[0] + "\n")
    print("Done !\n")

    res = []
    res = raw_data_to_monster_list(get_all_monster(water_5))
    print("Sorting mob by element...")
    for monster in res:
        f.write(monster[0] + "\n")
    print("Done !\n")

    f.write("[Wind]\n")
    res = []
    res = raw_data_to_monster_list(get_all_monster(wind_4))
    print("Sorting mob by element...")
    for monster in res:
        f.write(monster[0] + "\n")
    print("Done !\n")

    res = []
    res = raw_data_to_monster_list(get_all_monster(wind_5))
    print("Sorting mob by element...")
    for monster in res:
        f.write(monster[0] + "\n")
    print("Done !\n")



def get_all_monster(url):
    print("Downloading all monsters.. ")
    res = []
    while not url is None:
        print(url)
        resp = requests.get(url)
        res += [resp]
        url = resp.json().get("next")
    return res

def raw_data_to_monster_list(raw_datas):
    print("Reading all datas..")
    res = []
    for raw_data in raw_datas:
        monsters = raw_data.json().get("results")
        for monster in monsters :
            res += [[monster.get(i) for i in fields]]

    print("Monster found : ",len(res))
    return res

main()