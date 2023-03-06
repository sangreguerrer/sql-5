import psycopg2
from pw import password

with psycopg2.connect(database="Netology_db",user="postgres",password=password) as conn:
    with conn.cursor() as cur:
        def create_table(cursor):
            cursor.execute("""
                       CREATE TABLE IF NOT EXISTS customers(
                           id SERIAL PRIMARY KEY,
                           firstname VARCHAR(20) NOT NULL,
                           lastname VARCHAR(20) NOT NULL,
                           email VARCHAR(20)
                       );
                       """)

            conn.commit()
        def add_numtab(cursor):
            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS phone_table(
                            id SERIAL PRIMARY KEY,
                            phone_number VARCHAR(11),
                            customer_id INTEGER NOT NULL REFERENCES customers(id)
                        );
                        """)

            conn.commit()

        def add_customer(cursor,firstname,lastname,email):
            cursor.execute("""INSERT INTO customers(firstname,lastname,email) VALUES (%s, %s, %s);""",
                          (firstname,lastname,email))
            conn.commit()


        def add_phone(cursor,phone_number,customer_id):
            cursor.execute("""INSERT INTO phone_table (phone_number, customer_id) VALUES(%s,%s);
            """,(phone_number,customer_id))
            conn.commit()

        def change_first_name(cursor,customer_id,firstname=None):
            cursor.execute("""UPDATE customers SET firstname=%s WHERE id=%s;""",(firstname,customer_id,))
            conn.commit()
            print('Имя изменено успешно')

        def change_last_name(cursor,customer_id,lastname=None):
            cursor.execute("""UPDATE customers SET lastname=%s WHERE id=%s;""",(lastname,customer_id))
            conn.commit()
            print('Фамилия изменена успешно')

        def change_email(cursor, customer_id, email=None):
            cursor.execute("""UPDATE customers SET email=%s WHERE id=%s;""", (email,customer_id))
            conn.commit()
            print('Email изменён успешно')


        def change_phone_num(cursor, customer_id,old_number, phone_number=None):
            cursor.execute("""UPDATE phone_table SET phone_number=%s WHERE customer_id=%s and phone_number=%s;""",
                           (phone_number,customer_id,old_number))
            conn.commit()
            print('Номер изменён успешно')

        def delete_phone(cursor,customer_id,phone_number):
            cursor.execute("""DELETE FROM phone_table phone_number WHERE customer_id=%s and phone_number=%s;
            """, (phone_number,customer_id,))
            conn.commit()
            print('Номер удалён успешно')


        def delete_customer(cursor,customer_id):
            cursor.execute("""DELETE FROM phone_table WHERE customer_id=%s;""", (customer_id,))
            cursor.execute("""DELETE FROM customers WHERE id=%s;""",(customer_id,))
            conn.commit()

        def find_by_fn(cursor, firstname):
            cursor.execute("""SELECT firstname, lastname, email, phone_number FROM customers c
                           JOIN phone_table ph ON c.id=ph.customer_id WHERE firstname = %s """,[firstname])
            print(cur.fetchall())

        def find_by_ln(cursor, lastname=None):
            cursor.execute("""SELECT firstname, lastname, email, phone_number FROM customers c
                           JOIN phone_table ph ON c.id=ph.customer_id WHERE lastname=%s;""",[lastname])
            print(cur.fetchall())

        def find_by_email(cursor, email=None):
            cursor.execute("""SELECT firstname, lastname, email, phone_number FROM customers c
                           JOIN phone_table ph ON c.id=ph.customer_id WHERE email=%s;""",[email])
            print(cur.fetchall())

        def find_by_pn(cursor,phone_number=None):
            cursor.execute("""SELECT firstname, lastname, email, phone_number FROM customers c
                           LEFT JOIN phone_table ph ON c.id=ph.customer_id WHERE phone_number=%s;""", [phone_number])
            print(cur.fetchall())

        def main_change_func():
            command=input('Введите область для замены('
                          '\n1-имя,'
                          '\n2-фамилия,'
                          '\n3-email,'
                          '\n4-номер телефона):')
            if command=='1':
                id=int(input('Введите ID:'))
                change_fn=input('Введите новое имя:')
                change_first_name(cur,id,change_fn)
            elif command=='2':
                id = int(input('Введите ID:'))
                change_ln = input('Введите новую фамилию:')
                change_last_name(cur, id, change_ln)
            elif command=='3':
                id = int(input('Введите ID:'))
                changing_email = input('Введите новый email:')
                change_email(cur, id, changing_email)
            elif command=='4':
                id = int(input('Введите ID:'))
                old_num = input('Введите номер,который нужно заменить:')
                change_pn = input('Введите новый номер:')
                change_phone_num(cur,id,old_num,change_pn)
            else:
                print(f'Команды  {command} не найдено')

        def main_find_func():
            command=input('Введите область поиска('
                          '\n1-имя,'
                          '\n2-фамилия,'
                          '\n3-email,'
                          '\n4-номер телефона):')
            if command=='1':
                fbfn=input('Введите имя:')
                find_by_fn(cur,fbfn)
            elif command=='2':
                fbln=input('Введите фамилию:')
                find_by_ln(cur, fbln)
            elif command=='3':
                fbe=input('Введите email:')
                find_by_email(cur,fbe)
            elif command=='4':
                fbp=input('Введите номер телефона:')
                find_by_pn(cur,fbp)
            else:
                print(f'Команды  {command} не найдено')


        def main_func():
            command=input('Введите номер команды для работы с базой данных('
                          '\n1-добавить клиента,'
                          '\n2-добавить номер телефона,'
                          '\n3-изменить данные,'
                          '\n4-Удалить номер телефона,'
                          '\n5-Удалить клиента,'
                          '\n6-поиск клинта):')
            if command=='1':
                f_name=input('Введите имя:')
                l_name=input('Введите фамилию:')
                email=input('Введите email:')
                add_customer(cur,f_name,l_name,email)
                print('Пользователь добавлен')
            if command=='2':
                id=int(input('Введите ID:'))
                pn=input('Введите номер телефона:')
                add_phone(cur,pn,id)
                print(f'Номер {pn} успешно добавлен пользователю №{id}.')
            if command=='3':
                main_change_func()
            if command=='4':
                id = int(input('Введите ID:'))
                pn = input('Введите номер телефона:')
                delete_phone(cur,pn,id)
                print(f'Номер {pn} успешно удалён у пользователя №{id}.')
            if command=='5':
                id = int(input('Введите ID:'))
                delete_customer(cur,id)
                print('Клиент успешно удалён')
            if command=='6':
                main_find_func()
            print("Спасибо,заходите ещё!")



        if __name__=="__main__":
            create_table(cur)
            add_numtab(cur)
            main_func()

