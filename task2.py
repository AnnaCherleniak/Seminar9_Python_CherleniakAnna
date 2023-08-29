# Дополнительное: Напишите следующие функции:
# - Нахождение корней квадратного уравнения
# - Генерация csv файла с тремя случайными числами в каждой строке.
#  100-1000 строк.
# - Декоратор, запускающий функцию нахождения корней квадратного уравнения
#  с каждой тройкой чисел из csv файла.
# - Декоратор, сохраняющий переданные параметры и результаты работы функции
# в json файл.

import json
from typing import Callable
import csv
from random import randint
from functools import wraps


def from_csv(func: Callable):
    @wraps(func)
    def wrapper(file_name: str):
        result = []
        with open(file_name, 'r', newline='') as f:
            csv_file = csv.reader(f)
            for line in csv_file:
                a, b, c = map(int, line)
                result.append(func(a, b, c))
        return result
    return wrapper


def json_log(func: Callable):
    try:
        with open(f'{func.__name__}.json', 'r') as data:
            result_list = json.load(data)
    except FileNotFoundError:
        result_list = []

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        result_list.append({'args': args, **kwargs,
                            'result': result})
        with open(f'{func.__name__}.json', 'w') as data:
            json.dump(result_list, data, indent=4)
        return result
    return wrapper


@from_csv
@json_log
def square_root(a, b, c):
    if a == 0:
        return None
    else:
        d = b ** 2 - 4 * a * c
        if d > 0:
            res1 = (-b + d ** 0.5) / (2 * a)
            res2 = (-b - d ** 0.5) / (2 * a)
            return res1, res2
        elif d == 0:
            res1 = -b / (2 * a)
            return res1
        else:
            return 'roots complex'


def generate_numbers_csv(name_file, min_number, max_number, count_numbers,
                         count_rows):
    with open(name_file, 'w', newline='', encoding='utf-8') as f:
        temp = csv.writer(f, dialect='excel-tab', delimiter=',')
        for _ in range(count_rows):
            numbers = []
            for __ in range(count_numbers):
                numbers.append(randint(min_number, max_number))
            temp.writerow(numbers)


if __name__ == '__main__':
    generate_numbers_csv('numbers.csv', -10, 10, 3, 100)
    square_root('numbers.csv')
