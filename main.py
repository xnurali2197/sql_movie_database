import sqlite3
import time
from functools import wraps
import datetime

def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[DECORATOR] {func.__name__} — {end - start:.4f} soniya")
        return result
    return wrapper

class MovieDB:
    def __init__(self, app_name="Kinolar Bazasi"):
        self._app_name = app_name
        self._create_db()

    @property
    def app_name(self):
        return self._app_name

    @app_name.setter
    def app_name(self, value):
        if len(value.strip()) < 5:
            raise ValueError("Ilova nomi kamida 5 harfdan iborat bo'lishi kerak!")
        self._app_name = value
        print(f"Ilova nomi yangilandi: {value}")

    def _create_db(self):
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            director TEXT,
            year INTEGER,
            rating REAL,
            genre TEXT,
            added_date TEXT
        )''')
        conn.commit()
        conn.close()

    @timer_decorator
    def add_movie(self, title, director, year, rating, genre):
        if rating < 0 or rating > 10:
            print("Reyting 0 dan 10 gacha bo'lishi kerak!")
            return
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("INSERT INTO movies (title, director, year, rating, genre, added_date) VALUES (?, ?, ?, ?, ?, ?)",
                       (title, director, year, rating, genre, now))
        conn.commit()
        conn.close()
        print(f"✅ Kino qo'shildi: {title} ({year})")

    @timer_decorator
    def show_all_movies(self):
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies ORDER BY year DESC")
        movies = cursor.fetchall()
        conn.close()
        print(f"\n=== {self.app_name} — Barcha kinolar ===")
        if not movies:
            print("Hozircha kinolar yo'q.")
            return
        for m in movies:
            print(f"ID:{m[0]:<4} | {m[1]:<30} | Rejissor: {m[2]:<20} | Yil: {m[3]} | Reyting: {m[4]:.1f} | Janr: {m[5]}")

    @timer_decorator
    def search_by_genre(self, genre):
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies WHERE genre LIKE ? ORDER BY rating DESC", (f"%{genre}%",))
        movies = cursor.fetchall()
        conn.close()
        print(f"\n=== {genre} janridagi kinolar ===")
        if not movies:
            print("Bu janrda kino topilmadi.")
            return
        for m in movies:
            print(f"{m[1]} ({m[3]}) — Reyting: {m[4]:.1f}")

    def info(self):
        print(f"\n🎬 {self.app_name}")

if __name__ == "__main__":
    db = MovieDB()
    print("=== Movie Database Tizimi ===")
    while True:
        print("\n1. Kino qo'shish\n2. Barcha kinolarni ko'rish\n3. Janr bo'yicha qidirish\n4. Ilova nomini o'zgartirish\n5. Chiqish")
        choice = input("Tanlang (1-5): ").strip()
        if choice == "1":
            title = input("Kino nomi: ").strip()
            director = input("Rejissor: ").strip()
            year = int(input("Yil: "))
            rating = float(input("Reyting (0-10): "))
            genre = input("Janr: ").strip()
            db.add_movie(title, director, year, rating, genre)
        elif choice == "2":
            db.show_all_movies()
        elif choice == "3":
            genre = input("Qidiriladigan janr: ").strip()
            db.search_by_genre(genre)
        elif choice == "4":
            new_name = input("Yangi ilova nomi: ").strip()
            try:
                db.app_name = new_name
            except ValueError as e:
                print(e)
        elif choice == "5":
            print("Dastur tugadi!")
            break
        else:
            print("Noto'g'ri tanlov!")
