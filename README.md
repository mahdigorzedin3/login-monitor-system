# 🔐 Login Monitor System  

## 📌 About This Project  
This project is designed to monitor login attempts on your computer. If there are more than **three failed login attempts**, the system captures a photo using the webcam and sends it to your email as a security alert.  

## ⚙️ Setup Instructions  
To ensure the system works correctly, follow these steps:  

### 1️⃣ Change Power Mode  
By default, Windows may enter hibernation instead of fully shutting down. To prevent this:  
1. Open **Control Panel** → **Power Options**.  
2. Click **Choose what the power buttons do** from the left panel.  
3. Click **Change settings that are currently unavailable**.  
4. **Uncheck** *Turn on fast startup* and save changes.  
   
This ensures your system fully shuts down and restarts properly.  

### 2️⃣ Insert Your Email Credentials  
To enable email alerts, you must add your email credentials:  
1. Open `login_monitor.py`.  
2. Replace the placeholders with **your own email** and **app password**:  
   ```python
   SENDER_EMAIL = "your-email@gmail.com"
   SENDER_PASSWORD = "your-app-password"
   RECIPIENT_EMAIL = "your-email@gmail.com"
   ```  
3. **Important:** Use an app password instead of your real password. You can generate one in your email provider’s security settings.  

### 3️⃣ Auto-Connect to Trusted Wi-Fi  
Ensure your system connects to a **trusted Wi-Fi network** automatically when it turns on:  
1. Open **Command Prompt (cmd)** as **Administrator**.  
2. Run the following command (replace `"WiFi-Name"` with your network name):  
   ```sh
   netsh wlan set profileparameter name="WiFi-Name" connectionmode=auto
   ```  
3. This ensures the system is always online to send security alerts.  

### 4️⃣ Run the Automation Script as Administrator  
To schedule the monitoring system to run automatically:  
1. Open **Visual studio code** and run **automate.py**. don't worry you will get the error.  
2. Copy the line in VS code terminal that run this script
3. Open powershell as administrator and paste.

## 📧 Report Bugs  
If you find any issues or bugs, please email me at **mahdigorzedin@gmail.com**.  

---

✅ **Now your Login Monitor System is fully set up and ready to protect your device! Stay secure! 🔒🚀**
```
