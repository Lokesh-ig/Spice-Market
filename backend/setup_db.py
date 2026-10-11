import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import pymysql

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

db_name = os.getenv('DB_NAME', 'spice_market_db')
db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', '')
db_host = os.getenv('DB_HOST', '127.0.0.1')
db_port = int(os.getenv('DB_PORT', 3306))
db_engine = os.getenv('DB_ENGINE', 'mysql').lower()

print("=" * 60)
print("  Spice Market - MySQL Database & Django Migration Setup")
print("=" * 60)
print(f"Target Database Engine: {db_engine}")
print(f"Host: {db_host}:{db_port}")
print(f"User: {db_user}")
print(f"Database: {db_name}")

if db_engine == 'mysql':
    print("\n[1/4] Connecting to MySQL server...")
    try:
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            port=db_port,
            charset='utf8mb4'
        )
        with conn.cursor() as cursor:
            print(f"[2/4] Ensuring database '{db_name}' exists in MySQL...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print(f"      Database '{db_name}' is ready!")
        conn.close()
    except pymysql.err.OperationalError as e:
        print(f"\n[!] MySQL Connection Failed: {e}")
        print("\nIf your MySQL server requires a password, please update it in:")
        print(f"    {BASE_DIR / '.env'}")
        print("    DB_PASSWORD=your_actual_password")
        print("\nWould you like to continue with SQLite for local testing until you set the password? (or set DB_ENGINE=sqlite3 in .env)")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Unexpected error connecting to MySQL: {e}")
        sys.exit(1)

print("\n[3/4] Running Django Migrations...")
try:
    subprocess.run([sys.executable, str(BASE_DIR / 'manage.py'), 'makemigrations', 'api'], check=True)
    subprocess.run([sys.executable, str(BASE_DIR / 'manage.py'), 'migrate'], check=True)
except subprocess.CalledProcessError as e:
    print(f"\n[!] Migration failed: {e}")
    sys.exit(1)

print("\n[4/4] Seeding initial spice market products...")
try:
    subprocess.run([sys.executable, str(BASE_DIR / 'manage.py'), 'seed_data'], check=True)
except subprocess.CalledProcessError as e:
    print(f"\n[!] Seeding data failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("  Database Setup Completed Successfully!")
print("=" * 60)
