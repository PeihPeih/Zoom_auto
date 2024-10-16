from fastapi import APIRouter, HTTPException, Depends
import requests
from common.auth import get_token
from http_request.meeting import CreateMeetingRequest

router = APIRouter()

@router.get("/meetings/users/{user_id}", summary="Get meeting list by user's id")
async def get_meeting_list(user_id: str, ACCESS_TOKEN: str = Depends(get_token)):
    # Gọi API để lấy danh sách cuộc họp
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(
        f"https://api.zoom.us/v2/users/{user_id}/meetings", headers=headers)

    if response.status_code == 200:
        return response.json().get('meetings', [])

    # Nếu token hết hạn, yêu cầu refresh token
    # if response.status_code == 401:
    #     await refresh_token()  # Gọi hàm refresh_token để cập nhật access token
    #     return await get_meeting_list(user_id)  # Thử lại lần nữa

    raise HTTPException(status_code=response.status_code,
                        detail=response.json())


@router.get("/meetings/{meeting_id}", summary = "Get a meeting by meeting's id")
async def get_meeting_list(meeting_id: str, ACCESS_TOKEN: str = Depends(get_token)):
    # Gọi API để lấy danh sách cuộc họp
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(
        f"https://api.zoom.us/v2/meetings/{meeting_id}", headers=headers)

    if response.status_code == 200:
        return response.json()

    # Nếu token hết hạn, yêu cầu refresh token
    # if response.status_code == 401:
    #     await refresh_token()  # Gọi hàm refresh_token để cập nhật access token
    #     return await get_meeting_list(user_id)  # Thử lại lần nữa

    raise HTTPException(status_code=response.status_code,
                        detail=response.json())


# tạo cuộc họp 
@router.post("/meetings", summary="Create a meeting")
async def create_meeting(meeting: CreateMeetingRequest, ACCESS_TOKEN: str = Depends(get_token)):
    # Gọi API để tạo cuộc họp
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.zoom.us/v2/users/me/meetings", headers=headers, json=meeting.dict())

    if response.status_code == 201:
        return response.json()

    # # Nếu token hết hạn, yêu cầu refresh token
    # if response.status_code == 401:
    #     await refresh_token()  # Cập nhật access token
    #     return await create_meeting(meeting)  # Thử lại lần nữa

    raise HTTPException(status_code=response.status_code,
                        detail=response.json())
