import http.server
import socketserver
import json
import csv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPANY_FILE = os.path.join(BASE_DIR, "company_expenses_db.csv")
EMPLOYEE_FILE = os.path.join(BASE_DIR, "employees_db.csv")
REGISTERED_USERS_FILE = os.path.join(BASE_DIR, "registered_users.json")

# Global Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "matru19042003@gmail.com" 
SENDER_PASSWORD = "qbnbfaajkbmeoqmw" # MUST be a Google App Password without spaces!

def send_welcome_email(recipient_email, user_name):
    
    print(f"--> Preparing to send secure login notification to: {recipient_email}")
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = "Secure Login Alert: Milano Tech Solutions"
    
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="padding-bottom: 15px; border-bottom: 2px solid #eee; margin-bottom: 20px;">
                <strong style="font-size: 24px; color: #3b82f6; border: 2px solid #3b82f6; padding: 4px 10px; border-radius: 8px;">M</strong>
                <span style="font-size: 22px; font-weight: bold; margin-left: 10px;">Milano<span style="color: #3b82f6;">Tech</span></span>
            </div>
            <h2 style="color: #3b82f6;">Welcome, {user_name}!</h2>
            <p>We detected a successful login to your Milano Tech Solutions enterprise dashboard.</p>
            <p>If this was you, no further action is required. Enjoy your secure data session!</p>
            
            <div style="background: #f8fafc; border-left: 4px solid #3b82f6; padding: 15px; margin: 30px 0;">
                <p style="margin-top: 0; font-style: italic; color: #475569;">"At Milano Tech Solutions, we believe in empowering our teams with real-time, actionable insights. Thank you for driving our operations forward. Have a great session!"</p>
                <p style="margin-bottom: 0; margin-top: 15px; font-size: 22px; font-family: 'Brush Script MT', cursive, sans-serif; color: #0f172a;">Amrit Ketan Sahoo</p>
                <p style="margin: 0; font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">Amrit Ketan Sahoo — Chief Executive Officer</p>
            </div>
            
            <p style="font-size: 12px; color: #94a3b8;">Milano Security Team</p>
        </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()
        print(f"--> [LIVE] Welcome email successfully sent to {recipient_email}!")
    except Exception as e:
        print(f"--> Email sending failed: {e}")

def send_registration_email(recipient_email, user_name):
    
    print(f"--> Preparing to send new account welcome email to: {recipient_email}")
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = "Welcome to Milano Tech Solutions!"
    
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="padding-bottom: 15px; border-bottom: 2px solid #eee; margin-bottom: 20px;">
                <strong style="font-size: 24px; color: #10b981; border: 2px solid #10b981; padding: 4px 10px; border-radius: 8px;">M</strong>
                <span style="font-size: 22px; font-weight: bold; margin-left: 10px;">Milano<span style="color: #10b981;">Tech</span></span>
            </div>
            <h2 style="color: #10b981;">Welcome to Milano, {user_name}!</h2>
            <p>Your new enterprise account has been successfully created.</p>
            <p>You now have full access to our secure database analytics and financial modeling dashboards.</p>
            
            <div style="background: #f8fafc; border-left: 4px solid #10b981; padding: 15px; margin: 30px 0;">
                <p style="margin-top: 0; font-style: italic; color: #475569;">"Welcome to the Milano family! We are thrilled to have you on board. Our enterprise data engine is designed to give you unparalleled visibility into our corporate operations. I look forward to seeing the impact you'll make."</p>
                <p style="margin-bottom: 0; margin-top: 15px; font-size: 22px; font-family: 'Brush Script MT', cursive, sans-serif; color: #0f172a;">Amrit Ketan Sahoo</p>
                <p style="margin: 0; font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">Amrit Ketan Sahoo — Chief Executive Officer</p>
            </div>
            
            <p style="font-size: 12px; color: #94a3b8;">Milano Onboarding Team</p>
        </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()
        print(f"--> [LIVE] Registration email successfully sent to {recipient_email}!")
    except Exception as e:
        print(f"--> Registration email sending failed: {e}")

def load_users():
    if os.path.exists(REGISTERED_USERS_FILE):
        try:
            with open(REGISTERED_USERS_FILE, 'r') as f:
                return json.load(f)
        except: pass
    return {}

def save_users(users_dict):
    with open(REGISTERED_USERS_FILE, 'w') as f:
        json.dump(users_dict, f)

class MilanoAPIHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Authorization, Accept')
        self.end_headers()

    def do_POST(self):
        try:
            if self.path == '/api/login':
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data.decode('utf-8')) if content_length > 0 else {}
                
                email = payload.get('email', '').lower()
                password = payload.get('password', '')
                
                # 1. Check custom registered users first
                custom_users = load_users()
                if email in custom_users:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    if custom_users[email]['password'] == password:
                        self.wfile.write(json.dumps({"status": "success", "name": custom_users[email]['name']}).encode('utf-8'))
                        send_welcome_email(email, custom_users[email]['name'])
                    else:
                        self.wfile.write(json.dumps({"status": "error", "message": "you entered the wrong password"}).encode('utf-8'))
                    return

                # 2. Fallback to our generated Employee DB
                user_found = False
                user_name = ""
                
                with open(EMPLOYEE_FILE, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        expected_email = f"{row['first_name'].lower()}.{row['last_name'].lower()}@milano.com"
                        if email == expected_email:
                            user_found = True
                            user_name = row['full_name']
                            break
                            
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # For this demo, we accept any real user as long as the password is "admin123"
                if user_found:
                    if password == "admin123":
                        response = json.dumps({"status": "success", "name": user_name})
                        send_welcome_email(email, user_name)
                    else:
                        response = json.dumps({"status": "error", "message": "you entered the wrong password"})
                else:
                    response = json.dumps({"status": "error", "message": "you are not the register user"})
                self.wfile.write(response.encode('utf-8'))

            elif self.path == '/api/register':
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data.decode('utf-8')) if content_length > 0 else {}
                
                name = payload.get('name', '').strip()
                email = payload.get('email', '').lower().strip()
                password = payload.get('password', '')
                
                custom_users = load_users()
                custom_users[email] = {"name": name, "password": password}
                save_users(custom_users)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "name": name}).encode('utf-8'))
                send_registration_email(email, name)

            else:
                super().do_POST()

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

    def do_GET(self):
        if self.path == '/api/expenses':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            # Enable CORS for frontend consumption
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            data = []
            try:
                with open(COMPANY_FILE, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        data.append(row)
                response = json.dumps({"status": "success", "data": data})
            except Exception as e:
                response = json.dumps({"status": "error", "message": str(e)})
                
            self.wfile.write(response.encode('utf-8'))
        else:
            super().do_GET()

if __name__ == "__main__":
    PORT = 8080
    # Allows port to be reused immediately
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), MilanoAPIHandler) as httpd:
        print(f"Milano Tech Solutions API running on http://localhost:{PORT}/api/expenses ...")
        httpd.serve_forever()