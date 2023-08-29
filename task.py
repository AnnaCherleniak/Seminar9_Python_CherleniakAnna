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
        for el in result_list:
            if el['args'] == list(args):
                return el['result']
            else:
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

# # @json_cache
# def min_args(*args, **kwargs):
#     return min(args)


# # @json_cache
# def square_root(*args, **kwargs):
#     a, b, c = args
#     d = b ** 2 - 4 * a * c
#     if d > 0:
#         res1 = (-b + d ** 0.5) / (2 * a)
#         res2 = (-b - d ** 0.5) / (2 * a)
#         return res1, res2
#     elif d == 0:
#         res1 = -b / (2 * a)
#         return res1
#     else:
#         res1 = complex((-b + d ** 0.5) / (2 * a))
#         res2 = complex((-b - d ** 0.5) / (2 * a))
#         return res1, res2



    # print(square_root(1, 5, -8))
    # print(min_args(1, 547, -145, 0, 785))