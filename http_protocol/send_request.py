import socket
import json

def send_request(method, path, body=None, headers=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    request = f'{method} {path} HTTP/1.1\r\n'
    request += 'Host: localhost\r\n'

    if headers:
        for key, value in headers.items():
            request += f'{key}: {value}\r\n'
    
    if body:
        json_str = json.dumps(body)
        request += 'Content-Type: application/json\r\n'
        request += f'Content-Length: {len(json_str)}\r\n'
    
    request += '\r\n'
    
    if body:
        request += json_str

    client_socket.send(request.encode())

    response = client_socket.recv(4096).decode()
    print(f"ENVIANDO {method} {path}")
    if body:
        print(f"Body: {body}")
    print("\nRespuesta: ")
    print(response)
    print()

    client_socket.close()

#esto lo puse para generar el archivo .json, si no es necesario luego lo quitan
    return response

# pruebas :v

# 1. Insertar un sensor correctamente
sensor_1 = {
    "sensor_id": "S001",
    "name": "Temperatura",
    "value": 25.5,
    "unit": "C",
    "location": "Lab 1"
}
send_request('POST', '/api/sensors', body=sensor_1)

# 2. Intentar insertar el mismo sensor
send_request('POST', '/api/sensors', body=sensor_1)

# 3. Insertar otro sensor
sensor_2 = {
    "sensor_id": "S002",
    "name": "Humedad",
    "value": 60
}
send_request('POST', '/api/sensors', body=sensor_2)

# 4. JSON incompleto
sensor_malo = {
    "sensor_id": "S003",
    "name": "Presion"
}
send_request('POST', '/api/sensors', body=sensor_malo)

#Pruebas DELETE :

# 1.Sin autenticación
print("DELETE-Error 401")
send_request('DELETE', '/api/sensors/S001')

# 2. Con autenticación pero ID incorrecto
print("DELETE-Error 404")
headers_auth = {"Authorization": "Bearer 1234"}
send_request('DELETE', '/api/sensors/S999', headers=headers_auth)

# 3. Correcto
print("Delecte-Succes 200")
send_request('DELETE', '/api/sensors/S001', headers=headers_auth)
