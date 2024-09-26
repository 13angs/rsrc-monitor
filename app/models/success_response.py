from typing import Any, Dict, Optional
from pydantic import BaseModel

class SuccessResponse(BaseModel):
    data: Optional[Dict[str, Any]] = None
    status: int
    message: Optional[str]