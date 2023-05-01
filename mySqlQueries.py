# Запросы для семестровой работы
# Получить информацию обо всех зарегистрированных пользователях
def getUsersData(dbConnection):
    myCursor = dbConnection.cursor()

    # Обратиться к БД с запросом
    getUsersDataQuery = "SELECT * FROM users"
    myCursor.execute(getUsersDataQuery)

    # Вывести результат выполнения запроса
    for result in myCursor:
        print(result)

    myCursor.close()


# Добавить нового пользователя в таблицу users
def addNewUser(dbConnection):
    myCursor = dbConnection.cursor()

    # Получить данные от пользователя
    userLogin = input("Логин пользователя: ")

    # Проверить имеется ли хотя бы одна запись с заданным login в таблице users
    checkUserUniqueLoginQuery = "SELECT login FROM users WHERE login = '%s';"
    myCursor.execute(checkUserUniqueLoginQuery % userLogin)
    checkUserUniqueLoginResult = myCursor.fetchone()

    if not checkUserUniqueLoginResult:
        userPassword = input("Пароль пользователя: ")
        userNickname = input("Псевдоним пользователя: ")
        userMail = input("Почта пользователя: ")
        userInfo = (userLogin, userPassword, userNickname, userMail)

        # Обратиться к БД с запросом
        addNewUserQuery = "INSERT INTO users (login, password, nickname, mail, registration_date) VALUES ('%s','%s','%s','%s',NOW());"

        myCursor.execute(addNewUserQuery % userInfo)
        dbConnection.commit()
    else:
        print(f"Пользователь с логином {userLogin} уже существует")

    myCursor.close()


# Изменить информацию о пользователе по полю login
def updateUserData(dbConnection):
    myCursor = dbConnection.cursor()

    # Получить от пользователя login
    userLogin = input("Введите login пользователя: ")

    # Проверить имеется ли хотя бы одна запись с заданным login в таблице users
    checkUserLoginQuery = "SELECT login FROM users WHERE login = '%s';"
    myCursor.execute(checkUserLoginQuery % userLogin)
    checkUserLoginResult = myCursor.fetchone()

    if checkUserLoginResult:
        # Получить новые данные от пользователя
        newUserLogin = input("Введите новый логин пользователя: ")
        newUserPassword = input("Введите новый пароль пользователя: ")
        newUserNickname = input("Введите новый псевдоним пользователя: ")
        newUserMail = input("Введите новую почту пользователя: ")
        userData = (newUserLogin, newUserPassword, newUserNickname, newUserMail, userLogin)

        # Обратиться к БД с запросом
        updateUserDataQuery = """
                            UPDATE users 
                            SET login = '%s', 
                                password = '%s', 
                                nickname = '%s', 
                                mail = '%s' 
                            WHERE login = '%s';
        """
        myCursor.execute(updateUserDataQuery % userData)
        dbConnection.commit()
    else:
        # Вывести ошибку, что нет полей с заданным login в таблице users
        print(f"В таблице users нет пользователя с login '{userLogin}'")

    myCursor.close()


# Удалить пользователя из таблицы users
def deleteUser(dbConnection):
    myCursor = dbConnection.cursor()

    # Получить login пользователя
    userLogin = input("Введите login пользователя: ")

    # Проверить имеется ли хотя бы одна запись с заданным login в таблице users
    checkUserLoginQuery = "SELECT * FROM users WHERE login = '%s';"
    myCursor.execute(checkUserLoginQuery % userLogin)
    checkUserLoginResult = myCursor.fetchone()

    if checkUserLoginResult:
        # Обратиться к БД с запросом
        deleteUserQuery = "DELETE FROM users WHERE login = '%s';"
        myCursor.execute(deleteUserQuery % userLogin)
        dbConnection.commit()
    else:
        print(f"В таблице users нет пользователя с логином '{userLogin}'")

    myCursor.close()


# Работа со связью многие-ко-многим
# Добавить игру в заказ
def addGameToOrder(dbConnection):
    myCursor = dbConnection.cursor()

    # Получить данные от пользователя
    idOrder = int(input("Номер заказа: "))
    gameName = input("Название игры: ")

    # Проверить имеется ли запись с заданным id в таблице orders
    checkIdOrderQuery = "SELECT * FROM orders WHERE id_orders = %d;"
    myCursor.execute(checkIdOrderQuery % idOrder)
    checkIdOrderResult = myCursor.fetchone()

    if checkIdOrderResult:
        # Проверить имеется ли запись с заданной игрой в таблице pc_games
        checkGameNameQuery = "SELECT * FROM pc_games WHERE name = '%s';"
        myCursor.execute(checkGameNameQuery % gameName)
        checkGameNameResult = myCursor.fetchone()

        if checkGameNameResult:
            # Обратиться к БД с запросом
            addGameToOrderQuery = "INSERT INTO pc_games_to_orders (id_games, id_orders) VALUES ((SELECT id_games FROM pc_games WHERE name = '%s'), %d);"

            gameInOrder = (gameName, idOrder)
            myCursor.execute(addGameToOrderQuery % gameInOrder)
            dbConnection.commit()
        else:
            print(f"Игры с названием '{gameName}' не существует")
    else:
        print(f"Заказа с номер '{idOrder}' не существует")

    myCursor.close()


# Заменить игру в заказе
def updateGameInOrder(dbConnection):
    myCursor = dbConnection.cursor()

    # Получить номер заказа у пользователя
    idOrder = int(input("Номер заказа: "))

    # Проверить имеется ли запись с заданным номером заказа в таблице orders
    checkIdOrderQuery = "SELECT * FROM orders WHERE id_orders = %d;"
    myCursor.execute(checkIdOrderQuery % idOrder)
    checkIdOrderResult = myCursor.fetchone()

    if checkIdOrderResult:
        gameName = input("Название игры, которую хотите заменить: ")

        # Проверить имеется ли запись с заданной игрой в таблице pc_games_to_orders
        checkGameNameInOrderQuery = "SELECT * FROM pc_games_to_orders WHERE id_orders = %d AND id_games = (SELECT id_games FROM pc_games WHERE name = '%s');"
        myCursor.execute(checkGameNameInOrderQuery % (idOrder, gameName))
        checkGameNameInOrderResult = myCursor.fetchone()

        if checkGameNameInOrderResult:
            newGameName = input("Название игры, которую хотите добавить: ")

            # Проверить имеется ли запись с новой заданной игрой в таблице pc_games
            checkNewGameNameQuery = "SELECT * FROM pc_games WHERE id_games = (SELECT id_games FROM pc_games WHERE name = '%s');"
            myCursor.execute(checkNewGameNameQuery % newGameName)
            checkNewGameNameResult = myCursor.fetchone()

            if checkNewGameNameResult:
                gameInOrder = (newGameName, idOrder, gameName)

                # Обратиться к БД с запросом
                updateGameToOrderQuery = "UPDATE pc_games_to_orders SET id_games = (SELECT id_games FROM pc_games WHERE name = '%s') WHERE id_orders = %d AND id_games = (SELECT id_games FROM pc_games WHERE name = '%s');"
                myCursor.execute(updateGameToOrderQuery % gameInOrder)
                dbConnection.commit()
            else:
                print(f"Игры с названием '{newGameName}' не существует")
        else:
            print(f"Игры с названием '{gameName}' в заказе с номер '{idOrder}' не имеется")
    else:
        print(f"Заказа с номер '{idOrder}' не существует")

    myCursor.close()


# Удалить игру из заказа
def deleteGameFromOrder(dbConnection):
    myCursor = dbConnection.cursor()

    # Получить номер заказа у пользователя
    idOrder = int(input("Номер заказа: "))

    # Проверить имеется ли запись с заданным номером заказа в таблице orders
    checkIdOrderQuery = "SELECT * FROM orders WHERE id_orders = %d;"
    myCursor.execute(checkIdOrderQuery % idOrder)
    checkIdOrderResult = myCursor.fetchone()

    if checkIdOrderResult:
        gameName = input("Название игры, которую хотите удалить: ")

        # Проверить имеется ли запись с заданным названием в таблице pc_games
        checkGameNameQuery = "SELECT id_games FROM pc_games WHERE name = '%s';"
        myCursor.execute(checkGameNameQuery % gameName)
        checkGameNameResult = myCursor.fetchone()

        if checkGameNameResult:
            # Проверить имеется ли запись с заданной игрой в таблице pc_games_to_orders
            checkGameNameInOrderQuery = "SELECT * FROM pc_games_to_orders WHERE id_orders = %d AND id_games = (SELECT id_games FROM pc_games WHERE name = '%s');"
            myCursor.execute(checkGameNameInOrderQuery % (idOrder, gameName))
            checkGameNameInOrderResult = myCursor.fetchone()

            if checkGameNameInOrderResult:
                gameInOrder = (idOrder, gameName)

                # Обратиться к БД с запросом
                updateGameToOrderQuery = "DELETE FROM pc_games_to_orders WHERE id_orders = %d AND id_games = (SELECT id_games FROM pc_games WHERE name = '%s');"
                myCursor.execute(updateGameToOrderQuery % gameInOrder)
                dbConnection.commit()
            else:
                print(f"Игры с названием '{gameName}' в заказе с номер '{idOrder}' не имеется")
        else:
            print(f"Игры с названием '{gameName}' не существует")
    else:
        print(f"Заказа с номер '{idOrder}' не существует")

    myCursor.close()


# Аналитический запрос: Получить информацию обо всех заказов, в которых содержится игра с заданным названием
def getOrdersByGameName(dbConnection):
    myCursor = dbConnection.cursor()

    # Получить название игры у пользователя
    gameName = input("Введите название игры: ")

    # Проверить, имеется ли игра с заданным именем в таблице pc_games
    checkGameNameQuery = "SELECT id_games FROM pc_games WHERE name = '%s';"
    myCursor.execute(checkGameNameQuery % gameName)
    checkGameNameResult = myCursor.fetchone()

    if checkGameNameResult:
        # Обратиться к БД с запросом
        getOrdersDataByGameNameQuery = """
                        SELECT users.nickname, orders.id_orders, orders.order_date FROM pc_games
                        JOIN pc_games_to_orders ON pc_games.id_games = pc_games_to_orders.id_games
                        JOIN orders ON pc_games_to_orders.id_orders = orders.id_orders
                        JOIN users ON orders.id_users = users.id_users
                        WHERE pc_games.name = '%s';
        """

        myCursor.execute(getOrdersDataByGameNameQuery % gameName)
        ordersDataByGameNameResult = myCursor.fetchall()

        # Вывести результат выполнения запроса
        if ordersDataByGameNameResult:
            for result in ordersDataByGameNameResult:
                print(f"User: {result[0]}, Order ID: {result[1]}, Order date: {result[2]}")
        else:
            print(f"Ни один человек не приобрел игру '{gameName}'")
    else:
        print(f"Игры с названием '{gameName}' не существует")
    myCursor.close()
