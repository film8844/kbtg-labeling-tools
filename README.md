# kbtg-labeling-tools

```
.
├── README.md
└── src
    ├── __pycache__
    │   ├── app.cpython-310.pyc
    │   ├── config.cpython-310.pyc
    │   └── models.cpython-310.pyc
    ├── app.py
    ├── config.py
    ├── database.db
    ├── models.py
    ├── routes
    │   ├── __pycache__
    │   │   ├── auth.cpython-310.pyc
    │   │   └── main.cpython-310.pyc
    │   ├── api.py
    │   ├── auth.py
    │   └── main.py
    ├── run.py
    ├── setup.py
    ├── static
    ├── templates
    │   ├── auth
    │   ├── base.html
    │   ├── index.html
    │   ├── login.html
    │   ├── projects.html
    │   └── register.html
    └── utils
        ├── __pycache__
        │   └── forms.cpython-310.pyc
        └── forms.py
```

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
```python
python run
```