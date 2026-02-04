# Flask2_25052025

## Развертывание на локальной машине

1. Создаем виртуальное окружение: 
```
python3 -m venv flask_venv
```
2. Активируем `venv`: 
```
source flask_venv/bin/activate
```
3. Устанавливаем зависимости: 
```
pip install -r requirements.txt
```
4. Создаем локальную БД с таблицами: 
```
flask db upgrade
```
5. Создаем файл `.flaskenv`:
```
FLASK_APP=run.py
FLASK_DEBUG=1
```
6. Запускаем приложение: 
```
flask run
```

## Ссылка на документацию
1. Настройки для запуска `flask run` [тут](https://flask.palletsprojects.com/en/stable/cli/)
2. Настройки для конфигов [тут](https://flask.palletsprojects.com/en/stable/config/)

## Работа с sqlite3

1. Установка **CLI** для **sqlite**: 
```
sudo apt install sqlite3
```
2. Создать дамп БД (схема + данные): 
```
sqlite3 quotes.db .dump > db_sql/db_data.sql
```
3. Создать дамп БД (только схема): 
```
sqlite3 quotes.db ".schema quotes" > db_sql/db_schema.sql
```
4. Загрузить данные в БД: 
```
sqlite3 new_store.db ".read db_sql/db_data.sql"
```

## Дополнительно
1. Как объединить две `головы(heads)` в миграциях
```
flask db merge heads -m "Merge two heads"
```

2. Поддержка шаблонов `Jinja2` -> дополнение `Better Jinja`  
Добавить в `settings.json`: 
```
"files.associations": {
  "*.html": "jinja-html"
},
"emmet.includeLanguages": {
    "jinja-html": "html"
}
```

## Работа с OpenAPI v3.x.x
1. Основной URL `/docs`
2. Посмотреть спецификацию в терминале:
```
flask spec
```
3. Сгенерировать в формате `json`
```
flask spec --output openapi.json
```
4. Сгенерировать в формате `yaml`
```
flask spec --format yaml --output openapi.yaml
```