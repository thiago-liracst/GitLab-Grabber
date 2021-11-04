#!/usr/bin/env python

import gitlab
import csv


file = open('token.txt', 'r')
token = file.read()
file.close()
gl = gitlab.Gitlab('Sua URL Git', private_token = str(token))
gl.auth()

class ProjectManual():
    
    def get_project_list(self):
        projects = gl.projects.list(all=True)
        lista = []
        for project in projects:
            lista.append({'id': project.id,'name': project.name})
        return lista

    def get_id(self, project_name):
        project = gl.projects.get(project_name)
        return project
    
    def get_name(self, project_id):
        project = gl.projects.get(project_id)
        return project
    
    def get_project_branches(self, project_id):
        project = gl.projects.get(project_id)
        branches = project.branches.list(all=True)
        return branches
    
    def get_project_merges(self,project_id):
        project = gl.projects.get(project_id)
        merges  = project.mergerequests.list(all=True)
        return merges

    def export_branches_pdf(self,project_id, directory):
        branches = self.get_project_branches(project_id)
        project  = self.get_name(project_id)
        merges   = self.get_project_merges(project_id)
        fields = ['Branch','Sistema','Autor','Squad', 'Criação','Ultima alteração','Destino merge','URL merge','Tipo Branch','Quantidade de Commits', 'Commits atrás da master', 'Commits a frente da master', 'Diff com a master','Merge com a Master','Data merge']
        with open(directory + project.name+'.csv', 'a+',) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields, dialect='excel')
            reader = csv.DictReader(csvfile, fieldnames=fields)
            writer.writeheader()
            commits_master = len(project.commits.list(all=True,
                               query_parameters={'ref_name': 'master'}))
            for branch in branches:
                    date_create = branch.commit['authored_date'].split('T')[0]
                    date_mod = branch.commit['committed_date'].split('T')[0]
                    email_author = branch.commit['author_email'].split('@')[0]
                    squad_author = self.squad_dev(email_author.lower())
                    type_branch = self.branch_type(branch.name.lower())
                    list_mrs = project.mergerequests.list(all=True, query_parameters={'state': 'merged','source_branch': branch.name})
                    branches_merge, links_merge, dates_merge = self.values_merges_request(list_mrs)
                    branch_merge = self.branch_merge(branches_merge.lower())
                    qtd_commits = len(project.commits.list(all=True,
                               query_parameters={'ref_name': branch.name}))
                    compare_commits = project.repository_compare('master', branch.name)
                    commits_ahead = len(compare_commits['commits'])
                    diff_commits = len(compare_commits['diffs'])
                    commits_behind = self.calcule_commits_behind(commits_master,qtd_commits,commits_ahead)
                    try:
                        writer.writerow({'Branch': branch.name, 'Sistema': project.name, 'Autor': branch.commit['author_name'], 'Squad': squad_author,'Criação': date_create , 'Ultima alteração': date_mod, 'Tipo Branch': type_branch, 'Quantidade de Commits': qtd_commits, 'Commits atrás da master': commits_behind,'Commits a frente da master' : commits_ahead, 'Diff com a master': diff_commits, 'Data merge': dates_merge})
                    except:
                        print("Erro ao gerar relatório da branch "+str(branch.name)+" do pacote "+str(project.name))

    def commit_review(self,project_id):
        pass
    
    def values_merges_request(self, list_mrs):
        branches_merge=""
        links_merge=""
        dates_merge=""
        if len(list_mrs) > 0:
            for merge in list_mrs:
                branches_merge+=merge.target_branch + " "
                links_merge+= merge.web_url + " "
                dates_merge += merge.updated_at.split('T')[0]  + " "
        return branches_merge, links_merge, dates_merge

    def squad_dev(self, user_email):
        #Array com os ids dos contribuidores
        tr_squad_1 = []
        #Array com os emails dos contrinuintes
        squad_1 = []
        if user_email in tr_squad_1:
            return "Squad 1"
        if user_email in squad_1:
            return "Squad 1"
        else:
            return user_email
    
    def calcule_commits_behind(self, commits_master,qtd_commits, commits_ahead):
        result = commits_master -(qtd_commits - commits_ahead)
        return result
    
    def branch_type(self, branch):
        if branch.find("feature") == 0:
            return "feature"
        if branch.find("hotfix"):
            return "hotfix"
        if branch.find("release"):
            return "release"
        if branch.find("devops") == 0:
            return "devops"
        else:
            return ""

    def branch_merge(self, branches):
        if branches.find("post") == 0  or branches.find("prj") == 0:
            return "Foi mergeada"
        if branches.find("master") == 0:
            return "Foi mergeada"
        else:
            return "Não foi mergeada"
