#!/usr/bin/env python
import ProjectManual
import os
from datetime import date
from datetime import datetime

class Main():

    print('Iniciando Script\n')
    today = date.today()
    date = today.strftime("%d-%b-%Y")
    directory ='Seu diretório/'+ date +'/'
    if os.path.isdir(directory):
        now = str(datetime.now().time()).split('.')[0].replace(':','_')
        directory = directory + 'Hora_da_Geracao_' + now +'/'
        os.mkdir(directory)
    else:
        os.mkdir(directory)
    
    prj = ProjectManual.ProjectManual()

    #Se você não souber os ids dos projetos, pode descomentar as linhas seguintas para criar um arquivo JSON com os ids de todos os seus projetos
    #file = open("ids.json", "a")
    #file.write(str(prj.get_project_list()))

    status = 's'
    while(status == 's'):
        print('Qual projeto deseja gerar relatorio do gitlab? Digite o ID:\n')
        value = str(input())
        print('Gerando relatório...\n')
        prj.export_branches_pdf(value, str(directory))

        print('Deseja gerar relatório de outro projeto? Digite s/n')
        status = input().lower()
    
    print('Script finalizado com sucesso\n')