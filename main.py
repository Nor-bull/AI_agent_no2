import sqlite3
import os


def init_database():

    db_path = 'products.db'

    print("Inicializuji databazi...")

    # Pripojeni k databazi
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Vytvoreni tabulky
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            category TEXT NOT NULL
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM products')
    count = cursor.fetchone()[0]

    if count == 0:
        print("Vkladam data...")

        # Vzorová data
        sample_products = [
            ('Laptop Dell XPS 15', 35999, 5, 'Elektronika'),
            ('iPhone 15 Pro', 32999, 12, 'Elektronika'),
            ('Samsung Galaxy S24', 28999, 8, 'Elektronika'),
            ('Kancelarska zidle ErgoMax', 7500, 8, 'Nabytek'),
            ('Pracovni stul IKEA', 4990, 15, 'Nabytek'),
            ('Kavovar DeLonghi', 8999, 15, 'Domacnost'),
            ('Robot vysavac Xiaomi', 6499, 20, 'Domacnost'),
            ('Kniha - Python Programming', 899, 50, 'Knihy'),
            ('Kniha - Design Patterns', 1299, 30, 'Knihy'),
            ('Bezdratovs mys Logitech', 1499, 25, 'Elektronika')
        ]

        cursor.executemany(
            'INSERT INTO products (name, price, stock, category) VALUES (?, ?, ?, ?)',
            sample_products
        )

        conn.commit()
        print(f"Vlozeno {len(sample_products)} produktu")
    else:
        print(f"Databaze jiz obsahuje {count} produktu")

    # Zobrazení obsahu
    print("\nObsah databaze:")
    print("-" * 80)

    cursor.execute('''
        SELECT category, COUNT(*) as count, SUM(stock) as total_stock
        FROM products
        GROUP BY category
        ORDER BY category
    ''')

    print(f"\n{'Kategorie':<20} {'Pocet produktu':<20} {'Celkovy sklad'}")
    print("-" * 80)

    for row in cursor.fetchall():
        print(f"{row[0]:<20} {row[1]:<20} {row[2]} ks")

    print("-" * 80)

    cursor.execute('SELECT COUNT(*), SUM(stock) FROM products')
    total_products, total_stock = cursor.fetchone()
    print(f"{'CELKEM':<20} {total_products:<20} {total_stock} ks\n")

    conn.close()

    print(f"✨ Databaze je pripravena: {os.path.abspath(db_path)}")

    return db_path


if __name__ == '__main__':
    init_database()
