# 🔧 **kbtg-labeling-tools** 🔧

## 📦 Installation
1. 🔄 Clone this repository
```bash
git clone https://github.com/film8844/kbtg-labeling-tools.git
```
2. 📄 Create `.env` file. copy from `.docker.env`

## 🛠 Run on Local (for Development)
1. 🚀 Start database with docker
```bash
docker-compose -f docker-compos.database.yml up -d
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
export $(cat ../.env)
python run.py
```
## 🐳 Run on Docker (for Production)
```bash
docker compose up -d --build
```
