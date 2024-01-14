# Book 圖書管理系統

## 介紹

這是一個用於圖書管理的系統，使用 Python 和 Django 開發。

## 環境準備

在開始之前，請確保你的環境中安裝了以下工具：

- [pyenv](https://github.com/pyenv/pyenv)
- [poetry](https://python-poetry.org/)

安裝 Python 並設定虛擬環境：

```bash
$ cd Book

$ pyenv install 3.12.1
$ pyenv local 3.12.1

$ poetry shell
$ poetry install
```

## 運行專案

以下是啟動本地開發伺服器的指令：

```bash
$ python manage.py makemigrations
$ python manage.py migrate

$ python manage.py runserver
```

以上指令將執行遷移操作並啟動開發伺服器，你現在可以在瀏覽器中訪問 http://localhost:8000/ 查看專案。