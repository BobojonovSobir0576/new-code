SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "JWT [Bearer {JWT}]": {
            "name": "Authorization",
            "type": "apiKey",
            "in": "header",
        }
    },
    "TITLE": "Test",
    "DESCRIPTION": "Test",
    "VERSION": "0.1.0",
    "USE_SESSION_AUTH": False,
}
SPECTACULAR_SETTINGS = {
    "TITLE": "Test",
    "DESCRIPTION": "Test",
    "VERSION": "0.1.0"
}