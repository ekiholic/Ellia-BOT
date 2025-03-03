import random
import os

box_path = "Users/User_bestiary/"

def check_user(userid):
    with open('Users/user_list.txt', 'r+') as myfile:
        if f'{userid}\n' in myfile.read():
            return(0)
        else:
            myfile.write(userid + '\n')
            d = open('Users/User_bestiary/' + userid, 'w')
            d.close()
            return(1)
        
def is_new(id):
    # 0 = new, 1 = dupe
    global box_path
    f = open(box_path + id[0], 'r')
    for i in f:
        mob = id[1] + '\n'
        if mob == i:
            return 1
    return 0
        
def summon_vl():
    name = ""
    roll = random.randrange(10000)
    if roll <= 900:
        name = random.choice(os.listdir("assets/Monsters/5_elem"))
        while name[0] == '.':
            name = random.choice(os.listdir("assets/Monsters/5_elem"))
    else:
        name = random.choice(os.listdir("assets/Monsters/4_elem"))
        while name[0] == '.':
            name = random.choice(os.listdir("assets/Monsters/4_elem"))
    return(name)

def summon_ld():
    name = ""
    roll = random.randrange(10000)
    if roll <= 150:
        name = random.choice(os.listdir("assets/Monsters/5_ld"))
        while name[0] == '.':
            name = random.choice(os.listdir("assets/Monsters/5_ld"))
    elif roll <= 950 and roll > 150:
        name = random.choice(os.listdir("assets/Monsters/4_ld"))
        while name[0] == '.':
            name = random.choice(os.listdir("assets/Monsters/4_ld"))
    else:
        name = random.choice(os.listdir("assets/Monsters/3_ld"))
        while name[0] == '.':
            name = random.choice(os.listdir("assets/Monsters/3_ld"))
    return(name)

def summon_trans():
    name = random.choice(os.listdir("assets/Monsters/5_elem"))
    while name[0] == '.':
        name = random.choice(os.listdir("assets/Monsters/5_elem"))
    return(name)

def summon_trans_ld():
    name = ""
    name = random.choice(os.listdir("assets/Monsters/5_ld"))
    while name[0] == '.':
        name = random.choice(os.listdir("assets/Monsters/5_ld"))
    return(name)