from communication import *

if __name__ == '__main__':
    server = BindingConnection("192.168.1.24", 5555)
    conn = ConnectionHandler()
    server.start(conn.new_connection)