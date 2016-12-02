#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import checksumdir
from flask import Flask, render_template
app = Flask(__name__)

puppetWorkingDirectory='puppet'
environnements=['maquette','preprod', 'prod']

@app.route('/')
def accueil():
    modules=[]
    allModules=[]
    for env in environnements:
        for module in os.listdir(puppetWorkingDirectory+'/'+env):
            if module not in allModules:
                allModules.append(module)

    for module in allModules:
        precEnv=0
        curEnv=1
        mod={}
        mod["Name"]=module
        for id, env in enumerate(environnements):
            curEnvDir=puppetWorkingDirectory+'/'+env+"/"+mod["Name"]
            prevEnvDir=puppetWorkingDirectory+'/'+environnements[id-1]+"/"+mod["Name"]
            if os.path.exists(curEnvDir):
                if id > 0 :
                    curEnvMd5Sum=checksumdir.dirhash(curEnvDir)
                    if os.path.exists(prevEnvDir): 
                        prevEnvMd5sum=checksumdir.dirhash(prevEnvDir)
                        if curEnvMd5Sum == prevEnvMd5sum:
                            mod[env]="ok"
                        else:
                            mod[env]="nok"
                    else:
                        mod[env]="ok"
                elif id == 0:
                    mod[env]="ok"
            else:
                mod[env]="empty"
        modules.append(mod)
    return render_template('./index.html', titre="Welcome on my puppet modules dashboard !", environnements=environnements, modules=modules)

if __name__ == '__main__':
    app.run()

