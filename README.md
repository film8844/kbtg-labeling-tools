# kbtg-labeling-tools

# installation
1.install packgage
```bash
pip install -r requirements.txt
```
2.setup database
```
cd src
python setup.py
```

# run on local
3. run docker database
```bash
docker compose up -d --build
```
2.
```bash
cd src
export $(cat ../.env)
python run.py
```
