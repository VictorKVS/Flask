"""
1) Напишите программу, которая будет скачивать страницы из
списка URL-адресов и сохранять их в отдельные файлы на
диске.
2) В списке может быть несколько сотен URL-адресов.
3) При решении задачи нужно использовать многопоточность,
многопроцессорность и асинхронность.
4) Представьте три варианта решения.
Multiprocessing downloading
"""
from multiprocessing import Process
import requests
import time

URLS = [
    'https://habr.com/ru/articles/739012/',
    'https://vk.com/dmitry_voytik',
    'https://geekjob.ru',
    'https://euler.jakumo.org/problems.html',
    'https://gb.ru/lessons/309287/',
    'https://vladilen.notion.site/JavaScript-2022-8d7c0efdb28d4d779ad71c4ce0643151',
    'https://www.codewars.com',
    'https://habr.com/ru/companies/dcmiran/news/739008/',
    'https://codeforces.com',
    'https://news.ru/',
]


def download_url(url):
    response = requests.get(url)
    filename = f'Process_{url.replace("https://", "").replace(".", "").replace("/", "_")}.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f'{url} downloaded')


processes = []
start_time = time.time()


if __name__ == '__main__':
    for url in URLS:
        process = Process(target=download_url, args=(url,))
        processes.append(process)
        process.start()

    for thread in processes:
        thread.join()

    print(f'Elapsed time: {(time.time() - start_time):.2f}')
