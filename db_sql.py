import psycopg2
from pprint import pprint


def create_tables(cur):
    """Функция, создающая структуру БД (таблицы)"""

    # Создание таблицы основных данных
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS clients_db(
    id SERIAL PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    client_surname VARCHAR(100) NOT NULL,
    client_email VARCHAR(100) NOT NULL
    );
    """
    )

    # Создание отдельной таблицы с номерами
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS client_phonenumbers(
    id_phonenumbers SERIAL PRIMARY KEY,
    client_phonenumber VARCHAR(20) UNIQUE,
    client_id INTEGER NOT NULL REFERENCES clients_db(id)
    );
    """
    )


def add_new_client(cur, client_name, client_surname, client_email):
    """Функция, позволяющая добавить нового клиента"""
    cur.execute(
        """
    INSERT INTO clients_db(client_name, client_surname, client_email) VALUES(%s, %s, %s);
    """,
        (client_name, client_surname, client_email),
    )


def add_new_phonenumber(cur, client_id, phonenumber):
    """Функция, позволяющая добавить телефон для существующего клиента"""
    cur.execute(
        """
    INSERT INTO client_phonenumbers(client_id, client_phonenumber) VALUES(%s, %s);
    """,
        (client_id, phonenumber),
    )


def change_client_data():
    """Функция, позволяющая изменить данные о клиенте"""
    print(
        "Для изменения информации введите нужную команду.\n "
        "1 - изменить имя; 2 - изменить фамилию; 3 - изменить email; 4 - изменить номер телефона"
    )

    while True:
        command_symbol = int(input())
        if command_symbol == 1:
            input_id_for_changing_name = input(
                "Введите id клиента имя которого хотите изменить: "
            )
            input_name_for_changing = input("Введите имя для изменения: ")
            cur.execute(
                """
            UPDATE clients_db SET client_name = %s WHERE id = %s;
            """,
                (input_name_for_changing, input_id_for_changing_name),
            )
            break
        elif command_symbol == 2:
            input_id_for_changing_surname = input(
                "Введите id клиента фамилию которого хотите изменить: "
            )
            input_surname_for_changing = input("Введите фамилию для изменения: ")
            cur.execute(
                """
            UPDATE clients_db SET client_surname= %s WHERE id = %s;
            """,
                (input_surname_for_changing, input_id_for_changing_surname),
            )
            break
        elif command_symbol == 3:
            input_id_for_changing_email = input(
                "Введите id клиента email которого хотите изменить: "
            )
            input_email_for_changing = input("Введите email для изменения: ")
            cur.execute(
                """
            UPDATE clients_db SET client_email= %s WHERE id = %s;
            """,
                (input_email_for_changing, input_id_for_changing_email),
            )
            break
        elif command_symbol == 4:
            input_for_changing_phonenumber = input(
                "Введите номер телефона который хотите изменить: "
            )
            input_phonenumber_for_changing = input(
                "Введите номер телефона для изменения: "
            )
            cur.execute(
                """
            UPDATE client_phonenumbers SET client_phonenumber= %s WHERE client_phonenumber = %s;
            """,
                (input_phonenumber_for_changing, input_for_changing_phonenumber),
            )
            break
        else:
            print("Вы ввели неправильную команду, пожалуйста, повторите ввод")


def delete_client_phonenumber():
    """Функция, позволяющая удалить телефон для существующего клиента"""
    input_id_for_deleting_phonenumber = input(
        "Введите id клиента номер телефона которого хотите удалить: "
    )
    input_phonenumber_for_deleting = input(
        "Введите номер телефона который хотите удалить: "
    )
    with conn.cursor() as cur:
        cur.execute(
            """
        DELETE FROM client_phonenumbers WHERE client_id=%s AND client_phonenumber=%s            
        """,
            (input_id_for_deleting_phonenumber, input_phonenumber_for_deleting),
        )


def delete_client():
    """Функция, позволяющая удалить существующего клиента"""
    input_id_for_deleting_client = input("Введите id клиента которого хотите удалить: ")
    input_client_surname_for_deleting = input(
        "Введите фамилию клиента которого хотите удалить: "
    )
    with conn.cursor() as cur:
        # удаление связи с таблицей client_phonenumbers
        cur.execute(
            """
        DELETE FROM client_phonenumbers WHERE client_id = %s
        """,
            (input_id_for_deleting_client),
        )
        # удаление информации о клиенте из таблицы clients_db
        cur.execute(
            """
        DELETE FROM clients_db WHERE id = %s AND client_surname = %s
        """,
            (input_id_for_deleting_client, input_client_surname_for_deleting),
        )


def find_client():
    """Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону"""
    print(
        "Для поиска информации о клиенте, пожалуйста, введите команду:\n "
        "1 - найти по имени; 2 - найти по фамилии; 3 - найти по email; 4 - найти по номеру телефона"
    )
    while True:
        input_command_for_finding = int(
            input("Введите команду для поиска информации о клиенте: ")
        )
        if input_command_for_finding == 1:
            input_name_for_finding = input(
                "Введите имя для поиска информации о клиенте: "
            )
            cur.execute(
                """
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients_db cb
            LEFT JOIN client_phonenumbers cp ON cp.id_phonenumbers = cb.id
            WHERE client_name=%s
            """,
                (input_name_for_finding,),
            )
            print(cur.fetchall())
        elif input_command_for_finding == 2:
            input_surname_for_finding = input(
                "Введите фамилию для поиска информации о клиенте: "
            )
            cur.execute(
                """
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients_db cb
            LEFT JOIN client_phonenumbers cp ON cp.id_phonenumbers = cb.id
            WHERE client_surname=%s
            """,
                (input_surname_for_finding,),
            )
            print(cur.fetchall())
        elif input_command_for_finding == 3:
            input_email_for_finding = input(
                "Введите email для поиска информации о клиенте: "
            )
            cur.execute(
                """
            SELECT id , client_name, client_surname, client_email, client_phonenumber
            FROM clients_db cb
            LEFT JOIN client_phonenumbers cp ON cp.id_phonenumbers = cb.id
            WHERE client_email=%s
            """,
                (input_email_for_finding,),
            )
            print(cur.fetchall())
        elif input_command_for_finding == 4:
            input_phonenumber_for_finding = input(
                "Введите номер телефона для поиска информации о клиенте: "
            )
            cur.execute(
                """
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients_db cb 
            LEFT JOIN client_phonenumbers cp ON cp.id_phonenumbers = cb.id
            WHERE client_phonenumber=%s
            """,
                (input_phonenumber_for_finding,),
            )
            # return cur.fetchone()[0]
            print(cur.fetchall())
        else:
            print("Вы ввели неправильную команду, пожалуйста, повторите ввод")


def check_function(cur):
    """Проверочная функция, отображает содержимое таблиц"""
    cur.execute(
        """
    SELECT * FROM clients_db;
    """
    )
    pprint(cur.fetchall())
    cur.execute(
        """
    SELECT * FROM client_phonenumbers;
    """
    )
    pprint(cur.fetchall())


with psycopg2.connect(database="db_5", user="postgres", password="123ccc321") as conn:
    with conn.cursor() as cur:
        create_tables(cur)
        add_new_client(cur, "Dima", "Ivanov", "cool.writer1990@example.com")
        add_new_client(cur, "Gena", "Vonavi", "music.lover2020@example.com")
        add_new_client(cur, "Oleg", "Oniva", "travel.adventurer45@example.com")
        add_new_client(cur, "Gleb", "Petrov", "sunny.day123@example.com")
        add_new_client(cur, "Polina", "Biba", "tech.guru99@example.com")
        add_new_phonenumber(cur, 1, "74951234567")
        add_new_phonenumber(cur, 2, "79052345678")
        add_new_phonenumber(cur, 3, "79123456789")
        add_new_phonenumber(cur, 4, "79164567890")
        add_new_phonenumber(cur, 5, "79105678901")
        check_function(cur)
        change_client_data()
        delete_client_phonenumber()
        delete_client()
        find_client()

conn.close()
