import os
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *

def get_files_string(dataset):
    username = str(os.environ.get('USER'))
    inituser = str(os.environ.get('USER')[0])
    if username == 'apuglia':
        uid = 180940
    if not hasattr(dataset, "dataset"): 
        return "ERROR: a sample with dataset method is required"
    else:
        if not os.path.exists("/tmp/x509up_u" + str(uid)):
            os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
            os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")
            
        os.popen("export XRD_NETWORKSTACK=IPv4")
        command      = 'dasgoclient -query="file dataset='+dataset.dataset+' instance=prod/phys03"'
        out_stream   = os.popen(command)
        files_string = out_stream.read()
        out_stream.close()
        return files_string.split('\n')


ZtoNu_4Jets_800to1500       = sample(ROOT.kGray, 1, 1001, "ZtoNu_4Jets_800to1500", "ZtoNu_4Jets_800to1500")

ZtoNu_4Jets_800to1500.dataset = "/Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_800_1500_2022-0fa328e40e38f44cd311b92489b92b5b/USER"
strings = get_files_string(ZtoNu_4Jets_800to1500)
print(strings[0])
