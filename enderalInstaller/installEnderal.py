#!/usr/bin/python3
###
### Alternative Enderal installer
###

import argparse
import getpass
import os
import pathlib
import platform
import subprocess
import shutil
import sys
import urllib.request
import zipfile

try:
	import ctypes
except:
	pass

# Procedures
def _wget_reporthook(numblocks, blocksize, filesize, name):
	percent = numblocks*blocksize*100/filesize
	if percent < 0 or percent > 100:
		percent = 100
	sys.stdout.write("\r{0}\t{1:.2f}%".format(name, percent))

def wget(url, dst):
	print("Downloading " + url + " to " + dst + " ...")
	urllib.request.urlretrieve(url, dst,
		lambda nb, bs, fs, url=url: _wget_reporthook(nb,bs,fs,dst))
	print("")

def unzip(name, dst, case_sensitive):
	zf = zipfile.ZipFile(name, 'r')
	for x in zf.namelist():
		print("Unzipping " + x + " ...");
		y = x;
		if case_sensitive == True:
			y = y.lower()
		if x.endswith('/'):
			os.makedirs(dst + '/' + y, exist_ok=True)
		else:
			input_ = zf.open(x)
			output = open(dst + '/' + y, 'wb+')
			shutil.copyfileobj(input_, output)
			output.close()
			input_.close()
	zf.close()

def copy(src, dst):
	print("Copying file " + src + " ...")
	shutil.copy2(src, dst)

# Ini generator helper class
class IniGenerator:
	def __init__(self):
		self.LANGUAGE = "EN"
		self.RES_X = 1920
		self.RES_Y = 1080
		self.SetLevel("ultra", True)

	def SetLevel(self, level, mt):
		if level == "ultra":
			self.iPreloadSizeLimit=8053063680
			self.bReflectLODLand=1
			self.bReflectLODObjects=1
			self.bReflectSky=1
			self.bReflectLODTrees=1
			self.bFXAAEnabled=1
			self.iMultiSample=8
			self.iMaxAnisotropy=16
			self.iTexMipMapSkip=0
			self.iRadialBlurLevel=2
			self.iShadowMapResolution=4096
			self.fShadowBiasScale=0.15
			self.iBlurDeferredShadowMask=128
			self.iShadowMaskQuarter=4
			self.fShadowDistance=8000
			self.bTreesReceiveShadows=1
			self.fSpecularLODStartFade=2000
			self.fLightLODStartFade=3500
			self.bDecals=1
			self.bSkinnedDecals=1
			self.uMaxDecals=1000
			self.uMaxSkinDecals=100
			self.uMaxSkinDecalsPerActor=60
			self.fGrassStartFadeDistance=7000
			self.fTreeLoadDistance=75000
			self.fBlockMaximumDistance=250000
			self.fBlockLevel1Distance=70000
			self.fBlockLevel0Distance=35000
			self.fSplitDistanceMult=1.5
			self.fLODFadeOutMultObjects=15
			self.fLODFadeOutMultActors=15
			self.fLODFadeOutMultItems=15
		elif level == "vhigh":
			self.iPreloadSizeLimit=8053063680
			self.bReflectLODLand=1
			self.bReflectLODObjects=1
			self.bReflectSky=1
			self.bReflectLODTrees=1
			self.bFXAAEnabled=1
			self.iMultiSample=8
			self.iMaxAnisotropy=12
			self.iTexMipMapSkip=0
			self.iRadialBlurLevel=2
			self.iShadowMapResolution=4096
			self.fShadowBiasScale=0.15
			self.iBlurDeferredShadowMask=128
			self.iShadowMaskQuarter=4
			self.fShadowDistance=8000
			self.bTreesReceiveShadows=1
			self.fSpecularLODStartFade=1800
			self.fLightLODStartFade=3200
			self.bDecals=1
			self.bSkinnedDecals=1
			self.uMaxDecals=1000
			self.uMaxSkinDecals=100
			self.uMaxSkinDecalsPerActor=60
			self.fGrassStartFadeDistance=6000
			self.fTreeLoadDistance=75000
			self.fBlockMaximumDistance=250000
			self.fBlockLevel1Distance=70000
			self.fBlockLevel0Distance=35000
			self.fSplitDistanceMult=1.5
			self.fLODFadeOutMultObjects=14
			self.fLODFadeOutMultActors=12
			self.fLODFadeOutMultItems=13
		elif level == "high":
			self.iPreloadSizeLimit=4831838208
			self.bReflectLODLand=1
			self.bReflectLODObjects=1
			self.bReflectSky=1
			self.bReflectLODTrees=1
			self.bFXAAEnabled=1
			self.iMultiSample=4
			self.iMaxAnisotropy=8
			self.iTexMipMapSkip=0
			self.iRadialBlurLevel=2
			self.iShadowMapResolution=2048
			self.fShadowBiasScale=0.25
			self.iBlurDeferredShadowMask=64
			self.iShadowMaskQuarter=4
			self.fShadowDistance=4000
			self.bTreesReceiveShadows=1
			self.fSpecularLODStartFade=1600
			self.fLightLODStartFade=2500
			self.bDecals=1
			self.bSkinnedDecals=1
			self.uMaxDecals=250
			self.uMaxSkinDecals=50
			self.uMaxSkinDecalsPerActor=40
			self.fGrassStartFadeDistance=5000
			self.fTreeLoadDistance=40000
			self.fBlockMaximumDistance=150000
			self.fBlockLevel1Distance=40000
			self.fBlockLevel0Distance=25000
			self.fSplitDistanceMult=1.1
			self.fLODFadeOutMultObjects=12
			self.fLODFadeOutMultActors=10
			self.fLODFadeOutMultItems=10
		elif level == "med":
			self.iPreloadSizeLimit=4831838208
			self.bReflectLODLand=1
			self.bReflectLODObjects=0
			self.bReflectSky=1
			self.bReflectLODTrees=0
			self.bFXAAEnabled=0
			self.iMultiSample=2
			self.iMaxAnisotropy=4
			self.iTexMipMapSkip=1
			self.iRadialBlurLevel=1
			self.iShadowMapResolution=1024
			self.fShadowBiasScale=0.3
			self.iBlurDeferredShadowMask=32
			self.iShadowMaskQuarter=3
			self.fShadowDistance=2500
			self.bTreesReceiveShadows=0
			self.fSpecularLODStartFade=1000
			self.fLightLODStartFade=1000
			self.bDecals=1
			self.bSkinnedDecals=1
			self.uMaxDecals=100
			self.uMaxSkinDecals=35
			self.uMaxSkinDecalsPerActor=20
			self.fGrassStartFadeDistance=3000
			self.fTreeLoadDistance=25000
			self.fBlockMaximumDistance=100000
			self.fBlockLevel1Distance=32768
			self.fBlockLevel0Distance=20480
			self.fSplitDistanceMult=0.75
			self.fLODFadeOutMultObjects=8
			self.fLODFadeOutMultActors=6
			self.fLODFadeOutMultItems=8
		elif level == "low":
			self.iPreloadSizeLimit=2684354560
			self.bReflectLODLand=0
			self.bReflectLODObjects=0
			self.bReflectSky=1
			self.bReflectLODTrees=0
			self.bFXAAEnabled=0
			self.iMultiSample=1
			self.iMaxAnisotropy=2
			self.iTexMipMapSkip=2
			self.iRadialBlurLevel=0
			self.iShadowMapResolution=512
			self.fShadowBiasScale=0.5
			self.iBlurDeferredShadowMask=3
			self.iShadowMaskQuarter=3
			self.fShadowDistance=2000
			self.bTreesReceiveShadows=0
			self.fSpecularLODStartFade=400
			self.fLightLODStartFade=600
			self.bDecals=0
			self.bSkinnedDecals=0
			self.uMaxDecals=0
			self.uMaxSkinDecals=0
			self.uMaxSkinDecalsPerActor=0
			self.fGrassStartFadeDistance=1000
			self.fTreeLoadDistance=12500
			self.fBlockMaximumDistance=75000
			self.fBlockLevel1Distance=25000
			self.fBlockLevel0Distance=15000
			self.fSplitDistanceMult=0.4
			self.fLODFadeOutMultObjects=4
			self.fLODFadeOutMultActors=4
			self.fLODFadeOutMultItems=6
		elif level == "vlow":
			self.iPreloadSizeLimit=2684354560
			self.bReflectLODLand=1
			self.bReflectLODObjects=1
			self.bReflectSky=1
			self.bReflectLODTrees=1
			self.bFXAAEnabled=0
			self.iMultiSample=1
			self.iMaxAnisotropy=1
			self.iTexMipMapSkip=2
			self.iRadialBlurLevel=0
			self.iShadowMapResolution=512
			self.fShadowBiasScale=0.5
			self.iBlurDeferredShadowMask=3
			self.iShadowMaskQuarter=3
			self.fShadowDistance=2000
			self.bTreesReceiveShadows=0
			self.fSpecularLODStartFade=200
			self.fLightLODStartFade=200
			self.bDecals=0
			self.bSkinnedDecals=0
			self.uMaxDecals=0
			self.uMaxSkinDecals=0
			self.uMaxSkinDecalsPerActor=0
			self.fGrassStartFadeDistance=0
			self.fTreeLoadDistance=12500
			self.fBlockMaximumDistance=75000
			self.fBlockLevel1Distance=25000
			self.fBlockLevel0Distance=15000
			self.fSplitDistanceMult=0.4
			self.fLODFadeOutMultObjects=1
			self.fLODFadeOutMultActors=2
			self.fLODFadeOutMultItems=1
		else:
			raise ValueError("Invalid level specified")

		if mt == True:
			self.bLoadBackgroundFaceGen=1
			self.bLoadHelmetsInBackground=1
			self.bBackgroundLoadLipFiles=1
			self.bBackgroundCellLoads=1
			self.bUseBackgroundFileLoader=1
			self.bMultiThreadBoneUpdate=1
			self.bUseMultiThreadedFaceGen=1
			self.bUseThreadedParticleSystem=1
			self.bUseThreadedTempEffects=1
			self.bUseThreadedTextures=1
			self.bDecalMultithreaded=1
			self.bUseThreadedBlood=1
			self.bUseThreadedMeshes=1
			self.bUseMultiThreadedTrees=1
			self.bUseThreadedLOD=1
			self.bUseThreadedAI=1
			self.bMultiThreadMovement=1
			self.bUseThreadedMorpher=1
			self.iNumThreads=4
			self.iNumHWThreads=4
		else:
			self.bLoadBackgroundFaceGen=0
			self.bLoadHelmetsInBackground=0
			self.bBackgroundLoadLipFiles=0
			self.bBackgroundCellLoads=0
			self.bUseBackgroundFileLoader=0
			self.bMultiThreadBoneUpdate=0
			self.bUseMultiThreadedFaceGen=0
			self.bUseThreadedParticleSystem=0
			self.bUseThreadedTempEffects=0
			self.bUseThreadedTextures=0
			self.bDecalMultithreaded=0
			self.bUseThreadedBlood=0
			self.bUseThreadedMeshes=0
			self.bUseMultiThreadedTrees=0
			self.bUseThreadedLOD=0
			self.bUseThreadedAI=0
			self.bMultiThreadMovement=0
			self.bUseThreadedMorpher=0
			self.iNumThreads=2
			self.iNumHWThreads=2

	def Generate(self, path):
		os.makedirs(path + "Documents/My Games/Skyrim/", exist_ok=True)
		lang = "ENGLISH" if self.LANGUAGE == "EN" else "GERMAN"

		ini = \
			"[General]\n" + \
			"sLanguage=" + lang + "\n" + \
			"sIntroSequence=1\n" + \
			"uGridsToLoad=5\n" + \
			"uInterior Cell Buffer=6\n" + \
			"uExterior Cell Buffer=36\n" + \
			"iPreloadSizeLimit=" + "{0:d}".format(self.iPreloadSizeLimit) + "\n" + \
			"[Display]\n" + \
			"iPresentInterval=1\n" + \
			"fLightLODMaxStartFade=3500.0000\n" + \
			"iShadowMapResolutionPrimary=2048\n" + \
			"bAllowScreenshot=1\n" + \
			"fDefaultWorldFOV=75\n" + \
			"fDefault1stPersonFOV=75\n" + \
			"[BackgroundLoad/Multithreading]\n" + \
			"bLoadBackgroundFaceGen=" + "{0:d}".format(self.bLoadBackgroundFaceGen) + "\n" + \
			"bLoadHelmetsInBackground=" + "{0:d}".format(self.bLoadHelmetsInBackground) + "\n" + \
			"bBackgroundLoadLipFiles=" + "{0:d}".format(self.bBackgroundLoadLipFiles) + "\n" + \
			"bBackgroundCellLoads=" + "{0:d}".format(self.bBackgroundCellLoads) + "\n" + \
			"bUseBackgroundFileLoader=" + "{0:d}".format(self.bUseBackgroundFileLoader) + "\n" + \
			"bMultiThreadBoneUpdate=" + "{0:d}".format(self.bMultiThreadBoneUpdate) + "\n" + \
			"bUseMultiThreadedFaceGen=" + "{0:d}".format(self.bUseMultiThreadedFaceGen) + "\n" + \
			"bUseThreadedParticleSystem=" + "{0:d}".format(self.bUseThreadedParticleSystem) + "\n" + \
			"bUseThreadedTempEffects=" + "{0:d}".format(self.bUseThreadedTempEffects) + "\n" + \
			"bUseThreadedTextures=" + "{0:d}".format(self.bUseThreadedTextures) + "\n" + \
			"bDecalMultithreaded=" + "{0:d}".format(self.bDecalMultithreaded) + "\n" + \
			"bUseThreadedBlood=" + "{0:d}".format(self.bUseThreadedBlood) + "\n" + \
			"bUseThreadedMeshes=" + "{0:d}".format(self.bUseThreadedMeshes) + "\n" + \
			"bUseMultiThreadedTrees=" + "{0:d}".format(self.bUseMultiThreadedTrees) + "\n" + \
			"bUseThreadedLOD=" + "{0:d}".format(self.bUseThreadedLOD) + "\n" + \
			"bUseThreadedAI=" + "{0:d}".format(self.bUseThreadedAI) + "\n" + \
			"bMultiThreadMovement=" + "{0:d}".format(self.bMultiThreadMovement) + "\n" + \
			"bUseThreadedMorpher=" + "{0:d}".format(self.bUseThreadedMorpher) + "\n" + \
			"[HAVOK]\n" + \
			"iNumThreads=" + "{0:d}".format(self.iNumThreads) + "\n" + \
			"iNumHWThreads=" + "{0:d}".format(self.iNumHWThreads) + "\n" + \
			"[Audio]\n" + \
			"fMusicDuckingSeconds=6.0000\n" + \
			"fMusicUnDuckingSeconds=8.0000\n" + \
			"fMenuModeFadeOutTime=3.0000\n" + \
			"fMenuModeFadeInTime=1.0000\n" + \
			"[Grass]\n" + \
			"bAllowCreateGrass=1\n" + \
			"bAllowLoadGrass=0\n" + \
			"[GeneralWarnings]\n" + \
			"sGeneralMasterMismatchWarning=One or more plugins could not find " + \
				"the correct versions of the master files they depend on. Errors may " + \
				"occur during load or game play. Check the \"Warnings.txt\" file for " + \
				"more information.\n" + \
			"[Archive]\n" + \
			"bInvalidateOlderFiles=1\n" + \
			"sResourceArchiveList=Skyrim - Misc.bsa, Skyrim - Shaders.bsa, " + \
				"Skyrim - Textures.bsa, Skyrim - Interface.bsa, Skyrim - Animations.bsa, " + \
				"Skyrim - Meshes.bsa, Skyrim - Sounds.bsa\n" + \
			"sResourceArchiveList2=Enderal - Misc.bsa, Enderal - Meshes.bsa, " + \
				"Enderal - Sounds.bsa, Enderal - Textures.bsa, Enderal - Textures2.bsa, " + \
				"Enderal - Textures3.bsa, Enderal - Textures4.bsa, Enderal - Voices.bsa\n" + \
			"[Combat]\n" + \
			"fMagnetismStrafeHeadingMult=0.0000\n" + \
			"fMagnetismLookingMult=0.0000\n" + \
			"[Papyrus]\n" + \
			"fPostLoadUpdateTimeMS=500.0000\n" + \
			"bEnableLogging=0\n" + \
			"bEnableTrace=0\n" + \
			"bLoadDebugInformation=0\n" + \
			"[Water]\n" + \
			"bReflectLODLand=" + "{0:d}".format(self.bReflectLODLand) + "\n" + \
			"bReflectLODObjects=" + "{0:d}".format(self.bReflectLODObjects) + "\n" + \
			"bReflectSky=" + "{0:d}".format(self.bReflectSky) + "\n" + \
			"bReflectLODTrees=" + "{0:d}".format(self.bReflectLODTrees) + "\n" + \
			"[VATS]\n" + \
			"bVATSDisable=0\n" + \
			"fShadowLODMaxStartFade=1000.0000\n" + \
			"fSpecularLODMaxStartFade=2000.0000\n"

		print("Generating Skyrim.ini...")
		inifile = open(path + "Documents/My Games/Skyrim/Skyrim.ini", "w+")
		inifile.write(ini)
		inifile.close()

		prefs = \
			"[Launcher]\n" + \
			"bEnableFileSelection=1\n" + \
			"iScreenShotIndex=0\n" + \
			"[Imagespace]\n" + \
			"bDoDepthOfField=1\n" + \
			"[Display]\n" + \
			"bFull Screen=1\n" + \
			"bFXAAEnabled=" + "{0:d}".format(self.bFXAAEnabled) + "\n" + \
			"iSize W=" + "{0:d}".format(self.RES_X) + "\n" + \
			"iSize H=" + "{0:d}".format(self.RES_Y) + "\n" + \
			"iMultiSample=" + "{0:d}".format(self.iMultiSample) + "\n" + \
			"iMaxAnisotropy=" + "{0:d}".format(self.iMaxAnisotropy) + "\n" + \
			"iTexMipMapSkip=" + "{0:d}".format(self.iTexMipMapSkip) + "\n" + \
			"iRadialBlurLevel=" + "{0:d}".format(self.iRadialBlurLevel) + "\n" + \
			"iShadowMapResolution=" + "{0:d}".format(self.iShadowMapResolution) + "\n" + \
			"fShadowBiasScale=" + "{0:f}".format(self.fShadowBiasScale) + "\n" + \
			"iBlurDeferredShadowMask=" + "{0:d}".format(self.iBlurDeferredShadowMask) + "\n" + \
			"iShadowMaskQuarter=" + "{0:d}".format(self.iShadowMaskQuarter) + "\n" + \
			"fShadowDistance=" + "{0:f}".format(self.fShadowDistance) + "\n" + \
			"fInteriorShadowDistance=3000.0000\n" + \
			"bTreesReceiveShadows=" + "{0:d}".format(self.bTreesReceiveShadows) + "\n" + \
			"fLeafAnimDampenDistEnd=4600.0000\n" + \
			"fLeafAnimDampenDistStart=3600.0000\n" + \
			"fTreesMidLODSwitchDist=1e+007\n" + \
			"fGamma=1.0000\n" + \
			"iShadowFilter=3\n" + \
			"bShadowsOnGrass=1\n" + \
			"fDecalLOD2=1500.0000\n" + \
			"fDecalLOD1=1000.0000\n" + \
			"fSpecularLODStartFade=" + "{0:f}".format(self.fSpecularLODStartFade) + "\n" + \
			"fShadowLODStartFade=200.0000\n" + \
			"fLightLODStartFade=" + "{0:f}".format(self.fLightLODStartFade) + "\n" + \
			"iTexMipMapMinimum=0\n" + \
			"bTransparencyMultisampling=0\n" + \
			"iWaterMultiSamples=0\n" + \
			"bDeferredShadows=0\n" + \
			"iShadowMode=3\n" + \
			"bDrawLandShadows=0\n" + \
			"bDrawShadows=1\n" + \
			"fMeshLODFadePercentDefault=1.2000\n" + \
			"fMeshLODFadeBoundDefault=256.0000\n" + \
			"fMeshLODLevel2FadeTreeDistance=1e+007\n" + \
			"fMeshLODLevel1FadeTreeDistance=1e+007\n" + \
			"fMeshLODLevel2FadeDist=1e+007\n" + \
			"fMeshLODLevel1FadeDist=1e+007\n" + \
			"bShadowMaskZPrepass=0\n" + \
			"bMainZPrepass=0\n" + \
			"iMaxSkinDecalsPerFrame=3\n" + \
			"iMaxDecalsPerFrame=10\n" + \
			"bFloatPointRenderTarget=1\n" + \
			"[MAIN]\n" + \
			"fSkyCellRefFadeDistance=600000.0000\n" + \
			"bCrosshairEnabled=1\n" + \
			"fHUDOpacity=1.0000\n" + \
			"bSaveOnPause=1\n" + \
			"bSaveOnTravel=1\n" + \
			"bSaveOnWait=1\n" + \
			"bSaveOnRest=1\n" + \
			"[Decals]\n" + \
			"bDecals=" + "{0:d}".format(self.bDecals) + "\n" + \
			"bSkinnedDecals=" + "{0:d}".format(self.bSkinnedDecals) + "\n" + \
			"uMaxDecals=" + "{0:d}".format(self.uMaxDecals) + "\n" + \
			"uMaxSkinDecals=" + "{0:d}".format(self.uMaxSkinDecals) + "\n" + \
			"uMaxSkinDecalsPerActor=" + "{0:d}".format(self.uMaxSkinDecalsPerActor) + "\n" + \
			"[Grass]\n" + \
			"b30GrassVS=0\n" + \
			"fGrassStartFadeDistance=" + "{0:f}".format(self.fGrassStartFadeDistance) + "\n" + \
			"fGrassMaxStartFadeDistance=7000.0000\n" + \
			"fGrassMinStartFadeDistance=400.0000\n" + \
			"[GamePlay]\n" + \
			"bShowFloatingQuestMarkers=1\n" + \
			"bShowQuestMarkers=1\n" + \
			"iDifficulty=2\n" + \
			"[Interface]\n" + \
			"fMouseCursorSpeed=1.0000\n" + \
			"bShowCompass=1\n" + \
			"bGeneralSubtitles=1\n" + \
			"bDialogueSubtitles=1\n" + \
			"[Controls]\n" + \
			"fMouseHeadingSensitivity=0.0125\n" + \
			"bInvertYValues=0\n" + \
			"bGamePadRumble=0\n" + \
			"bAlwaysRunByDefault=1\n" + \
			"bUseKinect=0\n" + \
			"fGamepadHeadingSensitivity=1.9000\n" + \
			"[Particles]\n" + \
			"iMaxDesired=750\n" + \
			"[SaveGame]\n" + \
			"fAutosaveEveryXMins=15.0000\n" + \
			"[AudioMenu]\n" + \
			"fAudioMasterVolume=1.0000\n" + \
			"fVal7=1.0000\n" + \
			"uID7=0\n" + \
			"fVal6=1.0000\n" + \
			"uID6=0\n" + \
			"fVal5=1.0000\n" + \
			"uID5=0\n" + \
			"fVal4=0.7500\n" + \
			"uID4=0\n" + \
			"fVal3=0.9200\n" + \
			"uID3=466532\n" + \
			"fVal2=0.0000\n" + \
			"uID2=554685\n" + \
			"fVal1=1.0000\n" + \
			"uID1=554685\n" + \
			"fVal0=0.5500\n" + \
			"uID0=1007612\n" + \
			"[Clouds]\n" + \
			"fCloudLevel2Distance=262144.0000\n" + \
			"fCloudLevel1Distance=32768.0000\n" + \
			"fCloudLevel0Distance=16384.0000\n" + \
			"fCloudNearFadeDistance=9000.0000\n" + \
			"[TerrainManager]\n" + \
			"fTreeLoadDistance=" + "{0:f}".format(self.fTreeLoadDistance) + "\n" + \
			"fBlockMaximumDistance=" + "{0:f}".format(self.fBlockMaximumDistance) + "\n" + \
			"fBlockLevel1Distance=" + "{0:f}".format(self.fBlockLevel1Distance) + "\n" + \
			"fBlockLevel0Distance=" + "{0:f}".format(self.fBlockLevel0Distance) + "\n" + \
			"fSplitDistanceMult=" + "{0:f}".format(self.fSplitDistanceMult) + "\n" + \
			"bShowLODInEditor=0\n" + \
			"[NavMesh]\n" + \
			"fObstacleAlpha=0.5000\n" + \
			"fCoverSideHighAlpha=0.8000\n" + \
			"fCoverSideLowAlpha=0.6500\n" + \
			"fEdgeFullAlpha=1.0000\n" + \
			"fEdgeHighAlpha=0.7500\n" + \
			"fEdgeLowAlpha=0.5000\n" + \
			"fTriangleFullAlpha=0.7000\n" + \
			"fTriangleHighAlpha=0.3500\n" + \
			"fTriangleLowAlpha=0.2000\n" + \
			"fLedgeBoxHalfHeight=25.0000\n" + \
			"fEdgeDistFromVert=10.0000\n" + \
			"fEdgeThickness=10.0000\n" + \
			"fPointSize=2.5000\n" + \
			"[Trees]\n" + \
			"bRenderSkinnedTrees=1\n" + \
			"uiMaxSkinnedTreesToRender=40\n" + \
			"[LOD]\n" + \
			"fLODFadeOutMultObjects=" + "{0:f}".format(self.fLODFadeOutMultObjects) + "\n" + \
			"fLODFadeOutMultActors=" + "{0:f}".format(self.fLODFadeOutMultActors) + "\n" + \
			"fLODFadeOutMultItems=" + "{0:f}".format(self.fLODFadeOutMultItems) + "\n" + \
			"fLODFadeOutMultSkyCell=1.0000\n" + \
			"[Water]\n" + \
			"iWaterReflectHeight=512\n" + \
			"iWaterReflectWidth=512\n" + \
			"bUseWaterDisplacements=1\n" + \
			"bUseWaterRefractions=1\n" + \
			"bUseWaterReflections=1\n" + \
			"bUseWaterDepth=1\n" + \
			"[General]\n" + \
			"fDefaultFOV=75\n" + \
			"iStoryManagerLoggingEvent=-1\n" + \
			"bEnableStoryManagerLogging=0\n" + \
			"bGamepadEnable=0\n"

		print("Generating SkyrimPrefs.ini...")
		inifile = open(path + "Documents/My Games/Skyrim/SkyrimPrefs.ini", "w+")
		inifile.write(prefs)
		inifile.close()

# Installer class
class Installer:
	def __init__(self):
		# Constants / Globals
		self.DSTDIR   = "Skyrim"
		self.BAKDIR   = "_Skyrim_bak"
		self.CACHEDIR = "__cache__"
		self.LSTFILE  = "patches_"
		self.MAINPKG  = "EnderalInstall_"
		self.LANGUAGE = "EN"
		self.WINEPREFIX=os.getenv("WINEPREFIX", "~/.wine")
		self.USERNAME = getpass.getuser()
		self.LINUX = True if platform.system() == "Linux" else False

		self.INSTALL = False
		self.CONFIGURE = False
		self.USE_WINEPREFIX = False
		self.GET_LSTFILE = False
		self.USE_ONETWEAK = False
		self.USE_MT = True
		self.DETAILS = "ultra"

		self.ROOT_URL  = "http://1.dl4sureai.de/files/pro/enderal/upd"
		self.PATCH_URL = "getlist.php?laun=enderal1.0.0.0&lang="

		self.iniGen = IniGenerator()

		# Detect screen resolution
		if self.LINUX == True:
			output = subprocess.Popen("xrandr | grep \"\*\" | cut -d\" \" -f4",
				shell=True, stdout=subprocess.PIPE).communicate()[0]
			output = output.split(b"\n")[0].split(b"x")
			self.iniGen.RES_X = int(output[0])
			self.iniGen.RES_Y = int(output[1])
		else:
			self.iniGen.RES_X = ctypes.windll.user32.GetSystemMetrics(0)
			self.iniGen.RES_Y = ctypes.windll.user32.GetSystemMetrics(1)

	def generateConfig(self):
		self.iniGen.LANGUAGE = self.LANGUAGE
		self.iniGen.SetLevel(self.DETAILS, self.USE_MT)
		if self.LINUX == True:
			if self.USE_WINEPREFIX == True:
				self.updatePluginlist(self.WINEPREFIX + "/drive_c/users/" + \
					self.USERNAME.lower() + "/")
				self.iniGen.Generate(self.WINEPREFIX + "/drive_c/users/" + \
					self.USERNAME.lower() + "/")
			else:
				print("Warning: WINEPREFIX unspecified, config is not updated.")
		else:
			self.updatePluginlist("C:/Users/" + self.USERNAME.lower() + "/")
			self.iniGen.Generate("C:/Users/" + self.USERNAME.lower() + "/")

	def updatePluginlist(self, confPath):
		print("Updating DLC and plugin list...")
		CONF_PATH=confPath + "/AppData/Local/Skyrim/"
		os.makedirs(CONF_PATH, exist_ok=True)
		# Backup plugins.txt and dlclist.txt
		try:
			shutil.move(CONF_PATH + "DLClist.txt", CONF_PATH + "DLClist_bak.txt")
			shutil.move(CONF_PATH + "plugins.txt", CONF_PATH + "plugins_bak.txt")
		except:
			# Continue if files were not found
			pass
		# Create empty dlclist.txt
		dlclist_txt = open(CONF_PATH + "DLClist.txt", "w+")
		dlclist_txt.close()
		# Create plugins.txt
		plugins_txt = open(CONF_PATH + "plugins.txt", "w+")
		plugins_txt.write("skyrim.esm\nupdate.esm\n")
		plugins_txt.close()

	def install(self):
		# Prepare directories
		shutil.move(self.DSTDIR, self.BAKDIR)
		os.makedirs(self.DSTDIR, exist_ok=True)
		os.makedirs(self.CACHEDIR, exist_ok=True)

		# Get patchlist if required
		listfile = pathlib.Path(self.CACHEDIR + '/' + \
			self.LSTFILE + self.LANGUAGE.lower() + ".lst")
		if not listfile.is_file():
			self.GET_LSTFILE = True

		if self.GET_LSTFILE == True:
			print("Downloading patch list...")
			wget(self.ROOT_URL + '/' + self.PATCH_URL + self.LANGUAGE.lower(),
				self.CACHEDIR + '/' + self.LSTFILE + self.LANGUAGE.lower() + ".lst")

		# Read patchlist and get version
		listfile = open(self.CACHEDIR + '/' + \
			self.LSTFILE + self.LANGUAGE.lower() + ".lst", 'r')
		patches = listfile.read().split()
		listfile.close()
		version = patches[-1][patches[-1].find('[')+1:patches[-1].find(']')]
	
		# Check if main package exists
		mainpkg = pathlib.Path(self.CACHEDIR + '/' + self.MAINPKG)
		if not mainpkg.is_file():
			print(mainpkg)
			print("Main package not found. Abort!")
			sys.exit(2)

		# Unzip main package
		unzip(self.CACHEDIR + '/' + self.MAINPKG, self.DSTDIR, self.LINUX)

		# Get patches if required and unzip them
		for x in patches:
			path = pathlib.Path(self.CACHEDIR + '/' + x)
			if not path.is_file():
				wget(self.ROOT_URL + '/' + self.LANGUAGE.lower() + '/' + x,
					self.CACHEDIR + '/' + x)
			unzip(self.CACHEDIR + '/' + x, self.DSTDIR, self.LINUX)

		# Copy required Skyrim files
		os.makedirs(self.DSTDIR + "/skyrim", exist_ok=True)
		os.makedirs(self.DSTDIR + "/data", exist_ok=True)

		copy(self.BAKDIR + "/atimgpud.dll", self.DSTDIR)
		copy(self.BAKDIR + "/binkw32.dll", self.DSTDIR)
		copy(self.BAKDIR + "/high.ini", self.DSTDIR)
		copy(self.BAKDIR + "/installscript.vdf", self.DSTDIR)
		copy(self.BAKDIR + "/low.ini", self.DSTDIR)
		copy(self.BAKDIR + "/medium.ini", self.DSTDIR)
		copy(self.BAKDIR + "/readme.txt", self.DSTDIR)
		copy(self.BAKDIR + "/Skyrim_default.ini", self.DSTDIR)
		copy(self.BAKDIR + "/SkyrimLauncher.exe", self.DSTDIR)
		copy(self.BAKDIR + "/steam_api.dll", self.DSTDIR)
		copy(self.BAKDIR + "/TESV.exe", self.DSTDIR)
		copy(self.BAKDIR + "/VeryHigh.ini", self.DSTDIR)
		copy(self.BAKDIR + "/Skyrim/SkyrimPrefs.ini", self.DSTDIR + "/skyrim")
		copy(self.BAKDIR + "/Data/Skyrim - Animations.bsa", self.DSTDIR + "/data")
		copy(self.BAKDIR + "/Data/Skyrim - Interface.bsa", self.DSTDIR + "/data")
		copy(self.BAKDIR + "/Data/Skyrim - Meshes.bsa", self.DSTDIR + "/data")
		copy(self.BAKDIR + "/Data/Skyrim - Misc.bsa", self.DSTDIR + "/data")
		copy(self.BAKDIR + "/Data/Skyrim - Shaders.bsa", self.DSTDIR + "/data")
		copy(self.BAKDIR + "/Data/Skyrim - Sounds.bsa", self.DSTDIR + "/data")
		copy(self.BAKDIR + "/Data/Skyrim - Textures.bsa", self.DSTDIR + "/data")
		copy(self.BAKDIR + "/Data/Skyrim - Voices.bsa", self.DSTDIR + "/data")
		copy(self.BAKDIR + "/Data/Update.bsa", self.DSTDIR + "/data")

		# Disable OneTweak
		print("Deactivating OneTweak...")
		if self.USE_ONETWEAK == False:
			shutil.move(self.DSTDIR + "/data/skse/plugins/onetweak.dll",
				self.DSTDIR + "/data/skse/plugins/onetweak.dll.bak")

		# Generate launcher config
		print("Generating Enderal launcher config...")
		config = \
			"[Values]\n" + \
			"bBackupStatSkyrim=0\n" + \
			"sBackupPathSkyrim=path\n" + \
			"bBackupStatEnderal=0\n" + \
			"sBackupPathEnderal=path\n" + \
			"sCurrentVersion=" + version + "\n" + \
			"bInstallUpdateAfterDownload=0\n" + \
			"sSkyrimFolderPath=" + os.path.abspath(self.DSTDIR) + "\n" + \
			"bNetConection=0\n" + \
			"bStartSteamOnLauncherStart=0\n" + \
			"bCloseLauncherAfterGameStart=1\n" + \
			"bUseOneTweak=0\n" + \
			"bInstallStat=1\n"
		os.makedirs(self.DSTDIR + "/EnderalLauncher/system/config", exist_ok=True)
		conffile = open(self.DSTDIR + "/EnderalLauncher/system/config/conf.sur", "w+")
		conffile.write(config)
		conffile.close()

	def run(self):
		if self.INSTALL == False and self.CONFIGURE == False:
			return 1

		if self.INSTALL == True:
			self.install()
		if self.CONFIGURE == True:
			self.generateConfig()

		return 0

def main():
	# Program entry point
	app = Installer()

	# Analyze command line
	parser = argparse.ArgumentParser(description="Alternative Enderal installer.")
	parser.add_argument("--skyrimdir", help="Path to Skyrim directory")
	parser.add_argument("--bakdir", help="Path to Skyrim backup directory")
	parser.add_argument("--cachedir", help="Path to cache directory which contains downloaded files")
	parser.add_argument("--update", help="Force redownload of patch list", action="store_true")
	parser.add_argument("--install", help="Install Enderal", action="store_true")
	parser.add_argument("--config", help="Generate config files", action="store_true")
	parser.add_argument("--language", help="Language to install (EN is default)",
		choices=["DE", "EN"])
	parser.add_argument("--main-pkg", help="Path to main Enderal installation package (.gz)")
	parser.add_argument("--onetweak", help="Enables OneTweak (disabled by default)",
		action="store_true")
	parser.add_argument("--details", help="Detail level, ultra is the default.",
		choices=["vlow", "low", "med", "high", "vhigh", "ultra"])
	parser.add_argument("--singlethread", help="Disables Multithreading (enabled by default)",
		action="store_true")
	parser.add_argument("--resx", help="Screen width, default is 1920", type=int)
	parser.add_argument("--resy", help="Screen height, default is 1080", type=int)
	parser.add_argument("--wine", help="Install relative to WINEPREFIX environment variable",
		action="store_true")
	args = vars(parser.parse_args())

	if args["install"] == True:
		app.INSTALL = True
	if args["config"] == True:
		app.CONFIGURE = True
	if args["update"] == True:
		app.GET_LSTFILE = True
	if args["bakdir"] != None:
		app.BAKDIR = args["bakdir"]
	if args["skyrimdir"] != None:
		app.DSTDIR = args["skyrimdir"]
	if args["cachedir"] != None:
		app.CACHEDIR = args["cachedir"]
	if args["language"] != None:
		app.LANGUAGE = args["language"]
	if args["details"] != None:
		app.DETAILS = args["details"]
	if args["onetweak"] == True:
		app.USE_ONETWEAK = True
	if args["singlethread"] == True:
		app.USE_MT = False
	if args["resx"] != None:
		app.iniGen.RES_X = args["resx"]
	if args["resy"] != None:
		app.iniGen.RES_Y = args["resy"]
	if args["wine"] == True:
		app.USE_WINEPREFIX = True
	if args["main_pkg"] != None:
		app.MAINPKG = args["main_pkg"]
	else:
		app.MAINPKG = app.MAINPKG + app.LANGUAGE + ".gz"

	if app.run() != 0:
		parser.print_help()
		sys.exit(1)

	sys.exit(0)

if __name__ == "__main__":
	main()

