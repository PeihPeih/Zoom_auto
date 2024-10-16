from fastapi import APIRouter, Request

webhook_router = APIRouter()

@webhook_router.post("/webhook")
async def zoom_webhook(request: Request):
    payload = await request.json()
    
    # Xử lý dữ liệu từ webhook
    event = payload.get("event")
    meeting_data = payload.get("payload", {}).get("object", {})
    
    if event == "meeting.started":
        meeting_id = meeting_data.get("id")
        host_id = meeting_data.get("host_id")
        print(f"Cuộc họp {meeting_id} đã bắt đầu bởi {host_id}")
    
    elif event == "meeting.ended":
        meeting_id = meeting_data.get("id")
        print(f"Cuộc họp {meeting_id} đã kết thúc")
    
    return {"status": "received"}