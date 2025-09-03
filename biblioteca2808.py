from tkinter import *

class Livro:
    def __init__(self, titulo, tema):
        self.titulo = titulo
        self.tema = tema
        self.disponivel = True
        print(f"Livro cadastrado: {self.titulo} | Tema: {self.tema}")

class Membro:
    def __init__(self, nome):
        self.nome = nome
        self.emprestimos = []
        print(f"Membro cadastrado: {self.nome}")

livros = []
membros = []

def cadastrar_livro():
    titulo = entrada_titulo.get()
    tema = entrada_tema.get()
    if titulo and tema:
        novo = Livro(titulo, tema)
        livros.append(novo)
        entrada_titulo.delete(0, END)
        entrada_tema.delete(0, END)
        resultado["text"] = "Livro cadastrado com sucesso!"

def cadastrar_membro():
    nome = entrada_membro.get()
    if nome:
        novo = Membro(nome)
        membros.append(novo)
        entrada_membro.delete(0, END)
        resultado["text"] = "Membro cadastrado com sucesso!"

def emprestar():
    nome = entrada_membro.get()
    titulo = entrada_titulo.get()

    membro = next((m for m in membros if m.nome == nome), None)
    livro = next((l for l in livros if l.titulo == titulo), None)

    if not membro or not livro:
        resultado["text"] = "Erro: livro ou membro não encontrado."
        return

    if not livro.disponivel:
        dono = next((m for m in membros if livro in m.emprestimos), None)
        resultado["text"] = f"Livro já emprestado para {dono.nome}."
        return

    membro.emprestimos.append(livro)
    livro.disponivel = False
    resultado["text"] = f"{nome} emprestou '{titulo}'"

def devolver():
    nome = entrada_membro.get()
    titulo = entrada_titulo.get()
    membro = next((m for m in membros if m.nome == nome), None)
    if membro:
        livro = next((l for l in membro.emprestimos if l.titulo == titulo), None)
        if livro:
            livro.disponivel = True
            membro.emprestimos.remove(livro)
            resultado["text"] = f"{nome} devolveu '{titulo}'"
            return
    resultado["text"] = "Erro: empréstimo não encontrado."

def ver_emprestimos():
    texto = ""
    for m in membros:
        for l in m.emprestimos:
            texto += f"{m.nome} → {l.titulo}\n"
    resultado["text"] = texto or "Nenhum empréstimo registrado."

# Interface gráfica
janela = Tk()
janela.title("Sistema de Biblioteca")

Label(janela, text="Título do Livro").pack()
entrada_titulo = Entry(janela); entrada_titulo.pack()

Label(janela, text="Tema do Livro").pack()
entrada_tema = Entry(janela); entrada_tema.pack()

Label(janela, text="Nome do Membro").pack()
entrada_membro = Entry(janela); entrada_membro.pack()

Button(janela, text="Cadastrar Livro", command=cadastrar_livro).pack()
Button(janela, text="Cadastrar Membro", command=cadastrar_membro).pack()
Button(janela, text="Emprestar Livro", command=emprestar).pack()
Button(janela, text="Devolver Livro", command=devolver).pack()
Button(janela, text="Ver Empréstimos", command=ver_emprestimos).pack()

resultado = Label(janela, text="", justify=LEFT)
resultado.pack()

janela.mainloop()
