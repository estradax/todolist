# Todolist

## Requirements

- Docker
- Python
- NodeJS

## How to run

Start Keycloak server on port 8080 and Postgres on port 5432.

```bash
docker compose up -d
```

Visit `http://localhost:8080/admin`, log in with the credentials `admin:admin`, create a new client, and then set the `CLIENT_ID` and `CLIENT_SECRET_KEY` in the `.env` file.

Install flask dependecies and run flask server on port 5000.

```bash
pip3 install -r requirements.txt
python3 manage.py
python3 app.py
```

Open another terminal and change directory to `todolist-app` to run the React app.

```bash
npm install
npm run dev
```

Then visit `http://localhost:5173`, log in with the credentials `admin:admin`.
