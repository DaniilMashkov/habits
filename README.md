### API трекера привычек
---
#### Регистрация и авторизация требуется для всех действий, кроме регистрации нового пользователя. Администратор имеет доступ ко всем пользователям и привычкам, обычный пользователь только к своему аккаунту и привычкам.
---
Модель привычки: 
- *пользователь* - создатель привычки
- *место* - место, в котором необходимо выполнять привычку
- *время -* время, когда необходимо выполнять привычку
- *действие -* действие, которое представляет из себя привычка
- *признак приятной привычки* - привычка, которую можно привязать к выполнению полезной привычки
- *связанная привычка -* привычка, которая связана с другой привычкой, важно указывать для полезных привычек, но не для приятных
- *периодичность* (по умолчанию ежедневная) - периодичность выполнения привычки для напоминания в днях
- *вознаграждение -* чем пользователь должен себя вознаградить после выполнения
- *время на выполнение -* время, которое предположительно потратит пользователь на выполнение привычки
- *признак публичности -* привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать в пример чужие привычки

---
### Валидаторы

- исключить одновременный выбор связанной привычки и указания вознаграждения
- время выполнения должно быть не больше 120 секунд
- нельзя, чтобы связанная привычка и вознаграждение были одновременно пустые
- в связанные привычки могут попадать только привычки с признаком приятной привычки
- у приятной привычки не может быть вознаграждения или связанной привычки
- периодичность не может быть более 7 дней, то есть привычку нельзя выполнять больше, чем раз в неделю

### Права доступа

- каждый пользователь имеет доступ только к своим привычкам по механизму CRUD
- также пользователь может видеть список публичных привычек без возможности их как-то редактировать или удалять

### Эндпоинты

- регистрация
- авторизация
- список моих привычек
- список публичных привычек
- создание привычки
- редактирование привычки
- удаление привычки
---
### В приложении предусмотрены две отложенные задачи:
- Проверка новых пользователей раз в 30 секунд, которые подписались на telegram-бота. Для добавления задачи нужно выполнить команду "python3 manage.py set_tasks"
- Второй тип задач добавляется в БД автоматически при создании новой привычки и отправляет уведомление в telegram в указанное в привычке время

Команда для запуска: celery -A config worker --beat --scheduler django --loglevel=info

---
######
- По адресу localhost:8000/swagger доступна документация
- Директория htmlcov содержит результаты тестирования

