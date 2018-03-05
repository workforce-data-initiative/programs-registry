from flask import jsonify, make_response

def create_response(data, schema, status, custom_headers=None):
    """Create a custom JSON response. 
    (credits: WDI skills-api.common.utils)
    
    Args:
        data: List of objects to place in to the custom response body.
        schema(Schema()): Marshmallow schema to use for serialization of data.
        status (str): HTTP status code to return with the response.
        custom_headers (list): Any optional custom headers to return with the response.
    Returns:
        Custom JSON response.
    """
        
    response = make_response(schema.jsonify(data), status)
    response.headers['Content-Type'] = "application/json"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
    response.headers['Access-Control-Allow-Methods'] = "*"
    response.headers['Access-Control-Allow-Origin'] = "*"

    if custom_headers is not None:
        for custom_header in custom_headers:
            header = custom_header.strip().split('=')
            response.headers[header[0].strip()] = header[1].strip()

    return response