import socket

def send_request(request_line, headers_list=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    request = f'{request_line}\r\n'
    request += 'Host: localhost\r\n'
    
    if headers_list:
        for header in headers_list:
            request += f'{header}\r\n'
            
    request += '\r\n'
    
    client_socket.send(request.encode())

    response = client_socket.recv(4096).decode()
    print(response)

    client_socket.close()

print()
print("Prueba 1: Ruta raíz")
send_request('GET / HTTP/1.1')
print()

print("Prueba 2: Ruta /api")
send_request('GET /api HTTP/1.1')
print()

print("Prueba 3: Ruta /admin (Token correcto)")
send_request('GET /admin HTTP/1.1', headers_list=["Authorization: {token:1234}"])
print()

print("Prueba 4: Ruta /admin (Token incorrecto)")
send_request('GET /admin HTTP/1.1', headers_list=["Authorization: token-malo"])
print()

print("Prueba 5: Ruta /admin (Sin token)")
send_request('GET /admin HTTP/1.1')
print()

print("Prueba 6: Ruta que no existe")
send_request('GET /hola HTTP/1.1')