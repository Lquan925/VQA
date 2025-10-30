import json
import os
import random
from PIL import Image

import google.generativeai as genai
from google.generativeai import types

# --- KHAI BÁO CỐ ĐỊNH ---
IMAGE_DIR = "images"
OUTPUT_FILE = "vqa.json"

# --- CẤU HÌNH PROMPT GEMINI ---
PROMPT_GEMINI = """
Please generate 5 question– short answer pairs in Vietnamese about the image, following exactly these difficulty levels:

Level 1 (Very Easy): Ask about a basic attribute such as color or shape.
Example Q: "Lá cờ trong hình có màu gì?"
Example A: "Đỏ"

Level 2 (Easy): Ask about counting visible objects.
Example Q: "Trong hình có bao nhiêu đèn lồng?"
Example A: "Năm"

Level 3 (Medium): Ask about naming a known object/landmark.
Example Q: "Cây cầu này tên là gì?"
Example A: "Cầu Rồng"

Level 4 (Hard): Ask about cultural or contextual meaning (event, festival, tradition).
Example Q: "Lễ hội nào đang diễn ra trong ảnh này?"
Example A: "Lễ hội Cồng chiêng Tây Nguyên"

Level 5 (Very Hard): Ask about multiple entities and their relations.
Example Q: "Hai cây cầu trong ảnh có tên gì và chúng bắc qua sông nào?"
Example A: "Cầu Trường Tiền và Cầu Nguyễn Hoàng; sông Hương"

Return the result strictly as a JSON array of 5 objects, each object having one key–value pair where the key is the question and the value is the answer.
Example format:
[
  {"question":"question1", "answer":"answer1","level":1},
  ....
]
"""

# --- HÀM TẠO VQA TỪ GEMINI ---
def get_gemini_response(image_path: str, model: genai.GenerativeModel) -> dict:
    """
    Tạo câu hỏi-trả lời (VQA) bằng Gemini từ file ảnh đã cho.
    
    Args:
        image_path: Đường dẫn đầy đủ đến file ảnh.
        model: Đối tượng Gemini model đã cấu hình.
        
    Returns:
        Một dict chứa dữ liệu JSON đã trích xuất hoặc thông báo lỗi.
    """
    
    try:
        image = Image.open(image_path)
    except Exception as e:
        # print(f"❌ Lỗi: Không thể mở file ảnh: {image_path}. Lỗi: {e}")
        return {"error": "Image open failed"}

    try:
        response = model.generate_content(
            contents=[
                image,
                PROMPT_GEMINI.strip()
            ]
        )
    except Exception as e:
        print(f"❌ Lỗi khi gọi API Gemini: {e}")
        image.close()
        return {"error": "Gemini API call failed", "raw_response": str(e)}

    image.close()

    try:
        json_string = response.text.strip()
        if json_string.startswith("```json") and json_string.endswith("```"):
            json_string = json_string[7:-3].strip()
        extracted_data = json.loads(json_string)
        
        if not isinstance(extracted_data, list) or len(extracted_data) != 5:
             raise ValueError("Định dạng JSON không đúng (không phải list 5 mục).")
             
    except (json.JSONDecodeError, ValueError) as e:
        # print(f"❌ Lỗi xử lý JSON: {e}. Raw Response: {response.text}")
        extracted_data = {"error": "Failed to parse Gemini response", "raw_response": response.text}
    except Exception as e:
        # print(f"❌ Lỗi không xác định khi xử lý response: {e}. Raw Response: {response.text}")
        extracted_data = {"error": "Unknown response error", "raw_response": response.text}
    
    return extracted_data

# --- CHƯƠNG TRÌNH CHÍNH ---

# Cấu hình API key và tạo mô hình
try:
    # VUI LÒNG THAY API KEY CỦA BẠN VÀO ĐÂY
    genai.configure(api_key="AIzaSyB3s5itOHKuyFHe6ygoUc2M5xMnPVQQ4oo") 
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    print(f"❌ Lỗi khi cấu hình Gemini: {e}")
    exit()

data_out = []
processed_paths = set() 

# Bước 1: Đọc dữ liệu cũ từ vqa.json (nếu có)
if os.path.exists(OUTPUT_FILE):
    print(f"Đang đọc file {OUTPUT_FILE} cũ...")
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as fr:
            data_out = json.load(fr)
            if isinstance(data_out, list):
                for item in data_out:
                    if 'image_path' in item: 
                        processed_paths.add(item['image_path'])
            else:
                data_out = []
            print(f"✅ Đã tải {len(data_out)} mục đã xử lý từ file {OUTPUT_FILE}.")
    except Exception:
        print(f"⚠️ File {OUTPUT_FILE} bị lỗi hoặc rỗng. Bắt đầu tạo file mới.")
        data_out = []
else:
    print(f"File {OUTPUT_FILE} không tồn tại. Bắt đầu tạo mới.")


# Bước 2: Duyệt đệ quy qua thư mục ảnh
if not os.path.exists(IMAGE_DIR):
    print(f"❌ Lỗi: Không tìm thấy thư mục ảnh '{IMAGE_DIR}'.")
    exit()

valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
files_to_process = []

print(f"\n--- Bắt đầu quét thư mục '{IMAGE_DIR}' và các thư mục con... ---")

# Sử dụng os.walk để duyệt đệ quy
for root, dirs, files in os.walk(IMAGE_DIR):
    for file_name in files:
        if file_name.lower().endswith(valid_extensions):
            full_path = os.path.join(root, file_name)
            # Lưu trữ đường dẫn tương đối (ví dụ: images/Nhà thờ/image.jpg) để tránh lỗi trên các máy khác nhau
            relative_path = os.path.relpath(full_path) 
            files_to_process.append(relative_path)
            
print(f"✅ Tìm thấy {len(files_to_process)} file ảnh hợp lệ.")

# Bước 3: Xử lý từng file ảnh
for image_path in files_to_process:
    
    if image_path in processed_paths:
        print(f"👍 Ảnh '{image_path}' đã có trong {OUTPUT_FILE}, bỏ qua.")
        continue

    print(f"Đang xử lý ảnh MỚI: {image_path}")
    
    data_gemini = get_gemini_response(image_path, model)
    
    if "error" in data_gemini:
        print(f"❌ Lỗi từ Gemini, bỏ qua ảnh: {image_path}. Chi tiết: {data_gemini.get('raw_response', 'Không có chi tiết lỗi')[:100]}...") # Giới hạn in ra 100 ký tự lỗi
        continue

    # Lưu kết quả
    tmp = {"image_path": image_path} # Dùng image_path để lưu đường dẫn tương đối
    try:
        for idx, eg in enumerate(data_gemini):
            tmp[f'q{idx+1}'] = eg["question"]
            tmp[f'a{idx+1}'] = eg["answer"]
    except Exception:
        print(f"❌ Lỗi định dạng dữ liệu trả về từ Gemini cho ảnh {image_path}. Bỏ qua.")
        continue
        
    data_out.append(tmp)
    processed_paths.add(image_path)
    
    # Lưu file (liên tục) sau mỗi lần thêm dữ liệu mới
    random.shuffle(data_out)
    with open(OUTPUT_FILE,"w",encoding="utf-8") as fw:
        json.dump(data_out, fw, indent=4, ensure_ascii=False)
    
print("\n--- HOÀN THÀNH ---")
print(f"Đã xử lý và lưu thành công tổng cộng {len(data_out)} mục (VQA) vào file {OUTPUT_FILE}.")

# Lưu file lần cuối
with open(OUTPUT_FILE,"w",encoding="utf-8") as fw:
    json.dump(data_out, fw, indent=4, ensure_ascii=False)