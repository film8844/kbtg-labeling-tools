# 🔧 **kbtg-labeling-tools** 🔧

## 📦 Installation
1. 🔄 Clone this repository
```bash
git clone https://github.com/film8844/kbtg-labeling-tools.git
```
2. 📄 Create `.env` file. copy from `.docker.env`
```bash
cp .docker.env .env
```
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DB_USER` for database username
`DB_PASSWORD` for database password

## 🛠 Run Locally (for Development)
1. 🚀 Start database with docker
```bash
docker compose --file docker-compose.database.yaml up -d 
```
2. 📦 Install packages
```bash
pip install -r requirements.txt
```
3. 🏃 Run service
```bash
# don't forget to copy .docker.env to .env and change your env

# run
cd src
export $(cat ../.env.dev)
python run.py
```

## 🐳 Deployment with Docker (for Production)
```bash
docker compose up -d --build
```

