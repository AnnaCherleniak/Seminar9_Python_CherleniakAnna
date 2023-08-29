# Основное:
# Создать декоратор для использования кэша.
# Т.е. сохранять аргументы и результаты в словарь,
#  если вызывается функция с агрументами, которые уже записаны в кэше
#  - вернуть результат из кэша, если нет - выполнить функцию.
#  Кэш лучше хранить в json.
# Решение, близкое к решению данной задачи было разобрано на семинаре.

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


def json_cache(func: Callable):
    try:
        with open(f'{func.__name__}.json', 'r') as data:
            result_list = json.load(data)
    except FileNotFoundError:
        result_list = []

    def wrapper(*args, **kwargs):
        if result_list:
            for el in result_list:
                if el['args'] == list(args):
                    return el['result']
        result = func(*args, **kwargs)
        result_list.append({'args': args, **kwargs,
                            'result': result})
        with open(f'{func.__name__}.json', 'w') as data:
            json.dump(result_list, data, indent=4)
        return result
    return wrapper


@json_cache
def sum_args(*args, **kwargs):
    return sum(args)


if __name__ == '__main__':
    print(sum_args(10, 2, 3, 4))
