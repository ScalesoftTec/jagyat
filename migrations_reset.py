import os
import shutil

# Path to your Django project (where manage.py is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def reset_migrations():
    for root, dirs, files in os.walk(BASE_DIR):
        if "migrations" in dirs:
            migration_path = os.path.join(root, "migrations")
            
            # Skip Django internal migrations (admin, auth, etc.)
            if "site-packages" in migration_path or "venv" in migration_path:
                continue

            print(f"Resetting migrations in: {migration_path}")

            # Delete the migrations folder
            shutil.rmtree(migration_path, ignore_errors=True)

            # Recreate migrations folder
            os.makedirs(migration_path, exist_ok=True)

            # Create empty __init__.py
            init_file = os.path.join(migration_path, "__init__.py")
            with open(init_file, "w") as f:
                f.write("")

if __name__ == "__main__":
    reset_migrations()
    print("✅ All migrations folders reset successfully.")
