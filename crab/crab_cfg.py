from WMCore.Configuration import Configuration

config = Configuration()
config.section_('General')
config.General.requestName = 'TT_Mtt700to1000_2018'
config.General.transferLogs=True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py', '../scripts/keep_and_drop.txt']
config.JobType.sendPythonFolder = True
config.section_('Data')
config.Data.inputDataset = '/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM'
config.Data.allowNonValidInputDataset = True
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/%s/%s' % ('acagnott', 'DM_v0')
config.Data.publication = False
config.Data.outputDatasetTag = 'TT_Mtt700to1000_2018'
config.section_('Site')
config.Site.storageSite = 'T2_IT_Pisa'
