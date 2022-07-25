import socket
import threading
from helpers import send_message, get_message
import time

def start_listening(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            this_thread = threading.Thread(target=messaging, args=(conn, addr))
            this_thread.start()


def messaging(conn, addr):
    with conn:
        # send_message(conn, f'hi {addr}')
        while True:
            try:
                print('waiting for client message...')
                message_from_client = get_message(conn)
                time.sleep(2)
                print(message_from_client)
                result = send_message(conn, message_from_client)
                if message_from_client == 'exit' or not result:
                    break
            except Exception as e:
                print(f'{addr} closed because {str(e)}')
                break


if __name__ == '__main__':
    start_listening('127.0.0.1', 12345)
