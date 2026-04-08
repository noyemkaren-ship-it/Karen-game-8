# repository/game_repo.py
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from repository.database import Base
import os
from models.game import Game


class GameRepository:

    def __init__(self, db_url=None, echo=False):
        if db_url is None:
            data_dir = Path("./data")
            data_dir.mkdir(exist_ok=True)
            db_url = f"sqlite:///{data_dir}/games.db"
        
        self.db_url = db_url
        self.echo = echo
        
        print(f"📁 Инициализация репозитория с БД: {db_url}")
        
        self.engine = create_engine(
            db_url,
            echo=echo,
            connect_args={"check_same_thread": False} if "sqlite" in db_url else {}
        )
        
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        print(f"📋 Зарегистрированные таблицы в Base: {list(Base.metadata.tables.keys())}")
        self.create_tables()
    
        inspector = inspect(self.engine)
        existing_tables = inspector.get_table_names()
        print(f"✅ Существующие таблицы после создания: {existing_tables}")
        
        if 'games' not in existing_tables:
            print("⚠️ КРИТИЧЕСКАЯ ОШИБКА: Таблица 'games' не создана!")
            print("📋 Проверьте, что модель Game импортирована и использует тот же Base")
    
    def create_tables(self):
        """Создание всех таблиц на основе зарегистрированных моделей"""
        try:
            Base.metadata.create_all(bind=self.engine)
            print("✨ Таблицы успешно созданы")
        except Exception as e:
            print(f"❌ Ошибка при создании таблиц: {e}")
            raise
    
    def drop_tables(self):
        """Удаление всех таблиц"""
        Base.metadata.drop_all(bind=self.engine)
        print("🗑️ Таблицы удалены")
    
    def _get_session(self):
        return self.SessionLocal()
    
    def create(self, name, link):
        session = self._get_session()
        try:
            game = Game(name=name, link=link)
            session.add(game)
            session.commit()
            session.refresh(game)
            print(f"➕ Создана игра: {name}")
            return game
        except Exception as e:
            session.rollback()
            print(f"❌ Ошибка при создании игры: {e}")
            raise
        finally:
            session.close()
    
    def create_many(self, games_data):
        session = self._get_session()
        try:
            games = [Game(**data) for data in games_data]
            session.add_all(games)
            session.commit()
            for game in games:
                session.refresh(game)
            print(f"➕ Создано {len(games)} игр")
            return games
        except Exception as e:
            session.rollback()
            print(f"❌ Ошибка при создании игр: {e}")
            raise
        finally:
            session.close()
    
    def get_by_name(self, name):
        session = self._get_session()
        try:
            return session.query(Game).filter(Game.name == name).first()
        finally:
            session.close()
    
    def get_all(self, skip=0, limit=100):
        session = self._get_session()
        try:
            games = session.query(Game).offset(skip).limit(limit).all()
            print(f"📖 Загружено {len(games)} игр")
            return games
        except Exception as e:
            print(f"❌ Ошибка при загрузке игр: {e}")
            return []
        finally:
            session.close()
    
    def get_all_as_dict(self, skip=0, limit=100):
        games = self.get_all(skip, limit)
        return [game.to_dict() for game in games]
    
    def update(self, name, new_link):
        session = self._get_session()
        try:
            game = session.query(Game).filter(Game.name == name).first()
            if game:
                game.link = new_link
                session.commit()
                session.refresh(game)
                print(f"✏️ Обновлена игра: {name}")
                return game
            return None
        except Exception as e:
            session.rollback()
            print(f"❌ Ошибка при обновлении игры: {e}")
            raise
        finally:
            session.close()
    
    def delete(self, name):
        session = self._get_session()
        try:
            game = session.query(Game).filter(Game.name == name).first()
            if game:
                session.delete(game)
                session.commit()
                print(f"🗑️ Удалена игра: {name}")
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"❌ Ошибка при удалении игры: {e}")
            raise
        finally:
            session.close()
    
    def delete_all(self):
        session = self._get_session()
        try:
            count = session.query(Game).delete()
            session.commit()
            print(f"🗑️ Удалено {count} игр")
            return count
        except Exception as e:
            session.rollback()
            print(f"❌ Ошибка при удалении игр: {e}")
            raise
        finally:
            session.close()
    
    def count(self):
        session = self._get_session()
        try:
            return session.query(Game).count()
        finally:
            session.close()
    
    def exists(self, name):
        session = self._get_session()
        try:
            return session.query(Game).filter(Game.name == name).first() is not None
        finally:
            session.close()
    
    def search(self, search_term):
        session = self._get_session()
        try:
            return session.query(Game).filter(
                Game.name.contains(search_term)
            ).all()
        finally:
            session.close()
    
    def get_batch(self, names):
        session = self._get_session()
        try:
            return session.query(Game).filter(Game.name.in_(names)).all()
        finally:
            session.close()
    
    def __enter__(self):
        self.session = self._get_session()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'session'):
            self.session.close()
    
    def get_session(self):
        return self._get_session()