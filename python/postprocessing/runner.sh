#!/usr/bin/bash 
cd /afs/cern.ch/work/a/acagnott/CMSSW_12_4_7/src/PhysicsTools/NanoAODTools/python/postprocessing/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 run_postprocessor.py $1 $2 $3 $4
hadd $2 $3 histOut$4.root
