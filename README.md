# 🔍 Google Index Checker - Công Cụ Kiểm Tra Index Hàng Loạt (Playwright Chromium Engine)

Công cụ tự động hóa kiểm tra trạng thái lập chỉ mục (index) của danh sách URL trên Google Search bằng cú pháp tìm kiếm `site:url`. Hỗ trợ quét hàng loạt từ **100 đến 500+ URL** mượt mà nhờ công nghệ **Trình duyệt ngầm Playwright Chromium**.

---

## 🌟 Tính Năng Nổi Bật

- 🤖 **Trình duyệt ngầm Playwright Chromium Engine:** Tự động mở trình duyệt Chrome ngầm giả lập người dùng thật 100%, không bị CAPTCHA hay chặn IP.
- 🔓 **Không cần Google Cloud / Billing:** Quét tự do hoàn toàn miễn phí mà không cần API Key rắc rối.
- ⚡ **Sử dụng 1-Click đơn giản:** Hỗ trợ nhấp đúp file `run.bat` dành cho người dùng Windows không chuyên về lập trình.
- 📊 **Xuất báo cáo đa dạng:** Tự động xuất kết quả ra file **Excel (`.xlsx`)** và file **Markdown (`.md`)** chi tiết kèm icon phân loại trạng thái.
- 🎯 **Chính xác 100%:** Phân tích trực tiếp kết quả thô trên Google Search, loại bỏ hiện tượng báo sai (dương tính giả).

---

## 🚀 Hướng Dẫn Sử Dụng Nhanh (Quick Start)

### Cho Người Dùng Windows (1-Click)

1. **Cài đặt Python:** Tải và cài đặt [Python 3.x](https://www.python.org/downloads/) (Nhớ tích chọn *"Add Python to PATH"* khi cài đặt).
2. **Chuẩn bị URL:** Mở tệp `urls.txt`, dán danh sách các URL cần kiểm tra vào (mỗi dòng một URL) rồi lưu lại.
3. **Chạy công cụ:** Nhấp đúp chuột vào file **`run.bat`**.
4. **Nhận báo cáo:** File báo cáo Excel `Index_Report_TIMESTAMP.xlsx` sẽ tự động xuất hiện tại thư mục dự án.

---

### Cho Người Dùng Linux / macOS / Developer

1. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install -r requirements.txt
   python -m playwright install chromium
   ```
2. **Dán danh sách URL vào `urls.txt`**
3. **Chạy câu lệnh:**
   ```bash
   python check_index.py
   ```
   *Hoặc truyền danh sách URL trực tiếp qua tham số CLI:*
   ```bash
   python check_index.py -u "https://example.com/page1, https://example.com/page2"
   ```

---

## 📁 Cấu Trúc Dự Án

```text
├── check_index.py          # Mã nguồn chính sử dụng Playwright Chromium Engine
├── run.bat                 # Script chạy nhanh 1-click trên Windows
├── requirements.txt        # Danh sách thư viện Python phụ thuộc (playwright, pandas...)
├── config.json.example     # File mẫu cấu hình (tùy chọn)
├── urls.txt                # Danh sách URL cần kiểm tra
└── README.md               # Hướng dẫn sử dụng dự án
```

---

## 📄 Giấy Phép (License)

Dự án phát hành theo giấy phép [MIT License](LICENSE). Bạn có thể tự do chia sẻ, chỉnh sửa và sử dụng cho dự án cá nhân hoặc thương mại.
