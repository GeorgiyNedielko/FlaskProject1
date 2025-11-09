import sqlite3

# Подключаемся к базе
conn = sqlite3.connect("instance/example.db")  # путь к файлу базы
cursor = conn.cursor()

# Получаем список всех таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Таблицы в базе:")
for table in tables:
    print("-", table[0])

print("\nДанные из таблиц:")

# Проходим по всем таблицам и выводим данные
for table in tables:
    table_name = table[0]
    print(f"\n=== {table_name} ===")
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [col[1] for col in cursor.fetchall()]  # имена колонок
    print(" | ".join(columns))  # заголовки колонок

    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    for row in rows:
        print(" | ".join(str(item) for item in row))

# Закрываем соединение
conn.close()
