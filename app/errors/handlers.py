from typing import Any, Dict, Optional

error_types = {
    "not_found": {
        "type": "Not Found",
        "status": 404
    },
    "conflict": {
        "type": "Conflict or exist",
        "status": 409
    },
    "internal_server": {
        "type": "Internal server error",
        "status": 500
    },
}

class AppException(Exception):
    def __init__(self, error_type: str, message: str, details: Optional[Dict[str, Any]] = None):
        self.error_type = error_type
        self.message = message
        self.details = details

class DatabaseException(AppException):
    def __init__(self, error_type: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(error_type, message, details)

