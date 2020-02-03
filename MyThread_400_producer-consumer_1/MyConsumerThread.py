import json
import queue
import time
from threading import Thread


class MyConsumer(Thread):
    """
    Поток потребитель, принимает сообщения от другого потока
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
        while not self.stop_event.is_set():
            time.sleep(1)
            msg = ""

            # Код между lock.acquire() и lock.release() блокирующий, в него нужно класть только код необходимый
            # для обмена данными между потоками.
            self.queue_lock.acquire()       # блокировка
            try:
                msg = self.shared_queue.get_nowait()
            except queue.Empty:
                # В очереди нет новых сообщений
                print("%s reporting: No new messages." % self.name)
            self.queue_lock.release()       # разблокировка

            if msg:
                # Получено новое сообщение из другого потока
                print("%s reporting: received a new message:\n  %s" % (self.name, msg))

                # Делаем заметку в журнале (записываем в файл)
                my_record = ["Received at %s" % time.ctime(), "Message: %s" % msg]
                with open("my_data_log.txt", "a+") as f:
                    f.write(json.dumps(my_record) + "\n")
                    f.close()

        # Поступил запрос к остановке, stop_event.is_set()
        print("Terminating thread %s." % self.name)
