# 🚀 Deployment Guide: Host Your Atelier on PythonAnywhere 24/7

Since this is a full-stack Django application with an active database (SQLite), dynamic shopping cart, and client consultation registration, it requires a persistent Python web environment to run 24/7 (even when your PC is turned off).

**PythonAnywhere** is a completely free cloud hosting provider custom-tailored for Python/Django applications. It requires **no credit card** and guarantees **zero data loss**.

Follow this step-by-step checklist to take your luxury storefront live in under 5 minutes!

---

## 📋 The Step-by-Step Curation

### 1. Create a Free Account
1. Visit [PythonAnywhere](https://www.pythonanywhere.com/).
2. Click **Pricing & signup** in the top right.
3. Choose the **Create a Beginner account** (100% Free, no credit card required).
4. Choose your username carefully. Your site will be live at:
   `https://<your-username>.pythonanywhere.com`

---

### 2. Pull Your GitHub Repository
1. Log into PythonAnywhere and navigate to the **Dashboard**.
2. Click the **$ Bash** button under **New console** to launch a cloud command terminal.
3. In the terminal, clone your synchronized GitHub repository:
   ```bash
   git clone https://github.com/Ammar-32-dev/warmloop-couture.git
   ```
4. Change directory into the project folder:
   ```bash
   cd warmloop-couture
   ```

---

### 3. Set Up Your Python Virtual Environment & Dependencies
In the same Bash terminal on PythonAnywhere, create a fresh virtual environment and install the requirements:
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install packages
pip install django whitenoise pillow
```

---

### 4. Seed the Database (Zero Data Loss!)
We want to keep all of our custom luxury products, categories, and image assets intact. In the active virtual environment in the Bash terminal, run the standard Django migrations and execute our custom seeder script:
```bash
# 1. Generate empty database schema
python manage.py migrate

# 2. Seed the premium products, categories, and visual assets
python seed_db.py
```
*(You will see the database successfully seed in Indian Rupees (INR) with all of our handcrafted descriptions and details intact!)*

---

### 5. Configure the PythonAnywhere Web App
1. Go back to your PythonAnywhere dashboard and click the **Web** tab in the top right.
2. Click **Add a new web app**.
3. Under Select Domain, choose **Manual Configuration** (do NOT choose Django; Manual Configuration gives us exact virtual environment routing).
4. Select **Python 3.10** (or whichever matching version is running).
5. Once created, configure these paths in the Web tab form:
   * **Source code directory**: `/home/<your-username>/warmloop-couture`
   * **Working directory**: `/home/<your-username>/warmloop-couture`
   * **Virtualenv directory**: `/home/<your-username>/warmloop-couture/venv`

---

### 6. Set Up the WSGI Configuration
On the **Web** tab, look for **Code** -> **WSGI configuration file** and click the link to edit it. Replace the entire contents of that file with this standard luxury WSGI script:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/<your-username>/warmloop-couture'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*(Replace `<your-username>` with your actual PythonAnywhere username!)*

---

### 7. Configure Static and Media Routing
To make sure all of our beautiful Tailwind styling, visual layouts, and images render flawlessly, configure these paths at the bottom of the **Web** tab under the **Static files** section:

1. **Static Files Entry:**
   * **URL**: `/static/`
   * **Directory**: `/home/<your-username>/warmloop-couture/static`

2. **Media Files Entry (Your Product Photos!):**
   * **URL**: `/media/`
   * **Directory**: `/home/<your-username>/warmloop-couture/media`

---

### 8. Reload & Go Live! 💎
1. Scroll to the top of the **Web** tab.
2. Click the big green **Reload <your-username>.pythonanywhere.com** button.
3. Open a new browser tab and go to:
   `https://<your-username>.pythonanywhere.com`

**Your Warm Soft high-end boutique is now live 24/7 for the entire world to experience!**
