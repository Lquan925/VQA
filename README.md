 Giới thiệu
Dự án này tự động tạo dữ liệu huấn luyện cho mô hình Visual Question Answering (VQA) bằng cách:
Tải ảnh từ Wikimedia dataset.
Gửi ảnh cho mô hình Gemini để sinh ra 5 cặp câu hỏi – trả lời bằng tiếng Việt ở các mức độ khác nhau.
Lưu toàn bộ kết quả thành file JSON (vqa.json) theo định dạng sẵn sàng cho Label Studio hoặc các mô hình VQA khác.

Công nghệ sử dụng
Ngôn ngữ: Python 3.10+
Thư viện:
requests – tải ảnh từ Internet
PIL (Pillow) – xử lý ảnh
google-genai – gọi API Gemini
json, os, random – xử lý dữ liệu
Mô hình AI: gemini-2.5-flash từ Google

