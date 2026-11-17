import tkinter as tk
from tkinter import ttk, messagebox
import banco

#criando o banco de dados
banco.criar_tabela()
#criando a janela principal
janela = tk.Tk()
janela.title("Sistema de Supermercado")
janela.geometry("1000x600")
janela.configure(bg="#d9d9d9")

titulo = tk.Label(
            janela,
            text="Gerenciamento de produtos",
            font=('Arial', 20, 'bold'),
            bg="#d9d9d9"
)
titulo.pack(pady=15)
#FRAME DO FORMULARIO
frame = tk.LabelFrame(
    janela,
    text="Dados do Produto",
    font=('Arial', 12, 'bold'),
    padx=10,
    pady=10
)

frame.pack(fill="x", padx=20)


#variaveis
codigo = tk.StringVar()
nome = tk.StringVar()
categoria = tk.StringVar()
preco = tk.StringVar()
quantidade = tk.StringVar()
pesquisa = tk.StringVar()

#campos
campos = [
    ("Código", codigo),
    ("Nome",nome),
    ("Categoria", categoria),
    ("Preço",preco),
    ("Quantidade", quantidade)
]
for i,(texto, variavel) in enumerate(campos):
    tk.Label(frame, text=texto).grid(
        row=0 , column=i, padx=5, pady=5
    )
    tk.Entry(
        frame,
        textvariable=variavel,
        width=16).grid(row=1, column=i, padx=5, pady=5)
#tabela
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

#--------------CRIAÇÃO DE FUNÇOES
#FUNÇÃO DE CADASTRO
def cadastrar():
    try:
        if not codigo.get().strip() or not nome.get().strip():
            messagebox.showwarning("Atenção", "Preencha o código e o nome!!")
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
    except ValueError:
        messagebox.showerror("Erro","Informe preço e quantidade válidos ")
    except Exception as erro:
        messagebox.showerror("Erro",str(erro))
#BOTÕES
frame_botoes = tk.Frame(janela, bg="#d9d9d9")
frame_botoes.pack(pady=10)

tk.Button(
    frame_botoes,
    text="Cadastrar Produto",
    font=('Arial', 15, 'bold'),
    width=15,
    bg="#0cec2a",
    fg='black',
    command=cadastrar

).grid(row=0, column=0, padx=5)
janela.mainloop()