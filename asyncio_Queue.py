import asyncio
import random
import time

async def worker(name, queue):
    while True:
        # Вытаскиваем 'рабочий элемент' из очереди.
        sleep_for = await queue.get()
        # Задержка на 'sleep_for' секунд.
        await asyncio.sleep(sleep_for)
        # Сообщаем очереди, что 'рабочий элемент' обработан.
        queue.task_done()
        print(f'{name} has slept for {sleep_for:.2f} seconds')

async def main():
    # Создаем очередь, которую будем использовать
    # для хранения рабочей нагрузки.
    queue = asyncio.Queue()
    total_sleep_time = 0
    # создание данных для очереди
    for _ in range(20):
        # Генерируем случайные тайминги
        sleep_for = random.uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        # заполняем очередь.
        queue.put_nowait(sleep_for)

    # Создаем три рабочие задачи для одновременной обработки очереди.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    started_at = time.monotonic()
    # Запускаем обработку очереди и ожидаем,
    # пока элементы не закончатся.
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # После того как очередь израсходована
    # останавливаем задачи
    for task in tasks:
        task.cancel()
    # Ждем, остановку задач.
    await asyncio.gather(*tasks, return_exceptions=True)

    print('====')
    print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')

asyncio.run(main())