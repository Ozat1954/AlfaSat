import time
import queue
from threading import Thread


class MyProducer(Thread):
    """
    Поток производитель, отправляет данные другому потоку
    """

    def __init__(self, name, stop_event, shared_queue, queue_lock):
        """
        Инициализация потока
        """
        Thread.__init__(self)
        self.name = name

        # Объект Event (событие) для получения запроса о завершении
        self.stop_event = stop_event
        # Общий буфер (очередь) используемый для отправки данных другому потоку
        self.shared_queue = shared_queue
        # Объект Lock, т.е. простой семафор, для пользования shared_queue
        self.queue_lock = queue_lock

    def run(self):
        """
        Запуск потока
        """
        i = 0
        while not self.stop_event.is_set():
            time.sleep(1.5)
            msg = "%s is running     ++++01  >>  " % self.name

            i = i + 1
            if i > 20:
                i = 1
            msg += str(i)

            print("Sending message: " + msg)

            # Код между lock.acquire() и lock.release() блокирующий, в него нужно класть только код необходимый
            # для обмена данными между потоками.
            self.queue_lock.acquire()  # блокировка
            try:
                self.shared_queue.put_nowait(msg)
            except queue.Full:
                # Последнее сообщение не отправлено потому что очередь заполнена
                print("%s reporting: Queue is full." % self.name)
            self.queue_lock.release()  # разблокировка

        # Поступил запрос к остановке потока, stop_event.is_set()
        print("Terminating thread %s." % self.name)
