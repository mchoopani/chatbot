import socket

from helpers import send_message, get_message


def start_listening(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        messaging(conn, addr)


def messaging(conn, addr):
    with conn:
        # send_message(conn, f'hi {addr}')
        while True:
            print('waiting for client message...')
            message_from_client = get_message(conn)
            print(message_from_client)
            result = send_message(conn, message_from_client)
            if message_from_client == 'exit' or not result:
                break


if __name__ == '__main__':
    start_listening('127.0.0.1', 12345)
