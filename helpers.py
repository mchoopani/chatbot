def get_message(conn):
    return conn.recv(1024).decode('utf-8')


def send_message(conn, message):
    try:
        conn.sendall(message.encode())
        return True
    except Exception as e:
        print(str(e))
        return False