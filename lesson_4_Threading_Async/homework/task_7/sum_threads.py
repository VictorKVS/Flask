"""
1) Напишите программу на Python, которая будет находить
сумму элементов массива из 1000000 целых чисел.
2) Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
3) Массив должен быть заполнен случайными целыми числами
от 1 до 100.
4) При решении задачи нужно использовать многопоточность,
многопроцессорность и асинхронность.
5) В каждом решении нужно вывести время выполнения вычислений.
threads sum function
"""
from threading import Thread
import time
import random

t_sum = 0


def arr_creation():
    arr = [random.randint(1, 100) for _ in range(1_000_000)]
    return arr


def thread_sum():
    global t_sum
    for i in arr_creation():
        t_sum += i


threads = []
thread_time = time.time()
if __name__ == '__main__':
    t1 = Thread(target=arr_creation)
    threads.append(t1)
    t1.start()
    t2 = Thread(target=thread_sum)
    threads.append(t2)
    t2.start()
    for t in threads:
        t.join()
print(f'Summ for thread func: {t_sum}\nTime sync spent: {(time.time() - thread_time):.3f}\n'
      f'{"*" * 50}')
