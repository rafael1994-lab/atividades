import tkinter as tk
from tkinter import ttk, messagebox
import banco
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

# Criando o banco de dados e a tabela
banco.criar_tabela()


# ==========================================
# FUNÇÃO PARA ABRIR A TELA PRINCIPAL DO SISTEMA
# ==========================================
def abrir_sistema_principal():
    janela = tk.Tk()
    janela.title("Sistema de Supermercado")
    janela.geometry("1000x600")
    janela.configure(bg="#d9d9d9")

    # TÍTULO DA JANELA
    titulo = tk.Label(
        janela,
        text="Gerenciamento de produtos",
        font=('Arial', 20, 'bold'),
        bg="#d9d9d9"
    )
    titulo.pack(pady=15)

    # FRAME DO FORMULARIO
    frame = tk.LabelFrame(
        janela,
        text="Dados do Produto",
        font=('Arial', 12, 'bold'),
        padx=10,
        pady=10
    )
    frame.pack(fill="x", padx=20)

    # VARIÁVEIS
    global codigo, nome, categoria, preco, quantidade, tabela
    codigo = tk.StringVar()
    nome = tk.StringVar()
    categoria = tk.StringVar()
    preco = tk.StringVar()
    quantidade = tk.StringVar()

    # Campos
    campos = [
        ("Código", codigo),
        ("Nome", nome),
        ("Categoria", categoria),
        ("Preço", preco),
        ("Quantidade", quantidade)
    ]

    for i, (texto, variavel) in enumerate(campos):
        tk.Label(frame, text=texto).grid(
            row=0, column=i, padx=5, pady=5
        )
        tk.Entry(
            frame,
            textvariable=variavel,
            width=16
        ).grid(row=1, column=i, padx=5, pady=5)

    # TABELA
    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(fill="both", expand=True, padx=20, pady=15)

    colunas = (
        "ID", "Código", "Nome", "Categoria", "Preço", "Quantidade"
    )
    tabela = ttk.Treeview(
        frame_tabela,
        columns=colunas,
        show="headings"
    )

    for coluna in colunas:
        tabela.heading(coluna, text=coluna)
        tabela.column(coluna, width=120, anchor="center")

    tabela.pack(fill="both", expand=True)

    # ------------- CRIAÇÃO DE FUNÇÕES DA INTERFACE -------------

    def limpa():
        codigo.set("")
        nome.set("")
        categoria.set("")
        preco.set("")
        quantidade.set("")

    def atualizar(filtro=""):
        for item in tabela.get_children():
            tabela.delete(item)
        for produto in banco.listar_produtos():
            if filtro.lower() in str(produto[1]).lower():
                tabela.insert("", "end", values=produto)

    def cadastrar():
        try:
            if not codigo.get().strip() or not nome.get().strip():
                messagebox.showwarning("Atenção", "Preencha o código e o nome!")
                return
            valor = float(preco.get().replace(",", "."))
            qtd = int(quantidade.get())

            if valor < 0 or qtd < 0:
                raise ValueError

            banco.cadastrar_produto(
                codigo.get(),
                nome.get(),
                categoria.get(),
                valor,
                qtd
            )

            messagebox.showinfo("Sucesso", "Produto Cadastrado")
            limpa()
            atualizar()

        except ValueError:
            messagebox.showerror("Erro", "Informe preço e quantidade válidos")
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))  

    def excluir():
        selecionado = tabela.selection()

        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto")
            return
        
        produto = tabela.item(selecionado[0])["values"]

        confirmar = messagebox.askyesno("Confirmar", "Deseja Excluir o produto?")
        if confirmar:
            banco.excluir_produto(produto[0])
            atualizar()
            limpa()   

    def selecionar(event):
        selecionado = tabela.selection()

        if selecionado:
            produto = tabela.item(selecionado[0])["values"]
            codigo.set(produto[1])
            nome.set(produto[2])
            categoria.set(produto[3])
            preco.set(str(produto[4]))
            quantidade.set(str(produto[5]))

    def editar():
        selecionado = tabela.selection()

        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto")
            return
        
        try:
            produto = tabela.item(selecionado[0])["values"]
            valor = float(preco.get().replace(",", "."))
            qtd = int(quantidade.get()) 

            if valor < 0 or qtd < 0:
                raise ValueError
            
            banco.atualizar_produto(
                produto[0],
                codigo.get(),
                nome.get(),
                categoria.get(),
                valor,
                qtd
            )   

            messagebox.showinfo("Sucesso", "Produto Atualizado")
            limpa()
            atualizar()

        except ValueError:
            messagebox.showerror("Erro", "Preço ou quantidade inválidos!")
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))  

    # BOTÕES
    frame_botoes = tk.Frame(janela, bg="#d9d9d9")
    frame_botoes.pack(pady=20)

    tk.Button(
        frame_botoes,
        text="Cadastrar Produtos",
        font=('Arial', 15, 'bold'),
        width=15,
        bg="#0cec2a",
        fg='black',
        command=cadastrar
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        frame_botoes,
        text="Excluir Produto",
        font=('Arial', 15, 'bold'),
        width=15,
        bg="#f80404",
        fg='black',
        command=excluir
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        frame_botoes,
        text="Editar Produto",
        font=('Arial', 15, 'bold'),
        width=15,
        bg="#ffee00",
        fg='black',
        command=editar
    ).grid(row=0, column=2, padx=5)

    tabela.bind("<<TreeviewSelect>>", selecionar)
    atualizar()
    janela.mainloop()


# ==========================================
# TELA DE LOGIN (COM INPUTS NORMAIS)
# ==========================================
def tela_login():
    login_janela = tk.Tk()
    login_janela.title("Login - Sistema de Supermercado")
    login_janela.geometry("350x250")
    login_janela.configure(bg="#d9d9d9")
    login_janela.resizable(False, False)

    tk.Label(login_janela, text="Acesso ao Sistema", font=('Arial', 16, 'bold'), bg="#d9d9d9").pack(pady=15)

    frame_inputs = tk.Frame(login_janela, bg="#d9d9d9")
    frame_inputs.pack(pady=5)

    tk.Label(frame_inputs, text="Usuário:", font=('Arial', 11), bg="#d9d9d9").grid(row=0, column=0, sticky="w", pady=5)
    entry_usuario = tk.Entry(frame_inputs, font=('Arial', 11), width=18)
    entry_usuario.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(frame_inputs, text="Senha:", font=('Arial', 11), bg="#d9d9d9").grid(row=1, column=0, sticky="w", pady=5)
    
    # Campo de senha comum (Entry simples, sem ocultação de caracteres)
    entry_senha = tk.Entry(frame_inputs, font=('Arial', 11), width=18)
    entry_senha.grid(row=1, column=1, pady=5, padx=5)

    def verificar_login():
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()

        # Dois usuários permitidos
        usuarios_validos = {
            "admin": "1234",
            "gerente": "abcd"
        }

        if usuario in usuarios_validos and usuarios_validos[usuario] == senha:
            messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario}!")
            login_janela.destroy()  
            abrir_sistema_principal()  
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha incorretos!")

    tk.Button(
        login_janela,
        text="Entrar",
        font=('Arial', 12, 'bold'),
        bg="#0cec2a",
        fg="black",
        width=12,
        command=verificar_login
    ).pack(pady=15)

    login_janela.mainloop()

if __name__ == "__main__":
    tela_login()