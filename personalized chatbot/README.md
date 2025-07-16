# Personalized Chatbot

A general-purpose, company-ready chatbot web application built with Flask. It features a hybrid AI system that combines FAQ retrieval (using Sentence Transformers) with a fallback conversational model (DialoGPT). Includes an admin panel for managing FAQs and user authentication.

---

## Features

- **Modern Chat UI**: Responsive chat widget and main chat page.
- **Hybrid AI**: Answers user queries using both FAQ retrieval and a conversational AI fallback.
- **Admin Panel**: Secure login for admins to manage FAQs (add, edit, delete, enable/disable).
- **Easy Integration**: Embeddable widget for use on any website.
- **User Authentication**: Admin login/logout and session management.

---

## Project Structure

```
personalized-chatbot/
│
├── app/
│   ├── __init__.py           # Flask app factory and setup
│   ├── extensions.py         # Flask extensions (SQLAlchemy)
│   ├── models.py             # Database models (User, QAPair)
│   ├── routes/
│   │   ├── main_routes.py    # Main user and chat routes
│   │   └── admin_routes.py   # Admin panel and FAQ management routes
│   ├── templates/            # HTML templates (chat, admin, login, etc.)
│   ├── utils/
│   │   └── chatbot.py        # Hybrid chatbot logic (FAQ + DialoGPT)
│   └── static/               # Static files (CSS, JS, images)
│
├── chatbot_db.sqlite3        # (Optional) SQLite database file
├── fallback_chatbot.sqlite3  # (Optional) Fallback database
├── embededcode.txt           # Embeddable widget code
├── requirements.txt          # Python dependencies (create if missing)
└── README.md                 # Project documentation
```
