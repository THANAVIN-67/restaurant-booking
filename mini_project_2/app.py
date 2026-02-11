from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import DatabaseManager

app = Flask(__name__)
app.secret_key = "supersecret123"
app.jinja_env.globals.update(session=session)

# สร้าง instance ของ DatabaseManager
DB_PATH = 'yumpooma.db'
db = DatabaseManager(DB_PATH)


# --- ระบบตะกร้าอาหาร ---
def get_cart():
    return session.get('cart', [])


@app.route('/order_bill/<int:bill_id>')
def order_bill(bill_id):
    bill = db.get_bill(bill_id)
    import json
    items = json.loads(bill['items']) if bill and bill.get('items') else []
    return render_template('frontend/order_bill.html', bill=bill, items=items)


@app.route('/order_success')
def order_success():
    return render_template('frontend/order_success.html')


@app.route('/')
def index():
    # show featured or all menus on the homepage
    try:
        menu_items = db.get_menus()
    except Exception:
        menu_items = []
    return render_template('frontend/index.html', menu_items=menu_items)


@app.route("/menu")
def menu():
    menu_items = db.get_menus()
    return render_template("frontend/menu.html", menu_items=menu_items)

@app.route("/reservation", methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form.get('phone', '')
        date = request.form['date']
        time = request.form['time']
        table_no = request.form.get('table_no', None)
        people = request.form['people']

        # ตรวจสอบการจองซ้ำ
        from datetime import datetime, timedelta
        try:
            time_obj = datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')
        except Exception:
            flash('เวลาที่เลือกไม่ถูกต้อง', 'danger')
            return render_template("frontend/reservation.html")
        start_time = (time_obj - timedelta(minutes=30)).strftime('%H:%M')
        end_time = (time_obj + timedelta(hours=1)).strftime('%H:%M')
        # ใช้ DatabaseManager เพื่อตรวจสอบการชนกัน
        if db.has_conflicting_reservation(date, int(table_no) if table_no else None, start_time, end_time):
            return render_template("frontend/reservation.html", error_msg='มีคนจองโต๊ะนี้ในช่วงเวลานี้แล้ว กรุณาเลือกเวลาอื่น')
        # ถ้าไม่ซ้ำ ให้บันทึกการจอง
        db.add_reservation(name, phone, date, time, int(table_no) if table_no else None, int(people))
        flash('Reservation added successfully!', 'success')
        return redirect(url_for('reservation'))
    return render_template("frontend/reservation.html")

@app.route("/contact")
def contact():
    return render_template("frontend/contact.html")

# หลังบ้าน

# เก็บฟังก์ชัน get_db_connection() ไว้ไม่จำเป็นอีก เพราะ DatabaseManager ดูแลการเชื่อมต่อ

# ระบบ Login Admin
from flask import session

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.authenticate_admin(username, password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('admin_menus'))
        else:
            flash('Invalid username or password', 'danger')
            return render_template('admin/login.html')
    return render_template('admin/login.html')

@app.route('/admin/menus')
def admin_menus():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    menus = db.get_menus()
    return render_template('admin/menu_manage.html', menus=menus)

@app.route('/admin/menus/add', methods=['GET', 'POST'])
def add_menu():
    import os
    from werkzeug.utils import secure_filename
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description'] or None
        category = request.form['category']
        image_file = request.files.get('image')
        image_filename = None
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join('static', filename)
            image_file.save(image_path)
            image_filename = filename
        db.add_menu(name, float(price), description, image_filename, category)
        flash('Menu added successfully!', 'success')
        return redirect(url_for('admin_menus'))
    return render_template('admin/menu_add.html')

@app.route('/admin/menus/edit/<int:id>', methods=['GET', 'POST'])
def edit_menu(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    menu = db.get_menu(id)
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description'] or None
        image = request.form['image'] or None
        category = request.form['category']
        db.update_menu(id, name, float(price), description, image, category)
        flash('Menu updated successfully!', 'success')
        return redirect(url_for('admin_menus'))
    return render_template('admin/menu_edit.html', menu=menu)

@app.route('/admin/menus/delete/<int:id>')
def delete_menu(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    db.delete_menu(id)
    flash('Menu deleted successfully!', 'success')
    return redirect(url_for('admin_menus'))

@app.route('/admin/reservations')
def admin_reservations():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    reservations = db.get_reservations()
    return render_template('admin/reservations.html', reservations=reservations)

@app.route('/admin/reservations/delete/<int:id>')
def delete_reservation(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    db.delete_reservation(id)
    flash('Reservation deleted successfully!', 'success')
    return redirect(url_for('admin_reservations'))
       

# รายงานยอดขายรายวัน/รายเดือน
from datetime import datetime
@app.route('/admin/sales_report')
def sales_report():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    # รายวัน
    today = datetime.now().strftime('%Y-%m-%d')
    daily = db.get_daily_sales(today)
    # รายเดือน (แยกแต่ละเดือน)
    rows = db.get_monthly_sales()
    monthly_list = []
    for r in rows:
        year_thai = int(r['year']) + 543 if r.get('year') else ''
        monthly_list.append({
            'month': r.get('month'),
            'year_thai': year_thai,
            'qty': r.get('qty'),
            'total': r.get('total')
        })
    return render_template('admin/sales_report.html', daily=daily, monthly_list=monthly_list)


# (no-op) cart helper already defined above

@app.route('/cart')
def cart():
    cart = get_cart()
    # คำนวณยอดรวมแต่ละรายการ
    for item in cart:
        item['total'] = item['price'] * item['quantity']
    return render_template('frontend/cart.html', cart=cart)

@app.route('/cart/add/<int:menu_id>', methods=['POST'])
def cart_add(menu_id):
    menu = db.get_menu(menu_id)
    if not menu:
        flash('ไม่พบเมนู', 'danger')
        return redirect(url_for('menu'))
    cart = session.get('cart', [])
    # ตรวจสอบว่ามีเมนูนี้ในตะกร้าแล้วหรือยัง
    for item in cart:
        if item['id'] == menu_id:
            item['quantity'] += 1
            break
    else:
        cart.append({
            'id': menu_id,
            'name': menu['name'],
            'price': menu['price'],
            'quantity': 1
        })
    session['cart'] = cart
    flash('เพิ่มเมนูเข้าตะกร้าแล้ว', 'success')
    return redirect(url_for('menu'))

@app.route('/cart/update/<int:menu_id>', methods=['POST'])
def cart_update(menu_id):
    action = request.form.get('action')
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == menu_id:
            if action == 'increase':
                item['quantity'] += 1
            elif action == 'decrease' and item['quantity'] > 1:
                item['quantity'] -= 1
            break
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:menu_id>', methods=['POST'])
def cart_remove(menu_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != menu_id]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart/confirm', methods=['POST'])
def cart_confirm():
    cart = session.get('cart', [])
    table_no = request.form.get('table_no')
    if not cart or not table_no:
        flash('กรุณาเลือกเลขโต๊ะและตรวจสอบรายการอาหาร', 'danger')
        return redirect(url_for('cart'))
    import json
    from datetime import datetime
    bill_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    total = sum(item['price'] * item['quantity'] for item in cart)
    items_json = json.dumps(cart, ensure_ascii=False)
    # บันทึกบิลและยอดขายผ่าน DatabaseManager
    db.add_bill_and_sales(int(table_no), cart, bill_time)
    session['cart'] = []
    flash('สั่งอาหารสำเร็จ!', 'success')
    return redirect(url_for('cart'))

def init_db():
    # Delegate DB creation to DatabaseManager
    db.init_db()

if __name__ =="__main__":
    init_db()
    app.run(debug=True) 