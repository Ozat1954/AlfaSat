# -*- coding: utf-8 -*-
import random
import time
import queue
from threading import Event, Lock, Thread

#import self

# from MyClass_CommRx import my_thread09
# from My_class_file import my_thread_10
# from MyClassThread_8 import my_thread08
# from MyClassThread_1 import my_thread01
# from MyClassThread_2 import my_thread02
# from MyClassThread_3 import my_thread03
# from MyClassThread_4 import my_thread04
# from MyClassThread_5 import my_thread05
# from MyClassThread_6 import my_thread06
# from MyClassThread_7 import my_thread07
# from MyThread410_2 import my_thread_11
# from rett_410_2_1 import my_thread_12

from MyConsumerThread import MyConsumer
from MyProducerThread import MyProducer

def main():
    #    create_threads()

    # Создаем объект который будет уведомлять потоки о необходимости закругляться
    stop_event = Event()

    # Создаем очередь для обмена сообщениями
    shared_queue = queue.Queue()

    # Создаем объект Lock который будет показывать что очередь используется другим потоком
    queue_lock = Lock()

    # Создаем потоки
    my_producer = MyProducer("Producer22", stop_event, shared_queue, queue_lock)
    my_consumer = MyConsumer("Consumer55", stop_event, shared_queue, queue_lock)

    # Запускаем потоки
    print("MAIN: Starting threads.")
    my_producer.start()
    my_consumer.start()

    # my_thread01.start()
    # my_thread02.start()
    # my_thread03.start()
    # my_thread04.start()
    # my_thread05.start()
    # my_thread06.start()
    # my_thread07.start()
    # my_thread08.start()
    # my_thread09.start()
    # my_thread_10.start()
    # my_thread_11.start()
    # my_thread_12.start()i

    try:
        # Основной цикл
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Принят сигнал к закрытию программы: либо пользователь нажал Ctrl+C либо произошла ошибка.
        print("MAIN: Terminating all threads...")
        stop_event.set()

    my_consumer.join()
    my_producer.join()
    print("MAIN: Done.")


if __name__ == "__main__":
    main()
