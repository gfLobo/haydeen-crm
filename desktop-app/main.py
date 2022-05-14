# IMPORTS
import datetime
from tkinter import *
from tkinter import filedialog
import shutil
import PIL.Image
import requests
import pyrebase
import sqlite3
from sqlite3 import Error
import os

import squarify
from PIL import ImageTk
from matplotlib.ticker import MaxNLocator

y = datetime.datetime.now()
mes_hoje = y.strftime("%m")
ano_hoje = y.strftime("%Y")
dia_hoje = y.strftime("%d")

hora_minuto_segundo = f'{y.strftime("%H")}:{y.strftime("%M")}:{y.strftime("%S")}'
dia_mes_ano = f'{dia_hoje}-{mes_hoje}-{ano_hoje}'
mes_ano = f'{mes_hoje}/{ano_hoje}'
ano_mes_dia_hoje = int(f'{ano_hoje}{y.strftime("%m")}{y.strftime("%d")}')

ano_mes_dia = f'{ano_hoje}{mes_hoje}{dia_hoje}'
##Auth
firebaseConfig = {'apiKey': "YOURKEY",
                  'authDomain': "YOURDOMAIN", 
                  'projectId': "YOURID",
                  'storageBucket': "THESTORAGEBUCKET",
                  'messagingSenderId': "THEMESSAGESENDERID",
                  'appId': "YOURAPPID",
                  'databaseURL': 'YOURURL'}
firebase = pyrebase.initialize_app(firebaseConfig)









import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
storage = firebase.storage()


def abrir():
    #BANCO
    def conexao_db():
        caminho = f'C:\\CRM\\db_crm.db'
        con = None
        try:
            con = sqlite3.connect(caminho)
        except Error as ex:
            print(ex)
        return con

    def dql(query):  # select
        vcon = conexao_db()
        c = vcon.cursor()
        c.execute(query)
        res = c.fetchall()
        return res




    # db_crm
    vcon = conexao_db()



    ##Auth
    firebaseConfig = {'apiKey': "YOURKEY",
                    'authDomain': "YOURDOMAIN", 
                    'projectId': "YOURID",
                    'storageBucket': "THESTORAGEBUCKET",
                    'messagingSenderId': "THEMESSAGESENDERID",
                    'appId': "YOURAPPID",
                    'databaseURL': 'YOURURL'}
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()





















    ############# GUI's: ##############
    def main_crm():
        import requests
        from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
        from matplotlib.figure import Figure
        import matplotlib.patches
        from tkinter import messagebox
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
        import pyautogui
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
        from tkinter import ttk











        #  GUI Main c/ pers#
        #References for firebase
        userAuth = dql('SELECT auth FROM auth')[0][0]
        userToken = dql('SELECT token FROM auth')[0][0]
        yourEmailForSupport = 'myemail@mail.com'

        photoProfileRef = storage.child(f"users/{userAuth}/logo")

        infoMatriz = db.collection('users') \
            .document(f"{userAuth}") \
            .collection('info').document(f'{userAuth}').get()
        progressoRef = db.collection('users') \
            .document(f"{userAuth}") \
            .collection('progresso').document(f'{userAuth}')







        photoProfileRef.download(path="logoUser.png", filename="logoUser.png", token=f"{userToken}")
        try:
            with open('logoUser.png', 'rb') as arquivo:
                logoUSER = arquivo.read()



            vcon.cursor()
            vcon.execute('''REPLACE INTO logo (codigo,imagem)  VALUES (?,?)''', (1, logoUSER))
            vcon.commit()

            os.remove('logoUser.png')
        except:
            pass










        localMatriz = infoMatriz.to_dict()['local']
        nomeMatriz = infoMatriz.to_dict()['matriz']

        if dql("SELECT COUNT(*) FROM perfil")[0][0] != 0:
            UPDATEperfil = f"""UPDATE perfil SET 
                                    nome = '{nomeMatriz}',
                                    email = '{dql('SELECT email FROM auth')[0][0]}',
                                    localself = '{localMatriz}'
                        WHERE codigo = 1"""
        else:
            UPDATEperfil = f"""INSERT INTO perfil  (nome,email,localself)
            
                                VALUES(
                                        '{nomeMatriz}',
                                        '{dql('SELECT email FROM auth')[0][0]}',
                                        '{localMatriz}'
                                )
                                """


        vcon.cursor()
        vcon.execute(UPDATEperfil)
        vcon.commit()





        namecrm = '''SELECT nome FROM perfil WHERE codigo = 1'''
        sqlc = dql(namecrm)
        lista = []
        if len(sqlc) == 0:
            lista.append('⠀')

        else:
            lista.append(sqlc[0][0])

        root = Tk()
        root.title(f'myCrmName  |  CRM - {lista[0]}')
        root.state('zoomed')
        root.resizable(TRUE, TRUE)

        # Fotos Útilitárias
        url = 'myCRMOnlineUrlLogo.png'
        response = requests.get(url, stream=True)
        with open('logo.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

        url_on_btn = 'myCRMOnlineUrlBtnOn.png'
        response1 = requests.get(url_on_btn, stream=True)
        with open('btn_on.png', 'wb') as out_file1:
            shutil.copyfileobj(response1.raw, out_file1)

        url_off_btn = 'myCRMOnlineUrlBtnOff.png'
        response2 = requests.get(url_off_btn, stream=True)
        with open('btn_off.png', 'wb') as out_file2:
            shutil.copyfileobj(response2.raw, out_file2)

        icone_ = PhotoImage(file='logo.png')
        root.iconphoto(False, icone_)

        def refresh():
            root.destroy()
            main_crm()

        # Conjunto de Abas (Notebook)
        abas = ttk.Notebook(root)
        abas.pack()

        ##Frames abas
        home = Frame(abas)
        abas.add(home, text='Home')
        dashs = Frame(abas)
        abas.add(dashs, text='Dashsboards')
        clientes = Frame(abas)
        abas.add(clientes, text='Clientes')
        servicos = Frame(abas)
        abas.add(servicos, text='Serviços')
        mafi = Frame(abas)
        abas.add(mafi, text='Franquias e Filiais')

        ###Grades Abas
        # @home
        grade_lateral_dir = LabelFrame(home)
        grade_lateral_dir.pack(side=RIGHT, fill=Y, expand=FALSE)
        # @dashs
        grade_fat = LabelFrame(dashs)
        grade_fat.pack(side=RIGHT, anchor=N)
        grade_pagmt_grafico = LabelFrame(dashs, text='      💰 Faturamento      ', font='Arial 25', pady=38)
        grade_pagmt_grafico.pack(fill=Y)
        grade_faturamentos = LabelFrame(grade_pagmt_grafico)
        grade_faturamentos.pack(fill=BOTH)
        # @serviços
        grade_servicos_all = LabelFrame(servicos)
        grade_servicos_all.pack(fill=BOTH, expand=TRUE)
        # @clientes
        grade_lateral_dir2 = LabelFrame(clientes)
        grade_lateral_dir2.pack(side=RIGHT)
        grade_lateral_dir1 = LabelFrame(clientes, width=500)
        grade_lateral_dir1.pack(fill=X)
        # @perfil
        graficoall = LabelFrame(mafi)
        graficoall.pack(fill=BOTH)
        info_empresa = LabelFrame(mafi)
        info_empresa.pack(fill=BOTH)

        # Estilo Gráficos
        plt.style.use('ggplot')






















        ####Home
        grade_home_esq = LabelFrame(home)
        grade_home_esq.pack(fill=X)

        # Cadastro de Cargos
        grade_cadastro_cargos = LabelFrame(grade_home_esq,
                                           text="                                                                              👔 Cargos                                                                                     ",
                                           font="Arial 20",
                                           pady=18)
        grade_cadastro_cargos.pack(fill=X)
        # codigo, foto, nome, cargo, filial, email, telefone
        lb_codigo_cargo = Label(grade_cadastro_cargos, text="Código", font="Arial 16")
        lb_codigo_cargo.grid(row=0, column=0)
        txt_codigo_cargo = Entry(grade_cadastro_cargos, font="Arial 16", width=10)
        txt_codigo_cargo.grid(row=1, column=0)

        lb_nome_cargo = Label(grade_cadastro_cargos, text="Nome", font="Arial 16")
        lb_nome_cargo.grid(row=0, column=1, sticky=W + E)
        txt_nome_cargo = Entry(grade_cadastro_cargos, font="Arial 16", width=50)
        txt_nome_cargo.grid(row=1, column=1)

        vsql_cargo = '''SELECT DISTINCT(cargo) FROM cargos'''
        linhas_cargo = dql(vsql_cargo)
        lista_cargo = []
        for r in linhas_cargo:
            lista_cargo.append(r[0])

        lb_cargo_cargo = Label(grade_cadastro_cargos, text="Cargo", font="Arial 16")
        lb_cargo_cargo.grid(row=0, column=2)
        txt_cargo_cargo = ttk.Combobox(grade_cadastro_cargos, values=lista_cargo, font="Arial 16", width=30)
        txt_cargo_cargo.grid(row=1, column=2)

        lista_perfil = []

        def populador_local_mf():
            lista_perfil.clear()
            for r in dql('''SELECT codigo ||+" - "|| nome ||+"      ¬ "|| localself FROM perfil'''):
                lista_perfil.append(r[0])

        populador_local_mf()

        lb_lotacao_cargo = Label(grade_cadastro_cargos, text="Lotação", font="Arial 16")
        lb_lotacao_cargo.grid(row=2, column=0, columnspan=2, sticky=W + E)
        txt_lotacao_cargo = ttk.Combobox(grade_cadastro_cargos, values=lista_perfil, font="Arial 16")
        txt_lotacao_cargo.grid(row=3, column=0, columnspan=2, sticky=W + E)

        lb_email_cargo = Label(grade_cadastro_cargos, text="E-mail", font="Arial 16")
        lb_email_cargo.grid(row=2, column=2)
        txt_email_cargo = Entry(grade_cadastro_cargos, font="Arial 16", width=20)
        txt_email_cargo.grid(row=3, column=2, sticky=W + E)

        lb_tel_cargo = Label(grade_cadastro_cargos, text="Telefone", font="Arial 16")
        lb_tel_cargo.grid(row=4, column=2)
        txt_tel_cargo = Entry(grade_cadastro_cargos, font="Arial 16", width=20)
        txt_tel_cargo.grid(row=5, column=2, sticky=W + E)
        # =-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-

        # Treeview Cargos
        lbframe_cargos = LabelFrame(grade_home_esq)
        lbframe_cargos.pack(fill=BOTH)
        tv_cargos = ttk.Treeview(lbframe_cargos,
                                 columns=('codigo', 'nome', 'cargo', 'filial', 'email', 'telefone'),
                                 show='headings', height=12)
        tv_cargos.column('codigo', anchor=CENTER, width=0)
        tv_cargos.column('nome', anchor=CENTER, width=250)
        tv_cargos.column('cargo', anchor=CENTER, width=150)
        tv_cargos.column('filial', anchor=CENTER, width=250)
        tv_cargos.column('email', anchor=CENTER, width=150)
        tv_cargos.column('telefone', anchor=CENTER, width=50)

        tv_cargos.heading('codigo', text='ID', anchor=CENTER)
        tv_cargos.heading('nome', text='Nome', anchor=CENTER)
        tv_cargos.heading('cargo', text='Cargo', anchor=CENTER)
        tv_cargos.heading('filial', text='Lotação', anchor=CENTER)
        tv_cargos.heading('email', text='E-mail', anchor=CENTER)
        tv_cargos.heading('telefone', text='Telefone', anchor=CENTER)

        def mostra_todoscargos():

            tv_cargos.delete(*tv_cargos.get_children())
            db_queryperf = 'SELECT * FROM cargos'
            linhasperf = dql(db_queryperf)
            for yyyyyyyy in linhasperf:
                tv_cargos.insert('', 'end', values=(yyyyyyyy))
            lista_cargo.clear()
            for r in dql('''SELECT DISTINCT(cargo) FROM cargos'''):
                lista_cargo.append(r[0])
            txt_cargo_cargo.configure(values=lista_cargo)

        mostra_todoscargos()

        # Barra de rolagem
        vsb_cargos = ttk.Scrollbar(lbframe_cargos, orient='vertical')
        vsb_cargos.config(command=tv_cargos.yview)
        tv_cargos.configure(yscrollcommand=vsb_cargos.set)
        vsb_cargos.pack(side=RIGHT, fill=Y)
        tv_cargos.pack(fill=BOTH)

        # botoes query.
        def pdf_cargos():
            if len(txt_cargo_cargo.get()) == 0 and len(txt_lotacao_cargo.get()) == 0:
                Nome_relatorio = 'Todos os Cargos'
                x = dql('''SELECT 
                                            codigo,
                                            nome,
                                            cargo,
                                            filial,
                                            email,
                                            telefone
                                        FROM cargos''')
            elif len(txt_cargo_cargo.get()) != 0:
                Nome_relatorio = f'Cargo ¬ {txt_cargo_cargo.get()}'
                x = dql(f'''SELECT 
                                                                    codigo,
                                                                    nome,
                                                                    cargo,
                                                                    filial,
                                                                    email,
                                                                    telefone
                                         FROM cargos WHERE cargo = "{txt_cargo_cargo.get()}"''')
            else:
                Nome_relatorio = f'Cargos ¬ {txt_lotacao_cargo.get()}'
                x = dql(f'''SELECT 
                                                                                            codigo,
                                                                                            nome,
                                                                                            cargo,
                                                                                            filial,
                                                                                            email,
                                                                                            telefone
                                                                 FROM cargos WHERE filial = "{txt_lotacao_cargo.get()}"''')
            y = datetime.datetime.now()
            mes_hoje = y.strftime("%m")
            ano_hoje = y.strftime("%Y")
            dia_hoje = y.strftime("%d")

            hora_minuto_segundo = f'{y.strftime("%H")}:{y.strftime("%M")}:{y.strftime("%S")}'
            dia_mes_ano = f'{dia_hoje}-{mes_hoje}-{ano_hoje}'
            mes_ano = f'{mes_hoje}/{ano_hoje}'

            doc = SimpleDocTemplate(
                f'C:\\Users\\{os.getlogin()}\\Downloads\\{dia_mes_ano}  ¬Relatorio_{Nome_relatorio}.pdf',
                pagesize=letter)
            data = [['ID', 'NOME', 'CARGO', 'LOTAÇÃO', 'E-MAIL', 'TELEFONE']]  # give data as lists with lists.

            select_query = x

            for i in select_query:
                data.append(i)
            table = Table(data)

            tabla_style = TableStyle([
                ('BACKGROUND', (0, 0), (5, 0), colors.darkcyan),
                ('BACKGROUND', (0, 0), (0, 0), colors.darkblue),
                ('BACKGROUND', (0, 1), (0, len(data)), colors.gray),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('TEXTCOLOR', (0, 1), (0, len(data)), colors.white),
                ('TEXTCOLOR', (0, 0), (5, 0), colors.white),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
            table.setStyle(tabla_style)
            styleSheet = getSampleStyleSheet()

            titulo = Paragraph(f'Relatório de {Nome_relatorio}  ¬ {mes_ano}', style=styleSheet['Heading1'])
            emptyline = Paragraph(f'       ', style=styleSheet['Heading1'])

            infodoc = Paragraph(f'''Documento gerado às: {hora_minuto_segundo}''',
                                style=styleSheet['Normal'])

            doc_lenth = Paragraph(f'''Total de {Nome_relatorio} = {len(x)}''',
                                  style=styleSheet['Normal'])
            contato_dev = Paragraph(
                f'>>>  Algo errado? Reporte através do e-mail: {yourEmailForSupport}',
                style=styleSheet['Normal'])

            doc.build(
                [titulo, emptyline, emptyline, emptyline, emptyline, table, infodoc,
                 emptyline, emptyline, doc_lenth, emptyline, contato_dev])
            os.startfile(
                f'C:\\Users\\{os.getlogin()}\\Downloads\\{dia_mes_ano}  ¬Relatorio_{Nome_relatorio}.pdf')

        def dml_cargos():
            if len(txt_codigo_cargo.get()) != 0 and len(txt_nome_cargo.get()) != 0 and len(
                    txt_cargo_cargo.get()) != 0 and len(txt_lotacao_cargo.get()) != 0:
                query = f'''INSERT OR REPLACE INTO cargos (codigo,nome,cargo,filial,email,telefone) 
                                        VALUES ({txt_codigo_cargo.get()}, "{str(txt_nome_cargo.get())}",
                                                "{str(txt_cargo_cargo.get())}","{str(txt_lotacao_cargo.get())}",
                                                "{str(txt_email_cargo.get())}","{txt_tel_cargo.get()}")'''
                vcon.cursor()
                vcon.execute(query)
                vcon.commit()
                mostra_todoscargos()

                txt_codigo_cargo.delete(0, END)
                txt_nome_cargo.delete(0, END)
                txt_cargo_cargo.delete(0, END)
                txt_lotacao_cargo.delete(0, END)
                txt_email_cargo.delete(0, END)
                txt_tel_cargo.delete(0, END)

            else:
                messagebox.showinfo(title='Erro', message='Preencha todos os campos')
            mostra_todoscargos()

        def deleta_todos_cargos():
            query = f'''DELETE FROM cargos'''
            vcon.cursor()
            try:
                confirm = messagebox.askyesno(title='Deletando cargos',
                                              message='Deseja realmente remover TODOS os registros de cargos?')
                if confirm == 1:
                    vcon.execute(query)
                    vcon.commit()
                    mostra_todoscargos()
                else:
                    pass
            except:
                messagebox.showinfo(title='Erro', message=f'Algo de errado aconteceu')

        def search_cargos():
            tv_cargos.delete(*tv_cargos.get_children())
            try:
                if len(txt_codigo_cargo.get()) != 0:
                    vcon.cursor()
                    db_query2 = vcon.execute(
                        f'''SELECT * FROM cargos WHERE  codigo = {txt_codigo_cargo.get()}''')
                    vcon.commit()
                    linhas = db_query2
                    for i in linhas:
                        tv_cargos.insert('', 'end', values=(i))
                elif len(txt_nome_cargo.get()) != 0:
                    vcon.cursor()
                    db_query2 = vcon.execute(
                        f'''SELECT * FROM cargos WHERE  nome like "{txt_codigo_cargo.get()}%"''')
                    vcon.commit()
                    linhas = db_query2
                    for i in linhas:
                        tv_cargos.insert('', 'end', values=(i))
                elif len(txt_cargo_cargo.get()) != 0:
                    vcon.cursor()
                    db_query2 = vcon.execute(
                        f'''SELECT * FROM cargos WHERE cargo like "{txt_cargo_cargo.get()}%"''')
                    vcon.commit()
                    linhas = db_query2
                    for i in linhas:
                        tv_cargos.insert('', 'end', values=(i))
                elif len(txt_lotacao_cargo.get()) != 0:
                    vcon.cursor()
                    db_query2 = vcon.execute(
                        f'''SELECT * FROM cargos WHERE filial like "{txt_lotacao_cargo.get()}%"''')
                    vcon.commit()
                    linhas = db_query2
                    for i in linhas:
                        tv_cargos.insert('', 'end', values=(i))

                else:
                    messagebox.showinfo(title='Erro', message='Preencha pelo menos um campo')


            except:
                messagebox.showerror(title=f'Erro',
                                     message=f'Oops! Não encontramos nenhum cargo com esse registro 😕')

        def delete_cargos():
            if len(txt_codigo_cargo.get()) != 0:
                try:
                    vcon.cursor()
                    confirm = messagebox.askyesno(title='Deletando um cargo',
                                                  message=f'Deseja realmente remover o cargo de ID:{txt_codigo_cargo.get()}?')
                    if confirm == 1:
                        vcon.execute(f'''DELETE FROM cargos WHERE codigo={txt_codigo_cargo}''')
                        vcon.commit()
                        messagebox.showinfo(message='Cargo deletado com sucesso')
                        mostra_todoscargos()
                    else:
                        pass
                except Error as er:
                    messagebox.showinfo(title='Erro', message=f'Algo de errado aconteceu\n Tipo: {str(er)}')


            elif len(txt_lotacao_cargo.get()) != 0:
                try:
                    vcon.cursor()
                    confirm = messagebox.askyesno(title='Deletando cargos',
                                                  message=f'Deseja realmente remover todos os cargos da lotação {txt_lotacao_cargo.get()}?')
                    if confirm == 1:
                        vcon.execute(f'''DELETE FROM cargos WHERE filial="{txt_codigo_cargo}"''')
                        vcon.commit()
                        messagebox.showinfo(message='Cargo(s) deletado(s) com sucesso')
                        mostra_todoscargos()
                    else:
                        pass
                except Error as er:
                    messagebox.showinfo(title='Erro', message=f'Algo de errado aconteceu\n Tipo: {str(er)}')
            else:
                messagebox.showinfo(title='Erro',
                                    message='Digite o código identificados ou a lotação que deseja remover')

        btn_n_cargo = Button(grade_cadastro_cargos, text='➕', command=dml_cargos, bg='#a4d49a', font='Arial 12')
        btn_n_cargo.grid(row=0, column=4)
        btn_search_cargo = Button(grade_cadastro_cargos, text='🔎', command=search_cargos, bg='#bbd3ff',
                                  font='Arial 12')
        btn_search_cargo.grid(row=1, column=4, sticky=W + E + N + S)

        btn_deletar_cargo = Button(grade_cadastro_cargos, text='⛔', command=delete_cargos, bg='#ff9774',
                                   font='Arial 12')
        btn_deletar_cargo.grid(row=0, column=5)
        btn_mostra_tudo_cargos = Button(grade_cadastro_cargos, text="🌎", command=mostra_todoscargos,
                                        bg='#bbd3ff',
                                        font='Arial 12')
        btn_mostra_tudo_cargos.grid(row=1, column=5, sticky=W + E + N + S)
        btn_deleta_tudo_cargo = Button(grade_cadastro_cargos, text='Deletar Todos', command=deleta_todos_cargos,
                                       bg='#ff9774',
                                       font='Arial 12', width=12)
        btn_deleta_tudo_cargo.grid(row=0, column=6)
        btn_cargos_pdf = Button(grade_cadastro_cargos, text='PDF 💾', command=pdf_cargos, bg='#ffa31a',
                                font='Arial 12', width=12)
        btn_cargos_pdf.grid(row=1, column=6, sticky=W + E + N + S)

        # @ Gráficos
        anomf = []
        qtdmf = []

        anocli = []
        qtdcli = []

        def grafico_diag():
            vcon.cursor()
            vcon.execute(f'''UPDATE tasks SET 
                                                                clientes = {dql(f"""SELECT COUNT(DISTINCT clienteid) FROM compras 
                                                                                        WHERE status == 'Acompanhamento' OR status =='Execução'   
                                                                                            AND (registro_mes_ano NOT NULL 
                                                                                            OR _notif_mesano NOT NULL 
                                                                                            OR _notif_dia NOT NULL 
                                                                                            OR _notif_sem NOT NULL)""")[0][0]},
                                                                perfis = {dql(f"""SELECT COUNT(DISTINCT localself) FROM perfil """)[0][0]}
                                                            WHERE codigo ={dql("""SELECT COUNT(*) FROM tasks""")[0][0]}''')
            vcon.commit()
            dados = dql(
                f'''SELECT ano,clientes,perfis FROM tasks WHERE  ano BETWEEN {int(ano_hoje) - 4}  AND {ano_hoje} AND ano NOT NULL''')
            for x in dados:
                anomf.append(x[0])
                anocli.append(x[0])

                qtdmf.append(x[2])
                qtdcli.append(x[1])

        grafico_diag()

        def grafico_diag_rplc():
            anocli.clear()
            qtdcli.clear()
            anomf.clear()
            qtdmf.clear()

            axs2.clear()
            axs.clear()
            grafico_diag()
            axs.fill_between(anomf, qtdmf)
            axs.xaxis.set_major_locator(MaxNLocator(integer=True))
            axs.yaxis.set_major_locator(MaxNLocator(integer=True))
            canvas_hist.draw()
            axs2.fill_between(anocli, qtdcli)
            axs2.xaxis.set_major_locator(MaxNLocator(integer=True))
            axs2.yaxis.set_major_locator(MaxNLocator(integer=True))
            canvas_hist2.draw()

        # Filiais ao ano
        grade_hist_all = LabelFrame(grade_home_esq, text="  📊 Gráficos   ",
                                    font="Arial 20")
        grade_hist_all.pack(fill=X)
        grade_hist_mf = LabelFrame(grade_hist_all, width=1000)
        grade_hist_mf.grid(row=0, column=0, sticky=W + E)

        figura_mf_cl_anual = plt.Figure(figsize=(7.3, 3), dpi=95)
        axs = figura_mf_cl_anual.add_subplot(111)
        canvas_hist = FigureCanvasTkAgg(figura_mf_cl_anual, grade_hist_mf)
        canvas_hist.draw()
        canvas_hist.get_tk_widget().pack(fill=X)

        axs.fill_between(anomf, qtdmf)
        axs.xaxis.set_major_locator(MaxNLocator(integer=True))
        axs.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.ylabel("Alcance de Municípios")
        plt.xlabel("Linha do Tempo")
        figura_mf_cl_anual.suptitle(f'Expansão Empresarial')
        figura_mf_cl_anual.subplots_adjust(left=0.1, bottom=0.079, right=0.987, top=0.905)

        toolbarA = NavigationToolbar2Tk(canvas_hist, grade_hist_mf, pack_toolbar=True)
        toolbarA.update()

        # Clientes Ativos ao ano
        grade_hist_cl = LabelFrame(grade_hist_all, width=1000)
        grade_hist_cl.grid(row=0, column=1, sticky=W + E)

        figura_cl_anual = plt.Figure(figsize=(7.3, 3), dpi=95)
        axs2 = figura_cl_anual.add_subplot(111)
        canvas_hist2 = FigureCanvasTkAgg(figura_cl_anual, grade_hist_cl)
        canvas_hist2.draw()
        canvas_hist2.get_tk_widget().pack(fill=X)

        axs2.fill_between(anocli, qtdcli)
        axs2.xaxis.set_major_locator(MaxNLocator(integer=True))
        axs2.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.ylabel("Serviços em Andamento")
        plt.xlabel("Linha do Tempo")
        figura_cl_anual.suptitle(f'Clientes Ativos')
        figura_cl_anual.subplots_adjust(left=0.1, bottom=0.079, right=0.988, top=0.905)

        toolbarB = NavigationToolbar2Tk(canvas_hist2, grade_hist_cl, pack_toolbar=True)
        toolbarB.update()
        # -=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        # Grade direita
        if len(dql('''SELECT imagem FROM logo''')[0][0]) > 0:
            imgd = ImageTk.PhotoImage(data=dql('''SELECT imagem FROM logo''')[0][0])
            panel = Label(grade_lateral_dir, image=imgd, height=250, width=480)
            panel.image = imgd
            panel.pack()




        # File dialog to select files
        def filedialogs():
            global get_image
            get_image = filedialog.askopenfilenames(title="Selecione sua Logo",
                                                    filetypes=(
                                                        ("png", "*.png"), ("jpg", "*.jpg")))

            # Image need to be conver into binary before insert into database
            def conver_image_into_binary(filename):
                with open(filename, 'rb') as file:
                    photo_image = file.read()
                return photo_image

            def insert_image():
                vcon.cursor()

                for image in get_image:
                    insert_photo = conver_image_into_binary(image)

                    vcon.execute('INSERT OR REPLACE INTO logo (imagem,codigo) Values(:image,1)',
                                 {'image': insert_photo})

            insert_image()
            vcon.commit()





            refresh()

        grade_logo = LabelFrame(grade_lateral_dir)
        grade_logo.pack(fill=X)

        # select_image = Button(grade_logo, text="📸 Upload Logo", command=filedialogs, font='arial 15 bold ',
        #                       bg='#80ccff')
        # select_image.pack(fill=X)

        def pegar_cotacoes():
            import time
            time.sleep(0.1)
            requisicao = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL")

            requisicao_dic = requisicao.json()

            cotacao_dolar = requisicao_dic['USDBRL']['bid']
            cotacao_euro = requisicao_dic['EURBRL']['bid']
            cotacao_btc = requisicao_dic['BTCBRL']['bid']

            texto = f'''Dólar: {cotacao_dolar}    Euro: {cotacao_euro}\n\nBTC: {cotacao_btc}'''

            textocotacoes['text'] = texto

        ##Frame com cotações
        afastadela = LabelFrame(grade_lateral_dir, pady=40)
        afastadela.pack(fill=X)
        framecot = LabelFrame(afastadela, text='                        💲 Cotações                           ',
                              font='arial 18 bold')
        framecot.pack(side=BOTTOM)
        # texto
        texto = Label(framecot, text='Clique para obter a cotação atualizada', font='arial 12', anchor=CENTER)
        texto.pack(pady=20)
        # botão
        btn = Button(framecot, text='Atualizar 🔄', command=pegar_cotacoes, anchor=CENTER, font='arial 15 bold',
                     bg='#80ccff')
        btn.pack()
        # textocotações
        textocotacoes = Label(framecot, text='', font='Futura 20 bold', anchor=CENTER, pady=10)
        textocotacoes.pack()

        on_image_btn = PhotoImage(file='btn_on.png')
        of_image_btn = PhotoImage(file='btn_off.png')
        agenda = dql('''SELECT emails_compras,
                        emails_relatorios,fds_off FROM tasks WHERE codigo=1''')
        if agenda[0][0] == 0:
            estado = of_image_btn

        else:
            estado = on_image_btn

        if agenda[0][1] == 0:
            estado2 = of_image_btn

        else:
            estado2 = on_image_btn

        if agenda[0][2] == 1:
            estado3 = on_image_btn
        else:
            estado3 = of_image_btn

        def switch_notif_relatorios():
            agenda = dql('''SELECT emails_compras,
                                            emails_relatorios FROM tasks WHERE codigo=1''')
            if agenda[0][0] == 0:
                btn_pgmts_notif.config(image=on_image_btn)
                vcon.cursor()
                vcon.execute('''UPDATE tasks SET emails_compras=1 WHERE codigo=1''')
                vcon.commit()
            else:
                btn_pgmts_notif.config(image=of_image_btn)
                vcon.cursor()
                vcon.execute('''UPDATE tasks SET emails_compras=0 WHERE codigo=1''')
                vcon.commit()

        def switch_notif_diag():
            agenda = dql('''SELECT emails_compras,
                                            emails_relatorios FROM tasks WHERE codigo=1''')
            if agenda[0][1] == 0:
                btn_diag_notif.config(image=on_image_btn)
                vcon.cursor()
                vcon.execute('''UPDATE tasks SET emails_relatorios=1 WHERE codigo=1''')
                vcon.commit()

            else:
                btn_diag_notif.config(image=of_image_btn)
                vcon.cursor()
                vcon.execute('''UPDATE tasks SET emails_relatorios=0 WHERE codigo=1''')
                vcon.commit()

        def switch_fds_off():
            if dql("SELECT fds_off FROM tasks")[0][0] == 1:
                vcon.cursor()
                vcon.execute("""UPDATE tasks SET fds_off=0 WHERE codigo=1""")
                vcon.commit()
                btn_fds_notif.config(image=of_image_btn)
            else:
                vcon.cursor()
                vcon.execute("""UPDATE tasks SET fds_off=1 WHERE codigo=1""")
                vcon.commit()
                btn_fds_notif.config(image=on_image_btn)

        # Notificações
        fr_btn_notif = LabelFrame(grade_lateral_dir)
        fr_btn_notif.pack(fill=BOTH)

        lb_notificacoes = Label(fr_btn_notif, text='                     🔔 Notificações                ',
                                font='arial 18 bold', pady=35)
        lb_notificacoes.grid(row=0, column=0, columnspan=2, sticky=W + E)
        lb_s_relatorios = Label(fr_btn_notif, text='Relatórios de Pagamento                                        ',
                                font='Futura  13 ',
                                height=2)
        lb_s_relatorios.grid(row=1, column=0)
        btn_pgmts_notif = Button(fr_btn_notif, image=estado, command=switch_notif_relatorios, bd=0)
        btn_pgmts_notif.grid(row=1, column=1, sticky=W + E)
        lb_s_diag = Label(fr_btn_notif, text='Diagnósticos Anuais                 ', font='Futura  13 ', height=2)
        lb_s_diag.grid(row=2, column=0, sticky=W)
        btn_diag_notif = Button(fr_btn_notif, image=estado2, command=switch_notif_diag, bd=0, height=30)
        btn_diag_notif.grid(row=2, column=1, sticky=W + E)
        lb_fds = Label(fr_btn_notif, text='Fim de semana OFF                 ', font='Futura  13 ', height=2)
        lb_fds.grid(row=3, column=0, sticky=W)
        btn_fds_notif = Button(fr_btn_notif, image=estado3, command=switch_fds_off, bd=0, height=30)
        btn_fds_notif.grid(row=3, column=1, sticky=W + E)
        lb_explicacao = Label(fr_btn_notif, text='''➡ Avisos no e-mail cadastrado na matriz.''', height=3)
        lb_explicacao.grid(row=4, column=0, columnspan=2, sticky=W + E + S)












































































        #####Dashs
        figura_montante = plt.Figure(figsize=(20, 4.5), dpi=(100))
        ax_mont = figura_montante.add_subplot(111)
        canva_mont = FigureCanvasTkAgg(figura_montante, grade_faturamentos)
        canva_mont.get_tk_widget().pack(fill=BOTH, expand=TRUE)

        toolbar_mont = NavigationToolbar2Tk(canva_mont, grade_faturamentos, pack_toolbar=True)
        toolbar_mont.update()

        meses_mont = ["Jan", 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                      'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        values_mont = []

        def dados_mont():
            for i in dql('''SELECT 
                                            janeiro,
                                            fevereiro,
                                            marco,
                                            abril,
                                            maio,
                                            junho,
                                            julho,
                                            agosto,
                                            setembro,
                                            outubro,
                                            novembro,
                                            dezembro
                                    FROM tasks WHERE codigo=(SELECT COUNT(*)FROM tasks)''')[0]:
                values_mont.append(i)

        dados_mont()

        ax_mont.plot(meses_mont, values_mont)
        figura_montante.suptitle(f'{ano_hoje} ¬   Total = R$ {sum(values_mont)}')
        figura_montante.subplots_adjust(left=0.086, bottom=0.067, right=0.988, top=0.93)
        if dql("""SELECT COUNT(*) FROM tasks""")[0][0] > 5:
            var_scala = dql("""SELECT COUNT(*) FROM tasks""")[0][0] - 4
        else:
            var_scala = 2

        global _desligar_foco
        _desligar_foco = True

        def change_foco():
            global _desligar_foco
            if _desligar_foco:
                btn_fat.config(image=on_image_btn)
                _desligar_foco = False

                ax_mont.clear()
                ax_mont.plot(meses_mont, values_mont)
                ax_mont.legend(labels=(f'{ano_hoje}', f'{scale_mont.get()}'), ncol=2)

                canva_mont.draw()
            else:
                btn_fat.config(image=of_image_btn)
                _desligar_foco = True

                ax_mont.clear()
                ax_mont.plot(meses_mont, values_mont)
                ax_mont.legend(labels=(f'{ano_hoje}', f'{scale_mont.get()}'), ncol=2)

                canva_mont.draw()

        def scala_fat_cmd(values):
            if _desligar_foco or scale_mont.get() == int(ano_hoje):
                ax_mont.clear()
                ax_mont.plot(meses_mont, values_mont)
                ax_mont.legend(labels=(f'{ano_hoje}', f'{scale_mont.get()}'), ncol=2)

                canva_mont.draw()

            else:
                lista_novo_ano = []
                for i in dql(f'''SELECT 
                                            janeiro,
                                            fevereiro,
                                            marco,
                                            abril,
                                            maio,
                                            junho,
                                            julho,
                                            agosto,
                                            setembro,
                                            outubro,
                                            novembro,
                                            dezembro
                                    FROM tasks WHERE ano={int(scale_mont.get())}''')[0]:
                    lista_novo_ano.append(i)

                ax_mont.clear()
                ax_mont.plot(meses_mont, values_mont)
                ax_mont.plot(meses_mont, lista_novo_ano)
                ax_mont.legend(labels=(f'{ano_hoje}', f'{scale_mont.get()}'), ncol=2)
                canva_mont.draw()
                lista_novo_ano.clear()

        scale_mont = Scale(dashs,
                           from_=dql(f"""SELECT ano FROM tasks WHERE codigo = {var_scala} """)[0][0],
                           to=int(ano_hoje),
                           orient=HORIZONTAL, troughcolor='#ffffff', command=scala_fat_cmd
                           )
        scale_mont.set(int(ano_hoje))

        scale_mont.place(x=800, y=25, width=250)
        ax_mont.legend(labels=(f'{ano_hoje}', f'{scale_mont.get()}'), ncol=2)

        btn_fat = Button(dashs, image=of_image_btn, command=change_foco, bd=0, height=30)
        btn_fat.place(x=1070, y=43)

        square_display = LabelFrame(grade_fat, height=100, width=0)
        inactiveCustomers= dql(f'''SELECT COUNT(*) FROM compras WHERE status = "Apresentação"  or status = "Planejamento"''')[0][
            0]
        activeCustomers = \
            dql(f'''SELECT COUNT(*) FROM compras WHERE status = "Execução" or status = "Acompanhamento" ''')[
                0][0]

        figura_quadro_Serv = plt.Figure(figsize=(15, 8.8), dpi=(50))
        axQ = figura_quadro_Serv.add_subplot(111)
        canvaQ = FigureCanvasTkAgg(figura_quadro_Serv, square_display)

        figura_quadro_Serv.subplots_adjust(left=0, bottom=0, right=1, top=1)

        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        circleQ = matplotlib.patches.Circle((0, 0), 0.80, color='white')

        sizes = inactiveCustomers, activeCustomers, (inactiveCustomers + activeCustomers)
        colors_serv = ['chocolate', 'dodgerblue', 'white']

        axQ.pie(sizes, labels=(f"{inactiveCustomers} Planejamento\nou Apresentação", f"{activeCustomers} Andamento", "")
                , colors=colors_serv, textprops={'size': '26'})

        axQ.add_artist(circleQ)
        axQ.annotate(f"Aproveitamento\n     {(activeCustomers / (inactiveCustomers+activeCustomers)) * 100:.0f}%",
                     xy=(0, 0), fontsize=26, ha="center")
        canvaQ.draw()
        canvaQ.get_tk_widget().pack(fill=BOTH, expand=FALSE)
        square_display.pack(side=RIGHT, fill=BOTH, expand=FALSE)

        servicos = []
        serv_equal = []
        tamanho_serv = []

        def t_plot():
            servicos.clear()
            serv_equal.clear()
            tamanho_serv.clear()
            servicos_query_same = dql('''SELECT servicosid FROM compras WHERE status != "Apresentação"''')
            servicos_query_unic = dql('''SELECT DISTINCT servicosid FROM compras WHERE status != "Apresentação"''')

            for x in servicos_query_unic:
                servicos.append(x[0])

            for x in servicos_query_same:
                serv_equal.append(x[0])

            for x in servicos_query_unic:
                tamanho_serv.append(serv_equal.count(f'{x[0]}'))

        t_plot()

        figt_map, axs3 = plt.subplots(1)
        squarify.plot(sizes=tamanho_serv, label=servicos, alpha=0.5)
        plt.axis('off')

        figt_map.suptitle(f'Serviços Ativos')
        figt_map.subplots_adjust(left=0.053, bottom=0.070, right=0.987, top=0.905)
        plt.style.use('default')
        plt.savefig(fname=f'{ano_hoje} - Serviços.png', dpi=130)
        imgd_treemap = ImageTk.PhotoImage(PIL.Image.open(f'{ano_hoje} - Serviços.png'))
        panel_tmap = Label(dashs, image=imgd_treemap, height=650, width=770)
        panel_tmap.image = imgd_treemap
        panel_tmap.place(x=1155, y=270)
        os.remove(f'{ano_hoje} - Serviços.png')

        import pandas as pd
        import numpy as np
        lista_pgmnts = []

        def pgmt_():
            lista_pgmnts.clear()
            for i in dql('''SELECT pagamento FROM compras WHERE status != "Concluído"'''):
                lista_pgmnts.append(i[0])

        pgmt_()
        fig_pgmt = plt.Figure(figsize=(0, 3.37))
        fig_pgmt.subplots_adjust(left=0, bottom=0.067, right=0.996, top=1)
        plt.style.use('ggplot')

        df = pd.DataFrame({'Mensal': [lista_pgmnts.count('Mensal')], 'Semanal': [lista_pgmnts.count('Semanal')]})
        df2 = pd.DataFrame({'Anual': [lista_pgmnts.count('Anual')], 'Diário': [lista_pgmnts.count('Diário')]})

        gs = fig_pgmt.add_gridspec(2, 1, hspace=0.2)

        ax_pgmt = fig_pgmt.add_subplot(gs[0, 0])
        ax_pgmt2 = fig_pgmt.add_subplot(gs[1, 0])

        df.plot.barh(stacked=True, ax=ax_pgmt, edgecolor='white')
        df2.plot.barh(stacked=True, ax=ax_pgmt2, edgecolor='white')

        fig_pgmt.subplots_adjust(left=0.05, right=1, top=1)

        ax_pgmt.legend(ncol=2)
        ax_pgmt2.legend(ncol=2)
        ax_pgmt.set_yticks([])
        ax_pgmt2.set_yticks([])

        ax_pgmt2.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax_pgmt.xaxis.set_major_locator(MaxNLocator(integer=True))

        canva_pgmt = FigureCanvasTkAgg(fig_pgmt, grade_pagmt_grafico)
        canva_pgmt.get_tk_widget().pack(fill=BOTH, expand=TRUE)








































        ####Serviços
        grade_serv = LabelFrame(grade_servicos_all)
        grade_serv.pack(fill=BOTH, expand=TRUE)

        # @cadastro_serv

        lista_tipo = []
        lista_clientes = []
        lista_setor = []

        # @populadores
        def populando_servicos():
            lista_tipo.clear()
            lista_clientes.clear()
            lista_setor.clear()
            for r in dql('''SELECT tipo FROM servicos'''):
                lista_tipo.append(r[0])

            for r in dql('''SELECT setor FROM servicos'''):
                lista_setor.append(r[0])

            for r in dql('''SELECT codigo ||+" - "|| nome ||+"      ¬ "|| local FROM clientes'''):
                lista_clientes.append(r[0])





            concl = dql("""SELECT COUNT(clienteid) 
                                        FROM compras WHERE status == "Concluído"
                                        AND (registro_mes_ano NOT NULL OR
                                        _notif_mesano NOT NULL OR
                                        _notif_dia NOT NULL OR
                                        _notif_sem NOT NULL)""")[0][0]
            execu = dql("""SELECT COUNT(clienteid) 
                                        FROM compras WHERE status == "Execução"
                                        AND (registro_mes_ano NOT NULL OR
                                        _notif_mesano NOT NULL OR
                                        _notif_dia NOT NULL OR
                                        _notif_sem NOT NULL)""")[0][0]
            acomp = dql("""SELECT COUNT(clienteid) 
                                        FROM compras WHERE status == "Acompanhamento"
                                        AND (registro_mes_ano NOT NULL OR
                                        _notif_mesano NOT NULL OR
                                        _notif_dia NOT NULL OR
                                        _notif_sem NOT NULL)""")[0][0]
            planej = dql("""SELECT COUNT(clienteid) 
                                        FROM compras WHERE status == "Planejamento"
                                        AND (registro_mes_ano NOT NULL OR
                                        _notif_mesano NOT NULL OR
                                        _notif_dia NOT NULL OR
                                        _notif_sem NOT NULL)""")[0][0]

            progressoRef.update({'concluido': concl,
                                 'execucao': execu,
                                 'acompanhamento': acomp,
                                 'planejamento': planej})









        populando_servicos()

        grade_cad_serv = LabelFrame(grade_serv)

        # Novo Serviço
        grade_cade_serv_real = LabelFrame(grade_cad_serv, pady=55, padx=105, font='Arial 17',
                                          text='                                    📌 Novo Serviço                                     ')

        lb_Codigo_serv_real = Label(grade_cade_serv_real, text="Código:", font='Arial 15', bd=5)
        lb_Codigo_serv_real.grid(row=0, column=0)
        txt_Codigo_serv_real = Entry(grade_cade_serv_real, font='Arial 15', width=10)
        txt_Codigo_serv_real.grid(row=1, column=0)

        lb_Tipo_serv = Label(grade_cade_serv_real, text="Tipo:", font='Arial 15')
        lb_Tipo_serv.grid(row=2, column=0, columnspan=2, sticky=W + E)
        txt_Tipo_serv_nov = ttk.Combobox(grade_cade_serv_real, values=lista_tipo, font='Arial 15')
        txt_Tipo_serv_nov.grid(row=3, column=0, columnspan=2, sticky=W + E)

        lb_Serv_set_nov = Label(grade_cade_serv_real, text="Setor:", font='Arial 15')
        lb_Serv_set_nov.grid(row=0, column=1)
        txt_Serv_set_nov = ttk.Combobox(grade_cade_serv_real, values=lista_setor, font='Arial 15', width=25)
        txt_Serv_set_nov.grid(row=1, column=1)

        def dml_n_serv_cad():
            if len(txt_Codigo_serv_real.get()) != 0 and len(txt_Tipo_serv_nov.get()) != 0 and len(
                    txt_Serv_set_nov.get()) != 0:
                vcon.cursor()
                vcon.execute(f'''INSERT OR REPLACE INTO servicos (codigo, tipo,setor) 
                                            VALUES ({txt_Codigo_serv_real.get()}, "{txt_Tipo_serv_nov.get()}", "{txt_Serv_set_nov.get()}")''')
                vcon.commit()

                txt_Codigo_serv_real.delete(0, END)
                txt_Tipo_serv_nov.delete(0, END)
                txt_Serv_set_nov.delete(0, END)

                lista_setor.clear()
                lista_tipo.clear()
                for r in dql('''SELECT tipo FROM servicos'''):
                    lista_tipo.append(r[0])

                for r in dql('''SELECT setor FROM servicos'''):
                    lista_setor.append(r[0])
                txt_Tipo_serv_nov.config(values=lista_tipo)
                txt_Tipo_serv.config(values=lista_tipo)
                txt_Serv_set_nov.config(values=lista_setor)
                txt_Serv_set.config(values=lista_setor)

            else:
                messagebox.showinfo(title='Erro', message='Preencha todos os campos')

        def deleta_todos_serv_novo():
            vcon.cursor()
            try:
                confirm = messagebox.askyesno(title='Deletando serviços',
                                              message='Deseja realmente remover TODOS os serviços?')
                if confirm == 1:
                    vcon.execute(f'''DELETE FROM servicos''')
                    vcon.commit()

                    lista_setor.clear()
                    lista_tipo.clear()
                    for r in dql('''SELECT tipo FROM servicos'''):
                        lista_tipo.append(r[0])

                    for r in dql('''SELECT setor FROM servicos'''):
                        lista_setor.append(r[0])
                    txt_Tipo_serv_nov.config(values=lista_tipo)
                    txt_Tipo_serv.config(values=lista_tipo)
                    txt_Serv_set_nov.config(values=lista_setor)
                    txt_Serv_set.config(values=lista_setor)
                else:
                    pass
            except Error as er:
                messagebox.showinfo(title='Erro', message=f'Algo de errado aconteceu\n Tipo: {str(er)}')

        def search_servico():
            try:
                if len(txt_Codigo_serv_real.get()) != 0:
                    txt_Tipo_serv_nov.delete(0, END)
                    txt_Serv_set_nov.delete(0, END)
                    for i in dql(f'''SELECT * FROM servicos WHERE codigo = {txt_Codigo_serv_real.get()}'''):
                        txt_Tipo_serv_nov.insert(0, f'{i[1]}')
                        txt_Serv_set_nov.insert(0, f'{i[2]}')
                else:
                    messagebox.showinfo(title='Erro', message='Preencha o campo Código')


            except Error as er:
                messagebox.showerror(title=f'Erro',
                                     message=f'Oops! Não encontramos nenhum serviço com esse registro 😕\n{str(er)}')

        def delete_novo_serv():
            if len(txt_Codigo_serv_real.get()) != 0:
                try:
                    vcon.cursor()
                    confirm = messagebox.askyesno(title='Deletando um serviço',
                                                  message=f'Deseja realmente remover o serviço de Código:{str(txt_Codigo_serv_real.get())}?')
                    if confirm == 1:
                        vcon.execute(f'''DELETE FROM servicos WHERE codigo={txt_Codigo_serv_real.get()}''')
                        vcon.commit()

                        txt_Tipo_serv_nov.delete(0, END)
                        txt_Serv_set_nov.delete(0, END)
                        lista_setor.clear()
                        lista_tipo.clear()
                        for r in dql('''SELECT tipo FROM servicos'''):
                            lista_tipo.append(r[0])

                        for r in dql('''SELECT setor FROM servicos'''):
                            lista_setor.append(r[0])
                        txt_Tipo_serv_nov.config(values=lista_tipo)
                        txt_Tipo_serv.config(values=lista_tipo)
                        txt_Serv_set_nov.config(values=lista_setor)
                        txt_Serv_set.config(values=lista_setor)
                    else:
                        pass
                except Error as er:
                    messagebox.showinfo(title=f'Erro {er}', message=f'Algo de errado aconteceu.')

        btn_novo_serv = Button(grade_cade_serv_real, text='➕ Salvar', command=dml_n_serv_cad, bg='#a4d49a',
                               font='Arial 12')
        btn_novo_serv.grid(row=4, column=1, sticky=W + E)
        btn_search_novo_serv = Button(grade_cade_serv_real, text='🔎', command=search_servico, bg='#bbd3ff',
                                      font='Arial 12')
        btn_search_novo_serv.grid(row=4, column=0, sticky=W + E)
        btn_deletar_n_serv = Button(grade_cade_serv_real, text='⛔', command=delete_novo_serv, bg='#ff9774',
                                    font='Arial 12')
        btn_deletar_n_serv.grid(row=5, column=0, sticky=W + E)

        btn_deleta_tudo_n_s = Button(grade_cade_serv_real, text='Deletar Todos', command=deleta_todos_serv_novo,
                                     bg='#ff9774',
                                     font='Arial 12', width=12)
        btn_deleta_tudo_n_s.grid(row=5, column=1, sticky=W + E)

        grade_cade_serv_real.pack(side=RIGHT, anchor=N)









        lista_cl_atv = []
        lista_cl_int = []

        def _cl_atv():
            lista_cl_atv.clear()
            lista_cl_int.clear()
            for i in dql('''SELECT codigo ||+" - "|| nome ||+"      ¬ "|| local FROM clientes'''):
                if i[0] not in [aaaaaaaaaa[0] for aaaaaaaaaa in dql('''SELECT clienteid FROM compras WHERE status != "Concluído" 
                                                                                        AND (registro_mes_ano NOT NULL OR
                                                                                        _notif_mesano NOT NULL OR
                                                                                        _notif_dia NOT NULL OR
                                                                                        _notif_sem NOT NULL)''')]:
                    lista_cl_int.append(i[0])
                else:
                    lista_cl_atv.append(i[0])

            progressoRef.update({'ativos': len(lista_cl_atv),
                                 'inativos': len(lista_cl_int)})












        grade_det_btns = LabelFrame(grade_cad_serv, font='Arial 20', pady=20,
                                    text='                                                                     📝 Contratos                                                                      ')
        grade_det_btns.pack(fill=Y)

        lb_Codigo_serv = Label(grade_det_btns, text="ID:", font='Arial 15', bd=5)
        lb_Codigo_serv.grid(row=0, column=0)
        txt_Codigo_serv = Entry(grade_det_btns, font='Arial 15', width=10)
        txt_Codigo_serv.grid(row=1, column=0)

        lb_Tipo_serv = Label(grade_det_btns, text="Tipo:", font='Arial 15')
        lb_Tipo_serv.grid(row=0, column=1)
        txt_Tipo_serv = ttk.Combobox(grade_det_btns, values=lista_tipo, font='Arial 15', width=40)
        txt_Tipo_serv.grid(row=1, column=1)

        lb_Serv_set = Label(grade_det_btns, text="Setor:", font='Arial 15')
        lb_Serv_set.grid(row=0, column=2)
        txt_Serv_set = ttk.Combobox(grade_det_btns, values=lista_setor, font='Arial 15', width=25)
        txt_Serv_set.grid(row=1, column=2)

        # Grade Cliente/Serv
        grade_cliente_serv = LabelFrame(grade_cad_serv)
        grade_cliente_serv.pack(fill=BOTH)

        quadro_q_pgmt = LabelFrame(grade_cliente_serv)
        quadro_q_pgmt.grid(row=0, column=0, sticky=N + S)

        lb_Serv_cliente = Label(quadro_q_pgmt, text="Cliente: ", font='Arial 15', width=38)
        lb_Serv_cliente.grid(row=0, column=0, sticky=W + E)
        txt_Serv_cliente = ttk.Combobox(quadro_q_pgmt, values=lista_clientes, font='Arial 15', width=38)
        txt_Serv_cliente.grid(row=1, column=0, sticky=W + E)

        lb_Serv_mf = Label(quadro_q_pgmt, text="Franquia ou Filial: ", font='Arial 15', width=38)
        lb_Serv_mf.grid(row=0, column=1, sticky=W + E)
        txt_Serv_mf = ttk.Combobox(quadro_q_pgmt, values=lista_perfil, font='Arial 15', width=43)
        txt_Serv_mf.grid(row=1, column=1, sticky=W + E)

        scale = Scale(quadro_q_pgmt, cursor='plus',
                      from_=1, to=5, orient=HORIZONTAL, troughcolor='#ffffff',
                      sliderlength=200, bg='#e6f7ff', sliderrelief=GROOVE, bd=1, font='Arial 15',
                      activebackground='lightblue',
                      label='''Apresentação ⠀⠀⠀⠀⠀⠀ Planejamento ⠀⠀⠀⠀ Execução ⠀⠀⠀Acompanhamento ⠀⠀⠀ Concluído''')
        scale.grid(row=3, rowspan=5, column=0, columnspan=2, sticky=W + E + N + S)

        quadro_pgmt = LabelFrame(grade_cliente_serv)
        quadro_pgmt.grid(row=0, column=1)

        lb_Serv_pgmt = Label(quadro_pgmt, text="Pagamento (Frequência, Intervalo):", font='Arial 13')
        lb_Serv_pgmt.grid(row=0, column=3)

        txt_Serv_freq_pgmt = Spinbox(quadro_pgmt, from_=1, to=4,
                                     values=('Mensal', 'Anual', 'Diário', 'Semanal'),
                                     font='Arial 15', width=17, justify=CENTER, wrap=True)
        txt_Serv_freq_pgmt.grid(row=1, column=3, sticky=W + E)
        txt_Serv_interv_pgmt = Spinbox(quadro_pgmt, from_=1,
                                       to=99999999999999999999999999999999999999999999999999999,
                                       width=3, font='Arial 15', justify=CENTER)
        txt_Serv_interv_pgmt.grid(row=1, column=4, sticky=W + E)

        lb_Serv_df = Label(quadro_pgmt, text="Data Fim: ", font='Arial 15')
        lb_Serv_df.grid(row=2, column=3, sticky=W + E)
        txt_Serv_df_pgmt = Entry(quadro_pgmt, font='Arial 15', justify=CENTER, bd=5)
        txt_Serv_df_pgmt.grid(row=3, column=3, sticky=W + E)

        txt_Serv_df_pgmt.insert(0, 'AAAAMMDD')

        lb_Serv_vl = Label(quadro_pgmt, text="Valor: ", font='Arial 15')
        lb_Serv_vl.grid(row=4, column=3, sticky=W + E)
        lb_rcifrao_serv = Label(quadro_pgmt, text='R$', font='Arial 12 bold')
        lb_rcifrao_serv.grid(row=5, column=2)
        txt_Serv_vl_pgmt = Entry(quadro_pgmt, font='Arial 15', bd=5)
        txt_Serv_vl_pgmt.grid(row=5, column=3, sticky=W + E)
        txt_Serv_vl_pgmt.insert(0, '0')

        #####Tv Serv
        tv_serv_grade = LabelFrame(grade_serv)
        tv_serv_grade.pack(fill=BOTH, side=BOTTOM)
        serv = ttk.Treeview(tv_serv_grade,
                            columns=(
                                'ID', 'cliente', 'servico', 'perfil', 'pagamento', 'fim de contrato', 'status'),
                            show='headings',
                            height=23)

        serv.column('ID', anchor=CENTER, width=100)
        serv.column('cliente', anchor=CENTER, width=330)
        serv.column('servico', anchor=CENTER, width=300)
        serv.column('perfil', anchor=CENTER, width=285)
        serv.column('pagamento', anchor=CENTER, width=170)
        serv.column('fim de contrato', anchor=CENTER, width=70)
        serv.column('status', anchor=CENTER, width=150)

        serv.heading('ID', text='ID', anchor=CENTER)
        serv.heading('cliente', text='Cliente', anchor=CENTER)
        serv.heading('servico', text='Serviço', anchor=CENTER)
        serv.heading('perfil', text='Franquia ou Filial', anchor=CENTER)
        serv.heading('pagamento', text='Pagamento', anchor=CENTER)
        serv.heading('fim de contrato', text='FIM', anchor=CENTER)
        serv.heading('status', text='Status', anchor=CENTER)

        # Barra de rolagem
        barra = ttk.Scrollbar(tv_serv_grade, orient='vertical')
        barra.config(command=serv.yview)
        serv.configure(yscrollcommand=barra.set)
        barra.pack(side=RIGHT, fill=Y)

        serv.pack(fill=BOTH, side=BOTTOM)
        grade_cad_serv.pack(fill=Y, side=LEFT)

        # Botões
        def pdf_serv():

            Nome_relatorio_a = 'Serviços'
            if len(txt_Serv_mf.get()) or len(txt_Serv_cliente.get()) > 0:
                activeCustomers= dql(f'''SELECT codigo as "ID",
                                                clienteid as "Cliente",
                                                servicosid as "Serviço",
                                                perfilid as "Matriz ou Filial","Interv. "||
                                                intervalo  || pagamento as "Pagamento",
                                                "R$ " || valor as "Parcela",
                                                _fim as "Fim de Contrato" 
                                        FROM compras WHERE "Fim de Contrato" >={ano_hoje}{mes_hoje}{dia_hoje} and ("Matriz ou Filial" = "{txt_Serv_mf.get()}" or "Cliente" = "{txt_Serv_cliente.get()}")''')
            else:
                activeCustomers= dql(f'''SELECT codigo as "ID",
                                                clienteid as "Cliente",
                                                servicosid as "Serviço",
                                                perfilid as "Matriz ou Filial","Interv. "||
                                                intervalo  || pagamento as "Pagamento",
                                                "R$ " || valor as "Parcela",
                                                _fim as "Fim de Contrato" 
                                        FROM compras WHERE "Fim de Contrato" >={ano_hoje}{mes_hoje}{dia_hoje}''')

            doc = SimpleDocTemplate(
                f'C:\\Users\\{os.getlogin()}\\Downloads\\{dia_mes_ano}  ¬Relatorio_{Nome_relatorio_a}.pdf',
                pagesize=(letter[0] + 350, letter[1]))
            data = [['ID', 'Cliente', 'Serviço', 'Matriz ou Filial', 'Pagamento', 'Parcela',
                     'Fim de Contrato', ]]  # give data as lists with lists.

            select_query = activeCustomers

            for i in select_query:
                data.append(i)
            table = Table(data)

            tabla_style = TableStyle([
                ('BACKGROUND', (0, 0), (7, 0), colors.darkcyan),
                ('BACKGROUND', (0, 0), (0, 0), colors.darkblue),
                ('BACKGROUND', (0, 1), (0, len(data)), colors.gray),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('TEXTCOLOR', (0, 1), (0, len(data)), colors.white),
                ('TEXTCOLOR', (0, 0), (7, 0), colors.white),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
            table.setStyle(tabla_style)
            styleSheet = getSampleStyleSheet()

            titulo = Paragraph(f'Relatório de {Nome_relatorio_a} Ativos  ¬ {mes_ano}',
                               style=styleSheet['Heading1'])
            emptyline = Paragraph(f'       ', style=styleSheet['Heading1'])

            infodoc = Paragraph(f'''Documento gerado às: {hora_minuto_segundo}''', style=styleSheet['Normal'])

            doc_lenth = Paragraph(f'''Total de Serviços Ativos = {len(activeCustomers)}''',
                                  style=styleSheet['Normal'])
            contato_dev = Paragraph(
                f'>>>  Algo errado? Reporte através do e-mail: {yourEmailForSupport}',
                style=styleSheet['Normal'])

            doc.build(
                [titulo, emptyline, emptyline, emptyline, emptyline, table, infodoc,
                 emptyline, emptyline, doc_lenth, emptyline, contato_dev])
            os.startfile(
                f'C:\\Users\\{os.getlogin()}\\Downloads\\{dia_mes_ano}  ¬Relatorio_{Nome_relatorio_a}.pdf')

        def mostra_todosserv():
            serv.delete(*serv.get_children())

            linhas_serv = dql(f'''SELECT 
                                        codigo as "ID",
                                        clienteid as "Cliente",
                                        servicosid as "Serviço", 
                                        perfilid as "Matriz ou Filial",
                                        "Interv. "|| intervalo ||" " || pagamento || " de R$ " || valor as "Pagamento",
                                        _fim as "Fim de Contrato", 
                                        status as "Status" 
                                FROM compras WHERE _fim >={ano_mes_dia}''')
            for xxxxx in linhas_serv:
                serv.insert('', 'end', values=(xxxxx))

            concl = dql("""SELECT COUNT(clienteid) 
                                        FROM compras WHERE status == "Concluído"
                                        AND (registro_mes_ano NOT NULL OR
                                        _notif_mesano NOT NULL OR
                                        _notif_dia NOT NULL OR
                                        _notif_sem NOT NULL)""")[0][0]
            execu = dql("""SELECT COUNT(clienteid) 
                                        FROM compras WHERE status == "Execução"
                                        AND (registro_mes_ano NOT NULL OR
                                        _notif_mesano NOT NULL OR
                                        _notif_dia NOT NULL OR
                                        _notif_sem NOT NULL)""")[0][0]
            acomp = dql("""SELECT COUNT(clienteid) 
                                        FROM compras WHERE status == "Acompanhamento"
                                        AND (registro_mes_ano NOT NULL OR
                                        _notif_mesano NOT NULL OR
                                        _notif_dia NOT NULL OR
                                        _notif_sem NOT NULL)""")[0][0]
            planej = dql("""SELECT COUNT(clienteid) 
                                        FROM compras WHERE status == "Planejamento"
                                        AND (registro_mes_ano NOT NULL OR
                                        _notif_mesano NOT NULL OR
                                        _notif_dia NOT NULL OR
                                        _notif_sem NOT NULL)""")[0][0]

            progressoRef.update({'concluido': concl,
                                 'execucao': execu,
                                 'acompanhamento': acomp,
                                 'planejamento': planej})







        mostra_todosserv()

        def dml_serv():

            if len(txt_Codigo_serv.get()) != 0 and len(txt_Tipo_serv.get()) != 0 and len(
                    txt_Serv_set.get()) != 0 and len(txt_Serv_cliente.get()) != 0 and len(
                txt_Serv_mf.get()) != 0 and len(txt_Serv_vl_pgmt.get()) != 0 \
                    and len(txt_Serv_df_pgmt.get()) > 6:

                y = datetime.datetime.now()

                if ((int(txt_Serv_interv_pgmt.get()) + int(
                        y.strftime("%m"))) > 24 and txt_Serv_freq_pgmt.get() == 'Mensal') \
                        or ((int(txt_Serv_interv_pgmt.get()) + (
                        int(y.strftime("%w")) + 1)) > 14 and txt_Serv_freq_pgmt.get() == 'Diário') \
                        or ((int(txt_Serv_interv_pgmt.get()) + (
                        int(y.strftime("%U")) + 1)) > 104 and txt_Serv_freq_pgmt.get() == 'Semanal'):
                    messagebox.showerror(title='Erro de Alcance',
                                         message='''Escolha Frequência e Intervalo adequados.
        Atenção:
        USE ano para mais de 24 meses.
        USE semana para mais de 14 dias.
        ''')
                else:
                    if txt_Serv_freq_pgmt.get() == 'Mensal':
                        coluna_notif = '_notif_mesano'
                        valor_notif = int(y.strftime("%m"))
                        if (valor_notif + int(txt_Serv_interv_pgmt.get())) > 12:
                            novo_notif = (valor_notif + int(txt_Serv_interv_pgmt.get())) - 12
                        else:
                            novo_notif = valor_notif + int(txt_Serv_interv_pgmt.get())
                    elif txt_Serv_freq_pgmt.get() == 'Anual':
                        coluna_notif = '_notif_mesano'
                        novo_notif = int(y.strftime("%Y")) + int(txt_Serv_interv_pgmt.get())
                    elif txt_Serv_freq_pgmt.get() == 'Semanal':
                        coluna_notif = '_notif_sem'
                        valor_notif = int(y.strftime("%U"))
                        if (valor_notif + int(txt_Serv_interv_pgmt.get())) > 52:
                            novo_notif = (valor_notif + int(txt_Serv_interv_pgmt.get())) - 52
                        else:
                            novo_notif = valor_notif + int(txt_Serv_interv_pgmt.get())
                    else:
                        coluna_notif = '_notif_dia'
                        valor_notif = int(y.strftime("%w")) + 1
                        if (valor_notif + int(txt_Serv_interv_pgmt.get())) > 7:
                            novo_notif = (valor_notif + int(txt_Serv_interv_pgmt.get())) - 7
                        else:
                            novo_notif = valor_notif + int(txt_Serv_interv_pgmt.get())

                    if scale.get() == 1:
                        status = 'Apresentação'
                    elif scale.get() == 2:
                        status = 'Planejamento'
                    elif scale.get() == 3:
                        status = 'Execução'
                    elif scale.get() == 4:
                        status = 'Acompanhamento'
                    else:
                        status = 'Concluído'

                    vcon.cursor()
                    vcon.execute(
                        f'''INSERT OR REPLACE INTO compras (codigo, clienteid, servicosid, perfilid, pagamento, intervalo, _fim, valor,{coluna_notif},status) 
                                                                    VALUES ({txt_Codigo_serv.get()}, "{str(txt_Serv_cliente.get())}","{str(txt_Tipo_serv.get())}     ¬ {str(txt_Serv_set.get())}",
                                                                    "{str(txt_Serv_mf.get())}","{txt_Serv_freq_pgmt.get()}",{txt_Serv_interv_pgmt.get()},{txt_Serv_df_pgmt.get()},"{txt_Serv_vl_pgmt.get()}","{novo_notif}","{status}")''')
                    vcon.commit()

                    grafico_diag_rplc()

                    if dql(f"""SELECT COUNT(*) FROM servicos WHERE
                                                                                        tipo='{txt_Tipo_serv.get()}' AND
                                                                                        setor='{txt_Serv_set.get()}'""")[
                        0][0] == 0:
                        vcon.cursor()
                        vcon.execute(
                            f"""INSERT OR REPLACE INTO servicos (codigo, tipo,setor)   VALUES({txt_Codigo_serv.get()},
                                                                                                            '{txt_Tipo_serv.get()}',
                                                                                                            '{txt_Serv_set.get()}')""")
                        vcon.commit()

                    lista_clientes.clear()
                    lista_setor.clear()
                    lista_tipo.clear()
                    lista_perfil.clear()
                    populador_local_mf()
                    populando_servicos()
                    txt_lotacao_cargo.config(values=lista_perfil)
                    txt_Tipo_serv.config(values=lista_tipo)
                    txt_Serv_set.config(values=lista_setor)
                    txt_Serv_mf.config(values=lista_perfil)

                    txt_Codigo_serv.delete(0, END)
                    txt_Tipo_serv.delete(0, END)
                    txt_Serv_set.delete(0, END)
                    txt_Serv_cliente.delete(0, END)
                    txt_Serv_mf.delete(0, END)
                    txt_Serv_df_pgmt.delete(0, END)
                    txt_Serv_vl_pgmt.delete(0, END)
                    txt_Serv_vl_pgmt.insert(0, '0')
                    txt_Serv_df_pgmt.insert(0, 'AAAAMMDD')

                    axQ.clear()
                    inactiveCustomers= \
                        dql(f'''SELECT COUNT(*) FROM compras WHERE status = "Apresentação"  or status = "Planejamento"''')[
                            0][
                            0]
                    activeCustomers = \
                        dql(f'''SELECT COUNT(*) FROM compras WHERE status = "Execução" or status = "Acompanhamento"''')[
                            0][0]
                    sizes = inactiveCustomers, activeCustomers, (inactiveCustomers + activeCustomers)
                    colors_serv = ['chocolate', 'dodgerblue', 'white']

                    axQ.pie(sizes, labels=(f"{inactiveCustomers} Concluídos\nou Apresentação", f"{activeCustomers} Andamento", "")
                            , colors=colors_serv, textprops={'size': '26'})
                    axQ.add_artist(circleQ)
                    axQ.annotate(
                        f"Aproveitamento\n     {(activeCustomers / int(dql('SELECT COUNT(*) FROM compras')[0][0])) * 100:.0f}%",
                        xy=(0, 0), fontsize=26, ha="center")

                    canvaQ.draw()

                    pgmt_()

                    ax_pgmt.clear()
                    ax_pgmt2.clear()
                    ax_pgmt2.xaxis.set_major_locator(MaxNLocator(integer=True))
                    ax_pgmt.xaxis.set_major_locator(MaxNLocator(integer=True))
                    ax_pgmt.legend(ncol=2)
                    ax_pgmt2.legend(ncol=2)
                    pd.DataFrame(
                        {'Mensal': [lista_pgmnts.count('Mensal')],
                         'Semanal': [lista_pgmnts.count('Semanal')]}).plot.barh(stacked=True, ax=ax_pgmt,
                                                                                edgecolor='white')
                    pd.DataFrame(
                        {'Anual': [lista_pgmnts.count('Anual')], 'Diário': [lista_pgmnts.count('Diário')]}).plot.barh(
                        stacked=True, ax=ax_pgmt2, edgecolor='white')

                    canva_pgmt.draw()
                    mostra_todosserv()

                    _cl_atv()
                    ax_cl_atv.clear()
                    pd.DataFrame(
                        {'Ativos': [len(lista_cl_atv)], 'Inativos': [len(lista_cl_int)]}).plot.barh(stacked=True,
                                                                                                    ax=ax_cl_atv,
                                                                                                    edgecolor='white')
                    progressoRef.update({'ativos': len(lista_cl_atv),
                                         'inativos': len(lista_cl_int)})
                    ax_cl_atv.xaxis.set_major_locator(MaxNLocator(integer=True))
                    ax_cl_atv.legend(ncol=2)
                    plt.legend(fontsize=50)
                    canva_cl_atv.draw()



            else:
                messagebox.showerror(title='Erro', message='Preencha os campos corretamente.')

        def deleta_todos_serv():

            try:
                confirm = messagebox.askyesno(title='Deletando contrato',
                                              message='Deseja realmente remover TODOS os contratos ativos?')
                if confirm == 1:
                    vcon.cursor()
                    vcon.execute(f'''DELETE FROM compras WHERE status != "Concluído"''')
                    vcon.commit()

                    vcon.cursor()
                    vcon.execute('''INSERT INTO  compras (
                                                                                    codigo,
                                                                                    clienteid,
                                                                                    servicosid,
                                                                                    perfilid,
                                                                                    pagamento,
                                                                                    intervalo,
                                                                                    _fim,
                                                                                    valor,
                                                                                    status
                                                                                    )  
                                            VALUES (1,"Cliente Demonstrativo","Serviço","Empresa","Período",1,99999999,0,"Execução")''')
                    vcon.commit()

                    mostra_todosserv()
                    grafico_diag_rplc()

                    axQ.clear()
                    inactiveCustomers= \
                        dql(f'''SELECT COUNT(*) FROM compras WHERE status = "Apresentação"  or status = "Planejamento"''')[
                            0][
                            0]
                    activeCustomers = \
                        dql(f'''SELECT COUNT(*) FROM compras WHERE status = "Execução" or status = "Acompanhamento"''')[
                            0][0]
                    sizes = inactiveCustomers, activeCustomers, (inactiveCustomers + activeCustomers)
                    colors_serv = ['chocolate', 'dodgerblue', 'white']

                    axQ.pie(sizes, labels=(f"{inactiveCustomers} Concluídos\nou Apresentação", f"{activeCustomers} Andamento", "")
                            , colors=colors_serv, textprops={'size': '26'})
                    axQ.annotate(
                        f"Aproveitamento\n     {(activeCustomers / int(dql('SELECT COUNT(*) FROM compras')[0][0])) * 100:.0f}%",
                        xy=(0, 0), fontsize=26, ha="center")

                    axQ.add_artist(circleQ)
                    canvaQ.draw()

                    pgmt_()

                    ax_pgmt.clear()
                    ax_pgmt2.clear()
                    ax_pgmt2.xaxis.set_major_locator(MaxNLocator(integer=True))
                    ax_pgmt.xaxis.set_major_locator(MaxNLocator(integer=True))
                    ax_pgmt.legend(ncol=2)
                    ax_pgmt2.legend(ncol=2)
                    pd.DataFrame(
                        {'Mensal': [lista_pgmnts.count('Mensal')],
                         'Semanal': [lista_pgmnts.count('Semanal')]}).plot.barh(stacked=True, ax=ax_pgmt,
                                                                                edgecolor='white')
                    pd.DataFrame(
                        {'Anual': [lista_pgmnts.count('Anual')],
                         'Diário': [lista_pgmnts.count('Diário')]}).plot.barh(stacked=True, ax=ax_pgmt2,
                                                                              edgecolor='white')

                    canva_pgmt.draw()

                    _cl_atv()
                    ax_cl_atv.clear()
                    pd.DataFrame(
                        {'Ativos': [len(lista_cl_atv)], 'Inativos': [len(lista_cl_int)]}).plot.barh(
                        stacked=True, ax=ax_cl_atv, edgecolor='white')
                    progressoRef.update({'ativos': len(lista_cl_atv),
                                         'inativos': len(lista_cl_int)})
                    ax_cl_atv.xaxis.set_major_locator(MaxNLocator(integer=True))
                    ax_cl_atv.legend(ncol=2)
                    plt.legend(fontsize=50)
                    canva_cl_atv.draw()
                else:
                    pass
            except Error as er:
                messagebox.showinfo(title=f'Erro {er}', message=f'Algo de errado aconteceu.')

            txt_Codigo_serv.delete(0, END)
            txt_Tipo_serv.delete(0, END)
            txt_Serv_set.delete(0, END)
            txt_Serv_cliente.delete(0, END)
            txt_Serv_mf.delete(0, END)

        def search_serv():
            serv.delete(*serv.get_children())
            try:
                if len(txt_Codigo_serv.get()) != 0:

                    db_query2 = dql(
                        f'''SELECT 
                                codigo as "ID",
                                clienteid as "Cliente",
                                servicosid as "Serviço", 
                                perfilid as "Matriz ou Filial",
                                intervalo ||"x  " || pagamento || " de R$ " || valor as "Pagamento",
                                _fim as "Fim de Contrato", 
                                status as "Status" 
                            FROM compras WHERE codigo =="{txt_Codigo_serv.get()}"''')


                    for i in db_query2:
                        serv.insert('', 'end', values=(i))

                elif len(txt_Tipo_serv.get()) != 0:
                    db_query2 = dql(
                        f'''SELECT 
                                    codigo as "ID",
                                    clienteid as "Cliente",
                                    servicosid as "Serviço", 
                                    perfilid as "Matriz ou Filial",
                                    intervalo ||"x  " || pagamento || " de R$ " || valor as "Pagamento",
                                    _fim as "Fim de Contrato", 
                                    status as "Status" 
                            FROM compras WHERE _fim >={ano_mes_dia} AND servicosid like "{txt_Tipo_serv.get()}%"''')


                    for i in db_query2:
                        serv.insert('', 'end', values=(i))
                elif len(txt_Serv_set.get()) != 0:

                    db_query2 = dql(
                        f'''SELECT 
                                codigo as "ID",
                                clienteid as "Cliente",
                                servicosid as "Serviço", 
                                perfilid as "Matriz ou Filial",
                                intervalo ||"x  " || pagamento || " de R$ " || valor as "Pagamento",
                                _fim as "Fim de Contrato", 
                                status as "Status" 
                            FROM compras WHERE _fim >={ano_mes_dia} AND servicosid like "{txt_Serv_set.get()}%"''')


                    for i in db_query2:
                        serv.insert('', 'end', values=(i))
                elif len(txt_Serv_cliente.get()) != 0:

                    db_query2 = dql(
                        f'''SELECT 
                                codigo as "ID",
                                clienteid as "Cliente",
                                servicosid as "Serviço", 
                                perfilid as "Matriz ou Filial",
                                intervalo ||"x  " || pagamento || " de R$ " || valor as "Pagamento",
                                _fim as "Fim de Contrato", 
                                status as "Status" 
                            FROM compras WHERE _fim >={ano_mes_dia} AND  clienteid like "{txt_Serv_cliente.get()}%"''')

                    for i in db_query2:
                        serv.insert('', 'end', values=(i))
                elif len(txt_Serv_mf.get()) != 0:
                    db_query2 = dql(
                        f'''SELECT 
                                codigo as "ID",
                                clienteid as "Cliente",
                                servicosid as "Serviço", 
                                perfilid as "Matriz ou Filial",
                                intervalo ||"x  " || pagamento || " de R$ " || valor as "Pagamento",
                                _fim as "Fim de Contrato", 
                                status as "Status" 
                            FROM compras WHERE _fim >={ano_mes_dia} AND perfilid like "{txt_Serv_mf.get()}%"''')

                    for i in db_query2:
                        serv.insert('', 'end', values=(i))
                elif len(txt_Serv_freq_pgmt.get()) != 0:

                    db_query2 = dql(
                        f'''SELECT 
                                codigo as "ID",
                                clienteid as "Cliente",
                                servicosid as "Serviço", 
                                perfilid as "Matriz ou Filial",
                                intervalo ||"x  " || pagamento || " de R$ " || valor as "Pagamento",
                                _fim as "Fim de Contrato", 
                                status as "Status" 
                            FROM compras WHERE _fim >={ano_mes_dia} AND pagamento like "{txt_Serv_freq_pgmt.get()}%"''')

                    for i in db_query2:
                        serv.insert('', 'end', values=(i))
                else:

                    messagebox.showinfo(title='Erro', message='Preencha pelo menos um campo')


            except Error as er:
                messagebox.showerror(title=f'Erro',
                                     message=f'Oops! Não encontramos nenhum contrato com esse registro 😕\n{str(er)}')
            txt_Codigo1.delete(0, END)
            txt_Nome1.delete(0, END)
            txt_Local.delete(0, END)

        def delete_serv():
            try:
                if len(txt_Codigo_serv.get()) != 0:
                    try:
                        vcon.cursor()
                        confirm = messagebox.askyesno(title='Deletando um contrato',
                                                      message=f'Deseja realmente remover a relação cliente/serviço ID = {str(txt_Codigo_serv.get())}?')
                        if confirm == 1:
                            vcon.execute(f'''DELETE FROM compras WHERE codigo = {txt_Codigo_serv.get()} AND 
                                         status != 'Concluído'   
                                                                AND (registro_mes_ano NOT NULL 
                                                                OR _notif_mesano NOT NULL 
                                                                OR _notif_dia NOT NULL 
                                                                OR _notif_sem NOT NULL)''')
                            vcon.commit()
                            messagebox.showinfo(message='Contrato(s) deletado(s) com sucesso')
                            mostra_todosserv()

                            txt_Codigo_serv.delete(0, END)
                            txt_Tipo_serv.delete(0, END)
                            txt_Serv_set.delete(0, END)
                            txt_Serv_cliente.delete(0, END)
                            txt_Serv_mf.delete(0, END)

                            axQ.clear()
                            inactiveCustomers= \
                                dql(f'''SELECT COUNT(*) FROM compras WHERE status = "Apresentação"  or status = "Planejamento"''')[
                                    0][
                                    0]
                            activeCustomers = \
                                dql(f'''SELECT COUNT(*) FROM compras WHERE status = "Execução" or status = "Acompanhamento"''')[
                                    0][0]
                            sizes = inactiveCustomers, activeCustomers, (inactiveCustomers + activeCustomers)
                            colors_serv = ['chocolate', 'dodgerblue', 'white']

                            axQ.pie(sizes, labels=(f"{inactiveCustomers} Concluídos\nou Apresentação", f"{activeCustomers} Andamento", "")
                                    , colors=colors_serv, textprops={'size': '26'})
                            axQ.add_artist(circleQ)
                            axQ.annotate(
                                f"Aproveitamento\n     {(activeCustomers / int(dql('SELECT COUNT(*) FROM compras')[0][0])) * 100:.0f}%",
                                xy=(0, 0), fontsize=26, ha="center")

                            canvaQ.draw()
                            grafico_diag_rplc()

                            pgmt_()

                            ax_pgmt.clear()
                            ax_pgmt2.clear()
                            ax_pgmt2.xaxis.set_major_locator(MaxNLocator(integer=True))
                            ax_pgmt.xaxis.set_major_locator(MaxNLocator(integer=True))
                            ax_pgmt.legend(ncol=2)
                            ax_pgmt2.legend(ncol=2)
                            pd.DataFrame(
                                {'Mensal': [lista_pgmnts.count('Mensal')],
                                 'Semanal': [lista_pgmnts.count('Semanal')]}).plot.barh(stacked=True,
                                                                                        ax=ax_pgmt,
                                                                                        edgecolor='white')
                            pd.DataFrame(
                                {'Anual': [lista_pgmnts.count('Anual')],
                                 'Diário': [lista_pgmnts.count('Diário')]}).plot.barh(stacked=True, ax=ax_pgmt2,
                                                                                      edgecolor='white')

                            canva_pgmt.draw()

                            _cl_atv()
                            ax_cl_atv.clear()
                            pd.DataFrame(
                                {'Ativos': [len(lista_cl_atv)], 'Inativos': [len(lista_cl_int)]}).plot.barh(
                                stacked=True, ax=ax_cl_atv, edgecolor='white')
                            progressoRef.update({'ativos': len(lista_cl_atv),
                                                 'inativos': len(lista_cl_int)})
                            ax_cl_atv.xaxis.set_major_locator(MaxNLocator(integer=True))
                            ax_cl_atv.legend(ncol=2)
                            plt.legend(fontsize=50)
                            canva_cl_atv.draw()
                        else:
                            pass
                    except Error as er:
                        messagebox.showinfo(title='Erro', message=f'Algo de errado aconteceu\n Tipo: {str(er)}')

                    lista_clientes.clear()
                    lista_setor.clear()
                    lista_tipo.clear()
                    lista_perfil.clear()
                    populador_local_mf()
                    populando_servicos()
                    txt_lotacao_cargo.config(values=lista_perfil)
                    txt_Tipo_serv.config(values=lista_tipo)
                    txt_Serv_set.config(values=lista_setor)
                    txt_Serv_mf.config(values=lista_perfil)
                elif len(txt_Serv_mf.get()) != 0:
                    try:
                        vcon.cursor()
                        confirm = messagebox.askyesno(title='Deletando contrato por perfil',
                                                      message=f'Ao clicar em "sim", você removerá todos os contratos cadastrados com perfil {str(txt_Serv_mf.get())}')
                        if confirm == 1:
                            vcon.execute(f'''DELETE FROM compras WHERE perfilid="{str(txt_Serv_mf.get())}"''')
                            vcon.commit()
                            messagebox.showinfo(message='Contrato(s) deletado(s) com sucesso')
                            mostra_todosserv()

                            txt_Codigo_serv.delete(0, END)
                            txt_Tipo_serv.delete(0, END)
                            txt_Serv_set.delete(0, END)
                            txt_Serv_cliente.delete(0, END)
                            txt_Serv_mf.delete(0, END)

                            axQ.clear()
                            inactiveCustomers= \
                                dql(f'''SELECT COUNT(*) FROM compras WHERE status = "Apresentação"  or status = "Planejamento"''')[
                                    0][
                                    0]
                            activeCustomers = \
                                dql(f'''SELECT COUNT(*) FROM compras WHERE status = "Execução" or status = "Acompanhamento"''')[
                                    0][0]
                            sizes = inactiveCustomers, activeCustomers, (inactiveCustomers + activeCustomers)
                            colors_serv = ['chocolate', 'dodgerblue', 'white']

                            axQ.pie(sizes, labels=(f"{inactiveCustomers} Concluídos\nou Apresentação", f"{activeCustomers} Andamento", "")
                                    , colors=colors_serv, textprops={'size': '26'})
                            axQ.add_artist(circleQ)
                            canvaQ.draw()
                            grafico_diag_rplc()

                            pgmt_()

                            ax_pgmt.clear()
                            ax_pgmt2.clear()

                            pd.DataFrame(
                                {'Mensal': [lista_pgmnts.count('Mensal')],
                                 'Semanal': [lista_pgmnts.count('Semanal')]}).plot.barh(stacked=True,
                                                                                        ax=ax_pgmt,
                                                                                        edgecolor='white')
                            pd.DataFrame(
                                {'Anual': [lista_pgmnts.count('Anual')],
                                 'Diário': [lista_pgmnts.count('Diário')]}).plot.barh(stacked=True, ax=ax_pgmt2,
                                                                                      edgecolor='white')
                            progressoRef.update({'ativos': len(lista_cl_atv),
                                                 'inativos': len(lista_cl_int)})
                            ax_pgmt.legend(ncol=2)
                            ax_pgmt2.legend(ncol=2)
                            canva_pgmt.draw()
                        else:
                            pass
                    except:
                        messagebox.showinfo(title='Erro', message=f'Algo de errado aconteceu')
                    lista_clientes.clear()
                    lista_setor.clear()
                    lista_tipo.clear()
                    lista_perfil.clear()
                    populador_local_mf()
                    populando_servicos()
                    txt_lotacao_cargo.config(values=lista_perfil)
                    txt_Tipo_serv.config(values=lista_tipo)
                    txt_Serv_set.config(values=lista_setor)
                    txt_Serv_mf.config(values=lista_perfil)
            except:
                messagebox.showinfo(title='Erro',
                                    message='Digite o código de registro  que deseja remover da relação')

        def hist_serv():

            completedServices = dql(f'''SELECT codigo as "ID",
                                                                        clienteid as "Cliente",
                                                                        servicosid as "Serviço",
                                                                        perfilid as "Matriz ou Filial","Interv. "||
                                                                        intervalo ||" " || pagamento ||" de  R$ " || valor as "Pagamento",
                                                                        _fim as "Fim de Contrato" 
                                                                FROM compras WHERE "Fim de Contrato" < {ano_hoje}{mes_hoje}{dia_hoje}''')

            hist_serv_window = Tk()
            hist_serv_window.state('zoomed')
            hist_serv_window.title(f'myCrmName  |  CRM - {lista[0]}')

            frame_hist_consult = Frame(hist_serv_window)
            frame_hist_consult.pack(side=TOP)
            entry_hist = Entry(frame_hist_consult, width=50)
            entry_hist.grid(row=0, column=1, sticky=N + S)

            tv_frame = Frame(hist_serv_window)

            tv_hist = ttk.Treeview(tv_frame,
                                   columns=(
                                       'ID', 'cliente', 'servico', 'perfil', 'pagamento', 'fim de contrato'),
                                   show='headings', style='Treeview')
            # Estilo
            style = ttk.Style()
            # Tema
            style.theme_use('clam')
            # Cores
            style.configure("Treeview",
                            background="#bbd3ff",
                            foreground="#bbd3ff",
                            rowheight=25,
                            fieldbackground="#bbd3ff",
                            font='Arial 12')

            tv_hist.column('ID', anchor=CENTER, width=50)
            tv_hist.column('cliente', anchor=CENTER, width=250)
            tv_hist.column('servico', anchor=CENTER, width=500)
            tv_hist.column('perfil', anchor=CENTER, width=250)
            tv_hist.column('pagamento', anchor=CENTER, width=275)
            tv_hist.column('fim de contrato', anchor=CENTER, width=50)

            tv_hist.heading('ID', text='ID', anchor=CENTER)
            tv_hist.heading('cliente', text='Cliente', anchor=CENTER)
            tv_hist.heading('servico', text='Serviço', anchor=CENTER)
            tv_hist.heading('perfil', text='Matriz ou Filial', anchor=CENTER)
            tv_hist.heading('pagamento', text='Pagamento', anchor=CENTER)
            tv_hist.heading('fim de contrato', text='FIM', anchor=CENTER)

            # Barra de rolagem
            barra2 = ttk.Scrollbar(tv_frame, orient='vertical')
            barra2.config(command=tv_hist.yview)
            tv_hist.configure(yscrollcommand=barra2.set)
            barra2.pack(side=RIGHT, fill=Y)

            tv_frame.pack(fill=BOTH, expand=TRUE)
            def consulta_mostratudo():
                tv_hist.delete(*tv_hist.get_children())
                for x in inactiveCustomers:
                    tv_hist.insert('', 'end', values=(x))

            consulta_mostratudo()
            tv_hist.pack(fill=BOTH, expand=TRUE)


            def buscar_hist():

                if len(entry_hist.get()) != 0:
                    and_a2 = dql(f'''SELECT codigo as "ID",
                                                                        clienteid as "Cliente",
                                                                        servicosid as "Serviço",
                                                                        perfilid as "Matriz ou Filial","Interv. "||
                                                                        intervalo ||" " || pagamento ||" de  R$ " || valor as "Pagamento",
                                                                        _fim as "Fim de Contrato" 
                                                                FROM compras WHERE "Fim de Contrato" < {ano_hoje}{mes_hoje}{dia_hoje} 
                                                                    and ("Fim de Contrato" = {entry_hist.get()} or "ID" = {entry_hist.get()} or "Cliente" = "{entry_hist.get()}" or "Matriz ou Filial" = "{entry_hist.get()}" or "Serviço" = "{entry_hist.get()}")''')
                else:
                    and_a2 = inactiveCustomers

                tv_hist.delete(*tv_hist.get_children())
                for c in and_a2:
                    tv_hist.insert('', 'end', values=(c))

            def historico_gerar_pdf():
                Nome_relatorio_a = f'Histórico de Serviços'
                if len(entry_hist.get()) != 0:
                    and_a2 = dql(f'''SELECT codigo as "ID",
                                                                        clienteid as "Cliente",
                                                                        servicosid as "Serviço",
                                                                        perfilid as "Matriz ou Filial","Interv. "||
                                                                        intervalo ||" " || pagamento ||" de  R$ " || valor as "Pagamento",
                                                                        _fim as "Fim de Contrato" 
                                                                FROM compras WHERE "Fim de Contrato" < {ano_hoje}{mes_hoje}{dia_hoje} 
                                                                    and ("Fim de Contrato" = {entry_hist.get()} or "ID" = {entry_hist.get()} or "Cliente" = "{entry_hist.get()}" or "Matriz ou Filial" = "{entry_hist.get()}" or "Serviço" = "{entry_hist.get()}")''')

                else:
                    and_a2 = inactiveCustomers

                doc = SimpleDocTemplate(
                    f'C:\\Users\\{os.getlogin()}\\Downloads\\{dia_mes_ano}  ¬Histórico de Serviços.pdf',
                    pagesize=(letter[0] + 350, letter[1]))
                data = [['ID', 'Cliente', 'Serviço',
                         'Matriz ou Filial', 'Pagamento',
                         'Fim de Contrato', ]]  # give data as lists with lists.

                for i in and_a2:
                    data.append(i)
                table = Table(data)

                tabla_style = TableStyle([
                    ('BACKGROUND', (0, 0), (7, 0), colors.darkcyan),
                    ('BACKGROUND', (0, 0), (0, 0), colors.darkblue),
                    ('BACKGROUND', (0, 1), (0, len(data)), colors.gray),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('TEXTCOLOR', (0, 1), (0, len(data)), colors.white),
                    ('TEXTCOLOR', (0, 0), (7, 0), colors.white),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
                table.setStyle(tabla_style)
                styleSheet = getSampleStyleSheet()

                titulo = Paragraph(f'{Nome_relatorio_a}',
                                   style=styleSheet['Heading1'])
                emptyline = Paragraph(f'       ', style=styleSheet['Heading1'])

                infodoc = Paragraph(f'''Documento gerado às: {hora_minuto_segundo}''',
                                    style=styleSheet['Normal'])

                doc_lenth = Paragraph(f'''Total de Serviços = {len(and_a2)}''',
                                      style=styleSheet['Normal'])
                contato_dev = Paragraph(
                    f'>>>  Algo errado? Reporte através do e-mail: {yourEmailForSupport}',
                    style=styleSheet['Normal'])

                doc.build(
                    [titulo, emptyline, emptyline, emptyline, emptyline, table, infodoc,
                     emptyline, emptyline, doc_lenth, emptyline, contato_dev])
                os.startfile(
                    f'C:\\Users\\{os.getlogin()}\\Downloads\\{dia_mes_ano}  ¬Histórico de Serviços.pdf')


            def deletar_hist():
                vcon.cursor()
                vcon.execute(f"""DELETE FROM compras WHERE _fim < {ano_hoje}{mes_hoje}{dia_hoje} 
                                and (_fim = {entry_hist.get()} or codigo = {entry_hist.get()})""")
                vcon.commit()

                tv_hist.delete(*tv_hist.get_children())
                for x in inactiveCustomers:
                    tv_hist.insert('', 'end', values=(x))

            def deletar_todos_hist():
                vcon.cursor()
                vcon.execute(f"""DELETE FROM compras WHERE _fim < {ano_hoje}{mes_hoje}{dia_hoje}""")
                vcon.commit()

                tv_hist.delete(*tv_hist.get_children())
                for x in inactiveCustomers:
                    tv_hist.insert('', 'end', values=(x))



            lb_consulta_hist = Label(frame_hist_consult, text='Buscar:',
                                     font='Arial 12')
            lb_consulta_hist.grid(row=0, column=0)
            btn_consulta_hist = Button(frame_hist_consult, text='Filtrar 🔎',
                                       bg='#bbd3ff',
                                       command=buscar_hist,
                                       font='Arial 12')
            btn_consulta_hist.grid(row=0, column=2)
            btn_limpa_filtro = Button(frame_hist_consult, text='Remover Filtros',
                                      bg='#bbd3ff',
                                      command=consulta_mostratudo,
                                      font='Arial 12')
            btn_limpa_filtro.grid(row=0, column=3)
            btn_hist_del = Button(frame_hist_consult, text='⛔',
                                  command=deletar_hist,
                                  bg='#ff9774',
                                  font='Arial 12')
            btn_hist_del.grid(row=0, column=4)
            btn_hist_deltodos = Button(frame_hist_consult,
                                       text='Apagar Histórico',
                                       command=deletar_todos_hist,
                                       bg='#ff9774',
                                       font='Arial 12')
            btn_hist_deltodos.grid(row=0, column=5)
            btn_pdf_hist = Button(frame_hist_consult, text='PDF💾',
                                  command=historico_gerar_pdf,
                                  bg='#ffa31a',
                                  font='Arial 12')
            btn_pdf_hist.grid(row=0, column=6)
            lb_consulta_hist = Label(frame_hist_consult, text='Filtre a impressão do PDF como desejar')
            lb_consulta_hist.grid(row=0, column=7)

            hist_serv_window.mainloop()











        btn_n_serv = Button(grade_det_btns, text='➕', command=dml_serv, bg='#a4d49a',
                            font='Arial 12')
        btn_n_serv.grid(row=0, column=3, sticky=W + E)
        btn_search_serv = Button(grade_det_btns, text='🔎', command=search_serv,
                                 bg='#bbd3ff', font='Arial 12')
        btn_search_serv.grid(row=1, column=3, sticky=W + E)
        btn_pdf_serv = Button(grade_det_btns, text='PDF💾', command=pdf_serv,
                              bg='#ffa31a', font='Arial 12')
        btn_pdf_serv.grid(row=1, column=5, sticky=W + E)
        btn_deletar_serv = Button(grade_det_btns, text='⛔', command=delete_serv,
                                  bg='#ff9774', font='Arial 12')
        btn_deletar_serv.grid(row=0, column=4, sticky=W + E)

        btn_deleta_tudo_serv = Button(grade_det_btns, text='Deletar Todos', command=deleta_todos_serv,
                                      bg='#ff9774',
                                      font='Arial 12', width=12)
        btn_deleta_tudo_serv.grid(row=0, column=5, sticky=W + E + N + S)
        btn_mostra_tudo_serv = Button(grade_det_btns, text='🌎', command=mostra_todosserv,
                                      bg='#bbd3ff',
                                      font='Arial 12')
        btn_mostra_tudo_serv.grid(row=1, column=4, sticky=W + E)
        btn_hist_serv = Button(grade_det_btns, text='Histórico ⏳', command=hist_serv,
                               bg='#bbd3ff',
                               font='Arial 12')
        btn_hist_serv.grid(row=0, rowspan=2, column=6, sticky=N + S)

        ############################################################################################################























































        ####Perfil
        # @Perfil graficos

        grafico2 = LabelFrame(graficoall)
        grafico2.pack(fill=BOTH)
        # Grafico Crescimento Empresa
        figura = plt.Figure(figsize=(20, 4), dpi=(100))
        ax2 = figura.add_subplot(111)
        figura.subplots_adjust(left=0.02, bottom=0.062, right=0.993, top=0.926)
        canva2 = FigureCanvasTkAgg(figura, grafico2)
        canva2.get_tk_widget().pack(fill=BOTH, expand=TRUE)

        ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        names = []
        values = []

        def dados_mf():
            data = dql('''SELECT localself as local FROM perfil GROUP BY localself LIMIT 10''')
            data2 = dql('''SELECT COUNT(localself) as quantidade FROM perfil GROUP BY localself LIMIT 10''')
            for i in data:
                names.append(i[0])
            for i in data2:
                values.append(i[0])

        dados_mf()

        ax2.bar(names, values)
        figura.suptitle('TOP 10 Centrais')
        toolbar2 = NavigationToolbar2Tk(canva2, grafico2, pack_toolbar=True)
        toolbar2.update()

        # frame tv matriz e filiais
        y_mafi = 400
        x_mafi = 600
        lbl_mf_bnc = Label(mafi, text=f'🏢',
                           font='Arial 27')
        lbl_mf_bnc.place(x=(1187 + x_mafi), y=(60 + y_mafi))
        lbl_mf_qtd = Label(mafi, text=f'Unidades:  {dql("SELECT COUNT(*) FROM perfil")[0][0]}',
                           font='Arial 15')
        lbl_mf_qtd.place(x=(1150 + x_mafi), y=(120 + y_mafi))

        def mostra_todosperf():
            info.delete(*info.get_children())
            for kkkkkkkk in dql('SELECT * FROM perfil'):
                info.insert('', 'end', values=(kkkkkkkk))
            populador_local_mf()
            txt_Serv_mf.configure(values=lista_perfil)
            txt_lotacao_cargo.configure(values=lista_perfil)
            lbl_mf_qtd.configure(text=f'Unidades:  {dql("SELECT COUNT(*) FROM perfil")[0][0]}')

        lbframe_info = LabelFrame(info_empresa)
        info = ttk.Treeview(lbframe_info,
                            columns=('id', 'nome', 'telefone', 'email', 'site', 'local'),
                            show='headings',
                            height=15)
        info.column('id', anchor=CENTER, width=0)
        info.column('nome', anchor=CENTER, width=250)
        info.column('telefone', anchor=CENTER, width=10)
        info.column('email', anchor=CENTER, width=50)
        info.column('site', anchor=CENTER, width=50)
        info.column('local', anchor=CENTER, width=100)

        info.heading('id', text='ID', anchor=CENTER)
        info.heading('nome', text='NOME', anchor=CENTER)
        info.heading('telefone', text='TELEFONE', anchor=CENTER)
        info.heading('email', text='EMAIL', anchor=CENTER)
        info.heading('site', text='SITE', anchor=CENTER)
        info.heading('local', text='LOCAL', anchor=CENTER)

        mostra_todosperf()

        # Barra de rolagem
        vsb1 = ttk.Scrollbar(lbframe_info, orient='vertical')
        vsb1.config(command=info.yview)
        info.configure(yscrollcommand=vsb1.set)
        vsb1.pack(side=RIGHT, fill=Y)

        def deleta_todos1():
            info.delete(*info.get_children())
            delete_queryperf = 'DELETE FROM perfil WHERE codigo != 1'
            vcon.cursor()
            vcon.execute(delete_queryperf)
            vcon.commit()

            general = db.collection('users') \
                .document(f"{userAuth}") \
                .collection('info').document(f'{userAuth}') \
                .collection('filiais').get()

            for i in general:
                key = i.id
                db.collection('users') \
                    .document(f"{userAuth}") \
                    .collection('info').document(f'{userAuth}') \
                    .collection('filiais').document(key).delete()

            ax2.clear()
            names.clear()
            values.clear()
            dados_mf()
            ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
            ax2.bar(names, values)
            canva2.draw()

            grafico_diag_rplc()
            mostra_todosperf()

        frame_matrizfranc = LabelFrame(info_empresa)
        frame_matrizfranc.pack(fill=BOTH, expand=TRUE)

        lb_IDmf = Label(frame_matrizfranc, text='ID:', font='Arial 12', width=6)
        lb_IDmf.grid(row=0, column=0)
        txt_IDmf = Entry(frame_matrizfranc, font='Arial 15', width=6)
        txt_IDmf.grid(row=1, column=0)

        lb_Nomemf = Label(frame_matrizfranc, text='Nome:', font='Arial 12', width=30)
        lb_Nomemf.grid(row=0, column=1)
        txt_Nomemf = Entry(frame_matrizfranc, font='Arial 15', width=30)
        txt_Nomemf.grid(row=1, column=1)

        lb_Telemf = Label(frame_matrizfranc, text='Telefone:', font='Arial 12', width=17)
        lb_Telemf.grid(row=0, column=2)
        txt_Telemf = Entry(frame_matrizfranc, font='Arial 15', width=17)
        txt_Telemf.grid(row=1, column=2)

        lb_Emailmf = Label(frame_matrizfranc, text='Email:', font='Arial 12', width=35)
        lb_Emailmf.grid(row=0, column=3)
        txt_Emailmf = Entry(frame_matrizfranc, font='Arial 15')
        txt_Emailmf.grid(row=1, column=3, sticky=W + E)

        lb_Sitemf = Label(frame_matrizfranc, text='Site:', font='Arial 12', width=25)
        lb_Sitemf.grid(row=0, column=4)
        txt_Sitemf = Entry(frame_matrizfranc, font='Arial 15', width=25)
        txt_Sitemf.grid(row=1, column=4)

        # @populador
        vsql_locais1 = '''SELECT municipiouf FROM localizacoes'''
        linhasloc1 = dql(vsql_locais1)
        lista_op1 = [r for r, in linhasloc1]

        lb_Localmf = Label(frame_matrizfranc, text='Local:', font='Arial 12', width=35)
        lb_Localmf.grid(row=0, column=5)
        txt_Localmf = ttk.Combobox(frame_matrizfranc, values=lista_op1, font='Arial 15')
        txt_Localmf.grid(row=1, column=5, sticky=W + E)

        def dml1():
            if len(txt_IDmf.get()) != 0 and len(txt_Nomemf.get()) != 0\
                    and len(txt_Localmf.get()) != 0:

                if int(txt_IDmf.get()) == 1:
                    messagebox.showinfo(title='Matriz',
                                        message=f'A Matriz poderá ser deletada apenas no app.')

                    update_p = f'''INSERT OR REPLACE INTO  perfil (codigo,nome,telefone,email,site,localself)

                                            VALUES ({txt_IDmf.get()},"{str(txt_Nomemf.get())}", "+550{txt_Telemf.get()}", "{dql('SELECT email FROM auth')[0][0]}",
                                                    "{str(txt_Sitemf.get())}","{str(txt_Localmf.get())}")'''

                    db.collection('users') \
                        .document(f"{userAuth}") \
                        .collection('info').document(f'{userAuth}') \
                        .set({'matriz': txt_Nomemf.get(),'local': txt_Localmf.get()})
                else:
                    if len(txt_Emailmf.get())==0:
                        update_p = f'''INSERT OR REPLACE INTO  perfil (codigo,nome,telefone,email,site,localself)

                                                                    VALUES ({txt_IDmf.get()},"{str(txt_Nomemf.get())}", "+550{txt_Telemf.get()}", "{dql("SELECT email FROM auth")[0][0]}",
                                                                            "{str(txt_Sitemf.get())}","{str(txt_Localmf.get())}")'''
                    else:
                        update_p = f'''INSERT OR REPLACE INTO  perfil (codigo,nome,telefone,email,site,localself)

                                            VALUES ({txt_IDmf.get()},"{str(txt_Nomemf.get())}", "+550{txt_Telemf.get()}", "{str(txt_Emailmf.get())}",
                                                    "{str(txt_Sitemf.get())}","{str(txt_Localmf.get())}")'''
                    db.collection('users') \
                        .document(f"{userAuth}") \
                        .collection('info').document(f'{userAuth}')\
                        .collection('filiais')\
                        .add({
                        'nomeFilial':txt_Nomemf.get(),'localFilial':txt_Localmf.get()
                        })

                vcon.cursor()
                vcon.execute(update_p)
                vcon.commit()




                ax2.clear()
                names.clear()
                values.clear()
                dados_mf()
                ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
                ax2.bar(names, values)
                canva2.draw()
                lista.clear()
                if len(dql('''SELECT nome FROM perfil WHERE codigo = 1''')) == 0:
                    lista.append('⠀')

                else:
                    lista.append(dql('''SELECT nome FROM perfil WHERE codigo = 1''')[0][0])

                root.title(f'myCrmName  |  CRM - {lista[0]}')
                mostra_todosperf()

                grafico_diag_rplc()
                txt_Nomemf.delete(0, END)
                txt_Localmf.delete(0, END)
                txt_Emailmf.delete(0, END)
                txt_Telemf.delete(0, END)
                txt_Sitemf.delete(0, END)

            else:

                messagebox.showinfo(title='Erro', message='Preencha todos os campos')
            mostra_todosperf()

        def search1():
            info.delete(*info.get_children())
            try:
                if len(txt_Nomemf.get()) != 0:
                    vcon.cursor()
                    search_perfil = vcon.execute(
                        f'''SELECT * FROM perfil WHERE nome like "{txt_Nomemf.get()}%"''')
                    vcon.commit()
                    for i in search_perfil:
                        info.insert('', 'end', values=(i))
                elif len(txt_Localmf.get()) != 0:
                    vcon.cursor()
                    search_perfil = vcon.execute(
                        f'''SELECT * FROM perfil WHERE localself like "{txt_Localmf.get()}%"''')
                    vcon.commit()
                    for i in search_perfil:
                        info.insert('', 'end', values=(i))
                elif len(txt_IDmf.get()) != 0:
                    vcon.cursor()
                    search_perfil = vcon.execute(f'''SELECT * FROM perfil WHERE codigo = {txt_IDmf.get()}''')
                    vcon.commit()
                    for i in search_perfil:
                        info.insert('', 'end', values=(i))
                else:
                    messagebox.showinfo(title='Erro', message='Preencha pelo menos um campo')


            except Error as er:
                messagebox.showerror(title=f'Erro',
                                     message=f'Oops! Não encontramos esse registro 😕\n{str(er)}')

        def delete1():


            if len(txt_IDmf.get()) != 0 and txt_IDmf.get() != '1':
                try:

                    namelocal = dql(f"SELECT nome,localself FROM perfil WHERE codigo = {txt_IDmf.get()}")[0]

                    deletingFB = db.collection('users') \
                        .document(f"{userAuth}") \
                        .collection('info').document(f'{userAuth}') \
                        .collection('filiais')\
                        .get()
                    for i in deletingFB:

                        key = i.id
                        nome = i.to_dict()['nomeFilial']
                        local = i.to_dict()['localFilial']

                        if nome == namelocal[0] and local == namelocal[1]:
                            db.collection('users') \
                                .document(f"{userAuth}") \
                                .collection('info')\
                                .document(f'{userAuth}') \
                                .collection('filiais')\
                                .document(key).delete()




                    vcon.cursor()
                    vcon.execute(f'''DELETE FROM perfil WHERE codigo={txt_IDmf.get()}''')
                    vcon.commit()

                    messagebox.showinfo(message='Deletado com sucesso')
                    txt_IDmf.delete(0, END)
                    txt_Nomemf.delete(0, END)
                    txt_Localmf.delete(0, END)






                    ax2.clear()
                    names.clear()
                    values.clear()
                    dados_mf()
                    ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
                    ax2.bar(names, values)
                    canva2.draw()

                    grafico_diag_rplc()
                except Error as er:
                    messagebox.showinfo(title='Erro', message=f'Algo de errado aconteceu\n Tipo: {str(er)}')
                mostra_todosperf()


            elif len(txt_Nomemf.get()) != 0 and txt_IDmf.get() != '1':
                try:
                    vcon.cursor()
                    confirm = messagebox.askyesno(title='Deletando cadastro',
                                                  message=f'Ao clicar em "sim", você removerá todos os cadastros com nome={str(txt_Nomemf.get())}')
                    if confirm == 1:

                        namelocal = dql(f"SELECT nome FROM perfil WHERE nome LIKE '{str(txt_Nomemf.get())}' AND nome NOT IN (SELECT nome FROM perfil WHERE codigo = 1)")[0]

                        deletingFB = db.collection('users') \
                            .document(f"{userAuth}") \
                            .collection('info').document(f'{userAuth}') \
                            .collection('filiais') \
                            .get()
                        for i in deletingFB:

                            key = i.id
                            nome = i.to_dict()['nomeFilial']

                            if nome == namelocal[0]:
                                db.collection('users') \
                                    .document(f"{userAuth}") \
                                    .collection('info') \
                                    .document(f'{userAuth}') \
                                    .collection('filiais') \
                                    .document(key).delete()

                        vcon.execute(
                            f'''DELETE FROM perfil WHERE nome LIKE "{str(txt_Nomemf.get())}" AND nome NOT IN (SELECT nome FROM perfil WHERE codigo = 1)''')
                        vcon.commit()







                        mostra_todosperf()
                        messagebox.showinfo(message='Deletado com sucesso')
                        txt_IDmf.delete(0, END)
                        txt_Nomemf.delete(0, END)
                        txt_Localmf.delete(0, END)

                        ax2.clear()
                        names.clear()
                        values.clear()
                        dados_mf()
                        ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
                        ax2.bar(names, values)
                        canva2.draw()

                        grafico_diag_rplc()
                    else:
                        pass
                except Error as er:
                    messagebox.showinfo(title='Erro', message=f'Algo de errado aconteceu\n Tipo: {str(er)}')

            else:
                messagebox.showinfo(title='Erro',
                                    message='Certifique-se que digitou todos os campos de maneira correta e que não está tentando remover a matriz.')

        def pdf_mf():

            if len(txt_Localmf.get()) == 0:
                Nome_relatorio = 'Todas as Unidades em Funcionamento'

                x = dql('''SELECT codigo as "ID", nome as "Nome",localself as "Local", telefone as "Telefone",
                                             email as "E-mail", site as "Site" FROM perfil''')

                y = datetime.datetime.now()
                mes_hoje = y.strftime("%m")
                ano_hoje = y.strftime("%Y")
                dia_hoje = y.strftime("%d")

                hora_minuto_segundo = f'{y.strftime("%H")}:{y.strftime("%M")}:{y.strftime("%S")}'
                dia_mes_ano = f'{dia_hoje}-{mes_hoje}-{ano_hoje}'
                mes_ano = f'{mes_hoje}/{ano_hoje}'

                doc = SimpleDocTemplate(
                    f'C:\\Users\\{os.getlogin()}\\Downloads\\{dia_mes_ano}  ¬Relatorio_{Nome_relatorio}.pdf',
                    pagesize=letter)
                data = [
                    ['ID', 'Nome', 'Localização', 'Telefone', 'E-mail', 'Site']]  # give data as lists with lists.

                select_query = x

                for i in select_query:
                    data.append(i)
                table = Table(data)

                tabla_style = TableStyle([
                    ('BACKGROUND', (0, 0), (5, 0), colors.darkcyan),
                    ('BACKGROUND', (0, 0), (0, 0), colors.darkblue),
                    ('BACKGROUND', (0, 1), (0, len(data)), colors.gray),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('TEXTCOLOR', (0, 1), (0, len(data)), colors.white),
                    ('TEXTCOLOR', (0, 0), (5, 0), colors.white),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
                table.setStyle(tabla_style)
                styleSheet = getSampleStyleSheet()

                titulo = Paragraph(f'Relatório de {Nome_relatorio}  ¬ {mes_ano}', style=styleSheet['Heading1'])
                emptyline = Paragraph(f'       ', style=styleSheet['Heading1'])

                infodoc = Paragraph(f'''Documento gerado às: {hora_minuto_segundo}''', style=styleSheet['Normal'])

                doc_lenth = Paragraph(f'''Total de Franquias e Filiais = {len(x) - 1}''',
                                      style=styleSheet['Normal'])
                contato_dev = Paragraph(
                    f'>>>  Algo errado? Reporte através do e-mail: {yourEmailForSupport}',
                    style=styleSheet['Normal'])

                doc.build(
                    [titulo, emptyline, emptyline, emptyline, emptyline, table, infodoc,
                     emptyline, emptyline, doc_lenth, emptyline, contato_dev])
                os.startfile(
                    f'C:\\Users\\{os.getlogin()}\\Downloads\\{dia_mes_ano}  ¬Relatorio_{Nome_relatorio}.pdf')





            else:
                x = dql(f'''SELECT codigo as "ID", nome as "Nome", telefone as "Telefone",
                                              email as "E-mail", site as "Site" FROM perfil WHERE localself ="{txt_Localmf.get()}"''')
                Nome_relatorio = f'Unidades em Funcionamento  ¬{txt_Localmf.get()}'

                y = datetime.datetime.now()
                mes_hoje = y.strftime("%m")
                ano_hoje = y.strftime("%Y")
                dia_hoje = y.strftime("%d")

                hora_minuto_segundo = f'{y.strftime("%H")}:{y.strftime("%M")}:{y.strftime("%S")}'
                dia_mes_ano = f'{dia_hoje}-{mes_hoje}-{ano_hoje}'
                mes_ano = f'{mes_hoje}/{ano_hoje}'

                doc = SimpleDocTemplate(
                    f'C:\\Users\\{os.getlogin()}\\Downloads\\{dia_mes_ano}  ¬Relatorio_{Nome_relatorio}.pdf',
                    pagesize=letter)
                data = [
                    ['ID', 'Nome', 'Telefone', 'E-mail',
                     'Site']]  # give data as lists with lists.

                select_query = x

                for i in select_query:
                    data.append(i)
                table = Table(data)

                tabla_style = TableStyle([
                    ('BACKGROUND', (0, 0), (5, 0), colors.darkcyan),
                    ('BACKGROUND', (0, 0), (0, 0), colors.darkblue),
                    ('BACKGROUND', (0, 1), (0, len(data)), colors.gray),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('TEXTCOLOR', (0, 1), (0, len(data)), colors.white),
                    ('TEXTCOLOR', (0, 0), (5, 0), colors.white),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
                table.setStyle(tabla_style)
                styleSheet = getSampleStyleSheet()

                titulo = Paragraph(f'Relatório de {Nome_relatorio}  ¬ {mes_ano}', style=styleSheet['Heading1'])
                emptyline = Paragraph(f'       ', style=styleSheet['Heading1'])

                infodoc = Paragraph(f'''Documento gerado às: {hora_minuto_segundo}''',
                                    style=styleSheet['Normal'])

                doc_lenth = Paragraph(f'''Total de Franquias e Filiais = {len(x) - 1}''',
                                      style=styleSheet['Normal'])
                contato_dev = Paragraph(
                    '>>>  Algo errado? Reporte através do e-mail: gustavofernandeslobo@gmail.com',
                    style=styleSheet['Normal'])

                doc.build(
                    [titulo, emptyline, emptyline, emptyline, emptyline, table, infodoc,
                     emptyline, emptyline, doc_lenth, emptyline, contato_dev])
                os.startfile(
                    f'C:\\Users\\{os.getlogin()}\\Downloads\\{dia_mes_ano}  ¬Relatorio_{Nome_relatorio}.pdf')

        btn_n_filial = Button(frame_matrizfranc, text='➕', command=dml1, bg='#a4d49a', font='Arial 12')
        btn_n_filial.grid(row=0, column=6)
        btn_search1 = Button(frame_matrizfranc, text='🔎', command=search1, bg='#bbd3ff', font='Arial 12')
        btn_search1.grid(row=1, column=6, sticky=W + E + S + N)
        btn_pdf_mf = Button(frame_matrizfranc, text='💾', command=pdf_mf, bg='#ffa31a', font='Arial 12')
        btn_pdf_mf.grid(row=2, column=6, sticky=W + E + S + N)
        btn_deletar1 = Button(frame_matrizfranc, text='Deletar ⛔', command=delete1, bg='#ff9774',
                              font='Arial 12', width=12)
        btn_deletar1.grid(row=0, column=7)
        lineBtnAll = ["Mostrar Todos", "🌎"]
        btn_mostra_tudo1 = Button(frame_matrizfranc, text=f'{lineBtnAll[1]}\n{lineBtnAll[0]}', command=mostra_todosperf,
                                  bg='#bbd3ff',
                                  font='Arial 12', width=12)
        btn_mostra_tudo1.grid(row=2, column=7)
        btn_deleta_tudo1 = Button(frame_matrizfranc, text='Deletar Todos', command=deleta_todos1, bg='#ff9774',
                                  font='Arial 12', width=12)
        btn_deleta_tudo1.grid(row=1, column=7)

        info.pack(fill=BOTH, expand=TRUE)
        lbframe_info.pack(fill=BOTH)

        ############################################################################################################









































        ####Clientes
        # Cadastrando novo. apenas labels e entrys aqui.
        cadastro = LabelFrame(grade_lateral_dir1, text='👤 Novo Cliente', font='Arial 20', pady=50)
        cadastro.pack(fill=X)

        lb_Codigo1 = Label(cadastro, text='Código: ', font='Arial 15', width=10)
        lb_Codigo1.grid(row=0, column=0)
        txt_Codigo1 = Entry(cadastro, font='Arial 15', width=10)
        txt_Codigo1.grid(row=1, column=0)

        lb_Nome1 = Label(cadastro, text='Nome:', font='Arial 15', width=40)
        lb_Nome1.grid(row=0, column=1)
        txt_Nome1 = Entry(cadastro, font='Arial 15', width=40)
        txt_Nome1.grid(row=1, column=1, sticky=W + E)

        # @populador
        vsql_locais = '''SELECT municipiouf FROM localizacoes'''
        linhasloc = dql(vsql_locais)
        lista_op = [r for r, in linhasloc]

        lb_Local = Label(cadastro, text='Local: ', font='Arial 15')
        lb_Local.grid(row=0, column=2)
        txt_Local = ttk.Combobox(cadastro, values=lista_op, font='Arial 15')
        txt_Local.grid(row=1, column=2)

        lfcont = LabelFrame(cadastro)
        lfcont.grid(row=2, column=1, columnspan=2, sticky=W + E)

        lb_Telcl = Label(lfcont, text='Telefone: ', font='Arial 15')
        lb_Telcl.grid(row=0, column=0)
        txt_Telcl = Entry(lfcont, font='Arial 15')
        txt_Telcl.grid(row=1, column=0)

        lb_Emcl = Label(lfcont, text='Email: ', font='Arial 15')
        lb_Emcl.grid(row=0, column=1)
        txt_Emcl = Entry(lfcont, font='Arial 15', width=40)
        txt_Emcl.grid(row=1, column=1)

        # Treeview
        # tabela treeview
        treeview = ttk.Treeview(grade_lateral_dir1, height=100, style='Treeview')
        treeview['columns'] = ('ID', 'Nome', 'Local', 'Telefone', 'Email')

        # Estilo
        style = ttk.Style()
        # Tema
        style.theme_use('clam')
        # Cores
        style.configure("Treeview",
                        background="#bbd3ff",
                        foreground="#bbd3ff",
                        rowheight=25,
                        fieldbackground="#bbd3ff",
                        font='Arial 12')

        # Barra de rolagem
        vsb = ttk.Scrollbar(grade_lateral_dir1, orient='vertical')
        vsb.config(command=treeview.yview)
        treeview.configure(yscrollcommand=vsb.set)
        vsb.pack(side=RIGHT, fill=Y)
        ###################################################

        treeview.column('ID', anchor=CENTER, width=80)
        treeview.column('Nome', anchor=W, width=250)
        treeview.column('Local', anchor=CENTER, width=250)
        treeview.column('Telefone', anchor=CENTER, width=200)
        treeview.column('Email', anchor=CENTER, width=250)

        treeview.heading('ID', text='ID', anchor=CENTER)
        treeview.heading('Nome', text='Nome', anchor=CENTER)
        treeview.heading('Local', text='Local', anchor=CENTER)
        treeview.heading('Telefone', text='Telefone', anchor=CENTER)
        treeview.heading('Email', text='Email', anchor=CENTER)

        treeview['show'] = 'headings'

        def mostra_todos():

            treeview.delete(*treeview.get_children())
            db_query = 'SELECT codigo, nome, local, telefone, email FROM clientes'
            linhas_clientes_ = dql(db_query)
            for l_cliente in linhas_clientes_:
                treeview.insert('', 'end', values=(l_cliente))

            concl = dql("""SELECT COUNT(clienteid) 
                                        FROM compras WHERE status == "Concluído"
                                        AND (registro_mes_ano NOT NULL OR
                                        _notif_mesano NOT NULL OR
                                        _notif_dia NOT NULL OR
                                        _notif_sem NOT NULL)""")[0][0]
            execu = dql("""SELECT COUNT(clienteid) 
                                        FROM compras WHERE status == "Execução"
                                        AND (registro_mes_ano NOT NULL OR
                                        _notif_mesano NOT NULL OR
                                        _notif_dia NOT NULL OR
                                        _notif_sem NOT NULL)""")[0][0]
            acomp = dql("""SELECT COUNT(clienteid) 
                                        FROM compras WHERE status == "Acompanhamento"
                                        AND (registro_mes_ano NOT NULL OR
                                        _notif_mesano NOT NULL OR
                                        _notif_dia NOT NULL OR
                                        _notif_sem NOT NULL)""")[0][0]
            planej = dql("""SELECT COUNT(clienteid) 
                                        FROM compras WHERE status == "Planejamento"
                                        AND (registro_mes_ano NOT NULL OR
                                        _notif_mesano NOT NULL OR
                                        _notif_dia NOT NULL OR
                                        _notif_sem NOT NULL)""")[0][0]

            progressoRef.update({'concluido': concl,
                                 'execucao': execu,
                                 'acompanhamento': acomp,
                                 'planejamento': planej})



        mostra_todos()

        treeview.pack(fill=X)

        # Botões & Gráficos
        lbl_ferram = Label(clientes, text='🛠 Ferramentas',
                           font='Arial 25')
        lbl_ferram.place(x=1530, y=10)

        url_zap_btn = 'link.png'
        responsezap = requests.get(url_zap_btn, stream=True)
        with open('btn_zap.png', 'wb') as out_file1:
            shutil.copyfileobj(responsezap.raw, out_file1)

        def abrindo_zap():
            os.system("start \"\" https://web.whatsapp.com")

        url_zap_cnv = 'link.png'
        responsecnv = requests.get(url_zap_cnv, stream=True)
        with open('btn_cnv.png', 'wb') as out_filecnv:
            shutil.copyfileobj(responsecnv.raw, out_filecnv)

        def abrindo_cnv():
            os.system("start \"\" https://www.canva.com/pt_br/")

        url_site_btn = 'link.png'
        responsesite = requests.get(url_site_btn, stream=True)
        with open('btn_site.png', 'wb') as out_filesite:
            shutil.copyfileobj(responsesite.raw, out_filesite)

        def abrindo_site():
            if len(dql('SELECT site FROM perfil WHERE codigo = 1')[0][0]) != 0:
                try:
                    os.system(f"start \"\" {dql('SELECT site FROM perfil WHERE codigo = 1')[0][0]}")
                except:
                    messagebox.showerror(title=f'Erro ao tentar abrir o site',
                                         message=f"Não foi possível abrir o endereço da matriz solicitado. Corrija-o na aba Franquias e Filiais.\n   >{dql('SELECT site FROM perfil WHERE codigo = 1')[0][0]}")
            else:
                messagebox.showinfo(title='Site não encontrado',
                                    message='Cadastre um site para a sua matriz (código 1).\n   Aba > Franquias e Filiais')

        imgd_btn_zap = ImageTk.PhotoImage(PIL.Image.open('btn_zap.png'))
        btn_zap = Button(clientes, image=imgd_btn_zap, height=50,
                         width=50, bd=0, command=abrindo_zap)
        btn_zap.place(x=1800, y=100)
        os.remove('btn_zap.png')

        imgd_btn_site = ImageTk.PhotoImage(PIL.Image.open('btn_site.png'))
        btn_site = Button(clientes, image=imgd_btn_site, bd=0, command=abrindo_site)
        btn_site.place(x=1630, y=100)
        os.remove('btn_site.png')

        imgd_btn_canva = ImageTk.PhotoImage(PIL.Image.open('btn_cnv.png'))
        btn_canva = Button(clientes, image=imgd_btn_canva, bd=0, command=abrindo_cnv)
        btn_canva.place(x=1450, y=100)
        os.remove('btn_cnv.png')

        lbl_cl_bnc = Label(clientes, text=f'👥',
                           font='Arial 30')
        lbl_cl_bnc.place(x=1190, y=60)
        lbl_cl_qtd = Label(clientes, text=f'Total:  {dql("SELECT COUNT(*) FROM clientes")[0][0]}', font='Arial 25')
        lbl_cl_qtd.place(x=1150, y=120)

        lista_leg1 = []
        clientespmun1 = []

        def grafico_cl():
            list__aux = []
            for i in dql('''SELECT local FROM clientes'''):
                if i[0][0] + i[0][1] not in lista_leg1:
                    lista_leg1.append(i[0][0] + i[0][1])
                list__aux.append(i[0][0] + i[0][1])
            for i in lista_leg1:
                clientespmun1.append(list__aux.count(i))

        grafico_cl()

        ##Grafico
        framegraph = LabelFrame(grade_lateral_dir2)
        framegraph.pack()

        fig = matplotlib.figure.Figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.pie(clientespmun1, autopct='%1.0f%%', textprops={'size': 'x-large', 'color': 'w'})
        ax.legend(lista_leg1, fontsize=8, loc='lower left', bbox_to_anchor=(0.0, 0.0))
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
        circle = matplotlib.patches.Circle((0, 0), 0, color='white')
        ax.add_artist(circle)
        canvas = FigureCanvasTkAgg(fig, master=framegraph)
        canvas.get_tk_widget().pack()
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, framegraph, pack_toolbar=True)
        toolbar.update()

        _cl_atv()

        plt.style.use('fivethirtyeight')
        fig_cl_atv = plt.Figure(figsize=(10, 3), dpi=52)
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

        df_cl_atv = pd.DataFrame(
            {'Ativos': [len(lista_cl_atv)], 'Inativos': [len(lista_cl_int)]})

        progressoRef.update({'ativos':len(lista_cl_atv) ,
                          'inativos': len(lista_cl_int)})


        gs_cl_atv = fig_cl_atv.add_gridspec(1, 1, hspace=0.2)

        ax_cl_atv = fig_cl_atv.add_subplot(gs_cl_atv[0, 0])

        df_cl_atv.plot.barh(stacked=True, ax=ax_cl_atv, edgecolor='white')

        ax_cl_atv.legend(ncol=2)
        plt.legend(fontsize=350)
        ax_cl_atv.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax_cl_atv.xaxis.set_tick_params(labelsize=14)

        canva_cl_atv = FigureCanvasTkAgg(fig_cl_atv, clientes)
        canva_cl_atv.get_tk_widget().place(x=1420, y=770)

        # botoes query.
        def pdf_clientes():
            if len(txt_Local.get()) == 0:
                Nome_relatorio = 'Clientes'

                x = dql('''SELECT codigo as 'ID',nome as '   Nome   ', local as 'Localização',
                                                                        telefone as 'Telefone',email as'E-mail'
                                                                    FROM clientes''')
            else:
                Nome_relatorio = f'Clientes   ¬{txt_Local.get()}'

                x = dql(f'''SELECT codigo as 'ID',nome as '   Nome   ', local as 'Localização',
                                                                                                telefone as 'Telefone',email as'E-mail'
                                                                                            FROM clientes WHERE local = "{txt_Local.get()}"''')

            y = datetime.datetime.now()
            mes_hoje = y.strftime("%m")
            ano_hoje = y.strftime("%Y")
            dia_hoje = y.strftime("%d")

            hora_minuto_segundo = f'{y.strftime("%H")}:{y.strftime("%M")}:{y.strftime("%S")}'
            dia_mes_ano = f'{dia_hoje}-{mes_hoje}-{ano_hoje}'
            mes_ano = f'{mes_hoje}/{ano_hoje}'

            doc = SimpleDocTemplate(
                f'C:\\Users\\{os.getlogin()}\\Downloads\\{dia_mes_ano}  ¬Relatorio_{Nome_relatorio}.pdf',
                pagesize=letter)
            data = [['ID', 'Nome', 'Localização', 'Telefone', 'E-mail']]  # give data as lists with lists.

            select_query = x

            for i in select_query:
                data.append(i)
            table = Table(data)

            tabla_style = TableStyle([
                ('BACKGROUND', (0, 0), (4, 0), colors.darkcyan),
                ('BACKGROUND', (0, 0), (0, 0), colors.darkblue),
                ('BACKGROUND', (0, 1), (0, len(data)), colors.gray),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('TEXTCOLOR', (0, 1), (0, len(data)), colors.white),
                ('TEXTCOLOR', (0, 0), (4, 0), colors.white),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
            table.setStyle(tabla_style)
            styleSheet = getSampleStyleSheet()

            titulo = Paragraph(f'Relatório de {Nome_relatorio}  ¬ {mes_ano}', style=styleSheet['Heading1'])
            emptyline = Paragraph(f'       ', style=styleSheet['Heading1'])

            infodoc = Paragraph(f'''Documento gerado às: {hora_minuto_segundo}''',
                                style=styleSheet['Normal'])

            doc_lenth = Paragraph(f'''Total de clientes = {len(x)}''',
                                  style=styleSheet['Normal'])
            contato_dev = Paragraph(
                f'>>>  Algo errado? Reporte através do e-mail: {yourEmailForSupport}',
                style=styleSheet['Normal'])

            doc.build(
                [titulo, emptyline, emptyline, emptyline, emptyline, table, infodoc,
                 emptyline, emptyline, doc_lenth, emptyline, contato_dev])
            os.startfile(
                f'C:\\Users\\{os.getlogin()}\\Downloads\\{dia_mes_ano}  ¬Relatorio_{Nome_relatorio}.pdf')

        def dml():
            if len(txt_Codigo1.get()) != 0 and len(txt_Nome1.get()) != 0 and len(txt_Local.get()) != 0:

                query = f'''INSERT OR REPLACE INTO clientes (codigo, nome, local, telefone, email) VALUES ("{str(txt_Codigo1.get())}", "{str(txt_Nome1.get())}", "{str(txt_Local.get())}","{str(txt_Telcl.get())}","{str(txt_Emcl.get())}")'''
                vcon.cursor()
                vcon.execute(query)
                vcon.commit()
                clientespmun1.clear()
                lista_leg1.clear()
                grafico_cl()
                ax.clear()
                ax.pie(clientespmun1, autopct='%1.0f%%', textprops={'size': 'x-large', 'color': 'w'})
                ax.legend(lista_leg1, fontsize=8, loc='lower left', bbox_to_anchor=(0.0, 0.0))
                ax.add_artist(circle)
                canvas.draw()

                txt_Codigo1.delete(0, END)
                txt_Nome1.delete(0, END)
                txt_Local.delete(0, END)
                txt_Telcl.delete(0, END)
                txt_Emcl.delete(0, END)
                mostra_todos()
                lbl_cl_qtd.configure(text=f'Clientes:  {dql("SELECT COUNT(*) FROM clientes")[0][0]}', font='Arial 25')
                _cl_atv()
                ax_cl_atv.clear()
                pd.DataFrame(
                    {'Ativos': [len(lista_cl_atv)], 'Inativos': [len(lista_cl_int)]}).plot.barh(stacked=True,
                                                                                                ax=ax_cl_atv,
                                                                                                edgecolor='white')
                progressoRef.update({'ativos': len(lista_cl_atv),
                                     'inativos': len(lista_cl_int)})
                ax_cl_atv.xaxis.set_major_locator(MaxNLocator(integer=True))
                ax_cl_atv.legend(ncol=2)
                plt.legend(fontsize=50)
                canva_cl_atv.draw()
                populando_servicos()
                txt_Serv_cliente.configure(values=lista_clientes)

            else:

                messagebox.showinfo(title='Erro', message='Preencha todos os campos')
            mostra_todos()

        def deleta_todos():
            query = f'''DELETE FROM clientes'''
            vcon.cursor()
            try:
                confirm = messagebox.askyesno(title='Deletando um cliente',
                                              message='Deseja realmente remover TODOS os registros de clientes?')
                if confirm == 1:
                    vcon.execute(query)
                    vcon.commit()

                    clientespmun1.clear()
                    lista_leg1.clear()
                    grafico_cl()
                    ax.clear()
                    ax.pie(clientespmun1, autopct='%1.0f%%', textprops={'size': 'x-large', 'color': 'w'})
                    ax.legend(lista_leg1, fontsize=8, loc='lower left', bbox_to_anchor=(0.0, 0.0))
                    ax.add_artist(circle)
                    canvas.draw()
                    mostra_todos()
                    lbl_cl_qtd.configure(text=f'Clientes:  {dql("SELECT COUNT(*) FROM clientes")[0][0]}',
                                         font='Arial 25')
                    _cl_atv()
                    ax_cl_atv.clear()
                    pd.DataFrame(
                        {'Ativos': [len(lista_cl_atv)], 'Inativos': [len(lista_cl_int)]}).plot.barh(stacked=True,
                                                                                                    ax=ax_cl_atv,
                                                                                                    edgecolor='white')
                    progressoRef.update({'ativos': len(lista_cl_atv),
                                         'inativos': len(lista_cl_int)})
                    ax_cl_atv.xaxis.set_major_locator(MaxNLocator(integer=True))
                    ax_cl_atv.legend(ncol=2)
                    plt.legend(fontsize=50)
                    canva_cl_atv.draw()
                    populando_servicos()
                    txt_Serv_cliente.configure(values=lista_clientes)
                else:
                    pass
            except Error as er:
                messagebox.showinfo(title='Erro', message=f'Algo de errado aconteceu\n Tipo: {str(er)}')

            txt_Codigo1.delete(0, END)
            txt_Nome1.delete(0, END)
            txt_Local.delete(0, END)

        def search():
            treeview.delete(*treeview.get_children())
            try:
                if len(txt_Nome1.get()) != 0:
                    vcon.cursor()
                    db_query2 = vcon.execute(
                        f'''SELECT codigo,nome,local,telefone,email FROM clientes WHERE nome like "{txt_Nome1.get()}%"''')
                    vcon.commit()
                    linhas = db_query2
                    for i in linhas:
                        treeview.insert('', 'end', values=(i))
                elif len(txt_Codigo1.get()) != 0:
                    vcon.cursor()
                    db_query2 = vcon.execute(
                        f'''SELECT codigo,nome,local,telefone,email FROM clientes WHERE codigo = {txt_Codigo1.get()}''')
                    vcon.commit()
                    linhas = db_query2
                    for i in linhas:
                        treeview.insert('', 'end', values=(i))
                elif len(txt_Local.get()) != 0:
                    vcon.cursor()
                    db_query2 = vcon.execute(
                        f'''SELECT codigo,nome,local,telefone,email FROM clientes WHERE local like "{txt_Local.get()}%"''')
                    vcon.commit()
                    linhas = db_query2
                    for i in linhas:
                        treeview.insert('', 'end', values=(i))
                else:

                    messagebox.showinfo(title='Erro', message='Preencha pelo menos um campo')


            except Error as er:
                messagebox.showerror(title=f'Erro',
                                     message=f'Oops! Não encontramos nenhum cliente com esse registro 😕\n{str(er)}')

        def delete():
            if len(txt_Codigo1.get()) != 0:
                try:
                    vcon.cursor()
                    confirm = messagebox.askyesno(title='Deletando um cliente',
                                                  message=f'Deseja realmente remover o cliente de ID:{str(txt_Codigo1.get())}?')
                    if confirm == 1:
                        vcon.execute(f'''DELETE FROM clientes WHERE codigo="{str(txt_Codigo1.get())}"''')
                        vcon.commit()
                        messagebox.showinfo(message='Cliente deletado com sucesso')
                        mostra_todos()

                        clientespmun1.clear()
                        lista_leg1.clear()
                        grafico_cl()
                        ax.clear()
                        ax.pie(clientespmun1, autopct='%1.0f%%', textprops={'size': 'x-large', 'color': 'w'})
                        ax.legend(lista_leg1, fontsize=8, loc='lower left', bbox_to_anchor=(0.0, 0.0))
                        ax.add_artist(circle)
                        canvas.draw()
                        lbl_cl_qtd.configure(text=f'Clientes:  {dql("SELECT COUNT(*) FROM clientes")[0][0]}',
                                             font='Arial 25')

                    else:
                        pass
                except Error as er:
                    messagebox.showinfo(title='Erro', message=f'Algo de errado aconteceu\n Tipo: {str(er)}')


            elif len(txt_Nomemf.get()) != 0:
                try:
                    vcon.cursor()
                    confirm = messagebox.askyesno(title='Deletando clientes',
                                                  message=f'Ao clicar em "sim", você removerá todos os clientes cadastrados com nome={str(txt_Nome1.get())}')
                    if confirm == 1:
                        vcon.execute(f'''DELETE FROM clientes WHERE nome="{str(txt_Nome1.get())}"''')
                        vcon.commit()
                        messagebox.showinfo(message='Cliente(s) deletado(s) com sucesso')
                        mostra_todos()
                    else:
                        pass
                except Error as er:
                    messagebox.showinfo(title='Erro', message=f'Algo de errado aconteceu\n Tipo: {str(er)}')
            else:
                messagebox.showinfo(title='Erro',
                                    message='Digite o código de registro ou o nome do cliente que deseja remover')

            txt_Codigo1.delete(0, END)
            txt_Nome1.delete(0, END)
            txt_Local.delete(0, END)

            _cl_atv()
            ax_cl_atv.clear()
            pd.DataFrame(
                {'Ativos': [len(lista_cl_atv)], 'Inativos': [len(lista_cl_int)]}).plot.barh(stacked=True,
                                                                                            ax=ax_cl_atv,
                                                                                            edgecolor='white')
            progressoRef.update({'ativos': len(lista_cl_atv),
                                 'inativos': len(lista_cl_int)})
            ax_cl_atv.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax_cl_atv.legend(ncol=2)
            plt.legend(fontsize=50)
            canva_cl_atv.draw()
            populando_servicos()
            txt_Serv_cliente.configure(values=lista_clientes)

        btn_n_cliente = Button(cadastro, text='➕', command=dml, bg='#a4d49a', font='Arial 12')
        btn_n_cliente.grid(row=0, column=5)
        btn_search = Button(cadastro, text='🔎', command=search, bg='#bbd3ff', font='Arial 12')
        btn_search.grid(row=1, column=5, sticky=W + E)
        btn_deletar = Button(cadastro, text='⛔', command=delete, bg='#ff9774', font='Arial 12')
        btn_deletar.grid(row=0, column=6)
        btn_mostra_tudo = Button(cadastro, text='🌎', command=mostra_todos, bg='#bbd3ff',
                                 font='Arial 12')
        btn_mostra_tudo.grid(row=1, column=6, sticky=W + E)
        btn_deleta_tudo = Button(cadastro, text='Deletar Todos', command=deleta_todos, bg='#ff9774',
                                 font='Arial 12', width=12)
        btn_deleta_tudo.grid(row=0, column=7)
        btn_clientes_pdf = Button(cadastro, text='PDF 💾', command=pdf_clientes, bg='#ffa31a',
                                  font='Arial 12', width=12)
        btn_clientes_pdf.grid(row=1, column=7)

        ############################################################################################################
        def on_closing():
            root.quit()

        os.remove('btn_off.png'), os.remove('btn_on.png'), os.remove('logo.png')
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

    janela = Tk()
    janela.title('Login')

    janela.eval('tk::PlaceWindow . center')
    janela.resizable(FALSE, FALSE)

    url = 'myCRMOnlineUrlLogo.png'
    response = requests.get(url, stream=True)
    with open('logo.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)









    icone_ = PhotoImage(file='logo.png')
    janela.iconphoto(False, icone_)
    os.remove('logo.png')

    # textos
    lb1 = Label(janela, text='E-mail:',font='Arial 12')
    lb1.grid(row=0, column=0,sticky=W)
    lb2 = Label(janela, text='Senha:',font='Arial 12')
    lb2.grid(row=1, column=0,sticky=W)

    # caixas
    ed1 = Entry(janela,width=30)
    ed1.grid(row=0, column=1)
    ed2 = Entry(janela, show='*',width=30)
    ed2.grid(row=1, column=1)

    mensagem = StringVar()
    mensagem.set('Efetue seu Login')
    lb4 = Label(janela, textvariable=mensagem,font='Arial 10')
    lb4.grid(row=2, column=1)



    def on_closing_janela():
        janela.quit()

    def click_auth():


        try:
            email = ed1.get().lower().replace(" ", "")
            password = ed2.get().lower().replace(" ", "")
            user = auth.sign_in_with_email_and_password(email, password)



            vcon.cursor()
            vcon.execute(f"""INSERT INTO auth (auth,token,email)  
                            VALUES ('{user['localId'][15:]}','{user["idToken"]}','{email}')""")
            vcon.commit()



            mensagem.set('Logado com sucesso!')
            # Limpando Entry Boxes
            ed1.delete(0, END)
            ed2.delete(0, END)
            # Destruindo Janela
            janela.destroy()



            main_crm()

        except:
            mensagem.set('Email ou Senha incorretos')


    def click_n_pass():
        if len(ed1.get()) != 0:
            auth.send_password_reset_email(ed1.get())
            mensagem.set('Foi enviado um e-mail para redefinição.')



    url_login = 'link.png'
    response_login = requests.get(url_login, stream=True)
    with open('btn_login.png', 'wb') as out_file:
        shutil.copyfileobj(response_login.raw, out_file)
    imgd_btn_login = ImageTk.PhotoImage(PIL.Image.open('btn_login.png'))

    # Botões
    bt1 = Button(janela, command=click_auth,image=imgd_btn_login,bd=0)
    bt1.grid(row=0, column=2,rowspan=2, sticky=N + S)
    bt2 = Button(janela, text='Esqueci minha senha', command=click_n_pass,bg='#bbd3ff')
    bt2.grid(row=2, column=2, sticky=W  + E)



    janela.protocol("WM_DELETE_WINDOW", on_closing_janela)
    os.remove('btn_login.png')
    if len(dql('''SELECT * FROM auth''')) == 0:
        pass
    else:
        janela.destroy()
        main_crm()

    janela.mainloop()



try:
    pasta_crm = os.path.join('C:\\','CRM')
    os.mkdir(pasta_crm)


    ##db_crm
    def conexao_db():
        caminho = f'C:\\CRM\\db_crm.db'
        con = None
        try:
            con = sqlite3.connect(caminho)
        except Error as ex:
            print(ex)
        return con


    vcon = conexao_db()

    vsql = '''
                CREATE TABLE if not exists servicos (
                codigo INTEGER       PRIMARY KEY AUTOINCREMENT,
                tipo   VARCHAR (100) NOT NULL ON CONFLICT IGNORE,
                setor  VARCHAR (50) 
            )'''

    vsql2 = '''
                CREATE TABLE if not exists localizacoes (
                codigo,
                municipio   VARCHAR (100),
                uf          VARCHAR (2),
                lats        VARCHAR (20),
                longs,
                municipiouf PRIMARY KEY
            )'''

    vsql3 = '''
                CREATE TABLE if not exists clientes (
                codigo   INTEGER      NOT NULL
                                      PRIMARY KEY AUTOINCREMENT,
                nome     VARCHAR (50) NOT NULL,
                local                 REFERENCES localizacoes (municipiouf) ON DELETE CASCADE,
                telefone VARCHAR (19),
                email    VARCHAR (50),
                mesano
            )'''

    vsql4 = '''
                CREATE TABLE if not exists compras (
                                                    codigo           INTEGER PRIMARY KEY AUTOINCREMENT
                                                                    NOT NULL ON CONFLICT FAIL,
                                                    clienteid,
                                                    servicosid,
                                                    perfilid,
                                                    pagamento,
                                                    intervalo,
                                                    _fim,
                                                    valor,
                                                    status,
                                                    registro_mes_ano,
                                                    _notif_mesano,
                                                    _notif_dia,
                                                    _notif_sem
            )'''

    vsql5 = '''
                CREATE TABLE if not exists perfil (
                codigo      INTEGER      DEFAULT (0) 
                                     PRIMARY KEY AUTOINCREMENT,
            nome        VARCHAR (50) NOT NULL,
            telefone    VARCHAR (19),
            email       VARCHAR (50),
            site        VARCHAR (50),
            localself                REFERENCES localizacoes (municipiouf) ON DELETE CASCADE,
            mesano
            )'''

    vsql6 = '''CREATE TABLE if not exists tasks (
                codigo            INTEGER PRIMARY KEY AUTOINCREMENT,
            emails_compras,
            emails_relatorios,
            fds_off,
            ano,
            clientes,
            perfis,
            feito,
            janeiro,
            fevereiro,
            marco,
            abril,
            maio,
            junho,
            julho,
            agosto,
            setembro,
            outubro,
            novembro,
            dezembro
            )'''

    vsql7 = '''CREATE TABLE IF NOT EXISTS logo(
                codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                imagem BLOP
            )'''

    vsql8 = '''CREATE TABLE IF NOT EXISTS cargos(
                codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                nome, 
                cargo, 
                filial, 
                email, 
                telefone
            )'''

    vsql9 = '''CREATE TABLE auth (
                codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                auth,
                token,
                email
            )'''


    def preparando(conexao, sql):
        try:
            c = conexao.cursor()
            c.execute(sql)
        except Error as ex:
            print(ex)


    preparando(vcon, vsql)
    preparando(vcon, vsql2)
    preparando(vcon, vsql3)
    preparando(vcon, vsql4)
    preparando(vcon, vsql5)
    preparando(vcon, vsql6)
    preparando(vcon, vsql7)
    preparando(vcon, vsql8)
    preparando(vcon,vsql9)


    vcon.cursor()
    vcon.execute(
        f'''INSERT INTO tasks (codigo,emails_compras, emails_relatorios,fds_off)  VALUES (1,1,1,1)''')
    vcon.commit()
    vcon.cursor()
    vcon.execute(f'''INSERT INTO tasks (emails_relatorios,ano,clientes,perfis,feito,
    janeiro,
    fevereiro,
    marco,
    abril,
    maio,
    junho,
    julho,
    agosto,
    setembro,
    outubro,
    novembro,
    dezembro
) VALUES (0,{ano_hoje},0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)''')
    vcon.commit()

    url = 'myCRMOnlineUrlLogo.png'
    response = requests.get(url, stream=True)
    with open('logo.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

    with open('logo.png', 'rb') as arquivo:
        logo = arquivo.read()



    vcon.cursor()
    vcon.execute('''INSERT INTO logo (codigo,imagem)  VALUES (?,?)''',(1,logo))
    vcon.commit()


    def dql(query):  # select
        vcon = conexao_db()
        c = vcon.cursor()
        c.execute(query)
        res = c.fetchall()
        return res


    if len(dql('''SELECT * FROM compras''')) == 0:
        vcon.cursor()
        vcon.execute('''INSERT INTO  compras (
                                                    codigo,
                                                    clienteid,
                                                    servicosid,
                                                    perfilid,
                                                    pagamento,
                                                    intervalo,
                                                    _fim,
                                                    valor,
                                                    status
                                                    )  
            VALUES (1,"Cliente Demonstrativo","Serviço","Empresa","Período",1,99999999,0,"Execução")''')
        vcon.commit()





    #Inserindo Locais
    f_db = firebase.database()
    locais = f_db.child().get()

    from tkinter import ttk

    inserindo_mun = Tk()
    inserindo_mun.title('Preparando a Área de Trabalho')
    inserindo_mun.resizable(FALSE,FALSE)

    def exit():
        "dummy function"
        pass

    inserindo_mun.protocol("WM_DELETE_WINDOW", exit)
    barra = ttk.Progressbar(inserindo_mun, length=100,
                            mode='determinate', orient=HORIZONTAL)
    barra.grid(row=1, column=0, columnspan=2, sticky=W + E)
    variavel_load = StringVar()
    texto_load = Label(inserindo_mun,
                       textvariable=variavel_load,
                       pady=20,padx=20,anchor=NW,font='Arial 10')
    texto_load.grid(row=0,column=0,sticky=W+E)

    import time
    for mun in locais.each():
        vcon.cursor()
        vcon.execute(f'''INSERT INTO localizacoes (codigo,municipio,
                            uf,lats,longs,municipiouf) 
                            VALUES({mun.val()['codigo']},"{mun.val()['Municipio']}","{mun.val()['UF']}",
                                    {mun.val()['lats']},{mun.val()['longs']},"{mun.val()['UF - Municipio']}")''')
        vcon.commit()

        inserindo_mun.update()
        barra['value'] += 0.0179533213644524
        variavel_load.set(f"""Aguarde um instante enquanto preparamos o ambiente de trabalho...\n\n\n{barra['value']:.0f}%""")
    try:
        inserindo_mun.quit()
        inserindo_mun.destroy()
    except:
        inserindo_mun.destroy()
        inserindo_mun.quit()




    inserindo_mun.mainloop()




    os.remove('logo.png')

    config_data = dql('''SELECT _fim,codigo FROM compras''')

    for x in config_data:
        if x[0] < ano_mes_dia_hoje:
            vcon.cursor()
            vcon.execute(f'''UPDATE compras SET status = "Concluído" WHERE codigo = {x[1]}''')
            vcon.commit()
        else:
            pass
    try:
        os.replace(f'C:\\Users\\{os.getlogin()}\\Downloads\\email2.exe', f'C:\\CRM\\email2.exe')
    finally:
        abrir(),os.startfile(f'C:\\CRM\\email2.exe')

except:
    def conexao_db():
        caminho = f'C:\\CRM\\db_crm.db'
        con = None
        try:
            con = sqlite3.connect(caminho)
        except Error as ex:
            print(ex)
        return con


    vcon = conexao_db()
    def dql(query):  # select
        vcon = conexao_db()
        c = vcon.cursor()
        c.execute(query)
        res = c.fetchall()
        return res


    if len(dql('''SELECT * FROM compras'''))==0:
        vcon.cursor()
        vcon.execute('''INSERT INTO  compras (
                                                    codigo,
                                                    clienteid,
                                                    servicosid,
                                                    perfilid,
                                                    pagamento,
                                                    intervalo,
                                                    _fim,
                                                    valor,
                                                    status
                                                    )  
            VALUES (1,"Cliente Demonstrativo","Serviço","Empresa","Período",1,99999999,0,"Execução")''')
        vcon.commit()

    config_data = dql('''SELECT _fim,codigo FROM compras''')

    for x in config_data:
        if x[0] < ano_mes_dia_hoje:
            vcon.cursor()
            vcon.execute(f'''UPDATE compras SET status = "Concluído" WHERE codigo = {x[1]}''')
            vcon.commit()
        else:
            pass
    try:
        os.replace(f'C:\\Users\\{os.getlogin()}\\Downloads\\email2.exe', f'C:\\CRM\\email2.exe')
    finally:
        abrir(),os.startfile(f'C:\\CRM\\email2.exe')
