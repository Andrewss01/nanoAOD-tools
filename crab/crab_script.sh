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
ls $CMSSW_BASE/install/
rm -rf $CMSSW_BASE/install/
rm -rf $CMSSW_BASE/module/
rm -rf $CMSSW_BASE/python/
mv external $CMSSW_BASE/external
mv lib $CMSSW_BASE/lib
mv src $CMSSW_BASE/src
mv install $CMSSW_BASE/install
mv module $CMSSW_BASE/module
mv python $CMSSW_BASE/python
mv install_cmssw.sh $CMSSW_BASE/src/
cd $CMSSW_BASE/src
rm -r CMSJMECalculators
git clone https://gitlab.cern.ch/cms-analysis/general/CMSJMECalculators.git
cd CMSJMECalculators/
git fetch "https://:@gitlab.cern.ch:8443/aguzel/CMSJMECalculators.git" 'CMSJMECalculators-correctionlib'
git checkout -b 'CMSJMECalculators-CMSJMECalculators-correctionlib' FETCH_HEAD
cd ..
source $CMSSW_BASE/src/install_cmssw.sh
cd /srv
echo Found Proxy in: $X509_USER_PROXY
which python3
python3 crab_script.py $1
hadd tree_hadd.root tree.root hist.root
fi
