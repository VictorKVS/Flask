"""
1) Напишите программу на Python, которая будет находить
сумму элементов массива из 1000000 целых чисел.
2) Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
3) Массив должен быть заполнен случайными целыми числами
от 1 до 100.
4) При решении задачи нужно использовать многопоточность,
многопроцессорность и асинхронность.
5) В каждом решении нужно вывести время выполнения вычислений.
processes sum function
"""
from multiprocessing import Process, Value
import time
import random

p_sum = Value('i', 0)


def arr_creation():
    arr = [random.randint(1, 100) for _ in range(1_000_000)]
    return arr


def proc_sum(cnt):
    global p_sum
    for i in arr_creation():
        with cnt.get_lock():
            p_sum.value += i


proc_time = time.time()
if __name__ == '__main__':
    p1 = Process(target=arr_creation)
    p2 = Process(target=proc_sum(p_sum))
    processes = [p1, p2]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print(f'Summ for proc func: {p_sum.value}\nTime proc spent: {(time.time() - proc_time):.3f}\n'
          f'{"*" * 50}')
