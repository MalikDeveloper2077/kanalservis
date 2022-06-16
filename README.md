# Запуск  
```docker-compose up --build -d```

### В интерфейсе Docker  
Создание аккаунта в административной панели и запуск миграций:  
```python kanalservis/manage.py migrate```  
```python kanalservis/manage.py createsuperuser```  
  
Теперь при посещении страницы **localhost:8000/sheets** программа будет синхронизировать данные между БД и гугл таблицами.  
Чтобы наблюдать изменения перейдите на **localhost:8000/admin** в раздел **Orders**