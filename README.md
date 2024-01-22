# Gemini Backend

This repository builds a server for the tabbyML clients (VSCode, Vim, IntelliJ). The code is written in Python and uses FastAPI for HTTP request handling. It utilizes the Gemini API to fetch code snippets.

## Getting Started

The code requires the credentials of your google cloud service account, below is the official doc to generate a key.
[Create google account credentials](https://cloud.google.com/iam/docs/keys-create-delete#iam-service-account-keys-create-console)

To run this project, follow these steps:

1. **Create a Python Virtual Environment:**
   ```bash
   python -m venv .venv
   ```

   This command creates a Python virtual environment in the `.venv` folder.

2. **Activate virtual environment**
   ```bash
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   This command installs the required dependencies for the project.

4. **Run the Server:**
   ```bash
   uvicorn app.app:app
   ```

   This command starts the server using Uvicorn.

####Setting up .env
- Create a file named ".env" in the root directory.

- Add the following lines to the file.
   ```
   GOOGLE_APPLICATION_CREDENTIALS =
   JWT_SECRET_KEY=
   MONGO_CONNECTION_STRING=
   ```