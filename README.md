# Book 圖書管理系統

## Prepare environment

- pyenv
- poetry

```bash
$ cd Book

$ pyenv install 3.12.1
$ pyenv local 3.12.1

$ poetry shell
$ poetry install

$ python manage.py makemigrations
$ python manage.py migrate

$ python manage.py runserver
```