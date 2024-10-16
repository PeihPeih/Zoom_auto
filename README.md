# Thành viên
- Nguyễn Tiến Hiệp: B21DCCN048
- Chu Minh Hiếu: B21DCCN348
- Nguyễn Quốc Khánh: B21DCCN456

# Ứng Dụng Zoom API và Webhook cho Tự Động Hóa và Ghi Log Cuộc Họp

## Chức năng của Hệ thống:

### 1. Tự động hóa quy trình:
- Sử dụng **Zoom API** để tự động hóa các tác vụ như:
  - Lên lịch cuộc họp.
  - Gửi lời mời tham gia họp.
  - Ghi chú cuộc họp.
  - Quản lý người tham gia.
- Giảm thiểu thao tác thủ công và tăng hiệu quả quản lý cuộc họp.

### 2. Ghi log:
- Lưu trữ thông tin chi tiết về các cuộc họp, bao gồm:
  - Thời gian bắt đầu và kết thúc cuộc họp.
  - Thông tin người tham gia (tên, email).
  - Trạng thái cuộc họp (đã bắt đầu, đang diễn ra, đã kết thúc).
  - Nội dung hoặc ghi chú cuộc họp (nếu có).

### 3. Sử dụng Webhook:
- Thiết lập **webhook** để nhận thông báo theo thời gian thực khi có sự kiện xảy ra, chẳng hạn như:
  - Cuộc họp mới được tạo.
  - Người tham gia mới vào hoặc rời cuộc họp.
  - Cuộc họp kết thúc hoặc có bất kỳ thay đổi trạng thái nào.
- Tự động cập nhật và ghi log theo các sự kiện mà không cần phải kiểm tra thủ công.

