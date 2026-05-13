# CultureBridge

CultureBridge is a Python Tkinter desktop application I developed to help users share, browse, and learn about different cultures. I designed and implemented the entire feature set into a single, cohesive codebase, ensuring a seamless experience for browsing content and participating in cultural quizzes.

## Features

- **User Authentication:** Secure registration, login, and editable profiles with salted password hashing (`hashlib.pbkdf2_hmac`).
- **Robust Backend:** PostgreSQL database managing users, posts, comments, quiz questions, and scores.
- **Culture Feed:** Interactive feed with post creation, image uploads, category filtering, and full CRUD capabilities.
- **Dynamic Search:** Efficient discovery using PostgreSQL `ILIKE` for content filtering.
- **Cultural Exploration:** A browse page organized by country, leading to detailed country-specific post views.
- **Integrated Learning:** A dedicated learning module that connects countries, user posts, and interactive quizzes.
- **Quiz System:** Randomized five-question quizzes with detailed explanations and persistent score tracking.
- **Engagement:** Real-time comment system with auto-refresh and moderation features.

## Project Structure

```text
culturebridge/
├── main.py                 # Application entry point
├── app.py                  # Main application logic and navigation
├── config.py               # Configuration and environment loading
├── requirements.txt        # Project dependencies
├── database/               # Database logic and schema
│   ├── db_connect.py       # Connection management
│   ├── db_helper.py        # SQL execution wrappers
│   ├── db_setup.py         # Table creation and seeding script
│   └── schema.sql          # Database schema definitions
├── pages/                  # Individual UI pages
│   ├── base_page.py        # Base class for all pages
│   ├── login_page.py
│   ├── register_page.py
│   ├── profile_page.py
│   ├── feed_page.py
│   ├── new_post_page.py
│   ├── post_detail_page.py
│   ├── search_page.py
│   ├── browse_page.py
│   ├── culture_detail_page.py
│   ├── learn_page.py
│   ├── quiz_page.py
│   └── quiz_result_page.py
├── widgets/                # Reusable UI components
│   ├── navbar.py
│   ├── post_card.py
│   ├── culture_card.py
│   └── scrollable_frame.py
├── assets/                 # Icons and image assets
└── .env.example            # Template for environment variables
```

## How to Run Locally

Follow these steps to set up and run the application on your system.

### 1. Prerequisites

Ensure you have the following installed:

- **Python 3.10 or higher**
- **PostgreSQL 14 or higher** (Ensure the service is running)
- **Tkinter** (Usually included with Python; Linux users may need `sudo apt-get install python3-tk`)

### 2. Set Up the Database

Open your PostgreSQL terminal (psql) or a tool like pgAdmin and run:

```sql
CREATE DATABASE culturebridge_dev;
```

### 3. Clone and Environment Setup

Navigate to the project directory and create your environment file:

```bash
#For Mac Run
cp .env.example .env
#For Wwindows Run
copy .env.example .env
```

Edit the `.env` file and enter your PostgreSQL credentials:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=culturebridge_dev
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
```

### 4. Install Dependencies

It is recommended to use a virtual environment:

```bash
# Create virtual environment
#For Mac Run
python3 -m venv .venv
#For Windows Run
python -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install required libraries
pip install -r requirements.txt
```

### 5. Initialize the Database

Run the setup script to create the necessary tables and seed the database with initial quiz data (50 questions across 5 countries):

```bash
#For Mac Run
python3 -m database.db_setup
#For Windows Run
python -m database.db_setup
```

### 6. Launch the Application

Start the application by running:

```bash
#For Mac run
python3 main.py
#For Windows Run
python main.py
```
