import socket
from helpers import get_message, send_message


def start_messaging(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        messaging(s)


def messaging(conn):
    with conn:
        # welcome_message = get_message(conn)
        # print(welcome_message)
        while True:
            try:
                message = input('enter a message to echo: ')
                send_message(conn, message)
                print(get_message(conn))
                if message == 'exit':
                    break
            except Exception as e:
                print(f'Exception: {str(e)}')
                break


if __name__ == '__main__':
    start_messaging('127.0.0.1', 12345)
