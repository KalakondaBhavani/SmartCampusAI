# SmartCampusAI 🎓

SmartCampusAI is a production-ready, modern **Smart Campus Management System** built with **Python** and **Streamlit**. It features secure authentication, local JSON file-based database storage, custom glassmorphism dark-mode UI design, interactive charts, and an AI conversational campus helper integrated with OpenAI and Google Gemini APIs.

---

## Key Features

1.  **Antigravity Design Theme**: Visual layout featuring rounded cards, linear-gradient hover buttons, slate dark background, glassmorphism containers, and Google Outfit typography.
2.  **Role-Based Security Routing**: Dynamic navigation engine prevents users from accessing protected views before logging in. Restricts student and faculty capabilities (e.g. read-only profiles or directories).
3.  **Local JSON Database**: Standardized helper scripts handle CRUD operations for students, faculty, classes, settings, and logs using local JSON tables with zero external dependencies (No SQLite, MySQL, or MongoDB required).
4.  **Bcrypt Cryptography Hashing**: Secure password encryption and verification matching industry standards.
5.  **Analytics & Charts**: Detailed Plotly graphs tracking student ratios and weekly attendance rates.
6.  **AI Campus Assistant**: Conversational agent connecting to Gemini or OpenAI models. Automatically defaults to a local search engine if API keys are missing to remain operational.
7.  **Data Export Hub**: Export system rosters and class checklists to CSV or JSON formats.

---

## Project Directory Structure

```
SmartCampusAI/
│
├── app.py                      # Main entrypoint, controls secure page routing
├── requirements.txt            # Package dependency definitions
├── .env                        # Environment configurations
├── .env.example                # Templates for keys and settings
├── README.md                   # Documentation guide
│
├── database/                   # JSON database storage
│   ├── users.json
│   ├── activity.json
│   ├── settings.json
│   ├── students.json
│   ├── faculty.json
│   └── attendance.json
│
├── auth/                       # Credentials and session security
│   ├── login.py
│   ├── register.py
│   ├── auth_utils.py
│   └── session.py
│
├── dashboard/                  # Dashboard and analytics renderers
│   ├── dashboard.py
│   ├── sidebar.py
│   ├── cards.py
│   └── analytics.py
│
├── pages/                      # Rerouted campus pages
│   ├── Home.py
│   ├── Students.py
│   ├── Faculty.py
│   ├── Attendance.py
│   ├── AI_Assistant.py
│   ├── Reports.py
│   ├── Settings.py
│   └── Profile.py
│
├── utils/                      # Helper libraries
│   ├── json_db.py
│   ├── helpers.py
│   ├── validators.py
│   └── security.py
│
├── assets/                     # Stylesheet and visual indicators
│   ├── logo.png
│   └── styles.css
│
└── components/                 # Reusable layout building blocks
    ├── navbar.py
    ├── footer.py
    ├── buttons.py
    └── metrics.py
```

---

## Installation & Setup

Follow these commands to deploy SmartCampusAI locally:

### 1. Clone the Directory
Ensure your shell path is correct:
```bash
cd SmartCampusAI
```

### 2. Configure Virtual Environment
Create a clean environment for packages:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Pinned Dependencies
Installs Streamlit, bcrypt, plotly, and others:
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Config
Copy the example template to activate key variables:
```bash
copy .env.example .env
```
Open `.env` and enter your API keys if you plan to use live LLMs:
```env
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
SECRET_KEY=custom_key_here
```

---

## Run Command

Execute the Streamlit application using:
```bash
streamlit run app.py
```

---

## Default Login Credentials (Hashed Bootstrap)

Upon initial launch, the system automatically populates databases with the following credentials for evaluation:

| Username  | Password            | Role     | Description                  |
| :-------- | :------------------ | :------- | :--------------------------- |
| `admin`   | `AdminPassword123!` | `Admin`  | Full read/write admin checks |
| `faculty` | `FacultyPassword123!`| `Faculty`| Can mark attendance lists    |
| `student` | `StudentPassword123!`| `Student`| Read-only directory view     |

---

## Deployment to Streamlit Cloud

1. Commit and push the project files to a public GitHub repository.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io/).
3. Connect your GitHub account, choose the repository, and select `app.py` as the entrypoint.
4. Input your environment secrets (e.g. `GEMINI_API_KEY`) in the Streamlit Cloud dashboard console settings.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
