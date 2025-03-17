# Event Management System

## 📌 Project Overview
This is a **Flask-based Event Management System** that allows users to create, manage, and participate in events. The system supports three roles:
- **Admin**: Can create, delete, and manage users and events.
- **Organizer**: Can create, update, and delete events.
- **Attendee**: Can view and join events.

It also includes features like user authentication, email notifications, event search/filter and role-based access

---
## 🚀 Setup and Installation
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/nishhhhhh06/event_management.git
cd event_management
```

### **2️⃣ Create a Virtual Environment**   (optional)
```bash
python -m venv event_management
source event_management/bin/activate  # macOS/Linux
# OR
event_management\Scripts\activate  # Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```


### **5️⃣ Initialize the Database**
add user database credentials in the config file
```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### **6️⃣ Run the Application**
```bash
flask run
```
Your application will be running at: **`http://127.0.0.1:5000/`**


---
## 📧 Email Notifications
Users receive email notifications when they **create** or **join** an event.
Ensure that you have enabled **Less Secure Apps** or used an **App Password** in Gmail settings.
also uncomment the code for email sending.



