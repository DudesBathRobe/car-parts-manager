import sqlite3
from tabulate import tabulate

# --- ЧАСТЬ 1: ООП ---
class Accessory:
    def __init__(self, art, title, car_model, price):
        self.art = art
        self.title = title
        self.car_model = car_model
        self.price = price

    def __repr__(self):
        return f"Товар: {self.title} ({self.art}) для {self.car_model} ({self.price} руб.)"

# --- ЧАСТЬ 2: РАБОТА С БД (SQL) ---
def init_db():
    # Создаем подключение к файлу базы данных
    conn = sqlite3.connect('accessories.db')
    cursor = conn.cursor()

    # SQL-запрос на создание таблицы, если её нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            art TEXT NOT NULL,
            title TEXT NOT NULL,
            car_model TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_to_db(item):
    with sqlite3.connect('accessories.db') as conn:
        cursor = conn.cursor()
        # Используем SQL-запрос для вставки данных
        cursor.execute('INSERT INTO stock (art, title, car_model, price) VALUES (?, ?, ?, ?)',
                    (item.art, item.title, item.car_model, item.price))
        conn.commit()
    conn.close()
    print(f"--- [Успех]: {item.title} ({item.art}) добавлен в базу! ---")

def show_all_items():
    with sqlite3.connect('accessories.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT art, title, car_model, price FROM stock')
        rows = cursor.fetchall()                # fetchall() возвращает список кортежей

    if not rows:
        print("\n--- База данных пока пуста ---")
    else:
        print("\n--- СПИСОК ВСЕХ ТОВАРОВ ---")
        headers = ["Артикул", "Название", "Модель авто", "Цена (руб.)"]

        # Вся магия в одной строке!
        # tablefmt="grid" делает красивые рамки, как в настоящих БД
        print("\n" + tabulate(rows, headers=headers, tablefmt="pipe"))

    conn.close()

def find_by_art(art):
    with sqlite3.connect('accessories.db') as conn:
        cursor = conn.cursor()
        #Никаких .format() или f-строк внутри SQL! А то можно дропнуть бд
        #Осуществляем поиск по введенному артикулу
        query = "SELECT art, title, car_model, price FROM stock WHERE art = ?"
        cursor.execute(query, (art,))
        rows = cursor.fetchone()

    if not rows:
        print("\n--- Артикул не найден ---")
    else:
        print(f'Найдено: {rows}')

    conn.close()

def update_price(art, new_price):
    with sqlite3.connect('accessories.db') as conn:
        cursor = conn.cursor()

        # Выполняем обновление
        cursor.execute("UPDATE stock SET price = ? WHERE art = ?", (new_price, art))

        # Проверяем, была ли обновлена хоть одна строка
        if cursor.rowcount > 0:
            print(f"--- [Успех]: Цена для артикула {art} обновлена до {new_price} ---")
        else:
            print(f"--- [Ошибка]: Товар с артикулом {art} не найден ---")

        conn.commit()

    conn.close()

def delete_item(art):
    with sqlite3.connect('accessories.db') as conn:
        cursor = conn.cursor()

        # Выполняем удаление
        cursor.execute("DELETE FROM stock where art = ?", (art,))

        # Проверяем, была ли обновлена хоть одна строка
        if cursor.rowcount > 0:
            print(f"--- [Успех]: Товар с артикулом {art} был удален ---")
        else:
            print(f"--- [Ошибка]: Товар с артикулом {art} не найден ---")

        conn.commit()

    conn.close()

# --- ЧАСТЬ 3: ГЛАВНЫЙ ЦИКЛ ---
if __name__ == "__main__":
    init_db()
    print("Добро пожаловать в систему учета запчастей!")

    while True:
        print("\nМеню:")
        print("1. Добавить новый товар")
        print("2. Показать все товары")
        print("3. Поиск по артикулу")
        print("4. Измененить цену")
        print("5. Удалить товар по артикулу")
        print("0. Выход (exit)")

        choice = input("Выберите действие: ")

        if choice == '1':
            art = input("\nВведите артикул товара (или 'exit' для выхода): ")
            if art.lower() == 'exit':
                break
            name = input("Введите название товара: ")
            car = input("Для какой модели авто (напр. Haval F7x): ")
            price = float(input("Цена: "))

            # Создаем объект нашего класса
            new_item = Accessory(art, name, car, price)

            # Сохраняем его в базу данных
            add_to_db(new_item)

        elif choice == '2':
            show_all_items()

        elif choice == '3':
            search_art = input('Введите артикул: ')
            find_by_art(search_art)

        elif choice == '4':
            art = input('Введите артикул: ')
            try:
                new_price = float(input("Введите новую цену: "))
                update_price(art, new_price)
            except ValueError:
                print("Ошибка: Цена должна быть числом!")

        elif choice == '5':
            art = input("Введите артикул: ")
            print("")
            print(f"Вы дейсьвительно хотите удалить артикул {art} из списка товаров? y/n")
            temp_choice = input()
            if temp_choice.lower() == 'y':
                delete_item(art)

        elif choice == '0' or choice.lower() == 'exit':
            print("До встречи!")
            break
        else:
            print("Неверный ввод, попробуйте еще раз.")

