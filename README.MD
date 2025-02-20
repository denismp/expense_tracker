# 📊 Expense Tracker Application

A secure Django-based expense tracker application that allows users to manage monthly expenses, import/export data via Excel, and filter expenses by frequency, due dates, and more.

---

## 🚀 **Features**

- Add, update, and delete expenses
- Import/export expenses via Excel spreadsheets
- Secure user authentication with admin controls
- Filter and sort expenses by vendor, date, amount, and frequency
- Manage expense frequencies: **Monthly**, **Quarterly**, **Yearly**
- Admin panel for managing users and expenses

---

## ⚙️ **Setup Instructions**

### **1. Clone the Repository**

```bash
git clone https://github.com/your-repo/expense-tracker.git
cd expense-tracker
```

### **2. Run the Setup Script (Mac/Linux)**

```bash
bash setup_and_run_mac.sh
```

### **3. Run the Setup Script (Windows)**

```bat
setup_and_run_windows.bat
```

The setup scripts will:
- Create a virtual environment
- Install dependencies
- Apply migrations
- Start the Django development server

If you prefer manual setup, follow the instructions below.

---

## 🔄 **Manual Setup**

### **1. Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install the required packages manually:

```bash
pip install django pandas openpyxl
```

### **3. Apply Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

### **4. Create a Superuser** (for Admin Panel)

```bash
python manage.py createsuperuser
```

Enter your preferred username, email, and password when prompted.

### **5. Run the Development Server**

```bash
python manage.py runserver
```

Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the application.

### **6. Access the Django Admin Panel**

Visit: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  
Login using the superuser credentials.

---

## 👅 **Setup and Run Scripts**

### **For Mac/Linux Users**
Run the `setup_and_run_mac.sh` script:
```bash
bash setup_and_run_mac.sh
```

### **For Windows Users**
Run the `setup_and_run_windows.bat` script:
```bat
setup_and_run_windows.bat
```

These scripts will:
- Set up the virtual environment
- Install all dependencies
- Apply migrations
- Start the Django development server automatically

---

## 👅 **Import/Export Expenses**

- **Import:** Upload Excel files with the format: `vendor_name`, `due_day_of_month`, `amount`, `date_paid`, `frequency`.
- **Export:** Download current expense data as an Excel file.

---

## ✅ **Admin Features**

- Add/Delete users
- Force password changes
- Manage expenses from the Admin Panel

## 🚀 **Future Improvements**

- Add charts and visual analytics
- Multi-currency support
- Budget management features

---

## 🛠️ **Troubleshooting**

- **Database Issues?**  
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

- **Clear Cache Issues:**
  - Windows/Linux: `Ctrl + Shift + R`
  - Mac: `Cmd + Shift + R`

- **Reset Database (Optional):**
  ```bash
  rm db.sqlite3
  python manage.py migrate
  ```

## 👩‍💻 **Contributing**

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request

---

## 📝 **License**

This project is licensed under the MIT License.

---

**Happy Expense Tracking! 🚀💸**

