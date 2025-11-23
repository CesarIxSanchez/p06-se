import socket, datetime, json
from http_parser import parse_http_request, send_http_response
from urllib.parse import urlparse 

sensors_db = []

def start_server():
    # CONFIGURACIÓN DEL SERVIDOR (Código Base)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = '0.0.0.0'
    port = 8080
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor escuchando en {host}:{port}")

    # Función que maneja cada petición que llega
    def handler_path(method, path_with_query, headers, body):
        parsed_url = urlparse(path_with_query)
        path = parsed_url.path

        print(f"Recibido {method} en {path}")

        # RUTA PRINCIPAL: /api/sensors 
        if path == '/api/sensors':
            
            # MÉTODO POST
            if method == 'POST':
                try:
                    data = json.loads(body)
                except json.JSONDecodeError:
                    return send_http_response(400, 'Error: JSON invalido o malformado')

                # Validación de campos obligatorios
                required_fields = ['sensor_id', 'name', 'value']
                for field in required_fields:
                    if field not in data:
                        return send_http_response(400, f'Error: Falta el campo {field}')

                # Validación de duplicados
                for sensor in sensors_db:
                    if sensor['sensor_id'] == data['sensor_id']:
                        return send_http_response(409, 'Error: El sensor_id ya existe')

                # Creación del registro
                now = datetime.datetime.now().isoformat()
                new_sensor = {
                    'sensor_id': data['sensor_id'],
                    'name': data['name'],
                    'value': data['value'],
                    'unit': data.get('unit', ''),
                    'location': data.get('location', ''),
                    'created_at': now,
                    'updated_at': now
                }
                sensors_db.append(new_sensor)
                print(f"Guardado en DB. Total sensores: {len(sensors_db)}")

                # Respuesta exitosa (201 Created)
                response_body = {
                    "message": "Sensor creado exitosamente",
                    "sensor": new_sensor 
                }
                json_content = json.dumps(response_body)
                return send_http_response(201, json_content, content_type='application/json')


        # RUTA CON ID: /api/sensors/<id> 
        elif path.startswith('/api/sensors/'):
            
            if method == 'DELETE':
                
                # MÉTODO DELETE
                # Procesamiento y Lógica de Negocio)

                # 1. PROCESAMIENTO DE LA PETICIÓN
                try:
                    sensor_id = path.split('/')[-1] 
                except IndexError:
                    return send_http_response(400, '{"error": "ID invalido"}', 'application/json')
                auth_token = headers.get('Authorization')
                if auth_token != "Bearer 1234":
                    return send_http_response(401, '{"error": "Unauthorized: Token invalido o ausente"}', 'application/json')
                
                # 2. LÓGICA DE NEGOCIO 
                sensor_encontrado = None      
                for sensor in sensors_db:
                    if sensor['sensor_id'] == sensor_id:
                        sensor_encontrado = sensor
                        break 
                if not sensor_encontrado:
                    return send_http_response(404, '{"error": "Not Found: El sensor no existe"}', 'application/json')
                sensors_db.remove(sensor_encontrado)
                print(f"Sensor {sensor_id} eliminado. Restantes: {len(sensors_db)}")

                # Respuesta Exitosa)
                respuesta = {
                    "message": "Sensor eliminado",
                    "deleted_id": sensor_id,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                return send_http_response(200, json.dumps(respuesta), 'application/json')
        return send_http_response(404, 'Not found')
        
    # Bucle principal para mantener el servidor vivo
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            request_data = client_socket.recv(4096).decode('utf-8')

            if not request_data:
                client_socket.close()
                continue

            parsed = parse_http_request(request_data)

            response = handler_path(
                parsed.get('method'), 
                parsed.get('path'), 
                parsed.get('headers', {}),
                parsed.get('body')
            )

            client_socket.send(response.encode('utf-8'))
            client_socket.close()
    except KeyboardInterrupt:
        print('Apagando servidor')
    finally:
        server_socket.close()

if __name__ == '__main__':
    start_server()