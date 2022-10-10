import json
import xml.etree.ElementTree as ET

item_types = {"car"}
item_array = []
people_array = []


class Item:
    def __init__(self, type="", name="", people_id=-1):
        self.id = len(item_array)
        if (type == ""):
            print("Введите тип предмета: ", end="")
            self.type = input().lower()
        else:
            self.type = type
        if self.type not in item_types:
            item_types.add(self.type)
        if (name == ""):
            print("Введите название предмета: ", end="")
            self.name = input()
        else:
            self.name = name
        self.people_id = people_id

    def getinfo(self):
        print(" ID :", self.id, "\n\tТип: " + self.type + "\n\tНазвание: ", self.name)



class People:
    def __init__(self, name="", items=None, people_id=-1):
        if items is None:
            items = []
        self.id = len(people_array)
        if (name == ""):
            self.name = input("Введите имя: ")
            while True:
                for peopl in people_array:
                    if (peopl.name == self.name):
                        break
                if (peopl.name != self.name):
                    break
                self.name = input("Это имя уже занято. Попробуйте снова: ")
            temp = input("Человек успешно зарегистрирован\nНажмите Enter для продолжения.")
        else:
            self.name = name
        self.items = []
        if (items != []):
            self.items = list(items)

    def getitems(self):
        if (self.items == None):
            print(None)
        else:
            for i in range(0, len(self.items)):
                print(" " + str(i + 1) + ")", end="")
                item_array[self.items[i]].getinfo()

    def getinfo(self):
        print("\tId:", self.id, "\n\tName:", self.name, "\n\tItems: ")
        self.getitems()


class IO_manager:
    def write_json():
        data = {"item": [],
                "people": []}
        for i in item_array:
            data["item"].append({"id": i.id, "type": i.type, "name": i.name, "people_id": i.people_id})
        for i in people_array:
            data["people"].append({"id": i.id, "name": i.name, "items": i.items})
        json.dump(data, open("file.json", "w"))

    def read_json():
        try:
            data = json.load(open("file.json", "r"))
        except FileNotFoundError:
            print("Файл не найден.")
            return
        for i in data["item"]:
            item_array.append(Item(i["type"], i["name"], i["people_id"]))
            if i["type"].lower not in item_types:
                item_types.add(i["type"])
        for i in data["people"]:
            people_array.append(People(i["name"], i["items"]))

    def read_xml():
        try:
            root = ET.ElementTree(file='file.xml').getroot()
        except FileNotFoundError:
            print("Файл не найден.")
            return -1
        for it in root[0]:
            item = Item(name=it[1].text, people_id=int(it[2].text), type=it[3].text)
            item_array.append(item)
        for pe in root[1]:
            a = []
            for it in pe[1]:
                a.append(int(it.text))
            people_array.append(People(items=a, name=pe[2].text, people_id=int(pe[0].text)))

    def write_xml():
        data = ET.Element('root')
        i1 = ET.SubElement(data, "item")
        p1 = ET.SubElement(data, "people")
        for item in item_array:
            i2 = ET.SubElement(i1, "element")
            ET.SubElement(i2, "id").text = str(item.id)
            ET.SubElement(i2, "name").text = str(item.name)
            ET.SubElement(i2, "people_id").text = str(item.people_id)
            ET.SubElement(i2, "type").text = str(item.type)
        for people in people_array:
            p2 = ET.SubElement(p1, "element")
            ET.SubElement(p2, "id").text = str(people.id)
            p3 = ET.SubElement(p2, "items")
            for i in people.items:
                ET.SubElement(p3, "element").text = str(i)
            ET.SubElement(p2, "name").text = str(people.name)
        ET.ElementTree(data).write("file.xml")


def main():
    a = IO_manager
    ch = 0
    while True:
        ch = input("1\t-\tчтение из JSON\n2\t-\tчтение из XML\n")
        if(ch == "1"):
            if a.read_json() == -1:
                return -1
            break
        if(ch == "2"):
            if a.read_xml() == -1:
                return -1
            break

    while True:
        print()
        ch = input("\n" * 10 + "0\t-\tОстановить программу\n1\t-\tДобавить предмет\n2\t-\tДобавить человека\n3\t-\tВывести "
                          "информацию о человеке\n4\t-\tПрисвоить предмет человеку\n5\t-\tПередать предмет другому человку\nВыберите действие: ")
        if (ch == "0"):
            break
        if (ch == "1"):
            i = Item()
            item_array.append(i)
            temp = input("Предмет успешно создан\nНажмите Enter чтобы продолжить")
        if (ch == "2"):
            p = People()
            people_array.append(p)
            temp = input("Человек успешно добавлен\nНажмите Enter чтобы продолжить")
        if (ch == "3"):
            name = input("Введите имя: ")
            for people in people_array:
                if (people.name == name):
                    people.getinfo()
                    temp = input("Нажмите Enter чтобы продолжить")
                    break
            if (people.name != name):
                temp = input("\tЧеловека с таким именем не существует.\nНажмите Enter чтобы продолжить")
        if (ch == "4"):
            name = input("Введите имя: ")
            names_array = []
            for i in range(0, len(people_array)):
                names_array.append(people_array[i].name)
            while name not in names_array and name != "0":
                name = input("Такого человека не существует. Попробуйте снова(0 - выход): ")
            if (name == "0"):
                continue
            else:
                for people in people_array:
                    if (people.name == name):
                        print("Доступные типы: ", end="")
                        for typ in item_types:
                            print(typ, end=", ")
                        print("\nВведите тип предмета: ", end="")
                        type = input()
                        while type not in item_types and type != "0":
                            print("Неверный тип. Попробуйте снова(0 - выход): ", end="")
                            type = input()
                        if (type == "0"):
                            break
                        print("Доступные " + type + ": ", end="")
                        for item in item_array:
                            if item.type == type:
                                print(item.name, end=", ")

                        print("\nВведите название предмета(0 - выход): ", end="")
                        item = input()
                        while True:
                            if (item == "0"):
                                break
                            for it in item_array:
                                if it.name == item:
                                    break
                            if it.name == item:
                                if (it.people_id == -1):
                                    people.items.append(it.id)
                                    it.people_id = people.id
                                    item = input("Предмет успешно добавлен.\nНажмите Enter для продолжения.")
                                    break
                                else:
                                    item = input("Предмет уже пренадлежит кому-то, попробуйте его передать\nНажите Enter чтобы продолжить")
                                    break
                            item = input("Неверный предмет. Попробуйте снова(0 - выход): ")
        if (ch == "5"):
            name1 = input("Введите имя человека с предметом: ")
            names_array = []
            for i in range(0, len(people_array)):
                names_array.append(people_array[i].name)
            while name1 not in names_array and name1 != "0":
                name1 = input("Такого человека не существует. Попробуйте снова(0 - выход): ")
            if (name1 == "0"):
                continue
            name2 = input("Введите имя: ")
            while name2 not in names_array and name2 != "0":
                name2 = input("Такого человека не существует. Попробуйте снова(0 - выход): ")
            if (name2 == "0"):
                continue
            print("доступные предметы у", name1, ": ")
            for p1 in people_array:
                if p1.name == name1:
                    p1.getitems()
                    item_id = int(input("Введите id нужного предмета: "))

                    while item_id not in p1.items:
                        print("Такого предмета нет. Попробуйте еще раз: ", end="")
                        item_id = int(input())
                    for p2 in people_array:
                        if p2.name == name2:
                            p2.items.append(item_id)
                            p1.items.remove(item_id)
                            temp = input("Предмет успешно передан\nНажмите Enter чтобы продолжить")
        a.write_json()
        a.write_xml()

main()
