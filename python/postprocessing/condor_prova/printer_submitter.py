import os
import time 
import sys 
sys.path.append("/eos/user/a/apuglia/SWAN_projects/thesis/CMSSW_14_1_7/src/PhysicsTools/NanoAODTools/python/postprocessing/")
from samples.samples import *
username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])

if username == 'apuglia':
    uid = 180940
    
    
def sub_writer(stringa,folder="./"):
    f = open(folder+"condor_"+stringa+".sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/" + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write("universe                = vanilla\n")
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write("use_x509userproxy       = true\n")
    f.write("should_transfer_files   = YES\n")
    f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    #f.write("transfer_output_remaps  = \""+outname+"_Skim.root=root://eosuser.cern.ch///eos/user/"+inituser + "/" + username+"/DarkMatter/topcandidate_file/"+dat_name+"_Skim.root\"\n")
    f.write("+JobFlavour             = \"espresso\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    f.write("executable              = runner_" +stringa+ ".sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = "+folder+"condor/output/"+stringa+".out\n")
    f.write("error                   = "+folder+"condor/error/"+stringa+".err\n")
    f.write("log                     = "+folder+"condor/log/"+stringa+".log\n")

    f.write("queue\n")
    
def runner_writer(parola,folder="./"):
    f = open(folder+"runner_" + parola+ ".sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /eos/user/a/apuglia/SWAN_projects/thesis/CMSSW_14_1_7/src/PhysicsTools/NanoAODTools/python/postprocessing/condor_prova\n")
    f.write(f"python3 printer.py -s {parola}\n")
    
    

writepath="/afs/cern.ch/user/a/apuglia/condor_prova/"

if not os.path.exists(writepath+ "condor/output"):
    os.makedirs(writepath+"condor/output")
if not os.path.exists(writepath+"condor/error"):
    os.makedirs(writepath+"condor/error")
if not os.path.exists(writepath+"condor/log"):
    os.makedirs(writepath+"condor/log")
    
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")




lista_parole = ['andrea', 'leonardo', 'kakka','parola', 'ponys','fns']

os.system("cd /afs/cern.ch/user/a/apuglia/condor_prova/")



for parola in lista_parole:
    runner_writer(parola=parola,folder=writepath)
    sub_writer(stringa=parola,folder=writepath)
    os.popen('condor_submit '+writepath+'condor'+stringa+'.sub')
    time.sleep(5)
    print("ciccio")
