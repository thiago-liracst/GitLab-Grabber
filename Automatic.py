#!/usr/bin/env python
import ProjectAutomatic
import os
from datetime import date
from datetime import datetime

class Main():

    print('Iniciando Script\n')
    today = date.today()
    date = today.strftime("%d-%b-%Y")
    directory ='Seu Diretório/'+ date +'/'
    if os.path.isdir(directory):
        now = str(datetime.now().time()).split('.')[0].replace(':','_')
        directory = directory + 'Hora_da_Geracao_' + now +'/'
        os.mkdir(directory)
    else:
        os.mkdir(directory)
    
    prj = ProjectAutomatic.ProjectAutomatic()

    #Se você não souber os ids dos projetos, pode descomentar as linhas seguintas para criar um arquivo JSON com os ids de todos os seus projetos
    #file = open("ids.json", "a")
    #file.write(str(prj.get_project_list()))

    #Array com os ids dos projetos para extração
    ids = [];

    prj.export_branches_pdf(ids, str(directory))
    
    print('Script finalizado com sucesso\n')