"""
Test skript pro overeni funkcnosti databaze a toolu
"""

import sqlite3
import sys


def test_database_connection():
    """Test pripojeni k databazi"""
    print("Test 1: Pripojeni k databazi...")
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM products')
        count = cursor.fetchone()[0]
        conn.close()
        print(f"Uspech! Databaze obsahuje {count} produktu\n")
        return True
    except Exception as e:
        print(f"Chyba: {e}\n")
        return False


def test_search_products():
    """Test vyhledavani produktu"""
    print("Test 2: Vyhledavani produktu...")
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        query = "laptop"
        cursor.execute('''
            SELECT id, name, price, stock, category 
            FROM products 
            WHERE name LIKE ? OR category LIKE ?
        ''', (f'%{query}%', f'%{query}%'))

        results = cursor.fetchall()
        conn.close()

        if results:
            print(f"Nalezeno {len(results)} produktu pro dotaz '{query}':")
            for row in results:
                print(f"      - {row[1]} ({row[2]} Kč)")
            print()
            return True
        else:
            print(f"Zadne vysledky pro dotaz '{query}'\n")
            return False

    except Exception as e:
        print(f"Chyba: {e}\n")
        return False


def test_add_product():
    """Test pridani produktu"""
    print("Test 3: Pridani produktu...")
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        # pridani
        test_product = ('TEST Produkt', 999.99, 1, 'TEST')
        cursor.execute('''
            INSERT INTO products (name, price, stock, category)
            VALUES (?, ?, ?, ?)
        ''', test_product)

        product_id = cursor.lastrowid
        conn.commit()

        # overeni
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()

        # smazani
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()

        if product:
            print(f"Produkt pridan a smazan (ID: {product_id})\n")
            return True
        else:
            print(f"Produkt nenalezen\n")
            return False

    except Exception as e:
        print(f"Chyba: {e}\n")
        return False


def test_update_stock():
    """Test aktualizace skladu"""
    print("Test 4: Aktualizace skladu...")
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        # Získání prvního produktu
        cursor.execute('SELECT id, stock FROM products LIMIT 1')
        product = cursor.fetchone()

        if not product:
            print("Zadne produkty v databazi\n")
            conn.close()
            return False

        product_id, old_stock = product
        new_stock = old_stock + 1  # Přidáme 1 kus

        # aktualizace
        cursor.execute('UPDATE products SET stock = ? WHERE id = ?', (new_stock, product_id))
        conn.commit()

        # overeni
        cursor.execute('SELECT stock FROM products WHERE id = ?', (product_id,))
        updated_stock = cursor.fetchone()[0]

        # Vraceni zpet
        cursor.execute('UPDATE products SET stock = ? WHERE id = ?', (old_stock, product_id))
        conn.commit()
        conn.close()

        if updated_stock == new_stock:
            print(f"Sklad uspesne aktualizovan (ID: {product_id}, {old_stock} → {new_stock} → {old_stock})\n")
            return True
        else:
            print(f"Aktualizace selhala\n")
            return False

    except Exception as e:
        print(f"Chyba: {e}\n")
        return False


def test_get_all_products():
    """Test ziskani vsech produktu"""
    print("Test 5: Vsechny produkty...")
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, name, price, stock, category 
            FROM products 
            ORDER BY category, name
        ''')

        results = cursor.fetchall()
        conn.close()

        if results:
            print(f"Nacteno {len(results)} produktu")

            # seskupeni
            categories = {}
            for row in results:
                cat = row[4]
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(row)

            for cat, products in sorted(categories.items()):
                print(f"\n      📦 {cat} ({len(products)} produktu):")
                for p in products[:2]:  # max 2 z kazde kategorie
                    print(f"         - [{p[0]}] {p[1]}")
                if len(products) > 2:
                    print(f"         ... a dalsi {len(products) - 2}")

            print()
            return True
        else:
            print(f"Databaze je prazdna\n")
            return False

    except Exception as e:
        print(f"Chyba: {e}\n")
        return False


def main():
    """Spusteni vsech testu"""
    print("=" * 60)
    print("TESTOVANI DATABAZE A TOOLU")
    print("=" * 60)
    print()

    tests = [
        test_database_connection,
        test_search_products,
        test_add_product,
        test_update_stock,
        test_get_all_products
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)

    print("=" * 60)
    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"VSECHNY TESTY PROSLY ({passed}/{total})")
        print("Databaze je pripravena k pouziti!")
    else:
        print(f"  ⚠️  NEKTERE TESTY SELHALY ({passed}/{total})")
        print("  🔧 Zkontroluj chybove hlasky")

    print("=" * 60)
    print()

    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
