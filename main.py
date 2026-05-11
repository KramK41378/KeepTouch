import json

from server import start_backend_server, start_frontend_server

def set_root_directory():
    prev_config = json.load(open('config.json', 'r'))
    prev_config['root_dir'] = __name__
    json.dump(prev_config, open('config.json', 'w'))

def main():
    set_root_directory()
    start_backend_server()
    start_frontend_server()

if __name__ == '__main__':
    main()