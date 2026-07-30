# 🔍 Google Index Checker - Công Cụ Kiểm Tra Index Hàng Loạt & Phân Tích SEO

Công cụ tự động hóa kiểm tra trạng thái lập chỉ mục (index) của danh sách URL trên Google Search bằng cú pháp tìm kiếm `site:url`. Xuất báo cáo tự động ra file **Excel (`.xlsx`)** và **Markdown (`Index_Report.md`)**.

Dự án tích hợp sẵn **AI Agent Configuration** tối ưu riêng cho **Antigravity** và **Claude Desktop App / Claude Code**.

---

## 🌟 Tính Năng Nổi Bật

- ⚡ **Sử dụng 1-Click đơn giản:** Hỗ trợ nhấp đúp file `run.bat` dành cho người dùng Windows.
- 🤖 **Tích hợp AI Agent sẵn có:** Hỗ trợ trực tiếp **Antigravity** (Skills) và **Claude Desktop App / Claude Code** (`CLAUDE.md`). AI sẽ tự động đọc cấu hình và thực thi kiểm tra khi được yêu cầu.
- 📊 **Xuất báo cáo đa dạng:** Tự động xuất kết quả ra file **Excel (`.xlsx`)** và file **Markdown (`Index_Report.md`)** chi tiết kèm icon phân loại trạng thái.
- 🎯 **Chính xác & Nhanh chóng:** Kết nối API kiểm tra trạng thái index của hàng trăm URL chỉ trong vài phút.

---

## 🚀 Hướng Dẫn Sử Dụng (Quick Start)

### 1. Dùng trên Claude Desktop App (Claude Pro App) / Claude Code 🤖
1. Mở ứng dụng **Claude Desktop App** hoặc **Claude Code**.
2. Mở/Kéo thả thư mục dự án này vào Claude.
3. Dán danh sách URL vào file `urls.txt`.
4. Nhắn cho Claude trong chat:
   > *"Hãy kiểm tra trạng thái index cho danh sách URL trong urls.txt và phân tích bài nào chưa được index giúp tôi."*
   *(Claude sẽ tự động đọc hướng dẫn trong `CLAUDE.md`, chạy script Python và phân tích lý do bài viết chưa index).*

---

### 2. Dùng trên Antigravity AI Agent 🤖
1. Mở thư mục dự án bằng **Antigravity**.
2. Dán danh sách URL vào file `urls.txt`.
3. Nhắn cho Antigravity:
   > *"Kiểm tra index danh sách URL trong urls.txt giúp tôi."*
   *(Antigravity sẽ tự động kích hoạt Skill trong `.agents/skills/check_index_google/SKILL.md` và chạy script).*

---

### 3. Cho Người Dùng Windows (1-Click) 🖱️
1. Mở tệp `urls.txt`, dán danh sách các URL cần kiểm tra vào (mỗi dòng một URL) rồi lưu lại.
2. Nhấp đúp chuột vào file **`run.bat`**.
3. File báo cáo Excel `Index_Report_TIMESTAMP.xlsx` và `Index_Report.md` sẽ tự động xuất hiện tại thư mục dự án.

---

### 4. Cho Người Dùng Linux / macOS / Developer CLI 💻
1. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Cấu hình API Key:** Đảm bảo file `config.json` có chứa API key (tham khảo file `config.json.example`).
3. **Chạy kiểm tra:**
   ```bash
   python check_index.py
   ```
   *Hoặc truyền danh sách URL trực tiếp qua CLI:*
   ```bash
   python check_index.py -u "https://example.com/page1, https://example.com/page2"
   ```

---

## 📁 Cấu Trúc Dự Án

```text
├── check_index.py          # Mã nguồn chính kiểm tra index
├── run.bat                 # Script chạy nhanh 1-click trên Windows
├── requirements.txt        # Danh sách thư viện Python phụ thuộc (pandas, openpyxl...)
├── config.json             # File cấu hình chứa API Key (không push lên git)
├── config.json.example     # File mẫu cấu hình
├── urls.txt                # Danh sách URL cần kiểm tra
├── CLAUDE.md               # Hướng dẫn dành riêng cho Claude Desktop App / Claude Code Agent
├── .agents/skills/         # Thư mục Skill dành riêng cho Antigravity AI Agent
└── README.md               # Hướng dẫn sử dụng dự án
```

---

## 📄 Giấy Phép (License)

Dự án phát hành theo giấy phép [MIT License](LICENSE).
