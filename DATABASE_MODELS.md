# Database Models

เอกสารนี้สรุปโครงสร้างตารางและคลาส data model ที่ใช้ในโปรเจกต์

## ตารางใน SQLite

- **menus**
  - เก็บรายการอาหาร/เครื่องดื่ม
  - ฟิลด์: id, name, price, description, image, category

- **reservations**
  - ข้อมูลการจองโต๊ะ
  - ฟิลด์: id, name, phone, date, time, table_no, people, status

- **bills**
  - บิลการสั่งอาหารของโต๊ะ
  - ฟิลด์: id, table_no, bill_time, items (JSON), total

- **sales**
  - บันทึกยอดขายแยกรายเมนู (ใช้สร้างรายงานสถิติ)
  - ฟิลด์: id, sale_date, menu_id, quantity, total_price

- **admin**
  - ผู้ดูแลระบบเข้าใช้งานหลังบ้าน
  - ฟิลด์: id, username, password

## คลาส `@dataclass` ใน `models.py`

```python
@dataclass
class Menu:
    id: int
    name: str
    price: float
    description: Optional[str]
    image: Optional[str]
    category: str
```
- แทนแถวหนึ่งในตาราง `menus` ใช้สำหรับ serialize/deserialize เวลาอ่านจาก DB หรือส่งให้เทมเพลต

```python
@dataclass
class Reservation:
    id: int
    name: str
    phone: str
    date: str
    time: str
    table_no: int
    people: int
    status: Optional[str] = None
```
- ข้อมูลการจอง เหมือนแถวใน `reservations` ช่วยให้โค้ดระดับอื่น (เช่น view) ทำงานง่ายขึ้น

```python
@dataclass
class Bill:
    id: int
    table_no: int
    bill_time: str
    items: List[Dict[str, Any]]
    total: float
```
- ตัวแทนข้อมูลบิล เมื่ออ่านจาก `bills` จะคืน `items` เป็น JSON แปลงเป็น Python list ของ dictionary

```python
@dataclass
class Sale:
    id: int
    sale_date: str
    menu_id: int
    quantity: int
    total_price: float
```
- ใช้เมื่อบันทึกหรืออ่านยอดขายในตาราง `sales`

```python
@dataclass
class Admin:
    id: int
    username: str
    password: str
```
- เป็นโมเดลสำหรับตาราง `admin` ใช้กับฟังก์ชันยืนยันตัวตน

## คลาส `DatabaseManager`

ครอบคลุมการเชื่อมต่อและการใช้งาน SQL ของแต่ละตาราง

- `get_menus()`, `get_menu()`, `add_menu()`, `update_menu()`, `delete_menu()`
- `get_reservations()`, `has_conflicting_reservation()`, `add_reservation()`, `delete_reservation()`, `get_user_reservations()`, `get_reservation()`, `update_reservation()`
- `authenticate_admin()`
- `add_bill_and_sales()`

ทุกเมธอดใช้ `sqlite3` และ `contextlib.closing` เพื่อเปิด-ปิดการเชื่อมต่ออย่างปลอดภัย

---

