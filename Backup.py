import subprocess

class Backup():
    def realizaBackup(self, project, branch):
        repo_url = "Sua URL Git/"+ project +".git"
        
        process = subprocess.Popen(["git", "clone", repo_url], stdout=subprocess.PIPE)
        output = process.communicate()[0]

        process = subprocess.Popen(["cd", project], stdout=subprocess.PIPE)
        output = process.communicate()[0]

        process = subprocess.Popen(["git", "checkout", branch], stdout=subprocess.PIPE)
        output = process.communicate()[0]

        return "Sucess!"