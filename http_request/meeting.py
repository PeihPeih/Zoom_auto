from pydantic import BaseModel
import datetime

class CreateMeetingRequest(BaseModel):
    topic: str
    type: int
    start_time: str = datetime.datetime.now().isoformat()
    duration: int
    timezone: str
    agenda: str
    password: str = None  # Mật khẩu có thể không bắt buộc
    settings: dict = None  # Cài đặt bổ sung