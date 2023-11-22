from database import DataBase


def pizza_time():
    db.insert()
    category = ['Пицца', 'Паста', 'Горячие блюда', 'Салаты и закуски']
    for item in category:
        all_item = db.select_name(item).fetchall()
        for cur_item in all_item:
            item = db.select_elem(cur_item[0]).fetchall()
            print('Название: ' + item[0][0] + ' ' + item[0][1] + '\n' + 'Описание: ' + item[0][2] + '\n' + item[0][
                3] + '\n' + item[0][4])


if __name__ == '__main__':
    db = DataBase()
    pizza_time()
