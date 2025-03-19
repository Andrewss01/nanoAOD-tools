from WMCore.Configuration import Configuration

config = Configuration()
config.section_('General')
config.General.requestName = 'TTTo2J1L1Nu_v5'
config.General.transferLogs=True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.maxJobRuntimeMin = 2700
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script_copy.py', '../scripts/keep_and_drop.txt']
config.JobType.sendVenvFolder = False   #True
config.section_('Data')
config.Data.inputDataset = '/TTTo2J1L1Nu_CP5_13p6TeV_powheg-pythia8/Run3Winter22NanoAOD-122X_mcRun3_2021_realistic_v9-v1/NANOAODSIM'
config.Data.allowNonValidInputDataset = True
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'   #'FileBased' 
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/%s' % ('apuglia')
config.Data.publication = False
config.Data.outputDatasetTag = 'TTTo2J1L1Nu'
config.section_('Site')
config.Site.storageSite = 'T2_IT_Pisa'
