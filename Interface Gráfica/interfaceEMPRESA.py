from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno
from contextlib import closing
import sqlite3
from PIL import Image, ImageTk

#funções para alterar a cor do botão ao passar o mouse por cima
def on_enter(e):
    e.widget["bg"]=('white')
    e.widget["fg"]=('black')
def on_leave(e):
    e.widget["bg"]=('#161616')
    e.widget["fg"]=("white")
def on_enter_btsair(e):
    e.widget["bg"]=('white')
    e.widget["fg"]=('#ff0000')
def on_leave_btsair(e):
    e.widget["bg"]=('#161616')
    e.widget["fg"]=("#ff0000")

#mantém informações na tela atualizadas
def exibirlista():
    tree.delete(*tree.get_children())
    tree.place(x=180,y=25)
    label1.place_forget()
    label2.place_forget()
    Matr.place_forget()
    Nome.place_forget()
    btsave.place_forget()
    btreturn.place_forget()
    btalt.place_forget()
    bt2['state'] = NORMAL
    bt3['state'] = NORMAL
    bt4['state'] = NORMAL
    tree.place(x=180,y=25) 
    label3.place(x=300,y=350)
    label4.place(x=300,y=370) 
    tree.place(x=180,y=60) 
    lbl_NN.place_forget()
    Nome.place_forget()
    Valbl.place_forget()
    Val.place_forget()
    bt3.place(x=0,y=190)
    bt4.place(x=0,y=220)
    janela.geometry('660x400')
    texto.place(x=210,y=5)
    btsair.place(x=0,y=370)
    with sqlite3.connect("sqlite.db") as conexão:
            with closing(conexão.cursor()) as cursor:
                cursor.execute('''select * from Sigma''')
                resultado=cursor.fetchall()
                for i in resultado:
                    tree.insert('', END, values=i)

#função de inclusão
def incluir():
     Matr.delete(0, END) 
     Nome.delete(0, END)
     Val.delete(0, END)
     Quant.delete(0, END)
     #esconde imagens, botões e informações desnecessárias
     tree.place_forget() 
     label3.place_forget()
     label4.place_forget()
     texto.place_forget()
     bt3.place_forget() 
     bt4.place_forget() 
     #diminui tamanho da janela
     janela.geometry('660x250')
     btsair.place(x=0,y=220)
     label1.place(x=180,y=25)
     label2.place(x=180,y=50)
     labelval.place(x=180,y=75)
     labelquant.place(x=180,y=100)
     Matr.place(x=390,y=25) 
     Nome.place(x=390,y=50)
     Val.place(x=390,y=75)
     Quant.place(x=390,y=100)
     btsave.place(x=190,y=150)
     btreturn.place(x=340,y=150)

#função de exclusão
def deletar():
    bt2['state'] = DISABLED
    bt4['state'] = DISABLED
    if not tree.focus():
        showinfo(title='ERRO', message='Selecione um item para Exclusão')
        bt2['state'] = NORMAL
        exibirlista()
    else:
        #coletando informações do item selecionado
        item_selecionado = tree.focus()
        rowid = tree.item(item_selecionado)
        Matr_Exc = (rowid["values"][1])
        with sqlite3.connect("sqlite.db") as conexão:
            with closing(conexão.cursor()) as cursor:
                cursor.execute(f'delete from Sigma where Matricula = "{Matr_Exc}"')
                escolha=askyesno(title='confirmation', message='Tem certeza que deseja deletar o item selecionado?')
                if escolha:
                    conexão.commit()
                    tree.delete(item_selecionado)
                    bt2['state'] = NORMAL
                    exibirlista()
                else:
                    conexão.rollback()
                    bt2['state'] = NORMAL
                    exibirlista()

#função de atualizar informações
def atualizar():
     bt2['state'] = DISABLED
     bt3['state'] = DISABLED
     global Matr_Alt
     global Nome_Alt
     global Valor_Alt
     global Quant_Alt
     Nome.delete(0, END)
     Val.delete(0, END)
     Quant.delete(0, END)
     if not tree.focus():
        showinfo(title='ERRO', message='Selecione um item para Alteração')
        exibirlista()
        bt2['state'] = NORMAL
        bt3['state'] = NORMAL
     else:
        #esconde mensagens de rolagem de página e seleção de itens
        label3.place_forget()
        label4.place_forget()
        #aumenta tamanho da tela pra caber novas informações
        janela.geometry("680x450")
        btsair.place(x=0,y=420)
        #desabilita botões inutilizaveis
        bt2['state'] = DISABLED
        bt3['state'] = DISABLED
        #coletando informações do item selecionado
        item_selecionado = tree.focus()
        rowid = tree.item(item_selecionado)
        Matr_Alt = (rowid["values"][1])
        Nome_Alt = (rowid["values"][2])
        Valor_Alt = (rowid["values"][3])
        Quant_Alt = (rowid["values"][4])
        #coloca informações para alteração
        lbl_NN.place(x=180,y=320)
        Nome.insert(1, Nome_Alt) 
        Nome.place(x=180,y=340)
        Val.insert(2, Valor_Alt)
        Valbl.place(x=180,y=360)
        Val.place(x=180,y=380)
        Quant.insert(3, Quant_Alt)
        Qlbl.place(x=180,y=400)
        Quant.place(x=180,y=420)
        btreturn.place(x=450,y=400)
        btalt.place(x=450,y=350)

#função de salvar
def save():
    Matr_Alt=Matr.get()
    Nome_Alt=Nome.get()
    Valor_Alt=Val.get()
    Quant_Alt=Quant.get()
    try:
        Valor_Alt=float(Valor_Alt)
        Quant_Alt=int(Quant_Alt)
    except ValueError:
        showinfo(title='Erro', message='Por favor, insira números válidos para o valor e a quantidade.')
        Val.delete(0, END)
        Quant.delete(0, END)
        return
    Valor_Total_Alt=calcular_valor_total(Valor_Alt, Quant_Alt)
    try:
        with sqlite3.connect("sqlite.db") as conexão:
                with closing(conexão.cursor()) as cursor:
                    cursor.execute('''insert into Sigma (Matricula,Nome_Produto,Valor_Produto,Quantidade,Valor_Total) values (?,?,?,?,?)''',(Matr_Alt,Nome_Alt,float(Valor_Alt),int(Quant_Alt), Valor_Total_Alt))
                    conexão.commit()
                showinfo(title='Atenção', message='Item adicionado')
                exibirlista()
    except sqlite3.IntegrityError:
         showinfo(title='Erro', message='Matrícula ja existente')
         Matr.delete(0, END) 
         Nome.delete(0, END)
         Val.delete(0, END)
         Quant.delete(0, END)

#função de atualizar itens na tabela
def update():
    Nome_Alt=Nome.get()
    Valor_Alt=Val.get()
    Quant_Alt=Quant.get()
    try:
        Valor_Alt=float(Valor_Alt)
        Quant_Alt=int(Quant_Alt)
    except ValueError:
        showinfo(title='Erro', message='Por favor, insira números válidos para o valor e a quantidade.')
        Val.delete(0, END)
        Quant.delete(0, END)
        return
    Valor_Total_Alt=calcular_valor_total(Valor_Alt, Quant_Alt)
    with sqlite3.connect("sqlite.db") as conexão:
                with closing(conexão.cursor()) as cursor:
                    cursor.execute(f'update Sigma set Nome_Produto = "{Nome_Alt}", Valor_Produto = {Valor_Alt}, Quantidade = {Quant_Alt}, Valor_Total = {Valor_Total_Alt} where Matricula = "{Matr_Alt}"')
                    conexão.commit()
    selected_item = tree.selection()[0]
    tree.item(selected_item, text="blub", values=(Matr_Alt,Nome_Alt,Valor_Alt,Quant_Alt,Valor_Total_Alt))
    exibirlista()
    showinfo(title='Atenção', message='Registro Alterado')

#calcula valor total com base nas informações
def calcular_valor_total(valor, quantidade):
    return float(valor) * int(quantidade)

#função de sair do programa
def sair():
   with sqlite3.connect("sqlite.db") as connect:
                escolha=askyesno(title='Atenção', message='Deseja sair do programa?')
                if escolha:
                    janela.destroy()
                else:
                    connect.rollback()
                    bt2['state'] = NORMAL
                    exibirlista

#criando janela e botões
janela = Tk()
janela.title('EAPP ELETRÔNICOS')
janela.geometry('1800x1000')
janela.resizable(False,False)
janela["bg"]=("#4C4C4C")

#texto acima das opções
tit = Label(janela, text="Selecione uma opção")
tit.place(x=0,y=105)
tit["font"]=("Segoe", "10", "bold")
tit["bg"]=("#161616")
tit["fg"]=("white")

#exibição do texto superior
imag2=Image.open("Controle-de-Estoque.bmp")
resize2=imag2.resize((400,50))
img2=ImageTk.PhotoImage(resize2)
texto=Label(image=img2, borderwidth=0, highlightthickness=0)
texto.imag2 = img2
texto.place(x=210,y=5)

#exibição da lista
bt1 = Button(janela, text="Exibir lista", width=15, font=("Segoe", "10", "bold"))
bt1.place(x=0,y=130)
bt1["bg"]=("#161616")
bt1["fg"]=("white")
bt1['command']=exibirlista
bt1.bind("<Enter>", on_enter)
bt1.bind("<Leave>", on_leave)

#incluir
bt2 = Button(janela, text="Incluir item", width=15, font=("Segoe", "10", "bold"))
bt2.place(x=0,y=160)
bt2["bg"]=("#161616")
bt2["fg"]=("white")
bt2['command']=incluir
bt2.bind("<Enter>", on_enter)
bt2.bind("<Leave>", on_leave)

label1=Label(janela, width=25, text ="Entre com a matricula", font=("Segoe", "10", "bold"))
Matr=Entry(janela,width=5)
label2=Label(janela, width=25, text ="Entre com o nome do item", font=("Segoe", "10", "bold"))
Nome =Entry(janela,width=20)
labelval =Label(janela, width=25, text ="Entre com o valor do item", font=("Segoe", "10", "bold"))
Val=Entry(janela, width=10)
labelquant=Label(janela, wid=25, text ="Entre com a quantidade", font=("Segoe", "10", "bold"))
Quant=Entry(janela, width=10)

btsave = Button(janela, text="Salvar", width=15, font=("Segoe", "10", "bold"))
btsave['command']=save
btsave["bg"]=("#161616")
btsave["fg"]=("white")
btsave.bind("<Enter>", on_enter)
btsave.bind("<Leave>", on_leave)

#deletar
bt3 = Button(janela, text="Deletar item", width=15, font=("Segoe", "10", "bold"))
bt3.place(x=0,y=190)
bt3["bg"]=("#161616")
bt3["fg"]=("white")
bt3['command']=deletar
bt3.bind("<Enter>", on_enter)
bt3.bind("<Leave>", on_leave)

#atualizar
bt4 = Button(janela, text="Atualizar item", width=15, font=("Segoe", "10", "bold"))
bt4.place(x=0,y=220)
bt4["bg"]=("#161616")
bt4["fg"]=("white")
bt4['command']=atualizar
bt4.bind("<Enter>", on_enter)
bt4.bind("<Leave>", on_leave)

lbl_NN = Label(janela, text ="Entre com o novo nome")
lbl_NN["bg"]=("#4C4C4C")
lbl_NN["fg"]=("white")

Valbl = Label(janela, text="Entre com o novo valor")
Valbl["bg"]=("#4C4C4C")
Valbl["fg"]=("white")

Qlbl = Label(janela, text="Entre com a quantidade")
Qlbl["bg"]=("#4C4C4C")
Qlbl["fg"]=("white")

btalt = Button(janela, text="Salvar mudanças", width=15, font=("Segoe", "10", "bold"))
btalt["bg"]=("#161616")
btalt["fg"]=("white")
btalt['command']=update
btalt.bind("<Enter>", on_enter)
btalt.bind("<Leave>", on_leave)

#sair
btsair = Button(janela, text="Sair da aplicação",width=15, font=("Segoe", "10", "bold"))
btsair.place(x=0,y=350)
btsair["bg"] = ("#161616")
btsair["fg"] = ("#ff0000")
btsair['command']=sair
btsair.bind("<Enter>", on_enter_btsair)
btsair.bind("<Leave>", on_leave_btsair)

#retornar
btreturn = Button(janela, text="Voltar", width=15, font=("Segoe", "10", "bold"))
btalt["bg"]=("#161616")
btalt["fg"]=("white")
btreturn['command']=exibirlista
btreturn.bind("<Enter>", on_enter)
btreturn.bind("<Leave>", on_leave)

#exibição da tree.view
colunas=("Chave", "Matricula", "Nome", "Valor", "Quantidade", "Valortotal")
tree= ttk.Treeview(janela, columns=colunas, show='headings')
tree.place(x=0, y=0, height=250)
tree.heading('Chave', text='Chave')
tree.heading('Matricula', text='Matrícula')
tree.heading('Nome', text='Nome')
tree.heading('Valor', text='Valor')
tree.heading('Quantidade', text='Quantidade')
tree.heading('Valortotal', text='Valor Total')

tree.column('Chave', width=50)
tree.column('Matricula', width=60)
tree.column('Nome', width=125)
tree.column('Valor', width=75)
tree.column('Quantidade', width=70)
tree.column('Valortotal', width=85)

label3= Label(janela, text= "Role a lista para baixo com o scroll do mouse", font=("Segoe", "10", "bold"))
label3.place(x=300,y=350)
label3["bg"]=("#4C4C4C")
label3["fg"]=("white")

label4 = Label (janela, text = "Selecione o item para alterar ou exlcuir", font=("Segoe", "10", "bold"))
label4.place(x=300,y=370)
label4["bg"]=("#4C4C4C")
label4["fg"]=("white")

exibirlista()

#exibição do logotipo
imagem=Image.open("Vision-OS.bmp")
resize=imagem.resize((150,100))
img=ImageTk.PhotoImage(resize)
logo=Label(image=img, borderwidth=0, highlightthickness=0)
logo.image = img
logo.place(x=0,y=0)

#gerenciador de eventos
janela.mainloop()