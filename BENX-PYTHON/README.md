# BENX XITERS — Python Flask Website

এই project টি static HTML website এর পূর্ণ Python/Flask version।

## Project Structure

```
BENX-PYTHON/
├── app.py                  ← Main Flask application
├── requirements.txt        ← Python dependencies
├── data/
│   └── site_data.json      ← Site & product data (auto-created)
├── static/
│   ├── css/style.css       ← Main stylesheet
│   ├── js/main.js          ← Main JavaScript
│   └── images/BENXLOGO.png ← Logo
└── templates/
    ├── base.html           ← Base layout (navbar, flash messages)
    ├── _footer.html        ← Footer partial
    ├── index.html          ← Home page
    ├── products.html       ← Products page
    ├── pricing.html        ← Pricing page
    ├── features.html       ← Features page
    ├── contact.html        ← Contact page
    ├── login.html          ← Login page
    ├── register.html       ← Register page
    ├── dashboard.html      ← User dashboard
    ├── admin.html          ← Admin panel
    └── 404.html            ← 404 page
```

## Installation & Run

### 1. Python install করুন (Python 3.8+)

### 2. Dependencies install করুন
```bash
pip install -r requirements.txt
```

### 3. Run করুন
```bash
python app.py
```

### 4. Browser এ open করুন
```
http://127.0.0.1:5000
```

## Admin Access

- URL: `http://127.0.0.1:5000/admin`
- Login email: `75saydulbd@gmail.com`  
- Login URL: `http://127.0.0.1:5000/login`
- Admin password (gate): `benx@admin123`

## Routes

| Route              | Description          |
|--------------------|----------------------|
| `/`                | Home page            |
| `/products`        | Products page        |
| `/pricing`         | Pricing page         |
| `/features`        | Features page        |
| `/contact`         | Contact page         |
| `/login`           | Login                |
| `/register`        | Register             |
| `/dashboard`       | User dashboard       |
| `/admin`           | Admin panel          |
| `/logout`          | Logout               |
| `/api/product/<id>`| Product JSON API     |

## Notes

- Data `data/site_data.json` file এ save হয়
- Production এ real database (PostgreSQL/MongoDB) ব্যবহার করুন
- `app.secret_key` production এ পরিবর্তন করুন
