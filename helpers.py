from datetime import datetime


class ConnectionHelper:
    @staticmethod
    def get_message(conn):
        if message := conn.recv(1024).decode('utf-8') == '':
            raise Exception('Client disconnected!')
        return message

    @staticmethod
    def send_message(conn, message):
        try:
            conn.sendall(message.encode())
            return True
        except Exception as e:
            print(str(e))
            return False


def time_calculator(func):
    def wrap(*args, **kwargs):
        start = datetime.now().timestamp()
        return_value = func(*args, **kwargs)
        end = datetime.now().timestamp()
        print(f'This function run time is : {end - start}')
        return return_value

    return wrap
