"""
1) Напишите программу на Python, которая будет находить
сумму элементов массива из 1000000 целых чисел.
2) Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
3) Массив должен быть заполнен случайными целыми числами
от 1 до 100.
4) При решении задачи нужно использовать многопоточность,
многопроцессорность и асинхронность.
5) В каждом решении нужно вывести время выполнения вычислений.
asynchronous function
"""
import asyncio
import random
import time
from sum_sync import sync_sum


def arr_creation():
    arr = [random.randint(1, 100) for _ in range(1_000_000)]
    return arr


async def async_sum():
    sync_sum_val = 0
    for i in arr_creation():
        sync_sum_val += i
    print(f'Summ for async func: {sync_sum_val}')


async def main():
    task = asyncio.create_task(async_sum())
    await task

async_time = time.time()
if __name__ == '__main__':
    asyncio.run(main())
    print(f'Time async spent: {(time.time() - async_time):.3f}\n{"*" * 50}')
    sync_sum()
