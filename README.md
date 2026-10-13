# MiniSocial 🐦

Простая социальная сеть на Django: посты, лайки, комментарии, подписки и админ-панель.
Учебный выпускной проект курса «Программист на Python с нуля с помощью ChatGPT» (Зерокодер, 2025).

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## 🎯 Возможности

- 🔐 Регистрация, вход, выход (Django auth)
- 📝 Создание / редактирование / удаление постов (до 1000 символов)
- 🖼 Загрузка изображений к постам
- 📰 Лента постов с сортировкой по дате
- 👥 Подписки / отписки, персонализированная лента
- ❤️ Лайки (поставить / снять, счётчик)
- 💬 Комментарии к постам
- 🛠 Админ-панель Django для управления всеми объектами
- 🎨 Bootstrap-интерфейс

## 🛠 Стек

- Python 3.10+
- Django 5.2
- SQLite (dev)
- Django Templates + Bootstrap 5
- Pillow (для ImageField)

## ⚙️ Установка и запуск

```bash
git clone https://github.com/Valsw486/MyProDjango6.git
cd MyProDjango6

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Приложение: http://127.0.0.1:8000/
Админка: http://127.0.0.1:8000/admin/

## 📂 Структура проекта

```
MyProDjango/    — настройки Django-проекта
core/           — основное приложение: посты, комментарии, лайки, подписки
users/          — аутентификация и профиль
templates/      — общие шаблоны
```

## 🗄 Модели

- **Post** — текст, автор, изображение, дата
- **Comment** — пост, автор, текст, дата
- **Like** — пост, пользователь (уникальная пара)
- **Subscription** — подписчик, автор (уникальная пара)

## 🧪 Тесты

```bash
python manage.py test
```

## 🗺 Что можно добавить дальше

- [ ] AJAX-лайки без перезагрузки
- [ ] Поиск по постам и пользователям
- [ ] Личные сообщения
- [ ] Уведомления
- [ ] Postgres + Docker
- [ ] CI на GitHub Actions

## 👤 Автор

**Валерий** — [@Valsw486](https://github.com/Valsw486)

Сертификат №30778 от 05.11.2025 — курс «Программист на Python с нуля с помощью ChatGPT», Зерокодер.

## 📜 Лицензия

MIT