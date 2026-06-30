# STATION ✦ – Advanced Full-Stack AI Chat Platform

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F20?style=for-the-badge&logo=SQLAlchemy&logoColor=white" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/Groq_Cloud-F3702A?style=for-the-badge&logo=groq&logoColor=white" alt="Groq" />
  <img src="https://img.shields.io/badge/Bcrypt-🔑-blue?style=for-the-badge" alt="Bcrypt" />
  <img src="https://img.shields.io/badge/Render-000000?style=for-the-badge&logo=render&logoColor=white" alt="Render" />
</p>

**STATION ✦** is a modern, high-performance web application engineered to deliver a seamless, secure, and interactive intelligent chat environment. Built with a focus on asynchronous scalability and robust data integrity, the platform integrates state-of-the-art AI inference with enterprise-grade session authentication.

🌐 **Live Demo:** [https://iliizai.onrender.com](https://iliizai.onrender.com)

---

## 🛠️ Technical Architecture & Core Systems

* **Asynchronous Backend Core:** Powered by **FastAPI Architecture**, utilizing structural lifespan context management to handle active server lifetimes and resource allocation efficiently.
* **Persistent & Relational Storage:** Implements **SQLAlchemy (Object-Relational Mapping)** utilizing modern `Mapped` typing and declarative base structures. Data integrity is strictly maintained through automated table generations, cascade deletions, and explicit relationship constraints between Users and Messages.
* **Security & Encryption Framework:** Features an advanced, native **Bcrypt Hashing Pipeline** designed to handle full cryptographic salt generation and password verification under the latest Python environments.
* **Two-Factor Session Verification:** Implements a stateful, time-sensitive **OTP (One-Time Password) Registration Desk** that manages volatile user memory states using Python dictionaries, synchronized with strict UTC expiration policies (5-minute limits) and transported via the **Brevo SMTP API**.
* **Remote Intelligent Inference:** Utilizes a highly efficient, non-blocking **HTTPX AsyncClient** architecture to pipe stream-lined queries to the serverless **Groq API Cloud**, processing stateful system prompts and chat context for the custom **iliiz AI** persona (Llama 3.3).

---

## 🎨 Design Philosophy & User Experience

The front-end design of **STATION ✦** embraces a sophisticated **Cyber-Dark and Neon-Blue aesthetics framework**.

* **Cohesive UI/UX:** Built upon custom dark topologies that offer high visual comfort while ensuring critical terminal elements pop with vibrant neon blue highlights.
* **Dynamic Templating:** Driven by the **Jinja2 Templating Engine**, the interface reads server-side message payloads and dynamically decrypts message ownership based on user roles (`user` vs. `assistant`), flawlessly rendering asymmetric message layouts.
* **Omnichannel Branding:** The visual theme extends directly into the notification layout; user registration emails are delivered via custom-styled HTML templates that match the application’s signature neon-glow interface, establishing a unified product ecosystem from the very first interaction.

---

## 📂 Project Structure

```text
chatRoomAI/
│
├── apps/
│   ├── __init__.py
│   ├── email.py       # Brevo SMTP & HTML template delivery
│   ├── groq.py        # HTTPX AsyncClient connector for iliiz AI
│   ├── main.py        # FastAPI Core, application routes & session control
│   └── models.py      # SQLAlchemy Relational Models (User, Message)
│
├── templates/
│   ├── intro.html     # Application landing interface
│   ├── login.html     # Secure authentication gateway
│   ├── signup.html    # Registration desk
│   └── chat.html      # Asymmetric real-time chat workspace
│
├── .gitignore         # Local database & virtual env exclusion file
└── requirements.txt   # Server-side package dependencies
