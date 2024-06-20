# Проект Онлайн магазин "YourStore"
________
В данном проекте представлен онлайн магазин электроники, кухонной техники и многое другое!<br>
В проекте подключены:
1. Корзина товаров;
2. Регистрация и авторизация пользователя;
3. Админ-панель для суперпользователя;
4. Фильтрация товаров по категориям;
5. Страничная пагинация;
6. Профиль пользователя с возможностью менять данные, добавления аватарки и отображение товаров корзины;
7. Возможность оставлять коментарии под товаром;
8. Возможность писать, редактировать, удалять отдельный отзыв в разделе отзывы.

Данный проект написан не фрейморке Django, с подключением реляционной базы данных "PostgreSQL"<br>
Ипользовалось вирутальное окружение ```venv```
В  проекте построенно 7 модель БД:
1. Таблица "category";
2. Таблица "Product" прямая связь с "category";
3. Таблица "Users" прямая связь с "category" и "products";
4. Таблица "Carousel" связи нет;
5. Таблица "Basket" прямая связь с "Users", "Product";
6. Таблица "Comments" прямая связь c "Users", "Product";
7. Таблица "Version" прямая связь c "Product".

Для запуска проекта необходимо сделать 
1. git clone репозитория
```
git@github.com:Meatdam/online_shop.git
```
2. Установить виртуальное окружение `venv`
```
python3 -m venv venv для MacOS и Linux систем
python -m venv venv для windows
```
3. Активировать виртуальное окружение
```
source venv/bin/activate для MasOs и Linux систем
venv\Scripts\activate.bat для windows
```
4. установить файл с зависимостями
```
pip install -r requirements.txt
```
5. Создать базу данных в ```PgAdmin```, либо через терминал. Необходимо дать название в файле settings.py в каталоге 'config' в константе (словаре) 'DATABASES'

6. Создать файл .env в корне проекта и заполнить следующие данные:
```
# DB settings
ENGINE=
DB_NAME=
USER_DB=
PASSWORD_DB=

# Email settings
EMAIL_HOST_USER_MAIL=
EMAIL_HOST_PASSWORD_MAIL=

# email admin
ADMIN_EMAIL=

# secret key from django
KEY=

# domain settings
DOMAIN=

DEBUG=

# CACHE settings
CACHE_ENABLED=
CACHES_BACKEND=
CACHES_LOCATION=

```
Автор проекта:<br>
[Кузькин Илья](https://github.com/Meatdam)

