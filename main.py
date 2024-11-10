import json


class Entry:
    def __init__(self, line):
        self.name = line["name"]
        self.number = line["number"]
        self.comment = line["comment"]

    def __str__(self):
        return ("{} : {} : {}".format(self.name, self.number, self.comment))

    def as_dict(self):
        return {"name": self.name,
                "number": self.number,
                "comment": self.comment}


class Phone_book:
    def __init__(self, path):
        self.file_path = path
        self.entrys = list()
        try:
            with open(path, "r") as file:
                data = json.load(file)
                for line in data["entrys"]:
                    entry = Entry(line)
                    self.entrys.append(entry)
            self.is_load = True
        except Exception:
            self.is_load = False

    def print(self):
        if self.is_load:
            for entry in self.entrys:
                print(entry)
        else:
            print("Справочник не обнаружен или пуст")
            print("Добавьте запись в справочник")

    def add_entry(self, entry):
        self.entrys.append(entry)
        self.save()
        self.is_load = True

    def search_entry(self, field):
        for entry in self.entrys:
            search_index = entry.name.lower().find(field)
            search_index += entry.number.lower().find(field)
            search_index += entry.comment.lower().find(field)

            if search_index > -3:
                return entry

        return None

    def save(self):
        if self.is_load:
            data = dict()
            data["entrys"] = list()
            for entry in self.entrys:
                data["entrys"].append(entry.as_dict())

            with open(self.file_path, "w") as file:
                try:
                    json.dump(obj=data, fp=file, indent=4, ensure_ascii=False)
                except Exception:
                    return False
            return True
        else:
            return False

    def delete_entry(self, entry):
        self.entrys.remove(entry)
        return self.save()


def print_menu(current_entry):
    print("\n\n")
    print("Выберите пункт:")
    print("==============================")
    print("1. Распечатать весь справочник")
    print("2. Найти запись")
    print("3. Добавить запись")
    print("4. Отредактировать запись")
    print("5. Удалить запись")
    print("==============================")
    print("0. Выход\n")

    if current_entry is not None:
        print("Текущая запись: {}".format(current_entry))


def add_entry(phone_book):
    name = input("Введите имя: ")
    number = input("Введите номер: ")
    comment = input("Введите комментарий: ")

    line = {"name": name, "number": number, "comment": comment}

    entry = Entry(line)
    phone_book.add_entry(entry)

    return entry


def search_entry(phone_book):
    field = input("Введите строку для поиска: ").lower()
    print(field)
    return phone_book.search_entry(field)


def edit_entry(current_entry):
    print("Текущая запись {}".format(current_entry))
    name = input("Введите новое имя: ")
    number = input("Введите новое имя: ")
    comment = input("Введите новый комментарий: ")
    entry = Entry({"name": name, "number": number, "comment": comment})
    return entry


phone_book_path = "phonebook.json"


if __name__ == "__main__":
    phone_book = Phone_book(phone_book_path)
    current_entry = None

    print_menu(current_entry)
    user_input = input()

    while user_input != "0":
        if user_input == "1":    # Распечатать справочник
            phone_book.print()

        elif user_input == "2":  # Найти запись
            if phone_book.is_load:
                current_entry = search_entry(phone_book)
                if current_entry is not None:
                    print("Найдена запись в справочнике:")
                    print(current_entry)
            else:
                print("Телефонная книга не загружена")

        elif user_input == "3":  # Добавить запись
            current_entry = add_entry(phone_book)
            print("Добавлена запись {}".format(current_entry))

        elif user_input == "4":  # Отредактировать запись
            if current_entry is not None:
                old_entry = current_entry
                new_entry = edit_entry(current_entry)
                phone_book.delete_entry(old_entry)
                phone_book.add_entry(new_entry)
                current_entry = new_entry
            else:
                print("Текущая запись не выбрана. Создайте или найдите запись")

        elif user_input == "5":  # Удалить запись
            if current_entry is not None:
                phone_book.delete_entry(current_entry)
                current_entry = None

        print_menu(current_entry)
        user_input = input()
