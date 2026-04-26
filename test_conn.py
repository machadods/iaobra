import psycopg2
import sys

try:
    configs = [
        {'host': '127.0.0.1', 'user': 'postgres', 'password': 'postgres', 'label': 'postgres/postgres @ 127.0.0.1'},
        {'host': 'localhost', 'user': 'postgres', 'password': 'postgres', 'label': 'postgres/postgres @ localhost'},
        {'host': '127.0.0.1', 'user': 'postgres', 'password': '', 'label': 'postgres/sem-senha @ 127.0.0.1'},
        {'host': 'localhost', 'user': 'postgres', 'password': '', 'label': 'postgres/sem-senha @ localhost'},
    ]
    
    conn = None
    for config in configs:
        try:
            print(f"Tentando conectar {config['label']}:5434...")
            conn = psycopg2.connect(
                host=config['host'],
                user=config['user'], 
                password=config['password'],
                port=5434,
                database='postgres',
                connect_timeout=5
            )
            print(f"  ✅ Conectado de {config['label']}!")
            break
        except psycopg2.OperationalError as e:
            erro_str = str(e)
            print(f"  ❌ {erro_str[:80] if erro_str else 'OperationalError sem mensagem'}")
            continue
        except Exception as e:
            print(f"  ❌ {type(e).__name__}: {str(e)[:40]}")
            continue
    
    if not conn:
        print("Nenhuma configuração funcionou!")
        sys.exit(1)
    print("✅ Conectado com sucesso!")
    
    # Testar execute
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    print(f"PostgreSQL: {version[:50]}")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Erro: {type(e).__name__}")
    print(f"   {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
