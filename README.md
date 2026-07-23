 
# 💬 EchoLink — Chat Portal with FTP File Transfer

A real-time **web-based chat portal** with integrated FTP file sharing, built with Flask and Socket.IO. EchoLink lets users communicate instantly via WebSockets and securely upload/download files — all in one dark-themed, browser-accessible platform.

---

## ✨ Features

- 🔐 **User Authentication** — Secure login and registration with session management
- ⚡ **Real-Time Messaging** — WebSocket-powered chat; messages update instantly without page reload
- 📁 **FTP File Transfer** — Upload files to the server and download shared files via FTP
- 📋 **Activity Logs** — Every message and file transfer is logged for accountability
- 🌑 **Dark-Themed UI** — Clean, modern interface built with HTML, CSS, and JavaScript
- 🔒 **Access Control** — File upload/download routes protected; only authenticated users can access files

---

## 🏗️ System Architecture

```
Client (Browser)
      ↓
Flask Web Server
  ├── WebSocket (Socket.IO) → Real-time Chat
  ├── FTP Endpoints (pyftpdlib) → File Upload / Download
  └── Auth Routes → Login / Register / Session
      ↓
File System (/uploads) + Activity Logs (logs/)
```
<img width="1536" height="1024" alt="echolink" src="https://github.com/user-attachments/assets/a42afdc1-2633-480f-a593-cc61c8fa98bd" />



---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3, Flask |
| **Real-Time Chat** | Flask-SocketIO, WebSockets |
| **FTP Server** | pyftpdlib |
| **Frontend** | HTML, CSS, JavaScript |
| **Logging** | File-based activity logs |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/FatimaShakil/echolink.git
cd echolink
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the FTP server
```bash
python ftp_server.py
```

### 4. Start the Flask app
```bash
python app.py
```

### 5. Open in browser
```
http://localhost:5000
```

Register an account, log in, and start chatting or transferring files.

---

## 📁 Project Structure

```
echolink/
├── app.py                  # Main Flask app (routes, WebSocket, auth)
├── ftp_server.py           # FTP server setup (pyftpdlib)
├── style.css               # UI styling (dark theme)
├── templates/              # HTML templates (login, register, chat portal)
├── uploads/                # Uploaded files directory
├── ftp_files/              # FTP-accessible file storage
├── instance/               # Flask instance config
├── logs/                   # Activity logs (messages + file transfers)
├── requirements.txt
└── README.md
```

---

## 🖥️ Screenshots

| Page | Description |
|------|-------------|
| Login | Secure user login |
| Register | New user registration |
| Chat Portal | Real-time messaging interface |
| File Transfer | Upload, download, and share files |

---

## 📄 License

This project is for academic purposes.
