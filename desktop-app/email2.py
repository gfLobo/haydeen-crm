import datetime
import random
import shutil
import sqlite3
import os
from sqlite3 import Error

import matplotlib
import requests
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
import yagmail
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import squarify  # pip install squarify (algorithm for treemap)


now = datetime.datetime.now()
x = int(now.strftime("%U"))
styleSheet = getSampleStyleSheet()








def conexao_db():
    caminho = f'C:\\CRM\\db_crm.db'
    con=None
    try:
        con = sqlite3.connect(caminho)
    except Error as ex:
        print(ex)
    return con
#db_crm
vcon=conexao_db()
def dql(query):  # select
    vcon = conexao_db()
    c = vcon.cursor()
    c.execute(query)
    res = c.fetchall()
    return res
agenda = dql('''SELECT emails_compras,
    emails_relatorios FROM tasks WHERE codigo=1''')

y = datetime.datetime.now()

# SQL config. data
mes_hoje = int(y.strftime("%m"))
ano_hoje = int(y.strftime("%Y"))
dia_hoje = int(y.strftime("%w")) + 1
dia_hoje_mes = int(y.strftime('%d'))
sem_hoje = int(y.strftime("%U"))
ano_mes_dia_hoje = int(f'{ano_hoje}{y.strftime("%m")}{y.strftime("%d")}')
hora_minuto_segundo = f'{y.strftime("%H")}:{y.strftime("%M")}:{y.strftime("%S")}'
dia_mes_ano = f'{dia_hoje_mes}/{mes_hoje}/{ano_hoje}'
mes_ano = f'{mes_hoje}/{ano_hoje}'




config_data = dql('''SELECT _fim,codigo FROM compras''')

for x in config_data:
    if x[0] < ano_mes_dia_hoje:
        vcon.cursor()
        vcon.execute(f'''UPDATE compras SET status = "Concluído" WHERE codigo = {x[1]}''')
        vcon.commit()
    else:
        pass


config_diag = dql(f'''SELECT ano,clientes,perfis,feito 
                        FROM tasks WHERE codigo ={dql("""SELECT COUNT(*) FROM tasks""")[0][0]}''')

if mes_hoje ==12:
    vcon.cursor()
    vcon.execute(f'''UPDATE tasks SET 
                        clientes = {dql(f"""SELECT COUNT(DISTINCT clienteid) FROM compras 
                                            WHERE status != 'Concluído' AND status !='Apresentação'   
                                            AND (registro_mes_ano NOT NULL 
                                            OR _notif_mesano NOT NULL 
                                            OR _notif_dia NOT NULL 
                                            OR _notif_sem NOT NULL)""")[0][0]},
                        
                        perfis = {dql(f"""SELECT COUNT(DISTINCT localself) FROM perfil """)[0][0]}
                    WHERE codigo ={dql("""SELECT COUNT(*) FROM tasks""")[0][0]} and feito=0''')
    vcon.commit()


feito = dql(f'''SELECT feito FROM tasks WHERE codigo ={dql("""SELECT COUNT(*) FROM tasks""")[0][0]}''')[0][0]



companyName = 'myCompany'
emailCompany = 'your@gmail.com'
passwordCompany = 'yourPassword'





if int(agenda[0][0]) and int(agenda[0][1]) == 0:
    pass
elif dql('''SELECT COUNT (*) FROM perfil''')[0][0]>0:
    # SQL's emails hoje
    emails_compras_mes = dql(f'''SELECT     codigo,
                                                clienteid,
                                                servicosid,
                                                perfilid,
                                                pagamento,
                                                intervalo,
                                                _fim,
                                                valor,
                                                _notif_mesano
                                    FROM compras 
                                        WHERE pagamento = "Mensal" 
                                        and _notif_mesano = {mes_hoje} 
                                        and _fim >= {ano_mes_dia_hoje} 
                                        and status != "Apresentação" or "Planejamento"''')
    emails_compras_ano = dql(f'''SELECT     codigo,
                                                clienteid,
                                                servicosid,
                                                perfilid,
                                                pagamento,
                                                intervalo,
                                                _fim,
                                                valor,
                                                _notif_mesano
                                    FROM compras WHERE pagamento = "Anual" and _notif_mesano = {ano_hoje} and _fim >= {ano_mes_dia_hoje} and status != "Apresentação" or "Planejamento"''')
    emails_compras_dia = dql(f'''SELECT     codigo,
                                                clienteid,
                                                servicosid,
                                                perfilid,
                                                pagamento,
                                                intervalo,
                                                _fim,
                                                valor,
                                                _notif_dia
                                    FROM compras WHERE pagamento = "Diário" and _notif_dia = {dia_hoje} and _fim >= {ano_mes_dia_hoje} and status != "Apresentação" or "Planejamento"''')
    emails_compras_sem = dql(f'''SELECT     codigo,
                                                clienteid,
                                                servicosid,
                                                perfilid,
                                                pagamento,
                                                intervalo,
                                                _fim,
                                                valor,
                                                _notif_sem
                                    FROM compras WHERE pagamento = "Semanal" and _notif_sem = {sem_hoje} and _fim >= {ano_mes_dia_hoje}  and status != "Apresentação" or "Planejamento"''')




    #Logo Company
    url = 'myCRMOnlineUrlLogo.png'
    response = requests.get(url, stream=True)
    with open('logo.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

    with open('logo.png', 'rb') as arquivo:
        logo = arquivo.read()


    if agenda[0][0] > 0:
        dentro = []



        if len(emails_compras_ano) > 0:
            try:
                yag = yagmail.SMTP(emailCompany, passwordCompany)
            except:
                pass
            pagamentos = pd.read_sql(f'''SELECT clienteid as "Cliente   ", "R$ " || valor as "   Valor   ", _fim as "   Término Contratual   ", intervalo as "   Intervalo de Pagamento   " 
                                            FROM compras WHERE pagamento="Anual" and _notif_mesano = {ano_hoje} and _fim >= {ano_mes_dia_hoje}''',
                                     vcon)
            email = f'''Aqui estão os pagamentos referentes a este ano:\n'''




            rodape = '''Para maiores informações, entre em contato através deste email.'''
            try:
                yag.send(dql('''SELECT email FROM perfil WHERE codigo = 1''')[0][0],
                     f'Relação de valores a receber por contratos anuais -  {ano_hoje}',
                     (email, pagamentos,'logo.png', rodape))
            except:
                pass

            for cadaum in emails_compras_ano:
                vcon.cursor()
                if mes_hoje == 1:
                    diag_mes = 'janeiro'
                elif mes_hoje == 2:
                    diag_mes = 'fevereiro'
                elif mes_hoje == 3:
                    diag_mes = 'marco'
                elif mes_hoje == 4:
                    diag_mes = 'abril'
                elif mes_hoje == 5:
                    diag_mes = 'maio'
                elif mes_hoje == 6:
                    diag_mes = 'junho'
                elif mes_hoje == 7:
                    diag_mes = 'julho'
                elif mes_hoje == 8:
                    diag_mes = 'agosto'
                elif mes_hoje == 9:
                    diag_mes = 'setembro'
                elif mes_hoje == 10:
                    diag_mes = 'outubro'
                elif mes_hoje == 11:
                    diag_mes = 'novembro'
                else:
                    diag_mes = 'dezembro'
                vcon.execute(
                    f"""UPDATE tasks SET {diag_mes}={int(cadaum[7]) + int(dql(f'''SELECT {diag_mes} FROM tasks WHERE codigo ={dql('SELECT COUNT(*) FROM tasks')[0][0]}''')[0][0])}   
                                                                 WHERE codigo={dql('''SELECT COUNT(*) FROM tasks''')[0][0]}""")
                vcon.commit()
                vcon.cursor()
                vcon.execute(
                    f'''UPDATE compras SET _notif_mesano = {ano_hoje + cadaum[5]} WHERE pagamento = "Anual" and codigo = "{cadaum[0]}" and _fim >= {ano_mes_dia_hoje}''')
                vcon.commit()

            dentro.append(1)

        if len(emails_compras_mes) > 0:
            try:
                yag = yagmail.SMTP(emailCompany, passwordCompany)
            except:
                pass
            pagamentos = pd.read_sql(f'''SELECT clienteid as "Cliente   ", "R$ " || valor as "   Valor   ", _fim as "   Término Contratual   ", intervalo as "   Intervalo de Pagamento   " 
                FROM compras WHERE pagamento="Mensal" and _notif_mesano = {mes_hoje} and _fim >= {ano_mes_dia_hoje}''',
                                     vcon)

            email = f'''Aqui estão os pagamentos referentes a este mês:\n'''

            rodape = '''Para maiores informações, entre em contato através deste email.'''


            try:
                yag.send(dql('''SELECT email FROM perfil WHERE codigo = 1''')[0][0],
                     f'Relação de valores a receber no mês: {mes_hoje}/{ano_hoje}', (email, pagamentos,'logo.png', rodape))
            except:
                pass

            for cadaum in emails_compras_mes:
                vcon.cursor()
                if mes_hoje == 1:
                    diag_mes = 'janeiro'
                elif mes_hoje == 2:
                    diag_mes = 'fevereiro'
                elif mes_hoje == 3:
                    diag_mes = 'marco'
                elif mes_hoje == 4:
                    diag_mes = 'abril'
                elif mes_hoje == 5:
                    diag_mes = 'maio'
                elif mes_hoje == 6:
                    diag_mes = 'junho'
                elif mes_hoje == 7:
                    diag_mes = 'julho'
                elif mes_hoje == 8:
                    diag_mes = 'agosto'
                elif mes_hoje == 9:
                    diag_mes = 'setembro'
                elif mes_hoje == 10:
                    diag_mes = 'outubro'
                elif mes_hoje == 11:
                    diag_mes = 'novembro'
                else:
                    diag_mes = 'dezembro'
                vcon.execute(
                    f"""UPDATE tasks SET {diag_mes}={int(cadaum[7]) + int(dql(f'''SELECT {diag_mes} FROM tasks WHERE codigo ={dql('SELECT COUNT(*) FROM tasks')[0][0]}''')[0][0])}   
                                                 WHERE codigo={dql('''SELECT COUNT(*) FROM tasks''')[0][0]}""")
                vcon.commit()
                if mes_hoje + cadaum[5] > 12:
                    mes_prox = mes_hoje - 12
                else:
                    mes_prox = mes_hoje
                vcon.cursor()
                vcon.execute(f'''UPDATE compras SET _notif_mesano = {mes_prox + cadaum[5]} 
                                        WHERE pagamento = "Mensal" and codigo = "{cadaum[0]}" and _fim >= {ano_mes_dia_hoje}''')
                vcon.commit()

            dentro.append(1)

        if len(emails_compras_sem) > 0:

            try:
                yag = yagmail.SMTP(emailCompany, passwordCompany)
            except:
                pass


            pagamentos = pd.read_sql(
                f'''SELECT clienteid as "Cliente   ", "R$ " || valor as "   Valor   ", _fim as "   Término Contratual   ", intervalo as "   Intervalo de Pagamento   " 
                                FROM compras WHERE pagamento="Semanal" and _notif_sem = {sem_hoje} and _fim >= {ano_mes_dia_hoje}''',
                vcon)
            email = f'''Aqui estão os pagamentos da semana.\n'''
            rodape = '''Para maiores informações, entre em contato através deste email.'''


            try:
                yag.send(dql('''SELECT email FROM perfil WHERE codigo = 1''')[0][0],
                     f'Relação de valores a receber da semana:',
                     (email, pagamentos,'logo.png', rodape))
            except:
                pass



            for cadaum in emails_compras_sem:
                vcon.cursor()
                if mes_hoje == 1:
                    diag_mes = 'janeiro'
                elif mes_hoje == 2:
                    diag_mes = 'fevereiro'
                elif mes_hoje == 3:
                    diag_mes = 'marco'
                elif mes_hoje == 4:
                    diag_mes = 'abril'
                elif mes_hoje == 5:
                    diag_mes = 'maio'
                elif mes_hoje == 6:
                    diag_mes = 'junho'
                elif mes_hoje == 7:
                    diag_mes = 'julho'
                elif mes_hoje == 8:
                    diag_mes = 'agosto'
                elif mes_hoje == 9:
                    diag_mes = 'setembro'
                elif mes_hoje == 10:
                    diag_mes = 'outubro'
                elif mes_hoje == 11:
                    diag_mes = 'novembro'
                else:
                    diag_mes = 'dezembro'
                vcon.execute(
                    f"""UPDATE tasks SET {diag_mes}={int(cadaum[7]) + int(dql(f'''SELECT {diag_mes} FROM tasks WHERE codigo ={dql('SELECT COUNT(*) FROM tasks')[0][0]}''')[0][0])}   
                                                                 WHERE codigo={dql('''SELECT COUNT(*) FROM tasks''')[0][0]}""")
                vcon.commit()
                if sem_hoje + cadaum[5] > 52:
                    sem_prox = sem_hoje - 52
                else:
                    sem_prox = sem_hoje
                vcon.cursor()
                vcon.execute(
                    f'''UPDATE compras SET _notif_sem = {sem_prox + cadaum[5]} WHERE pagamento = "Semanal" and codigo = "{cadaum[0]}" and _fim >= {ano_mes_dia_hoje}''')
                vcon.commit()
            dentro.append(1)

        if len(emails_compras_dia) > 0:
            try:
                yag = yagmail.SMTP(emailCompany, passwordCompany)
            except:
                pass
            pagamentos = pd.read_sql(
                f'''SELECT clienteid as "Cliente   ", "R$ " || valor as "   Valor   ", _fim as "   Término Contratual   ", intervalo as "   Intervalo de Pagamento   " 
                                                FROM compras WHERE pagamento="Diário" and _notif_dia = {dia_hoje} and _fim >= {ano_mes_dia_hoje}''',
                vcon)
            email = f'''Aqui estão os pagamentos do dia.\n'''
            rodape = '''Para maiores informações, entre em contato através deste email.'''
            if dql('SELECT fds_off FROM tasks WHERE codigo=1')[0][0]==1 \
                    and dia_hoje != (1 or 7):
                try:
                    yag.send(dql('''SELECT email FROM perfil WHERE codigo = 1''')[0][0],
                         f'Relação de valores a receber do dia: {dia_hoje_mes}/{mes_hoje}/{ano_hoje}',
                         (email, pagamentos,'logo.png',rodape))
                except:
                    pass
                dentro.append(1)
            else:
                try:
                    yag.send(dql('''SELECT email FROM perfil WHERE codigo = 1''')[0][0],
                             f'Relação de valores a receber do dia: {dia_hoje_mes}/{mes_hoje}/{ano_hoje}',
                             (email, pagamentos, 'logo.png', rodape))
                except:
                    pass
                dentro.append(1)
            for cadaum in emails_compras_dia:
                vcon.cursor()
                if mes_hoje == 1:
                    diag_mes = 'janeiro'
                elif mes_hoje == 2:
                    diag_mes = 'fevereiro'
                elif mes_hoje == 3:
                    diag_mes = 'marco'
                elif mes_hoje == 4:
                    diag_mes = 'abril'
                elif mes_hoje == 5:
                    diag_mes = 'maio'
                elif mes_hoje == 6:
                    diag_mes = 'junho'
                elif mes_hoje == 7:
                    diag_mes = 'julho'
                elif mes_hoje == 8:
                    diag_mes = 'agosto'
                elif mes_hoje == 9:
                    diag_mes = 'setembro'
                elif mes_hoje == 10:
                    diag_mes = 'outubro'
                elif mes_hoje == 11:
                    diag_mes = 'novembro'
                else:
                    diag_mes = 'dezembro'
                vcon.execute(
                    f"""UPDATE tasks SET {diag_mes}={int(cadaum[7]) + int(dql(f'''SELECT {diag_mes} FROM tasks WHERE codigo ={dql('SELECT COUNT(*) FROM tasks')[0][0]}''')[0][0])}   
                                 WHERE codigo={dql('''SELECT COUNT(*) FROM tasks''')[0][0]}""")
                vcon.commit()
                if dia_hoje + int(cadaum[5]) > 7:
                    dia_prox = dia_hoje - 7
                else:
                    dia_prox = dia_hoje
                vcon.cursor()
                vcon.execute(
                    f'''UPDATE compras SET _notif_dia = {dia_prox + int(cadaum[5])} WHERE pagamento = "Diário" and codigo = "{cadaum[0]}" and _fim >= {ano_mes_dia_hoje}''')
                vcon.commit()

        if len(dentro)>0:
            vcon.cursor()
            vcon.execute(f'''UPDATE tasks SET feito=1 WHERE codigo = {dql("""SELECT COUNT(*) FROM tasks""")[0][0]} ''')
            vcon.commit()

            import tkinter as tk

            aviso_relat = tk.Tk()
            aviso_relat.title(f'{companyName} CRM  -  Relatório(s) Enviado(s)')
            aviso_relat.eval('tk::PlaceWindow . center')
            aviso_relat.geometry('500x100')
            aviso_relat.resizable(tk.FALSE, tk.FALSE)
            aviso_relat.protocol("WM_DELETE_WINDOW", aviso_relat.quit)
            simple_text_relat = tk.Label(aviso_relat,
                                   text=f'''Relatório(s) de valores a receber enviados ao e-mail:
            {dql("""SELECT email FROM perfil WHERE codigo = 1""")[0][0]}''')
            simple_text_relat.pack()

            simple_button_relat = tk.Button(aviso_relat, text='OK',font='Arial 12',
                                      bg='#80ccff',command=aviso_relat.quit)
            simple_button_relat.pack(fill=tk.X,side=tk.BOTTOM)
            aviso_relat.mainloop()

    if agenda[0][1] > 0 and mes_hoje == 12 and dql(f'''SELECT emails_relatorios FROM tasks WHERE codigo=(SELECT COUNT(*) FROM tasks)''')[0][0] == 0:
        dados = dql(f'''SELECT ano,clientes,perfis FROM tasks WHERE (ano BETWEEN {ano_hoje  - 5}  AND {ano_hoje} AND ano NOT NULL)''')

        anomf =[]
        qtdmf =[]

        anocli = []
        qtdcli = []
        for x in dados:
            anomf.append(x[0])
            anocli.append(x[0])

            qtdmf.append(x[2])
            qtdcli.append(x[1])

















        # Estilo Gráficos
        plt.style.use('ggplot')
















        #Filiais ao ano
        fig = plt.figure()

        gs = fig.add_gridspec(2, 1, hspace=0.5)
        ax2 = fig.add_subplot(gs[1, 0])
        ax1 = fig.add_subplot(gs[0, 0])

        ax2.grid(True)
        plt.ylabel("Alcance de Municípios",fontdict={'size':7})
        ax2.fill_between(anocli, qtdcli, color=(random.random(),random.random(),random.random()))
        ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax2.set_title(f'Clientes Ativos')

        # Clientes Ativos ao ano
        ax1.fill_between(anomf, qtdmf, color=(random.random(),random.random(),random.random()))
        ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax1.set_title(f'Expansão Empresarial')

        plt.savefig(fname=f'{ano_hoje} - Clientes Ativos & Exp Empresarial.png')
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=






        # Treemap Serviços
        servicos = []
        serv_equal = []
        servicos_query_same = dql('''SELECT servicosid FROM compras WHERE status != "Apresentação"''')
        servicos_query_unic = dql('''SELECT DISTINCT servicosid FROM compras WHERE status != "Apresentação"''')

        for x in servicos_query_unic:
            servicos.append(x[0])

        tamanho_serv = []
        for x in servicos_query_same:
            serv_equal.append(x[0])

        for x in servicos_query_unic:
            tamanho_serv.append(serv_equal.count(f'{x[0]}'))

        fig3, axs3 = plt.subplots(1)
        a = squarify.plot(sizes=tamanho_serv, label= servicos,alpha=0.5)
        plt.axis('off')
        fig3.suptitle(f'Serviços Ativos')

        serv = plt.savefig(fname=f'{ano_hoje} - Serviços.png')
        #-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
























        #Atividade Serviço
        fig_at_serv = plt.Figure(figsize=(8,3),dpi=90)
        ax_at_serv = fig_at_serv.add_subplot(111)

        legenda_ativ = ["Apresentação","Planejamento",'Execução','Acompanhamento','Concluído']
        qtd_ativ = []

        for i in legenda_ativ:
            qtd_ativ.append(dql(f"""SELECT COUNT(*) FROM compras WHERE status = '{i}'""")[0][0])




        ax_at_serv.bar(legenda_ativ, qtd_ativ, color=(random.random(),random.random(),random.random()))
        fig_at_serv.suptitle('Atividade dos Serviços')
        ax_at_serv.yaxis.set_major_locator(MaxNLocator(integer=True))
        fig_at_serv.savefig(f'{ano_hoje} - Atividade dos Serviços.png')







        # Montante
        figura_montante = plt.Figure()
        ax_mont = figura_montante.add_subplot(111)

        meses_mont = ["Jan", 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                      'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        values_mont = []
        lista_novo_ano = []


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
                                            FROM tasks WHERE ano={ano_hoje - 1}''')[0]:
                lista_novo_ano.append(i)

        dados_mont()

        ax_mont.plot(meses_mont, values_mont)
        ax_mont.plot(meses_mont, lista_novo_ano)
        ax_mont.legend(labels=(f'{ano_hoje}', f'{dql(f"SELECT ano FROM tasks WHERE codigo=(SELECT COUNT(*) - 1 FROM tasks)")[0][0]}'), ncol=2)

        figura_montante.suptitle(f'{ano_hoje} ¬   Total = R$ {sum(values_mont)}')
        figura_montante.subplots_adjust(left=0.086, bottom=0.067, right=0.988, top=0.93)
        figura_montante.savefig(f'{ano_hoje} - Montante.png')





















        lista_pgmnts = []


        def pgmt_():
            lista_pgmnts.clear()
            for i in dql('''SELECT pagamento FROM compras WHERE status != "Concluído"'''):
                lista_pgmnts.append(i[0])


        pgmt_()
        fig_pgmt, ax_pgmt = plt.subplots(nrows=2, ncols=1)
        df = pd.DataFrame({'Mensal': [lista_pgmnts.count('Mensal')], 'Semanal': [lista_pgmnts.count('Semanal')]})
        df2 = pd.DataFrame({'Anual': [lista_pgmnts.count('Anual')], 'Diário': [lista_pgmnts.count('Diário')]})

        df.plot.barh(stacked=True, ax=ax_pgmt[0], edgecolor='white')
        df2.plot.barh(stacked=True, ax=ax_pgmt[1], edgecolor='white')

        ax_pgmt[1].legend(ncol=2,prop={'size': 17})
        ax_pgmt[0].legend(ncol=2,prop={'size': 17})

        ax_pgmt[0].xaxis.set_major_locator(MaxNLocator(integer=True))
        ax_pgmt[1].xaxis.set_major_locator(MaxNLocator(integer=True))

        ax_pgmt[0].xaxis.set_tick_params(labelsize=24)
        ax_pgmt[1].xaxis.set_tick_params(labelsize=24)

        fig_pgmt.subplots_adjust(left=0.05, right=1,top=1)
        for i in ax_pgmt:
            i.set_yticks([])

        fig_pgmt.savefig(f'{ano_hoje} - Pagamentos.png')























        ##Local
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

        fig_locs, ax_locs = plt.subplots(figsize=(5, 5))
        ax_locs.pie(clientespmun1, autopct='%1.0f%%', textprops={'size': 'x-large', 'color': 'w'})
        ax_locs.legend(lista_leg1, fontsize=10.5, loc='lower left', bbox_to_anchor=(0.0, 0.0))
        fig_locs.subplots_adjust(left=0, bottom=0, right=1, top=1)
        circle_locs = matplotlib.patches.Circle((0, 0), 0, color='white')
        ax_locs.add_artist(circle_locs)
        fig_locs.savefig(f'{ano_hoje} - Locais.png')





















        #PDF Diagnóstico
        grafico_mf_cl = f'{ano_hoje} - Clientes Ativos & Exp Empresarial.png'
        grafico_t_serv = f'{ano_hoje} - Serviços.png'
        grafico_mont = f'{ano_hoje} - Montante.png'
        grafico_pgmts = f'{ano_hoje} - Pagamentos.png'
        grafico_atividade = f'{ano_hoje} - Atividade dos Serviços.png'
        grafico_locais = f'{ano_hoje} - Locais.png'



        if dql('''SELECT COUNT(*) FROM tasks''')[0][0]>2:
            y_grade1 =390
            x_grade1 = 85
            resize_grade1 = 100
            x_grade2 = 120
            resize_atv = 50
            resize_pgmts = 100
            x_t_pg = 30
            c = Canvas(
                f'C:\\Users\\{os.getlogin()}\\Downloads\\Diagnóstico empresarial - {ano_hoje}.pdf',
                pagesize=((792.0 + 100), (612.0 + 100)))

            c.bezier(x1=-150, y1=800, x2=250, y2=(15 * 27), x3=500, y3=(25 * 27), x4=1500, y4=1000)
            c.drawImage(image=grafico_t_serv,x=(445 + x_t_pg),y=322,height=((380 + 20) - resize_grade1),width=((445 + 50) - resize_grade1))
            c.drawImage(image=grafico_mf_cl,x=((30 + 50) - x_grade1),y=220,height=(480 - resize_grade1),width=(580 - resize_grade1))
            c.drawImage(image=grafico_atividade, x=-3, y=20, height=(250 - resize_atv), width=(533 - resize_atv))
            c.drawImage(image=grafico_mont,x=460,y=20,height=190,width=400)
            c.drawImage(image=grafico_pgmts,x=(605 + x_t_pg),y=225,height=(230 - resize_pgmts) ,width= (320 - resize_pgmts))
            c.drawImage(image=grafico_locais,x=(467 + x_t_pg),y=215,height=(240 - resize_pgmts) ,width= (240 - resize_pgmts))
            c.drawImage(image='logo.png',x=0,y=612, height=100, width=100)
            c.setFont('Helvetica', 15)
            c.drawString(x=130, y=665, text=f'Diagnóstico empresarial - {ano_hoje}')
            c.setFont('Helvetica', 10)
            c.drawString(x=130, y=640, text=f'CRM   by {companyName}')
            c.drawString(text=f'''Documento gerado às: {hora_minuto_segundo}. Data: {dia_mes_ano}''',x=(130 * 5), y=5)
            c.circle(x_cen=150,y_cen=1110,r=500,stroke=1,fill=0)
            c.bezier(x1=-100, y1=900, x2=250, y2=570, x3=500, y3=650, x4=1000, y4=900)

            c.save()


            # E-mail
            try:
                yag = yagmail.SMTP(emailCompany, passwordCompany)
            except:
                pass

            try:
                contents = [yagmail.inline('logo.png')]
                titulo = f'''Diagnóstico empresarial - {ano_hoje}\n'''
                rodape = '''Para maiores informações, entre em contato através deste email.'''
            except:
                pass


            try:
                yag.send(to=dql('''SELECT email FROM perfil WHERE codigo = 1''')[0][0],subject=f'''Diagnóstico empresarial - {ano_hoje}\n''',
                     contents=(f"Mais um ano com a sua companhia ❤\n{companyName} preparou um diagnóstico da sua empresa nos últimos anos.\n\nObrigado por apoiar esse projeto!\n\n\nPara demais informações, entre em contado com este e-mail.",
                               f'C:\\Users\\{os.getlogin()}\\Downloads\\Diagnóstico empresarial - {ano_hoje}.pdf','logo.png'))
            except:
                pass




            vcon.cursor()
            vcon.execute(f'''UPDATE tasks SET emails_relatorios = 1 WHERE codigo={dql("""SELECT COUNT(*) FROM tasks""")[0][0]}''')
            vcon.commit()

            os.remove('logo.png')
            os.remove(f'C:\\Users\\{os.getlogin()}\\Downloads\\Diagnóstico empresarial - {ano_hoje}.pdf')
            os.remove(f'{ano_hoje} - Atividade dos Serviços.png')
            os.remove(f'{ano_hoje} - Clientes Ativos & Exp Empresarial.png')
            os.remove(f'{ano_hoje} - Montante.png')
            os.remove(f'{ano_hoje} - Serviços.png')
            os.remove(grafico_pgmts)
            os.remove(grafico_locais)

            import tkinter as tk
            aviso_diag = tk.Tk()
            aviso_diag.title(f'{companyName} CRM  -  Diagnóstico Anual')

            aviso_diag.eval('tk::PlaceWindow . center')
            aviso_diag.resizable(tk.FALSE, tk.FALSE)
            aviso_diag.geometry('500x100')
            aviso_diag.protocol("WM_DELETE_WINDOW", aviso_diag.quit)
            simple_text = tk.Label(aviso_diag,text=f'''O diagnóstico empresarial está pronto e disponível no e-mail:
            {dql("""SELECT email FROM perfil WHERE codigo = 1""")[0][0]}''')
            simple_text.pack()

            simple_button = tk.Button(aviso_diag,text='OK',font='Arial 12',
                                      bg='#80ccff',command=aviso_diag.quit)
            simple_button.pack(fill=tk.X,side=tk.BOTTOM)
            aviso_diag.mainloop()





        else:
            pass




else:
    pass


if ano_hoje != dql(f'''SELECT ano FROM tasks WHERE codigo = {dql("""SELECT COUNT(*) FROM tasks""")[0][0]}''')[0][0]:
    vcon.cursor()
    vcon.execute(f'''INSERT INTO tasks (emails_relatorios,ano,feito,
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
                    ) VALUES (0,{ano_hoje},0,0,0,0,0,0,0,0,0,0,0,0)''')
    vcon.commit()






from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials




cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


userAuth = dql('SELECT auth FROM auth')[0][0]
userToken = dql('SELECT token FROM auth')[0][0]

db = firestore.client()

faturamento = dql('''SELECT 
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
                    FROM tasks 
                    WHERE codigo = (SELECT COUNT(*) FROM tasks)''')[0]



progressoRef = db.collection('users') \
    .document(f"{userAuth}") \
    .collection('faturamento').document(f'{userAuth}')\
    .update({'jan':faturamento[0],
             'fev':faturamento[1],
             'mar':faturamento[2],
             'abr':faturamento[3],
             'mai':faturamento[4],
             'jun':faturamento[5],
             'jul':faturamento[6],
             'ago':faturamento[7],
             'set':faturamento[8],
             'out':faturamento[9],
             'nov':faturamento[10],
             'dez':faturamento[11]})
try:
    os.remove('logo.png')
except:
    pass