import http.server
import socketserver
import json
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPANY_FILE = os.path.join(BASE_DIR, "company_expenses_db.csv")
EMPLOYEE_FILE = os.path.join(BASE_DIR, "employees_db.csv")
REGISTERED_USERS_FILE = os.path.join(BASE_DIR, "registered_users.json")

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