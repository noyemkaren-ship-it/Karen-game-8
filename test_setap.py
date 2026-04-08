# test_setup.py
print("=" * 50)
print("Тестирование настройки базы данных")
print("=" * 50)

print("\n1. Проверка импортов...")
try:
    from repository.database import Base
    print("   ✅ Base импортирован")
except Exception as e:
    print(f"   ❌ Ошибка импорта Base: {e}")

try:
    from models.game import Game
    print(f"   ✅ Game импортирован, таблица: {Game.__tablename__}")
except Exception as e:
    print(f"   ❌ Ошибка импорта Game: {e}")

print("\n2. Создание репозитория...")
try:
    from repository.game_repo import GameRepository
    repo = GameRepository()
    print("   ✅ Репозиторий создан")
except Exception as e:
    print(f"   ❌ Ошибка создания репозитория: {e}")
    exit(1)

print("\n3. Проверка данных...")
try:
    games = repo.get_all()
    print(f"   ✅ Найдено игр: {len(games)}")
except Exception as e:
    print(f"   ❌ Ошибка получения данных: {e}")

print("\n4. Добавление тестовой игры...")
try:
    if repo.count() == 0:
        game = repo.create("Тестовая игра", "/test-link")
        print(f"   ✅ Добавлена игра: {game.name}")
    else:
        print("   ⏭️ Игры уже есть, пропускаем")
except Exception as e:
    print(f"   ❌ Ошибка добавления: {e}")

print("\n5. Финальная проверка...")
try:
    all_games = repo.get_all()
    print(f"   ✅ Всего игр в БД: {len(all_games)}")
    for game in all_games:
        print(f"      - ID: {game.id}, Name: {game.name}, Link: {game.link}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

print("\n" + "=" * 50)
print("Тестирование завершено!")
print("=" * 50)