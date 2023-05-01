import mysql.connector
from mysql.connector import Error
import mySqlQueries as queries


# Соединить приложение и БД
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("\nConnection to MySQL DB successful\n")
    except Error:
        print(f"\nThe error occurred: '{Error}'\n")

    return connection


if __name__ == '__main__':
    # Открыть доступ к БД
    dbConnection = create_connection("host_name", "user_name", "user_password", "db_name")

    # Вводное сообщение
    print("Запросы для семестровой работы:\n"
          "1 - Получить информацию обо всех зарегистрированных пользователях\n"
          "2 - Добавить нового пользователя в таблицу users\n"
          "3 - Изменить информацию о пользователе по полю login\n"
          "4 - Удалить пользователя из таблицы users\n"
          "5 - Добавить игру к заказу (связь: многие ко многим)\n"
          "6 - Заменить игру в заказе (связь: многие ко многим)\n"
          "7 - Удалить игру из заказа (связь: многие ко многим)\n"
          "8 - Аналитический запрос - Получить список всех заказов, в которых содержится игра с заданным названием\n")

    # Узнать, какой запрос хочет выполнить пользователь
    userChoice = int(input("Ваш выбор: "))

    # Проверка на значение, которое вводить пользователь
    if userChoice < 1 or userChoice > 8:
        print(f"\nЗначения '{userChoice}' нет в списке выбора")
    else:
        # Вызвать запрос, который попросил пользователь
        if userChoice == 1:
            queries.getUsersData(dbConnection)
        elif userChoice == 2:
            queries.addNewUser(dbConnection)
        elif userChoice == 3:
            queries.updateUserData(dbConnection)
        elif userChoice == 4:
            queries.deleteUser(dbConnection)
        elif userChoice == 5:
            queries.addGameToOrder(dbConnection)
        elif userChoice == 6:
            queries.updateGameInOrder(dbConnection)
        elif userChoice == 7:
            queries.deleteGameFromOrder(dbConnection)
        elif userChoice == 8:
            queries.getOrdersByGameName(dbConnection)

    # Закрыть доступ к БД
    dbConnection.close()
