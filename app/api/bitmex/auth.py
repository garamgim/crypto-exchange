import hashlib
import hmac
import json
import urllib
from urllib.parse import urlparse

from pydantic import BaseModel


def generate_signature(secret, verb, url, nonce, query_params=None, data=""):
    # https://github.com/BitMEX/api-connectors/blob/master/official-http/python-swaggerpy/BitMEXAPIKeyAuthenticator.py

    # Parse the URL to extract the path
    parsedURL = urlparse(url)
    path = parsedURL.path

    # Append query parameters to the path if they exist
    if query_params:
        path = path + '?' + urllib.parse.urlencode(query_params, doseq=True)

    # If the data is in bytes or bytearray, decode it to a string
    if isinstance(data, (bytes, bytearray)):
        data = data.decode('utf8')

    # Create the message to be signed: verb + path + nonce + data
    message = verb + path + str(nonce) + data

    # Generate the HMAC signature using SHA-256 and return it
    signature = hmac.new(bytes(secret, 'utf8'), bytes(message, 'utf8'), digestmod=hashlib.sha256).hexdigest()
    return signature


def to_valid_json(data):
    # If the data is a Pydantic BaseModel, convert it to a dictionary and exclude None values
    if isinstance(data, BaseModel):
        data = data.model_dump(exclude_none=True)

    # If the data is a dictionary, convert it to a JSON string (no extra spaces or newlines), excluding None values
    if isinstance(data, dict):
        data = json.dumps({key: value for key, value in data.items() if value is not None}, separators=(',', ':'))

    return data

