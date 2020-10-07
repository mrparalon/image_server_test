## Требования

- python3.7
- rabbit mq на стандартном порту
- mongodb:27017

```bash
pip install -r requirements.txt
```


## Запуск

```bash
export FLASK_APP=server.py
flask run
```

`python db_worker.py`


## Тестирование

В файле test.py есть пара функций для тестирования API, на aiohttp
