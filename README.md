# ร้านยำปูม้าเจ็ดยอด - ระบบจัดการร้านอาหาร

ระบบจัดการร้านอาหาร ที่รองรับการจองโต๊ะ, จัดการเมนู, และรายงานยอดขาย

## 🛠️ เทคโนโลยีที่ใช้

### Backend
- **Python 3.x** - ภาษาหลักสำหรับการพัฒนา
- **Flask** - Web Framework สำหรับสร้าง API และจัดการ routing
- **SQLite** - ฐานข้อมูล relational

### Frontend
- **HTML5** - โครงสร้างเนื้อหา
- **CSS3** - การออกแบบสไตล์
- **Bootstrap 5** - Framework CSS สำหรับ responsive design
- **Jinja2** - Template engine (ทำงานกับ Flask)

### Tools & Libraries
- **Werkzeug** - WSGI utilities และ secure file handling
- **SQLite3** - Database driver สำหรับ Python

## 📋 ความสามารถหลัก

### ฝั่งเว็บไซต์ (Frontend)
- 📱 **หน้าแสดงเมนู** - ดูรายการอาหารพร้อมรูปและราคา
- 🛒 **ตะกร้าอาหาร** - เพิ่ม/ลบ/แก้ไขจำนวนอาหาร
- 🪑 **ระบบจองโต๊ะ** - จองโต๊ะพร้อมเลือกวันที่/เวลา/จำนวนคน
- 👀 **ดูการจองของฉัน** - ค้นหาและแสดงการจองทั้งหมด
- ✏️ **แก้ไขการจอง** - เปลี่ยนเวลา หรือ จำนวนคน ได้ตลอดเวลา
- ❌ **ยกเลิกการจอง** - ยกเลิกการจองที่ไม่ต้องการ
- 📋 **ระบบบิล** - ออกใบเสร็จหลังสั่งอาหาร

### ฝั่งแอดมิน (Admin)
- 🔐 **ระบบ Login** - เข้าสู่ระบบแอดมิน
- 🍽️ **จัดการเมนู** - เพิ่ม/แก้ไข/ลบเมนูอาหาร
- 📸 **อัปโหลดรูป** - เพิ่มรูปภาพสำหรับเมนูอาหาร
- 📊 **ดูการจองทั้งหมด** - แสดงรายการจดหมายของลูกค้า
- 💰 **รายงานยอดขาย** - สถิติยอดขายรายวัน/รายเดือน

## 📁 โครงสร้างไฟล์

```
mini_project_2/
├── app.py                   # ไฟล์หลักของ Flask application
├── models.py               # Database models และ DatabaseManager class
├── README.md              # ไฟล์นี้
├── yumpooma.db            # ฐานข้อมูล SQLite
├── static/                # ไฟล์ static (รูปภาพ, CSS)
│   ├── logo.jpg
│   ├── seat.png
│   └── shopping-cart.png
└── templates/             # HTML templates
    ├── frontend/          # หน้าเว็บไซต์สำหรับลูกค้า
    │   ├── base.html
    │   ├── layout.html
    │   ├── index.html
    │   ├── menu.html
    │   ├── cart.html
    │   ├── contact.html
    │   ├── reservation.html
    │   ├── my_reservations_search.html
    │   ├── my_reservations_list.html
    │   ├── edit_reservation.html
    │   ├── order_bill.html
    │   └── order_success.html
    └── admin/             # หน้าแอดมิน
        ├── layout_admin.html
        ├── login.html
        ├── menu_manage.html
        ├── menu_add.html
        ├── menu_edit.html
        ├── reservations.html
        ├── dashboard.html
        └── sales_report.html
```

## 🚀 การติดตั้งและรัน

### ข้อกำหนด
- Python 3.7+
- pip (Package manager)

### ขั้นตอนการติดตั้ง

1. **Clone หรือ Download โปรเจ็กต์**
   ```bash
   cd mini_project_2
   ```

2. **สร้าง Virtual Environment (ทางเลือก)**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **ติดตั้ง Dependencies**
   ```bash
   pip install flask werkzeug
   ```

4. **รันแอปพลิเคชัน**
   ```bash
   python app.py
   ```

5. **เข้าถึงแอปพลิเคชัน**
   - หน้าหลัก: `http://localhost:5000/`
   - แอดมิน: `http://localhost:5000/admin/login`

## 📊 ฐานข้อมูล

### ตารางหลัก
- **menus** - เมนูอาหاร (id, name, price, description, image, category)
- **reservations** - การจองโต๊ะ (id, name, phone, date, time, table_no, people)
- **admin** - ข้อมูลแอดมิน (id, username, password)
- **bills** - ใบเสร็จ (id, table_no, bill_time, items, total)
- **sales** - บันทึกยอดขาย (id, sale_date, menu_id, quantity, total_price)

## 🔍 ตัวอย่าง Routes หลัก

### Frontend Routes
| Route | Method | คำอธิบาย |
|-------|--------|---------|
| `/` | GET | หน้าแรก |
| `/menu` | GET | แสดงเมนูอาหาร |
| `/reservation` | GET, POST | จองโต๊ะ |
| `/my_reservations` | GET, POST | ค้นหาการจอง |
| `/my_reservations/<phone>` | GET | ดูการจองทั้งหมด |
| `/edit_reservation/<id>` | GET, POST | แก้ไขการจอง |
| `/cancel_reservation/<id>` | GET | ยกเลิกการจอง |
| `/cart` | GET | ดูตะกร้า |
| `/contact` | GET | ติดต่อเรา |

### Admin Routes
| Route | Method | คำอธิบาย |
|-------|--------|---------|
| `/admin/login` | GET, POST | เข้าสู่ระบบ |
| `/admin/menus` | GET | จัดการเมนู |
| `/admin/menus/add` | GET, POST | เพิ่มเมนู |
| `/admin/menus/edit/<id>` | GET, POST | แก้ไขเมนู |
| `/admin/reservations` | GET | ดูการจองทั้งหมด |
| `/admin/sales_report` | GET | รายงานยอดขาย |

## 💡 ลักษณะเด่น

✨ **Responsive Design** - ทำงานได้ดีบนทุกขนาดหน้าจอ (Mobile, Tablet, Desktop)

✨ **ตรวจสอบการชนกัน** - ระบบตรวจสอบว่าโต๊ะมีการจองอื่นในช่วงเวลาเดียวกานหรือไม่

✨ **ส่วนเก็บหลายถาดชั้น** - แยกระหว่างเว็บไซต์และแอดมิน

✨ **ระบบบิลอัตโนมัติ** - ออกใบเสร็จ บันทึกยอดขายโดยอัตโนมัติ

## 📝 หมายเหตุ

- ระบบใช้ SQLite ซึ่งเหมาะสำหรับแอปพลิเคชันขนาดเล็กถึงกลาง
- รหัสผ่านแอดมินถูกเก็บเป็นข้อความธรรมชาติ (ในสภาพแวดล้อมผลิตภาพ ควรใช้ Hashing)
- ระบบใช้ Session แบบ Client-side (หากต้องการความปลอดภัยสูง ควรใช้ Server-side Sessions)

## 👨‍💼 ผู้พัฒนา

โปรเจ็กต์นี้เป็นระบบจัดการร้านอาหารสำหรับการเรียน

---

**Last Updated:** March 2026
