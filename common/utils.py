# -*- coding: utf-8 -*-

import json
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
    
    if schema:
        response = make_response(schema.jsonify(data), status)
    else:
        response = make_response(jsonify(data), status)
    
    response.headers['Content-Type'] = "application/json"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
    response.headers['Access-Control-Allow-Methods'] = "*"
    response.headers['Access-Control-Allow-Origin'] = "*"

    if custom_headers is not None:
        for custom_header in custom_headers:
            header = custom_header.strip().split('=')
            response.headers[header[0].strip()] = header[1].strip()

    return response

def load_json(file_path):
    """Load json from file
    
    :param file_path: absolute file path string
    :returns json_data: deserialized contents of json file
    """
    
    with open(file_path, encoding='utf-8-sig') as json_path:
            json_data = json.load(json_path)
        
    return json_data
