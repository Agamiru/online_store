from typing import Union

from django.db import models
from django.conf import settings

import cloudinary
from cloudinary import uploader

# CLOUDINARY_SECRET = settings.CLOUDINARY.get("api_secret")
#
# django_model = models.Model

cloudinary.config(**settings.CLOUDINARY)

path_or_url = Union[str, bytes]
response_or_error = Union[dict, cloudinary.exceptions.Error]


# Generic uploader for cloudnary images
def upload_image_or_error(image: path_or_url, public_id: str) -> response_or_error:

    upload_kwargs = {
        "file": image, "public_id": public_id,
        "type": "upload", "access_mode": "public",
        "allowed_formats": ["jpg", "png"], "invalidate": True
    }
    try:
        return uploader.upload(**upload_kwargs)
    except cloudinary.exceptions.Error as e:
        return e











# def get_cloudinary_notification_headers(request) -> Dict[str, Union[str, None]]:
#     # For rest_framework parsed request
#     if hasattr(request, "data"):
#         request = request._request
#
#     timestamp = "X-Cld-Timestamp"
#     signature = "X-Cld-Signature"
#
#     timestamp = request.headers.get(timestamp)
#     signature = request.headers.get(signature)
#
#     # Can both be none
#     return {"timestamp": timestamp, "signature": signature}
#
#
# def validate_notification_signature(
#         request, api_secret=CLOUDINARY_SECRET) -> bool:
#     """
#     Returns a bool or error dict if timestamp/signature is None
#     """
#     header_kwargs = get_cloudinary_notification_headers(request)
#     request_timestamp = header_kwargs.get("timestamp")
#     request_signature = header_kwargs.get("signature")
#
#     if (request_timestamp or request_signature) is None:
#         raise NoneTypeError(["Timestamp", "Signature"])
#
#     # For rest_framework parsed request
#     if hasattr(request, "data"):
#         # Parse request.data to original json format representation as a string
#         # json.dumps removes the extra spaces
#         # replace, replaces single with double quotes
#         json_body = json.dumps(request.data, separators=(",", ":")).replace("'", '"')
#         hash_string = json_body + request_timestamp + api_secret
#     else:
#         # For django requests
#         # Convert request.body from bytes to dict
#         json_body = json.loads(request.body.decode(encoding=DEFAULT_CHARSET))
#         # Convert dict to string
#         json_body = json.dumps(json_body, separators=(",", ":")).replace("'", '"')
#         hash_string = json_body + request_timestamp + api_secret
#
#     generated_signature = hashlib.sha1(hash_string.encode(DEFAULT_CHARSET)).hexdigest()
#
#     if generated_signature == request_signature:
#         return True
#     return False
