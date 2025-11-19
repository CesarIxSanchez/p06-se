import socket, datetime
from http_parser import parse_http_request, send_http_response
from urllib.parse import urlparse 

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = '0.0.0.0'
    port = 8080
    server_socket.bind((host, port))
    server_socket.listen(5)

    def handler_path(path_with_query, headers):
        
        parsed_url = urlparse(path_with_query)
        path = parsed_url.path

        print(f"Headers recibidos: {headers}")

        if (path == '/'):
            return send_http_response(200, 'Hola mundo desde handler')
        elif (path == '/api'):
            now = datetime.datetime.now()
            time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            return send_http_response(200, f'Hora actual: {time_str}')
        elif (path == '/admin'):
            auth_header = headers.get('Authorization')
            if (auth_header == '{token:1234}'):
                return send_http_response(200, 'Bienvenido, Admin')
            else:
                return send_http_response(401, 'Token invalido o ausente')
        return send_http_response(404, 'Not found')
        
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f'\nConexión exitosa con: {client_address}')

            request_data = client_socket.recv(1024).decode('utf-8')

            if not request_data:
                client_socket.close()
                continue

            parsed = parse_http_request(request_data)

            print(parsed)
            print(f"Ruta de la petición: {parsed.get('path')}")

            response = handler_path(parsed.get('path'), parsed.get('headers', {}))

            client_socket.send(response.encode('utf-8'))
            client_socket.close()
    except KeyboardInterrupt:
        print('Apagando servidor')
    finally:
        server_socket.close()

if __name__ == '__main__':
    start_server()