"""Создаёт демо-данные MiniSocial по мотивам docs/screenshots/.
Запуск: python manage.py seed_demo
"""
from datetime import datetime, timezone as dt_timezone
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Post, Comment, Like, Subscription

User = get_user_model()

USERS = [
    ("admin",  "Admin#Root-2026",  True),
    ("Greg",   "Greg#Sky-2026",    False),
    ("Goga",   "Goga#Wood-2026",   False),
    ("Slava",  "Slava#River-2026", False),
    ("Vanya",  "Vanya#Stone-2026", False),
    ("Marina", "Marina#Pearl-2026",False),
    ("Nina",   "Nina#Star-2026",   False),
]

POSTS = [
    ("admin",  "Django + Bootstrap — отличный стек для веб-приложений!",
     datetime(2026, 10, 13, 17, 37, tzinfo=dt_timezone.utc)),
    ("admin",  "Привет! Это мой первый пост в MiniSocial",
     datetime(2026, 10, 13, 17, 37, tzinfo=dt_timezone.utc)),
    ("Nina",   "надо здесь почаще появляться))",
     datetime(2025, 10, 28, 22, 49, tzinfo=dt_timezone.utc)),
    ("Nina",   "о как тут у вас здорово!!!",
     datetime(2025, 10, 28, 22, 48, tzinfo=dt_timezone.utc)),
    ("Vanya",  "как дела?",
     datetime(2025, 10, 28, 21, 19, tzinfo=dt_timezone.utc)),
    ("Slava",  "скоро победим!!!",
     datetime(2025, 10, 28, 20, 58, tzinfo=dt_timezone.utc)),
    ("Slava",  "вроде, движется вперед!!!",
     datetime(2025, 10, 28, 20, 57, tzinfo=dt_timezone.utc)),
    ("Marina", "что еще сделать?",
     datetime(2025, 10, 28, 0, 47, tzinfo=dt_timezone.utc)),
    ("Marina", "Ура! все работает!!!!) что бы еще сделать?",
     datetime(2025, 10, 28, 0, 37, tzinfo=dt_timezone.utc)),
    ("Vanya",  "как тут у вас дела?",
     datetime(2025, 10, 27, 22, 41, tzinfo=dt_timezone.utc)),
    ("Slava",  "это Слава. Я делаю первый пост! и еще сделаю))",
     datetime(2025, 10, 27, 15, 18, tzinfo=dt_timezone.utc)),
    ("Goga",   "движемся вперед!!! все быстрее и быстрее))",
     datetime(2025, 10, 27, 4, 37, tzinfo=dt_timezone.utc)),
    ("Goga",   "Сделал пост!!! Ура!!!",
     datetime(2025, 10, 27, 4, 11, tzinfo=dt_timezone.utc)),
]

COMMENTS = [
    (2,  "Vanya",  "будем ради вкачать))"),
    (4,  "Vanya",  "норм"),
    (5,  "Slava",  "ага"),
    (6,  "Slava",  "стараемся"),
    (7,  "Vanya",  "скоро будет все хорошо!!"),
    (9,  "Slava",  "все получится"),
    (9,  "Goga",   "молодец!"),
    (10, "Nina",   "привет!"),
    (11, "Marina", "неплохо!"),
]

LIKES = [
    (2,  "admin"),
    (3,  "admin"),
    (4,  "admin"),
    (5,  "admin"),
    (6,  "admin"),
    (7,  "admin"), (7, "Nina"), (7, "Vanya"),
    (8,  "admin"), (8, "Nina"), (8, "Vanya"),
    (9,  "admin"), (9, "Nina"), (9, "Slava"), (9, "Goga"),
    (10, "admin"), (10, "Nina"), (10, "Vanya"),
    (11, "admin"), (11, "Nina"), (11, "Slava"), (11, "Vanya"),
    (12, "admin"), (12, "Nina"), (12, "Slava"), (12, "Vanya"),
]

SUBSCRIPTIONS = [
    ("admin", "Greg"),
    ("admin", "Marina"),
    ("admin", "Nina"),
]


class Command(BaseCommand):
    help = "Создаёт демо-данные MiniSocial"

    def handle(self, *args, **options):
        for username, password, is_staff in USERS:
            u, created = User.objects.get_or_create(
                username=username,
                defaults={"is_staff": is_staff, "is_superuser": is_staff},
            )
            if created:
                u.set_password(password)
                u.save()
                self.stdout.write(self.style.SUCCESS(f"+ user {username}"))

        posts = []
        for author_name, text, dt in POSTS:
            author = User.objects.get(username=author_name)
            p, created = Post.objects.get_or_create(author=author, text=text)
            if created:
                Post.objects.filter(pk=p.pk).update(created_at=dt)
                p.refresh_from_db()
                self.stdout.write(self.style.SUCCESS(f"+ post #{p.id} by {author_name}"))
            posts.append(p)

        for idx, author_name, text in COMMENTS:
            Comment.objects.get_or_create(
                post=posts[idx],
                author=User.objects.get(username=author_name),
                text=text,
            )

        for idx, username in LIKES:
            Like.objects.get_or_create(
                post=posts[idx],
                user=User.objects.get(username=username),
            )

        for subscriber, target in SUBSCRIPTIONS:
            Subscription.objects.get_or_create(
                subscriber=User.objects.get(username=subscriber),
                target=User.objects.get(username=target),
            )

        self.stdout.write(self.style.SUCCESS("\nГотово! Итог:"))
        self.stdout.write(f"  Users:         {User.objects.count()}")
        self.stdout.write(f"  Posts:         {Post.objects.count()}")
        self.stdout.write(f"  Comments:      {Comment.objects.count()}")
        self.stdout.write(f"  Likes:         {Like.objects.count()}")
        self.stdout.write(f"  Subscriptions: {Subscription.objects.count()}")
