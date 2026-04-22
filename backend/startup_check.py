import sys, os
sys.stdout.write("START\n")
sys.stdout.flush()
sys.stdout.write(f"Python: {sys.version}\n")
sys.stdout.flush()
sys.stdout.write(f"CWD: {os.getcwd()}\n")
sys.stdout.flush()
sys.stdout.write(f"DB: {bool(os.environ.get('DATABASE_URL'))}\n")
sys.stdout.flush()
