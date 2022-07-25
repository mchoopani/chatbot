import random
import socket
import threading
from datetime import datetime

from helpers import get_message, send_message


def start_messaging(HOST, PORT, thread_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        messaging(s, thread_id)


def messaging(conn, current_thread_id):
    with conn:
        for _ in range(2):
            try:
                message = str(random.Random().randint(a=1, b=50))
                send_message(conn, message)
                print(f'client {current_thread_id} logs: {get_message(conn)}')
            except Exception as e:
                print(f'Exception: {str(e)}')
                break
        send_message(conn, 'exit')
        get_message(conn)


if __name__ == '__main__':
    start = datetime.now().timestamp()
    thrds = []
    for i in range(10):
        thr = threading.Thread(target=start_messaging, args=('127.0.0.1', 12346, i))
        thr.start()
        thrds.append(thr)

    for thr in thrds:
        thr.join()
    end = datetime.now().timestamp()
    print(f'Process time is : {end - start}')
