from WMCore.Configuration import Configuration

config = Configuration()
config.section_('General')
config.General.requestName = 'DataMETD_2018'
config.General.transferLogs=True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.maxJobRuntimeMin = 2700
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py', '../scripts/keep_and_drop.txt']
config.section_('Data')
config.Data.inputDataset = '/MET/Run2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'
config.Data.allowNonValidInputDataset = True
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.lumiMask = ''
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/%s/%s' % ('acagnott', 'DM_Run3_v0')
config.Data.publication = False
config.Data.outputDatasetTag = 'DataMETD_2018'
config.section_('Site')
config.Site.storageSite = 'T2_IT_Pisa'
