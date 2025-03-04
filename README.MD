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

### **2. Install the Package**

Run the following command to install the package into your Python environment:

```bash
pip install .
```

After installation, run the following commands to set up the database:

```bash
expense_tracker makemigrations
expense_tracker migrate
expense_tracker createsuperuser
```

---

## 🔄 **Manual Setup (Alternative Method)**

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

## 📥 **Import/Export Expenses**

- **Import:** Upload Excel files with the format: `vendor_name`, `due_day_of_month`, `amount`, `date_paid`, `frequency`.
- **Export:** Download current expense data as an Excel file.

---
## 📥 **Importing and Exporting Expenses
The Expense Tracker Application allows users to easily import and export their expense data using Excel files. This functionality is designed to be user-friendly and secure, with all file operations handled directly from the user's local computer, ensuring no files are stored on the server.

### Exporting Expenses

#### How to Export:
- **Log in to the application** and navigate to `/expenses/export/` (Export Expenses tab).  
- **Click the "Export" button** to initiate the download of your expense data.  

## 📂 File Format  
The exported **Excel file** contains your expense data with the following columns:  

- **Vendor Name**: The name of the vendor.  
- **Due Date**: Formatted based on the expense frequency:  
  - **Monthly**: Day of the month (e.g., `15`).  
  - **Quarterly/Yearly**: Month and day (e.g., `March 15`).  
- **Amount**: The expense amount (e.g., `100.00`).  
- **Date Paid**: The date the expense was paid, if applicable (e.g., `2025-01-01`).  
- **Frequency**: The frequency of the expense (`Monthly`, `Quarterly`, `Yearly`).  

## ⚙️ Technical Details  
- The **Excel file is generated in memory** using Python's `BytesIO` and `pandas` libraries.  
- It is sent to your browser as an **HTTP response** with the `Content-Disposition: attachment` header, prompting an **automatic download** to your local machine (typically to your **Downloads folder**).  
- **No files are saved on the server**, ensuring **efficiency and privacy**.  
### Importing Expenses

#### How to Import:
- **Log in to the application** and navigate to `/expenses/import/` (Import Expenses tab).  
- **Use the form to upload an Excel file** from your local computer.  
- After uploading, the app **processes the file and adds valid expenses** to your list, then redirects you to the **expense list page**.  

## 📂 File Format Requirements  
Your **Excel file** must include the following required columns:  

- **Vendor Name**: The name of the vendor (**string**).  
- **Due Date**:  
  - **For Monthly expenses**: A number representing the **day of the month** (e.g., `"15"`).  
  - **For Quarterly or Yearly expenses**: `"Month Day"` format (e.g., `"March 15"`).  
- **Amount**: The expense amount (**decimal**, e.g., `"100.00"`).  
- **Frequency**: The frequency of the expense (`"Monthly"`, `"Quarterly"`, or `"Yearly"`).  

### 📝 Optional Column  
- **Date Paid**: The date the expense was paid (**e.g., `"2025-01-01"`**).  
##### Example of a valid Excel file:
```
Vendor Name | Due Date    | Amount | Date Paid  | Frequency
Vendor A    | 15          | 100.00 | 2025-01-01 | Monthly
Vendor B    | March 20    | 200.00 | 2025-03-20 | Quarterly
Vendor C    | December 25 | 300.00 | 2025-12-25 | Yearly
```
#### Processing and Validation:
- The app **reads the uploaded file in memory** using `pandas`.  
- Each row is **validated**:  
  - **Missing or invalid data** (e.g., incorrect Due Date format based on frequency) is **skipped**, with debug logs recorded.  
  - **Valid expenses are added** to the database.  
  - **Duplicates** (based on vendor name for the user) are **skipped** to prevent overwriting.  

## ⚠️ Error Handling  
- If the file is **missing required columns** or contains **invalid data**, an **error message** is displayed on the import page (e.g., `"Missing required columns: vendor_name"`).  
- Ensure your file **matches the required format** to avoid import errors.  

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