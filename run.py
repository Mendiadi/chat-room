from communication import *

if __name__ == '__main__':
    server = BindingConnection("127.1.1.1", 5555)
    conn = ConnectionHandler()
    server.start(conn.new_connection)