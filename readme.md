# Бэк

## запуск

### это база

```sh
$ docker-compose up
```

На линуксе (arch) у меня постгресс поднимается только если перед этим снять сервис постгресса:

```bash
$ sudo systemctl stop postgresql
```

#### подключение к бд

```bash
psql postgresql://testuser:testpass@localhost:5432/testdb
```

### пакеты

```bash
pip install -r requirements.txt
```

### сервак

знаю, что принято запускать через консольный вызов сервака, но я не понял, как через него запускать целый модуль.
потому:

```bash
python main.py
```

### роли

сервер и фронт построены так, что у ролей должны быть определённые коды

1 - admin
2 - client
3 - librarian


