# SnortRuleGenerator

На текущий момент реализован только тестовый запуск с чтением из pcap файла `test.pcap`

### Запуск
Добавьте в корневую директорию проекта файл 'test.pcap'

Выполните
```bash
docker-compose pull
docker-compose up -d
docker logs -f analyzer
```

### Остановка

В корневой директории проекта выполнить

```bash
docker-compose down -v
```


**************



### How to run
Add to project root directory 'test.pcap' file

Run
```bash
docker-compose pull
docker-compose up -d
docker logs -f analyzer
```

### Stop

In project root directory run

```bash
docker-compose down -v
```

