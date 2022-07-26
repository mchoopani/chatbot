import socket
from helpers import ConnectionHelper
import time
from concurrent.futures import ThreadPoolExecutor


class Server:

    instance = None

    @classmethod
    def get_instance(cls, HOST, PORT, multi_client_count):
        if cls.instance is None:
            cls.instance = Server(HOST, PORT, multi_client_count)
        return cls.instance

    def __init__(self, HOST, PORT, multi_client_count):
        self.HOST = HOST
        self.PORT = PORT
        self.multi_client_count = multi_client_count

    def start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            with ThreadPoolExecutor(max_workers=self.multi_client_count) as executor:
                while True:
                    conn, addr = s.accept()
                    executor.submit(self.messaging, conn, addr)

    def messaging(self, conn, addr):
        with conn:
            while True:
                try:
                    message_from_client = ConnectionHelper.get_message(conn)
                    time.sleep(1)
                    result = ConnectionHelper.send_message(conn, message_from_client)
                    if message_from_client == 'exit' or not result:
                        break
                except Exception as e:
                    print(f'{addr} closed because {str(e)}')
                    break


if __name__ == '__main__':
    server = Server.get_instance('127.0.0.1', 12346,5)
    server.start_listening()
