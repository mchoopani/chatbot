import socket
from helpers import send_message, get_message
import time
from concurrent.futures import ThreadPoolExecutor


def start_listening(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        with ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                conn, addr = s.accept()
                executor.submit(messaging, conn, addr)


def messaging(conn, addr):
    with conn:
        while True:
            try:
                print('waiting for client message...')
                message_from_client = get_message(conn)
                time.sleep(1)
                print(message_from_client)
                result = send_message(conn, message_from_client)
                if message_from_client == 'exit' or not result:
                    break
            except Exception as e:
                print(f'{addr} closed because {str(e)}')
                break


if __name__ == '__main__':
    start_listening('127.0.0.1', 12346)
