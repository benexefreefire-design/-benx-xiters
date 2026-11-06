"""
BENX XITERS — Flask Web Application
=====================================
Python/Flask version of the BENX XITERS website.
Run: python app.py
"""

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, jsonify, flash
)
from functools import wraps
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'benx_secret_key_2024_local_only')

# ── Config ──────────────────────────────────────────────────
ADMIN_EMAIL    = '75saydulbd@gmail.com'
ADMIN_PASSWORD = 'benx@admin123'
DATA_FILE      = os.path.join(os.path.dirname(__file__), 'data', 'site_data.json')

# ── Default site data ────────────────────────────────────────
DEFAULT_DATA = {
    "site": {
        "name": "BENX XITERS",
        "title": "Next-Gen Gaming Tools",
        "logo": "BENXLOGO.png",
        "telegram": "https://t.me/benxuiters",
        "email": "support@benxuiters.com",
        "discord": "",
        "youtube": ""
    },
    "products": [
        {
            "id": "p1",
            "name": "LITE",
            "title": "",
            "game": "Free Fire",
            "daily": 49,
            "monthly": 899,
            "image": "",
            "badge": "",
            "features": "Basic Aimbot\nSimple ESP\nSpeed Hack\nCommunity Support",
            "desc": "Entry-level tool for casual players.",
            "active": True,
            "popular": False
        },
        {
            "id": "p2",
            "name": "PRO",
            "title": "",
            "game": "Free Fire",
            "daily": 99,
            "monthly": 1799,
            "image": "",
            "badge": "Most Popular",
            "features": "AI Neural Aimbot\nFull ESP + Radar\nSpeed + Jump Hack\nAnti-Ban System\nNo Recoil\nAuto Update",
            "desc": "The most popular plan for serious players.",
            "active": True,
            "popular": True
        },
        {
            "id": "p3",
            "name": "ULTRA",
            "title": "",
            "game": "Free Fire",
            "daily": 199,
            "monthly": 3499,
            "image": "",
            "badge": "",
            "features": "All PRO Features\nAI Auto-Mode\nSkins ESP\nDevice ID Spoofer\nPriority Updates\nVIP Support 24/7\nPrivate Telegram",
            "desc": "Maximum power for elite players.",
            "active": True,
            "popular": False
        }
    ]
}


# ── Data helpers ─────────────────────────────────────────────
def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA


def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── Auth decorators ──────────────────────────────────────────
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ═══════════════════════════════════════════════════════════
#   PUBLIC ROUTES
# ═══════════════════════════════════════════════════════════

@app.route('/')
def index():
    data = load_data()
    active_products = [p for p in data['products'] if p.get('active')]
    return render_template('index.html',
                           site=data['site'],
                           products=active_products[:3],
                           page='home')


@app.route('/products')
def products():
    data = load_data()
    active_products = [p for p in data['products'] if p.get('active')]
    return render_template('products.html',
                           site=data['site'],
                           products=active_products,
                           page='products')


@app.route('/pricing')
def pricing():
    data = load_data()
    return render_template('pricing.html',
                           site=data['site'],
                           page='pricing')


@app.route('/features')
def features():
    data = load_data()
    return render_template('features.html',
                           site=data['site'],
                           page='features')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    data = load_data()
    success = False
    if request.method == 'POST':
        # In a real app: send email / save to DB
        name    = request.form.get('name', '').strip()
        email   = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        if name and email and subject and message:
            success = True
        else:
            flash('Please fill in all required fields.', 'error')
    return render_template('contact.html',
                           site=data['site'],
                           success=success,
                           page='contact')


# ── Auth ─────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = load_data()
    if session.get('logged_in'):
        if session.get('is_admin'):
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('dashboard'))

    error = None
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if email and password:
            session['logged_in'] = True
            session['user_email'] = email

            if email == ADMIN_EMAIL.lower():
                # Admin login
                session['is_admin'] = True
                return redirect(url_for('admin_dashboard'))
            else:
                # Normal user login
                session['is_admin'] = False
                return redirect(url_for('dashboard'))
        else:
            error = 'Please enter your email and password.'

    return render_template('login.html',
                           site=data['site'],
                           error=error,
                           page='login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    data = load_data()
    error = None
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name  = request.form.get('last_name', '').strip()
        email      = request.form.get('email', '').strip()
        password   = request.form.get('password', '')
        password2  = request.form.get('password2', '')

        if not (first_name and last_name and email and password):
            error = 'Please fill in all required fields.'
        elif password != password2:
            error = 'Passwords do not match.'
        elif len(password) < 8:
            error = 'Password must be at least 8 characters.'
        else:
            # In a real app: save user to DB
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html',
                           site=data['site'],
                           error=error,
                           page='register')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ── User Dashboard ───────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    data = load_data()
    # Demo user data — in production this comes from a DB
    user = {
        'name': 'Rafi Hasan',
        'email': session.get('user_email', ''),
        'plan': 'PRO',
        'avatar': 'R',
    }
    keys = [
        {'name': 'BENX PRO Panel — Free Fire', 'code': 'BENX-PRO-FF-X9A3-KD82', 'status': 'active',   'expires': '15 days'},
        {'name': 'BENX LITE — Free Fire',       'code': 'BENX-LT-FF-P7M1-QW44',  'status': 'active',   'expires': '3 days'},
        {'name': 'BENX Phone Tools',             'code': 'BENX-PB-V2-M5N9-XT01',  'status': 'expired',  'expires': 'Expired 2 days ago'},
    ]
    orders = [
        {'name': 'BENX PRO Panel', 'date': 'Nov 5, 2024 · 15 days', 'price': '৳1,485'},
        {'name': 'BENX LITE',       'date': 'Nov 3, 2024 · 3 days',  'price': '৳147'},
        {'name': 'BENX Phone Tools','date': 'Oct 28, 2024 · 7 days', 'price': '৳903'},
    ]
    return render_template('dashboard.html',
                           site=data['site'],
                           user=user,
                           keys=keys,
                           orders=orders,
                           page='dashboard')


# ═══════════════════════════════════════════════════════════
#   ADMIN ROUTES
# ═══════════════════════════════════════════════════════════

@app.route('/admin')
@admin_required
def admin_dashboard():
    data = load_data()
    return render_template('admin.html',
                           site=data['site'],
                           products=data['products'],
                           page='admin')


@app.route('/admin/site', methods=['POST'])
@admin_required
def admin_save_site():
    data = load_data()
    for key in ['name', 'title', 'telegram', 'email', 'discord', 'youtube']:
        val = request.form.get(key, '').strip()
        if val is not None:
            data['site'][key] = val
    save_data(data)
    flash('Site settings saved!', 'success')
    return redirect(url_for('admin_dashboard') + '#site')


@app.route('/admin/products/add', methods=['POST'])
@admin_required
def admin_add_product():
    data = load_data()
    import time
    new_product = {
        'id':       'p' + str(int(time.time())),
        'name':     request.form.get('name', '').strip(),
        'title':    request.form.get('title', '').strip(),
        'game':     request.form.get('game', '').strip(),
        'badge':    request.form.get('badge', '').strip(),
        'daily':    int(request.form.get('daily', 0) or 0),
        'monthly':  int(request.form.get('monthly', 0) or 0),
        'image':    request.form.get('image', '').strip(),
        'features': request.form.get('features', '').strip(),
        'desc':     request.form.get('desc', '').strip(),
        'active':   request.form.get('active') == 'on',
        'popular':  request.form.get('popular') == 'on',
    }
    data['products'].append(new_product)
    save_data(data)
    flash('Product added!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/products/edit/<product_id>', methods=['POST'])
@admin_required
def admin_edit_product(product_id):
    data = load_data()
    for i, p in enumerate(data['products']):
        if p['id'] == product_id:
            data['products'][i] = {
                'id':       product_id,
                'name':     request.form.get('name', '').strip(),
                'title':    request.form.get('title', '').strip(),
                'game':     request.form.get('game', '').strip(),
                'badge':    request.form.get('badge', '').strip(),
                'daily':    int(request.form.get('daily', 0) or 0),
                'monthly':  int(request.form.get('monthly', 0) or 0),
                'image':    request.form.get('image', '').strip(),
                'features': request.form.get('features', '').strip(),
                'desc':     request.form.get('desc', '').strip(),
                'active':   request.form.get('active') == 'on',
                'popular':  request.form.get('popular') == 'on',
            }
            break
    save_data(data)
    flash('Product updated!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/products/delete/<product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    data = load_data()
    data['products'] = [p for p in data['products'] if p['id'] != product_id]
    save_data(data)
    flash('Product deleted!', 'success')
    return redirect(url_for('admin_dashboard'))


# ── API — product data JSON (for modal) ──────────────────────

@app.route('/api/product/<product_id>')
def api_product(product_id):
    data = load_data()
    product = next((p for p in data['products'] if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(product)


# ── 404 ──────────────────────────────────────────────────────

@app.errorhandler(404)
def page_not_found(e):
    data = load_data()
    return render_template('404.html', site=data['site']), 404


# ── Run ───────────────────────────────────────────────────────

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    load_data()  # initialise data file
    print("✅ BENX XITERS Flask app starting...")
    print("🌐 Open: http://127.0.0.1:5000")
    print("🔑 Admin login: 75saydulbd@gmail.com")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
