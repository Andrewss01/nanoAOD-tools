from WMCore.Configuration import Configuration

config = Configuration()
config.section_('General')
config.General.requestName = 'TprimeToTZ_700_2022'
config.General.transferLogs=True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.maxJobRuntimeMin = 2700
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py', '../scripts/keep_and_drop.txt', './Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt', './Cert_Collisions2022_355100_362760_Golden.json', './Cert_Collisions2023_366442_370790_Golden.json', '../../../install_cmssw.sh']
config.JobType.sendVenvFolder = True
config.section_('Data')
config.Data.inputDataset = '/TprimeBtoTZ_M-700_LH_TuneCP5_13p6TeV_madgraph-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v3/NANOAODSIM'
config.Data.allowNonValidInputDataset = True
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/%s/%s' % ('acagnott', 'DM_Run3_v0')
config.Data.publication = False
config.Data.outputDatasetTag = 'TprimeToTZ_700_2022'
config.section_('Site')
config.Site.storageSite = 'T2_IT_Pisa'
