from databases import global_init
from server import start_backend_server, start_frontend_server

def main():
    global_init('databases/keeptouch.db')
    start_backend_server()
    start_frontend_server()

if __name__ == '__main__':
    main()