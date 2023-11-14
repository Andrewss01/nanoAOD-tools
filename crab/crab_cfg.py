from WMCore.Configuration import Configuration

config = Configuration()
config.section_('General')
config.General.requestName = 'DataHTA_2018'
config.General.transferLogs=True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.maxJobRuntimeMin = 2700
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py', '../scripts/keep_and_drop.txt']
config.section_('Data')
config.Data.inputDataset = '/MET/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD'
config.Data.allowNonValidInputDataset = True
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
config.Data.unitsPerJob = 80
config.Data.outLFNDirBase = '/store/user/%s/%s' % ('acagnott', 'DM_Run3_v0')
config.Data.publication = False
config.Data.outputDatasetTag = 'DataHTA_2018'
config.section_('Site')
config.Site.storageSite = 'T2_IT_Pisa'
