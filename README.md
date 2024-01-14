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

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   This command installs the required dependencies for the project.

3. **Run the Server:**
   ```bash
   uvicorn server:app
   ```

   This command starts the server using Uvicorn.

## Contributing

If you would like to contribute to this project, please follow the [contribution guidelines](CONTRIBUTING.md).

# Note
The latency of the gemini api is slow so configure the tabbyML extension to incerase the completion request timeout. Below is the command to open the config file of tabby agent. Uncomment the Completion section and change timeout from 4000ms to 15000ms. Reload the extension after changes in file.

   ```bash
   nano ~/.tabby-client/agent/config.toml
   ```
 