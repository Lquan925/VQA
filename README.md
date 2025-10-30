## 🧠 Visual Question Answering (VQA)

- Dự án này triển khai mô hình trả lời câu hỏi dựa trên hình ảnh (Visual Question Answering).  
- Người dùng nhập một hình ảnh và một câu hỏi liên quan, mô hình sẽ suy luận để đưa ra câu trả lời phù hợp.
- Ví dụ:  
  - Ảnh: Một con chó đang gặm xương.  
  - Câu hỏi: “Con vật trong ảnh là gì?”  
  - Trả lời: “Con Chó.”

## ✨ Tính năng
- Nhận đầu vào là **ảnh + câu hỏi**.
- Dự đoán câu trả lời bằng mô hình VQA (Transformer/CNN + LLM).
- Hỗ trợ **ngôn ngữ tiếng Việt**.
- Có thể huấn luyện lại với dataset tùy chỉnh.

## 🧩 Dataset & Training
### 1️⃣ Thu thập dữ liệu
- Dữ liệu được lấy từ **DATASET** (https://drive.google.com/drive/u/0/folders/1OkH_aZEHb5byK2kYPnRyTt85VYrwNSPC), gồm:
  - ~300 địa điểm
  - ~2,000 ảnh
  - ~10000 câu hỏi
  - ~10000 câu trả lời gán nhãn

