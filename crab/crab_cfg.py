from WMCore.Configuration import Configuration

config = Configuration()
config.section_('General')
config.General.requestName = 'DataHTF_2022'
config.General.transferLogs=True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py', '../scripts/keep_and_drop.txt']
config.JobType.sendPythonFolder = True
config.section_('Data')
config.Data.inputDataset = '/JetMET/Run2022F-PromptNanoAODv10_v1-v2/NANOAOD'
config.Data.allowNonValidInputDataset = True
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 500
config.Data.outLFNDirBase = '/store/user/%s/%s' % ('acagnott', 'DM_Run3_v0')
config.Data.publication = False
config.Data.outputDatasetTag = 'DataHTF_2022'
config.section_('Site')
config.Site.storageSite = 'T2_IT_Pisa'
