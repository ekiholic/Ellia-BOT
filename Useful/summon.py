from doctest import debug_script
import os
import random
from tabnanny import check
import time
import pickle
import discord
from discord.ext import commands

TOKEN = ""
GUILD2 = "Raoq Gang"
servers = [976120059598610462, 738379299962355813, 340556133280251906] # EBT, RG, Fukoudane

box_path = "../Users/User_bestiary/"
summoner_box = {}

def save_bestiary(id):
    global summoner_box
    global box_path
    with open(box_path + id[0], 'wb') as f:
        pickle.dump(id[1], f)

def read_bestiary(id):
    global box_path
    with open(box_path + id, 'rb') as f:
        pi = pickle.load(f)
    print(pi)

data = ["147746286383136769", "Karnal"]
read_bestiary(data[0])