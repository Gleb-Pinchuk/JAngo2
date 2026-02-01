# Django Catalog Project

Учебный проект на Django, реализующий каталог товаров с домашней страницей, страницей контактов и функционалом управления товарами.

## Основные функции
- Отображение списка опубликованных товаров на главной странице
- Страница с подробной информацией о товаре
- Страница с контактной информацией
- Администрирование товаров (создание, редактирование, удаление)
- Ролевая модель: группа «Модератор продуктов» с правами:
  - отменять публикацию товара (`can_unpublish_product`)
  - удалять любые товары
- Использование Bootstrap 5 для стилизации
- Подключение PostgreSQL в качестве СУБД


## Установка и запуск

1. Клонируйте репозиторий:
[ git clone https://github.com/Gleb-Pinchuk/JAngo2.git](https://github.com/Gleb-Pinchuk/JAngo2/pull/3)
 
2. Создайте и активируйте виртуальное окружение:
   python -m venv venv
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate
3. Установите зависимости:
  pip install -r requirements.txt

3. Выполните миграции:
python manage.py migrate

4. Запустите сервер:
python manage.py runserver
