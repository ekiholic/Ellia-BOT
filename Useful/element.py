def get_element(mob):
    f = open('Unit_by_element.txt', 'r')
    elem = ""

    for i in f:
        if i == "[Light]\n" or i == "[Dark]\n" or i == "[Fire]\n" or i == "[Water]\n" or i == "[Wind]\n":
            elem = i
        if i[:-1] == mob:
            return elem
    return ("")

print(get_element("Monte"))