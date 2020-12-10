# Course Platform API

## Task

Реализовать систему по проведению онлайн курсов. Подразумевается использование фреймворков Django/DRF. Вся логика 
приложения должна быть реализована и доступна через API.

Все пользователи системы имеют следующие возможности: 
  * регистрация (при регистрации выбирается роль пользователя: преподаватель/студент);
  * авторизация.
  
Преподаватели имеют следующие возможности: 
  * CRUD своих курсов;
  * добавление/удаление студента к своему курсу;
  * добавление нового преподавателя к своему курсу;
  * CRUD лекций своих курсов (лекция - это тема и файл с презентацией);
  * к каждой лекции добавлять домашние задания (текстовая информация);
  * просмотр выполненных домашних заданий;
  * к каждому выполненному домашнему заданию выставлять/менять оценки для каждого студента, который отправил домашнее задание;
  * к каждой оценке добавлять комментарии.
  
Студенты имеют следующие возможности: 
  * просмотр доступных курсов;
  * просмотр доступных лекций в рамках выбранного доступного курса;
  * просмотр ДЗ доступной лекции;
  * отправка ДЗ на проверку;
  * просмотр своих ДЗ;
  * просмотр оценок своих ДЗ;
  * просмотр/добавление комментариев к оценке.
  
К требованиям также относится: 
  * безопасность данных (permissions для всех CRUD действий);
  * Наличие документации API (swagger).
  
## Getting Started
1. Installing virtualenv

   ```
   pip install virtualenv
   ```
2. Start a new virtual environment
   * Create
   
     ```
     unix:    virtualenv -p python3 .venv
     windows: virtualenv .venv
     ```
   * Activate
   
     ```
     unix:    source .venv/bin/activate
     windows: .venv\Scripts\activate
     ```
   * Deactivate
   
     ```
     deactivate
     ```
4. Installing packages

   ```
   pip install -r requirements.txt
   ```
5. Configure database (MySQL db by default)
   
   Make SQL queries in MySQL:
   
      * Create user: "CREATE USER 'test_user'@'localhost' IDENTIFIED BY 'password';"
      * Set privileges: "GRANT ALL PRIVILEGES ON *.* TO 'test_user'@'localhost';"
      * Create database: "CREATE DATABASE IF NOT EXISTS 'database';"
     
   Configure next fields in settings.py:
         
      * 'NAME': 'database'
      * 'USER': 'test_user'
      * 'PASSWORD': 'password'
      * 'HOST': 'localhost'

6. Run Server

   ```
   python manage.py runserver
   python run_server.py
   ```
6. Get documentation

   ```
   http://127.0.0.1:8000/swagger/
   ```