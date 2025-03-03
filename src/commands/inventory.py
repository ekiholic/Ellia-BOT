from os import path

box_path = "Users/User_bestiary/"

def save_bestiary(id):
    global box_path

    with open(box_path + id[0], 'a') as f:
        f.write(id[1] + "\n")

def check_mob(userid, mob):
    with open("Useful/Unit_by_element.txt", "r", encoding="utf-8") as f:
        list = f.readlines()
    if mob+'\n' not in list: 
        return 2
    with open(box_path + userid, "r") as f:
        lines = f.readlines()
    if mob+'\n' not in lines:
        return 1
    else:
        return 0

def get_elem_emote(elem):
    if elem == "[Light]\n":
        return("<:ellia_light:977122506223808512>")
    if elem == "[Dark]\n":
        return("<:ellia_dark:977122506085388308>")
    if elem == "[Fire]\n":
        return("<:ellia_fire:977122505854701630>")
    if elem == "[Wind]\n":
        return("<:ellia_wind:977122506156695552>")
    if elem == "[Water]\n":
        return("<:ellia_water:977122506207023154>")

def get_grade(mob):
    stars = ""
    star = "<:ellia_star:976853657540767835>"
    if path.exists('assets/Monsters/3_ld/' + mob):
        stars = f'{star}{star}{star}'
    elif path.exists('assets/Monsters/4_ld/' + mob) or path.exists('assets/Monsters/4_elem/' + mob):
        stars = f'{star}{star}{star}{star}'
    elif path.exists('assets/Monsters/5_ld/' + mob) or path.exists('assets/Monsters/5_elem/' + mob):
        stars = f'{star}{star}{star}{star}{star}'
    return stars

def get_element(mob):
    with open('Useful/Unit_by_element.txt', 'r', encoding='utf-8') as f:
        elem = ""

        for i in f:
            if i == "[Light]\n" or i == "[Dark]\n" or i == "[Fire]\n" or i == "[Water]\n" or i == "[Wind]\n":
                elem = i
            if i[:-1] == mob:
                return elem
    return ("")

def sort_monster(element, etoile, mob):
    star = "<:ellia_star:976853657540767835>"
    grade = ""
    elems = []
    if element == "Light & Dark":
        elems.append("[Light]\n")
        elems.append("[Dark]\n")
    elif element == "Elementaires":
        elems.append("[Fire]\n")
        elems.append("[Wind]\n")
        elems.append("[Water]\n")
    elif element != "":
        elems.append(element)
    if element != "":
        if get_element(mob) not in elems:
            return (1)
    if etoile != "":
        if etoile == "3":
            grade = star+star+star
        elif etoile == "4" :
            grade = star+star+star+star
        elif etoile == "5":
            grade = star+star+star+star+star
        if grade != get_grade(mob):
            return (1)
    return (0)

def delete_mob(userid, mob):
    done = 0

    with open(box_path + userid, "r") as f:
        lines = f.readlines()
    with open(box_path + userid, "w") as f:
        for line in lines:
            if line.lower() != mob.lower()+"\n":
                f.write(line)
            if line.lower() == mob.lower()+"\n":
                if done == 1:
                    f.write(line)
                else:
                    done = 1
    return