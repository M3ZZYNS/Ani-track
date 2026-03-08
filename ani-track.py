import sqlite3
import subprocess
import os

DB = "anime.db"


# -------------------------
# DATABASE
# -------------------------

def setup_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS anime (
        title TEXT PRIMARY KEY,
        episode INTEGER
    )
    """)

    conn.commit()
    conn.close()


def get_episode(title):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT episode FROM anime WHERE title=?", (title,))
    result = cur.fetchone()

    conn.close()

    return result[0] if result else 0


def update_episode(title, ep):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO anime (title, episode)
    VALUES (?, ?)
    ON CONFLICT(title)
    DO UPDATE SET episode=excluded.episode
    """, (title, ep))

    conn.commit()
    conn.close()


def list_anime():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT title, episode FROM anime")

    shows = cur.fetchall()

    conn.close()

    return shows


# -------------------------
# PLAYER
# -------------------------

def play(anime, episode):

    print(f"\nStarting {anime} episode {episode}\n")

    subprocess.run([
        "ani-cli",
        anime,
        "-e",
        str(episode)
    ])

    update_episode(anime, episode)


# -------------------------
# MENU FUNCTIONS
# -------------------------

def watch_anime():

    anime = input("\nAnime name: ")

    last = get_episode(anime)

    if last > 0:
        print(f"Last watched episode: {last}")

        choice = input("Resume next episode? (y/n): ")

        if choice.lower() == "y":
            ep = last + 1
        else:
            ep = int(input("Episode number: "))
    else:
        ep = int(input("Start episode: "))

    play(anime, ep)


def show_library():

    shows = list_anime()

    if not shows:
        print("\nLibrary empty\n")
        return

    print("\nYour Anime Library\n")

    for i, show in enumerate(shows, 1):
        print(f"{i}. {show[0]} (episode {show[1]})")

    print()


def continue_watching():

    shows = list_anime()

    if not shows:
        print("\nNothing to continue\n")
        return

    print("\nContinue Watching\n")

    for i, show in enumerate(shows, 1):
        print(f"{i}. {show[0]} (next episode {show[1]+1})")

    choice = input("\nSelect show number: ")

    try:
        index = int(choice) - 1
        anime, ep = shows[index]

        play(anime, ep + 1)

    except:
        print("Invalid selection")


# -------------------------
# MAIN MENU
# -------------------------

def menu():

    while True:

        print("\n========== Ani-Track ==========")
        print("1 Watch Anime")
        print("2 Continue Watching")
        print("3 View Library")
        print("4 Exit")

        choice = input("> ")

        if choice == "1":
            watch_anime()

        elif choice == "2":
            continue_watching()

        elif choice == "3":
            show_library()

        elif choice == "4":
            break

        else:
            print("Invalid option")


# -------------------------

setup_db()

try:
    menu()
except KeyboardInterrupt:
    print("\n\nExiting Ani-Track. Goodbye.\n")