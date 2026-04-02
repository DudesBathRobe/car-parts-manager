import sqlite3

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
    conn = sqlite3.connect('accessories.db')
    cursor = conn.cursor()
    # Используем SQL-запрос для вставки данных
    cursor.execute('INSERT INTO stock (art, title, car_model, price) VALUES (?, ?, ?, ?)',
                   (item.art, item.title, item.car_model, item.price))
    conn.commit()
    conn.close()
    print(f"--- [Успех]: {item.title} ({item.art}) добавлен в базу! ---")

def show_all_items():
    conn = sqlite3.connect('accessories.db')
    cursor = conn.cursor()

    # Выбираем все данные из таблицы
    cursor.execute('SELECT art, title, car_model, price FROM stock')
    rows = cursor.fetchall() # fetchall() возвращает список кортежей

    if not rows:
        print("\n--- База данных пока пуста ---")
    else:
        print("\n--- СПИСОК ВСЕХ ТОВАРОВ ---")
        for row in rows:
            # Превращаем данные из БД обратно в объект нашего класса (ООП в действии!)
            item = Accessory(row[0], row[1], row[2], row[3])
            print(item)

    conn.close()

# --- ЧАСТЬ 3: ГЛАВНЫЙ ЦИКЛ ---
if __name__ == "__main__":
    init_db()
    print("Добро пожаловать в систему учета запчастей!")

    while True:
        print("\nМеню:")
        print("1. Добавить новый товар")
        print("2. Показать все товары")
        print("3. Выход (exit)")

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

        elif choice == '3' or choice.lower() == 'exit':
            print("До встречи!")
            break
        else:
            print("Неверный ввод, попробуйте еще раз.")

