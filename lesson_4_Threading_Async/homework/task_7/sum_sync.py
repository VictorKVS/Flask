"""
1) Напишите программу на Python, которая будет находить
сумму элементов массива из 1000000 целых чисел.
2) Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
3) Массив должен быть заполнен случайными целыми числами
от 1 до 100.
4) При решении задачи нужно использовать многопоточность,
многопроцессорность и асинхронность.
5) В каждом решении нужно вывести время выполнения вычислений.
synchronous function
"""
import random
import time


def arr_creation():
    arr = [random.randint(1, 100) for _ in range(1_000_000)]
    return arr


def sync_sum():
    sync_time = time.time()
    sync_sum_val = 0
    for i in arr_creation():
        sync_sum_val += i
    return f'Summ for sync func: {sync_sum_val}\nTime sync spent: {(time.time() - sync_time):.3f}\n' \
           f'{"*" * 50}'


print(sync_sum())
