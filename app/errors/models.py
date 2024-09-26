from pydantic import BaseModel
from typing import Any, Dict, Optional

class ErrorDetails(BaseModel):
    type: str
    message: str
    details: Optional[Dict[str, Any]] = None