import os
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
uid = int(os.getuid())



def get_files_string(dataset):
    username = str(os.environ.get('USER'))
    inituser = str(os.environ.get('USER')[0])
    # if username == 'apuglia':
    #     uid = 180940 
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




def get_files_string_from_path(dataset_path):
    username = str(os.environ.get('USER'))
    inituser = str(os.environ.get('USER')[0])
    # if username == 'apuglia':
    #     uid = 180940 

    if not os.path.exists("/tmp/x509up_u" + str(uid)):
        os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
        os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")
        
    os.popen("export XRD_NETWORKSTACK=IPv4")
    command      = 'dasgoclient -query="file dataset='+dataset_path+' instance=prod/phys03"'
    out_stream   = os.popen(command) 
    files_string = out_stream.read()
    out_stream.close()
    return files_string.split('\n')
