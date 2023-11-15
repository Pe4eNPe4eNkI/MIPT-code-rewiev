from database import DataBase


def pizza_time():
    db.insert()
    print(db.select().fetchall())


if __name__ == '__main__':
    try:
        db = DataBase()
        pizza_time()

    except:
        print("Oops!")
