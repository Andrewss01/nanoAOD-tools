#!/bin/bash
echo Check if TTY
if ["`tty`" != "not a tty" ]; then
  echo "YOU SHOULD NOT RUN THIS IN INTERACTIVE, IT DELETES YOUR LOCAL FILES"
else

echo "ENV..................................."
env
echo "VOMS"
voms-proxy-info -all
echo "CMSSW BASE, python path, pwd"
echo $CMSSW_BASE
echo $PYTHON_PATH
echo $PWD
rm -rf $CMSSW_BASE/lib/
rm -rf $CMSSW_BASE/src/
rm -rf $CMSSW_BASE/external/
rm -rf $CMSSW_BASE/install/
mv install $CMSSW_BASE/install
mv external $CMSSW_BASE/external
mv lib $CMSSW_BASE/lib
mv src $CMSSW_BASE/src
mv module $CMSSW_BASE/module
mv python $CMSSW_BASE/python
cmsenv
scram-venv
cmsenv
echo Found Proxy in: $X509_USER_PROXY
which python3
python3 -c 'from CMSJMECalculators import loadJMESystematicsCalculators;print('ok')'
hadd tree_hadd.root tree.root hist.root
fi
