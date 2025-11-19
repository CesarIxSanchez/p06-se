def parse_http_request(request):
    parts = request.split('\r\n\r\n', 1)
    
    header_section = parts[0]
    body = parts[1] if len(parts) > 1 else ""
    
    lines = header_section.split('\r\n')

    # peticiones vacías
    if not lines or not lines[0]:
        return {'method': 'GET', 'path': '/invalid', 'version': 'HTTP/1.1', 'headers': {}, 'body': ''}
    
    request_line = lines[0]
    req_parts = request_line.split(' ')
    if len(req_parts) != 3:
        return {'method': 'GET', 'path': '/invalid', 'version': 'HTTP/1.1', 'headers': {}, 'body': ''}

    method, path, version = req_parts

    headers = {}
    for line in lines[1:]:
        if line == "":
            break
        
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()

    return {
        'method': method,
        'path': path, 
        'version': version,
        'headers': headers,
        'body': body
    }

def send_http_response(status_code, content, content_type='text/plain'):
    status_messages = {
        200: 'OK',
        201: 'Created', # POST exitoso
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not found',
        409: 'Conflict', # para ID duplicado
        500: 'Internal Server Error'
    }

    status_text = status_messages.get(status_code, 'Unknown Status')
    response = f'HTTP/1.1 {status_code} {status_text}\r\n'
    response += f'Content-Type: {content_type}\r\n'
    response += f'Content-Length: {len(content)}\r\n'
    response += f'\r\n'
    response += content

    return response