# kbtg-labeling-tools

# installation
1.Clone this repository
```bash
git clone https://github.com/film8844/kbtg-labeling-tools.git
```
2.Create `.env` file. copy from `.docker.env`

## run on local for development
1. start database with docker
```bash
docker-compose -f docker-compos.database.yml up -d
```
2. install packages
```bash
pip install -r requirements.txt
```
3. run service
```bash
# don't forget to copy .env.template to .env and change your env

# run
cd src
export $(cat ../.env)
python run.py
```
## run on docker for production
```bash
docker compose up -d --build
```
