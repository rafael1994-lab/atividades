import sqlite3

def conectar():
    return sqlite3.connect("supermercado.db")

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            categoria TEXT,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)
    conexao.commit()
    conexao.close() 

def cadastrar_produto(codigo, nome, categoria, preco, quantidade):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO produtos
        (codigo, nome, categoria, preco, quantidade)
        VALUES (?, ?, ?, ?, ?)""", (codigo, nome, categoria, preco, quantidade))
    conexao.commit()
    conexao.close()

def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM produtos ORDER BY nome
    """)  

    produtos = cursor.fetchall()
    conexao.close()
    return produtos  

def excluir_produto(id_produto):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
    conexao.commit()
    conexao.close()

def atualizar_produto(id_produto, codigo, nome, categoria, preco, quantidade):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE produtos
        SET codigo = ?, nome = ?, categoria = ?,
        preco = ?, quantidade = ?
        WHERE id = ?
    """, (codigo, nome, categoria, preco, quantidade, id_produto))
    conexao.commit()
    conexao.close()