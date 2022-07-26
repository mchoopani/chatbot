import random
import socket
import threading

from helpers import ConnectionHelper, time_calculator


class Client:
    _threads = []

    def __init__(self, HOST, PORT, id_):
        self.HOST = HOST
        self.PORT = PORT

        thread = threading.Thread(target=self.start_messaging, args=(self.HOST, self.PORT, id_))
        thread.start()
        Client._threads.append(thread)

    def start_messaging(self, HOST, PORT, thread_id):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            self.messaging(s, thread_id)

    def messaging(self, conn, current_thread_id):
        with conn:
            for _ in range(2):
                try:
                    # message = str(random.Random().randint(a=1, b=50))
                    message = input('Enter sth to echo: ')
                    ConnectionHelper.send_message(conn, message)
                    print(f'client {current_thread_id} logs: {ConnectionHelper.get_message(conn)}')
                except Exception as e:
                    print(f'Exception: {str(e)}')
                    break
            ConnectionHelper.send_message(conn, 'exit')
            ConnectionHelper.get_message(conn)

    @staticmethod
    def client_joins():
        for thread in Client._threads:
            thread.join()


@time_calculator
def run_clients(count, HOST, PORT):
    for i in range(count):
        Client(HOST, PORT, i)
    Client.client_joins()


if __name__ == '__main__':
    run_clients(1, '127.0.0.1', 12346)
