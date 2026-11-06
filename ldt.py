#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2026.2.2),
    on Thu Nov  5 21:04:10 2026
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (
    NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, STOPPING, FINISHED, PRESSED, 
    RELEASED, FOREVER, priority
)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2026.2.2'
expName = 'ldt'  # from the Builder filename that created this script
expVersion = ''
# a list of functions to run when the experiment ends (starts off blank)
runAtExit = []
# information about this experiment
expInfo = {
    'participant': '1',
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'expVersion|hid': expVersion,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1024,768]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']
    # replace default participant ID
    if prefs.piloting['replaceParticipantID']:
        expInfo['participant'] = 'pilot'

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = 'data/' + expInfo['participant'] + '_' + expName + '_' + expInfo['date']
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version=expVersion,
        extraInfo=expInfo, runtimeInfo=None,
        originPath='ldt.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    # store pilot mode in data file
    thisExp.addData('piloting', PILOTING, priority=priority.LOW)
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('info')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    if PILOTING:
        # show a visual indicator if we're in piloting mode
        if prefs.piloting['showPilotingIndicator']:
            win.showPilotingIndicator()
        # always show the mouse in piloting mode
        if prefs.piloting['forceMouseVisible']:
            win.mouseVisible = True
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    ioSession = ioServer = eyetracker = None
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ptb'
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], currentRoutine=None):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    currentRoutine : psychopy.data.Routine
        Current Routine we are in at time of pausing, if any. This object tells PsychoPy what Components to pause/play/dispatch.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='PsychToolbox',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # dispatch messages on response components
        if currentRoutine is not None:
            for comp in currentRoutine.getDispatchComponents():
                comp.device.dispatchMessages()
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # update experiment info
    expInfo['date'] = data.getDateStr()
    expInfo['expName'] = expName
    expInfo['expVersion'] = expVersion
    expInfo['psychopyVersion'] = psychopyVersion
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='PsychToolbox'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "instructions" ---
    # Run 'Begin Experiment' code from setupTask
    win.recordFrameIntervals = False
    win.frameIntervals.clear()
    win.refreshThreshold = 1.5 * frameDur
    instructionText = visual.TextStim(win=win, name='instructionText',
        text='',
        font='Arial',
        pos=[0,0], draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    beginKey = keyboard.Keyboard(deviceName='defaultKeyboard', backend='PsychToolbox')
    
    # --- Initialize components for Routine "trial" ---
    fixation = visual.TextStim(win=win, name='fixation',
        text='+',
        font='Arial',
        pos=[0,0], draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    prime_text = visual.TextStim(win=win, name='prime_text',
        text='',
        font='Arial',
        pos=[0,0], draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    target_text = visual.TextStim(win=win, name='target_text',
        text='',
        font='Arial',
        pos=[0,0], draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    decision = keyboard.Keyboard(deviceName='defaultKeyboard', backend='PsychToolbox')
    
    # --- Initialize components for Routine "feedback" ---
    feedbackText = visual.TextStim(win=win, name='feedbackText',
        text='',
        font='Arial',
        pos=[0,0], draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "interval" ---
    blankScreen = visual.TextStim(win=win, name='blankScreen',
        text=' ',
        font='Arial',
        pos=[0,0], draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "rest" ---
    breakText = visual.TextStim(win=win, name='breakText',
        text='Practice is complete. Take a break.\n\nPress SPACE to start the main trials.',
        font='Arial',
        pos=[0,0], draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    resumeKey = keyboard.Keyboard(deviceName='defaultKeyboard', backend='PsychToolbox')
    
    # --- Initialize components for Routine "trial" ---
    fixation = visual.TextStim(win=win, name='fixation',
        text='+',
        font='Arial',
        pos=[0,0], draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    prime_text = visual.TextStim(win=win, name='prime_text',
        text='',
        font='Arial',
        pos=[0,0], draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    target_text = visual.TextStim(win=win, name='target_text',
        text='',
        font='Arial',
        pos=[0,0], draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    decision = keyboard.Keyboard(deviceName='defaultKeyboard', backend='PsychToolbox')
    
    # --- Initialize components for Routine "interval" ---
    blankScreen = visual.TextStim(win=win, name='blankScreen',
        text=' ',
        font='Arial',
        pos=[0,0], draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "endScreen" ---
    endText = visual.TextStim(win=win, name='endText',
        text='Thank you. The task is complete.',
        font='Arial',
        pos=[0,0], draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    if eyetracker is not None:
        eyetracker.enableEventReporting()
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "instructions" ---
    # create an object to store info about Routine instructions
    instructions = data.Routine(
        name='instructions',
        components=[instructionText, beginKey],
    )
    instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from setupTask
    participantNumber = int(expInfo['participant'])
    listPath = f'trial_lists/trials_p{participantNumber:02d}.csv'
    wordKey, nonwordKey = ('f', 'j') if participantNumber % 2 else ('j', 'f')
    if not expInfo.get('frameRate'):
        raise RuntimeError('Refresh rate could not be measured. Restart on a display with a stable refresh rate.')
    refreshHz = round(expInfo['frameRate'])
    fixFrames = round(0.5 * refreshHz)
    primeFrames = round(0.15 * refreshHz)
    responseFrames = round(2 * refreshHz)
    instructionText.setText(f'Look at the UPPERCASE letters.\n\nPress {wordKey.upper()} for a real English word.\nPress {nonwordKey.upper()} for a made-up word.\n\nUse the keys by themselves. Press SPACE to begin practice.')
    # create starting attributes for beginKey
    beginKey.keys = []
    beginKey.rt = []
    _beginKey_allKeys = []
    # store start times for instructions
    instructions.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instructions.tStart = globalClock.getTime(format='float')
    instructions.status = STARTED
    thisExp.addData('instructions.started', instructions.tStart)
    instructions.maxDuration = None
    # keep track of which components have finished
    instructionsComponents = instructions.components
    for thisComponent in instructions.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "instructions" ---
    thisExp.currentRoutine = instructions
    instructions.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instructionText* updates
        
        # if instructionText is starting this frame...
        if instructionText.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instructionText.frameNStart = frameN  # exact frame index
            instructionText.tStart = t  # local t and not account for scr refresh
            instructionText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructionText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instructionText.started')
            # update status
            instructionText.status = STARTED
            instructionText.setAutoDraw(True)
        
        # if instructionText is active this frame...
        if instructionText.status == STARTED:
            # update params
            pass
        
        # *beginKey* updates
        waitOnFlip = False
        
        # if beginKey is starting this frame...
        if beginKey.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            beginKey.frameNStart = frameN  # exact frame index
            beginKey.tStart = t  # local t and not account for scr refresh
            beginKey.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(beginKey, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'beginKey.started')
            # update status
            beginKey.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(beginKey.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(beginKey.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if beginKey.status == STARTED and not waitOnFlip:
            theseKeys = beginKey.getKeys(keyList=["space"], ignoreKeys=["escape"], waitRelease=False)
            _beginKey_allKeys.extend(theseKeys)
            if len(_beginKey_allKeys):
                beginKey.keys = _beginKey_allKeys[-1].name  # just the last key pressed
                beginKey.rt = _beginKey_allKeys[-1].rt
                beginKey.duration = _beginKey_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=instructions,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            instructions.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if instructions.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in instructions.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instructions" ---
    for thisComponent in instructions.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instructions
    instructions.tStop = globalClock.getTime(format='float')
    instructions.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instructions.stopped', instructions.tStop)
    # check responses
    if beginKey.keys in ['', [], None]:  # No response was made
        beginKey.keys = None
    thisExp.addData('beginKey.keys',beginKey.keys)
    if beginKey.keys != None:  # we had a response
        thisExp.addData('beginKey.rt', beginKey.rt)
        thisExp.addData('beginKey.duration', beginKey.duration)
    thisExp.nextEntry()
    # the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    practice_loop = data.TrialHandler2(
        name='practice_loop',
        nReps=1, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions(
        listPath, 
        selection='0:8'
    )
    , 
        seed=None, 
        isTrials=True, 
    )
    thisExp.addLoop(practice_loop)  # add the loop to the experiment
    thisPractice_loop = practice_loop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPractice_loop.rgb)
    if thisPractice_loop != None:
        for paramName in thisPractice_loop:
            globals()[paramName] = thisPractice_loop[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisPractice_loop in practice_loop:
        practice_loop.status = STARTED
        if hasattr(thisPractice_loop, 'status'):
            thisPractice_loop.status = STARTED
        currentLoop = practice_loop
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisPractice_loop.rgb)
        if thisPractice_loop != None:
            for paramName in thisPractice_loop:
                globals()[paramName] = thisPractice_loop[paramName]
        
        # --- Prepare to start Routine "trial" ---
        # create an object to store info about Routine trial
        trial = data.Routine(
            name='trial',
            components=[fixation, prime_text, target_text, decision],
        )
        trial.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from trialTiming
        targetFrame = fixFrames + round(soa * refreshHz / 1000)
        firstInterval = len(win.frameIntervals)
        dropsAtStart = win.nDroppedFrames
        win.recordFrameIntervals = True
        prime_text.setText(prime)
        target_text.setText(target.upper())
        # create starting attributes for decision
        decision.keys = []
        decision.rt = []
        _decision_allKeys = []
        # store start times for trial
        trial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        trial.tStart = globalClock.getTime(format='float')
        trial.status = STARTED
        thisExp.addData('trial.started', trial.tStart)
        trial.maxDuration = None
        # keep track of which components have finished
        trialComponents = trial.components
        for thisComponent in trial.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "trial" ---
        thisExp.currentRoutine = trial
        trial.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisPractice_loop, 'status') and thisPractice_loop.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fixation* updates
            
            # if fixation is starting this frame...
            if fixation.status == NOT_STARTED and frameN >= 0:
                # keep track of start time/frame for later
                fixation.frameNStart = frameN  # exact frame index
                fixation.tStart = t  # local t and not account for scr refresh
                fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation.started')
                # update status
                fixation.status = STARTED
                fixation.setAutoDraw(True)
            
            # if fixation is active this frame...
            if fixation.status == STARTED:
                # update params
                pass
            
            # if fixation is stopping this frame...
            if fixation.status == STARTED:
                if frameN >= (fixation.frameNStart + fixFrames):
                    # keep track of stop time/frame for later
                    fixation.tStop = t  # not accounting for scr refresh
                    fixation.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation.stopped')
                    # update status
                    fixation.status = FINISHED
                    fixation.setAutoDraw(False)
            
            # *prime_text* updates
            
            # if prime_text is starting this frame...
            if prime_text.status == NOT_STARTED and frameN >= fixFrames:
                # keep track of start time/frame for later
                prime_text.frameNStart = frameN  # exact frame index
                prime_text.tStart = t  # local t and not account for scr refresh
                prime_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(prime_text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'prime_text.started')
                # update status
                prime_text.status = STARTED
                prime_text.setAutoDraw(True)
            
            # if prime_text is active this frame...
            if prime_text.status == STARTED:
                # update params
                pass
            
            # if prime_text is stopping this frame...
            if prime_text.status == STARTED:
                if frameN >= (prime_text.frameNStart + primeFrames):
                    # keep track of stop time/frame for later
                    prime_text.tStop = t  # not accounting for scr refresh
                    prime_text.tStopRefresh = tThisFlipGlobal  # on global time
                    prime_text.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'prime_text.stopped')
                    # update status
                    prime_text.status = FINISHED
                    prime_text.setAutoDraw(False)
            
            # *target_text* updates
            
            # if target_text is starting this frame...
            if target_text.status == NOT_STARTED and frameN >= targetFrame:
                # keep track of start time/frame for later
                target_text.frameNStart = frameN  # exact frame index
                target_text.tStart = t  # local t and not account for scr refresh
                target_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(target_text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'target_text.started')
                # update status
                target_text.status = STARTED
                target_text.setAutoDraw(True)
            
            # if target_text is active this frame...
            if target_text.status == STARTED:
                # update params
                pass
            
            # if target_text is stopping this frame...
            if target_text.status == STARTED:
                if frameN >= (target_text.frameNStart + responseFrames):
                    # keep track of stop time/frame for later
                    target_text.tStop = t  # not accounting for scr refresh
                    target_text.tStopRefresh = tThisFlipGlobal  # on global time
                    target_text.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'target_text.stopped')
                    # update status
                    target_text.status = FINISHED
                    target_text.setAutoDraw(False)
            
            # *decision* updates
            waitOnFlip = False
            
            # if decision is starting this frame...
            if decision.status == NOT_STARTED and frameN >= targetFrame:
                # keep track of start time/frame for later
                decision.frameNStart = frameN  # exact frame index
                decision.tStart = t  # local t and not account for scr refresh
                decision.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(decision, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'decision.started')
                # update status
                decision.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(decision.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(decision.clearEvents, eventType='keyboard')  # clear events on next screen flip
            
            # if decision is stopping this frame...
            if decision.status == STARTED:
                if frameN >= (decision.frameNStart + responseFrames):
                    # keep track of stop time/frame for later
                    decision.tStop = t  # not accounting for scr refresh
                    decision.tStopRefresh = tThisFlipGlobal  # on global time
                    decision.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'decision.stopped')
                    # update status
                    decision.status = FINISHED
                    decision.status = FINISHED
            if decision.status == STARTED and not waitOnFlip:
                theseKeys = decision.getKeys(keyList=["f","j"], ignoreKeys=["escape"], waitRelease=False)
                _decision_allKeys.extend(theseKeys)
                if len(_decision_allKeys):
                    decision.keys = _decision_allKeys[0].name  # just the first key pressed
                    decision.rt = _decision_allKeys[0].rt
                    decision.duration = _decision_allKeys[0].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=trial,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                trial.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if trial.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in trial.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "trial" ---
        for thisComponent in trial.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for trial
        trial.tStop = globalClock.getTime(format='float')
        trial.tStopRefresh = tThisFlipGlobal
        thisExp.addData('trial.stopped', trial.tStop)
        # Run 'End Routine' code from trialTiming
        win.recordFrameIntervals = False
        thisExp.addData('dropped_frames', win.nDroppedFrames - dropsAtStart)
        thisExp.addData('recorded_intervals', len(win.frameIntervals) - firstInterval)
        thisExp.addData('trial_last_flip', float(win.lastFrameT))
        # check responses
        if decision.keys in ['', [], None]:  # No response was made
            decision.keys = None
        practice_loop.addData('decision.keys',decision.keys)
        if decision.keys != None:  # we had a response
            practice_loop.addData('decision.rt', decision.rt)
            practice_loop.addData('decision.duration', decision.duration)
        # Run 'End Routine' code from scoreTrial
        expectedKey = wordKey if correct_response == 'word' else nonwordKey
        
        def storeResponse(keyName, keyRT):
            correct = int(keyName == expectedKey)
            thisExp.addData('key', keyName)
            thisExp.addData('rt', keyRT)
            thisExp.addData('accuracy', correct)
            thisExp.addData('timeout', int(keyName == ''))
            if keyName == '':
                return 'Too slow'
            return 'Correct' if correct else 'Incorrect'
        
        pressed = decision.keys in ('f', 'j') and 0 <= decision.rt <= 2.0
        pendingDeadline = not pressed
        if pressed:
            feedbackMessage = storeResponse(decision.keys, decision.rt)
        else:
            feedbackMessage = ''
            def finishResponseWindow():
                # The deadline flip has removed the target. Include queued events
                # through 2.000 s, including ones after the final drawing iteration.
                remaining = 2.0 - decision.clock.getTime()
                if remaining > 0:
                    core.wait(remaining)
                keys = decision.getKeys(keyList=['f', 'j'], waitRelease=False)
                valid = [k for k in keys if 0 <= k.rt <= 2.0]
                event = min(valid, key=lambda k: k.rt) if valid else None
                message = storeResponse(event.name, event.rt) if event else storeResponse('', '')
                currentLoop.addData('decision.keys', event.name if event else None)
                currentLoop.addData('decision.rt', event.rt if event else None)
                currentLoop.addData('decision.duration', event.duration if event else None)
                if phase == 'practice':
                    feedbackText.setText(message)
            win.callOnFlip(finishResponseWindow)
        
        thisExp.addData('prime_shown', prime_text.text)
        thisExp.addData('target_shown', target_text.text)
        thisExp.addData('prime_onset', thisExp.thisEntry['prime_text.started'])
        thisExp.addData('target_onset', thisExp.thisEntry['target_text.started'])
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "feedback" ---
        # create an object to store info about Routine feedback
        feedback = data.Routine(
            name='feedback',
            components=[feedbackText],
        )
        feedback.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        feedbackText.setText(feedbackMessage)
        # store start times for feedback
        feedback.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        feedback.tStart = globalClock.getTime(format='float')
        feedback.status = STARTED
        thisExp.addData('feedback.started', feedback.tStart)
        feedback.maxDuration = None
        # keep track of which components have finished
        feedbackComponents = feedback.components
        for thisComponent in feedback.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "feedback" ---
        thisExp.currentRoutine = feedback
        feedback.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisPractice_loop, 'status') and thisPractice_loop.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *feedbackText* updates
            
            # if feedbackText is starting this frame...
            if feedbackText.status == NOT_STARTED and frameN >= int(pendingDeadline):
                # keep track of start time/frame for later
                feedbackText.frameNStart = frameN  # exact frame index
                feedbackText.tStart = t  # local t and not account for scr refresh
                feedbackText.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(feedbackText, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'feedbackText.started')
                # update status
                feedbackText.status = STARTED
                feedbackText.setAutoDraw(True)
            
            # if feedbackText is active this frame...
            if feedbackText.status == STARTED:
                # update params
                pass
            
            # if feedbackText is stopping this frame...
            if feedbackText.status == STARTED:
                if frameN >= (feedbackText.frameNStart + refreshHz):
                    # keep track of stop time/frame for later
                    feedbackText.tStop = t  # not accounting for scr refresh
                    feedbackText.tStopRefresh = tThisFlipGlobal  # on global time
                    feedbackText.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'feedbackText.stopped')
                    # update status
                    feedbackText.status = FINISHED
                    feedbackText.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=feedback,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                feedback.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if feedback.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in feedback.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "feedback" ---
        for thisComponent in feedback.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for feedback
        feedback.tStop = globalClock.getTime(format='float')
        feedback.tStopRefresh = tThisFlipGlobal
        thisExp.addData('feedback.stopped', feedback.tStop)
        # the Routine "feedback" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "interval" ---
        # create an object to store info about Routine interval
        interval = data.Routine(
            name='interval',
            components=[blankScreen],
        )
        interval.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # store start times for interval
        interval.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        interval.tStart = globalClock.getTime(format='float')
        interval.status = STARTED
        thisExp.addData('interval.started', interval.tStart)
        interval.maxDuration = None
        # keep track of which components have finished
        intervalComponents = interval.components
        for thisComponent in interval.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "interval" ---
        thisExp.currentRoutine = interval
        interval.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisPractice_loop, 'status') and thisPractice_loop.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *blankScreen* updates
            
            # if blankScreen is starting this frame...
            if blankScreen.status == NOT_STARTED and frameN >= 0:
                # keep track of start time/frame for later
                blankScreen.frameNStart = frameN  # exact frame index
                blankScreen.tStart = t  # local t and not account for scr refresh
                blankScreen.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blankScreen, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blankScreen.started')
                # update status
                blankScreen.status = STARTED
                blankScreen.setAutoDraw(True)
            
            # if blankScreen is active this frame...
            if blankScreen.status == STARTED:
                # update params
                pass
            
            # if blankScreen is stopping this frame...
            if blankScreen.status == STARTED:
                if frameN >= (blankScreen.frameNStart + fixFrames):
                    # keep track of stop time/frame for later
                    blankScreen.tStop = t  # not accounting for scr refresh
                    blankScreen.tStopRefresh = tThisFlipGlobal  # on global time
                    blankScreen.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blankScreen.stopped')
                    # update status
                    blankScreen.status = FINISHED
                    blankScreen.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=interval,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                interval.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if interval.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in interval.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "interval" ---
        for thisComponent in interval.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for interval
        interval.tStop = globalClock.getTime(format='float')
        interval.tStopRefresh = tThisFlipGlobal
        thisExp.addData('interval.stopped', interval.tStop)
        # the Routine "interval" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        # mark thisPractice_loop as finished
        if hasattr(thisPractice_loop, 'status'):
            thisPractice_loop.status = FINISHED
        # if awaiting a pause, pause now
        if practice_loop.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            practice_loop.status = STARTED
        thisExp.nextEntry()
        
    # completed 1 repeats of 'practice_loop'
    practice_loop.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "rest" ---
    # create an object to store info about Routine rest
    rest = data.Routine(
        name='rest',
        components=[breakText, resumeKey],
    )
    rest.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for resumeKey
    resumeKey.keys = []
    resumeKey.rt = []
    _resumeKey_allKeys = []
    # store start times for rest
    rest.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    rest.tStart = globalClock.getTime(format='float')
    rest.status = STARTED
    thisExp.addData('rest.started', rest.tStart)
    rest.maxDuration = None
    # keep track of which components have finished
    restComponents = rest.components
    for thisComponent in rest.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "rest" ---
    thisExp.currentRoutine = rest
    rest.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *breakText* updates
        
        # if breakText is starting this frame...
        if breakText.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            breakText.frameNStart = frameN  # exact frame index
            breakText.tStart = t  # local t and not account for scr refresh
            breakText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(breakText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'breakText.started')
            # update status
            breakText.status = STARTED
            breakText.setAutoDraw(True)
        
        # if breakText is active this frame...
        if breakText.status == STARTED:
            # update params
            pass
        
        # *resumeKey* updates
        waitOnFlip = False
        
        # if resumeKey is starting this frame...
        if resumeKey.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            resumeKey.frameNStart = frameN  # exact frame index
            resumeKey.tStart = t  # local t and not account for scr refresh
            resumeKey.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(resumeKey, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'resumeKey.started')
            # update status
            resumeKey.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(resumeKey.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(resumeKey.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if resumeKey.status == STARTED and not waitOnFlip:
            theseKeys = resumeKey.getKeys(keyList=["space"], ignoreKeys=["escape"], waitRelease=False)
            _resumeKey_allKeys.extend(theseKeys)
            if len(_resumeKey_allKeys):
                resumeKey.keys = _resumeKey_allKeys[-1].name  # just the last key pressed
                resumeKey.rt = _resumeKey_allKeys[-1].rt
                resumeKey.duration = _resumeKey_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=rest,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            rest.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if rest.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in rest.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "rest" ---
    for thisComponent in rest.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for rest
    rest.tStop = globalClock.getTime(format='float')
    rest.tStopRefresh = tThisFlipGlobal
    thisExp.addData('rest.stopped', rest.tStop)
    # check responses
    if resumeKey.keys in ['', [], None]:  # No response was made
        resumeKey.keys = None
    thisExp.addData('resumeKey.keys',resumeKey.keys)
    if resumeKey.keys != None:  # we had a response
        thisExp.addData('resumeKey.rt', resumeKey.rt)
        thisExp.addData('resumeKey.duration', resumeKey.duration)
    thisExp.nextEntry()
    # the Routine "rest" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    main_loop = data.TrialHandler2(
        name='main_loop',
        nReps=1, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions(
        listPath, 
        selection='8:104'
    )
    , 
        seed=None, 
        isTrials=True, 
    )
    thisExp.addLoop(main_loop)  # add the loop to the experiment
    thisMain_loop = main_loop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisMain_loop.rgb)
    if thisMain_loop != None:
        for paramName in thisMain_loop:
            globals()[paramName] = thisMain_loop[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisMain_loop in main_loop:
        main_loop.status = STARTED
        if hasattr(thisMain_loop, 'status'):
            thisMain_loop.status = STARTED
        currentLoop = main_loop
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisMain_loop.rgb)
        if thisMain_loop != None:
            for paramName in thisMain_loop:
                globals()[paramName] = thisMain_loop[paramName]
        
        # --- Prepare to start Routine "trial" ---
        # create an object to store info about Routine trial
        trial = data.Routine(
            name='trial',
            components=[fixation, prime_text, target_text, decision],
        )
        trial.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from trialTiming
        targetFrame = fixFrames + round(soa * refreshHz / 1000)
        firstInterval = len(win.frameIntervals)
        dropsAtStart = win.nDroppedFrames
        win.recordFrameIntervals = True
        prime_text.setText(prime)
        target_text.setText(target.upper())
        # create starting attributes for decision
        decision.keys = []
        decision.rt = []
        _decision_allKeys = []
        # store start times for trial
        trial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        trial.tStart = globalClock.getTime(format='float')
        trial.status = STARTED
        thisExp.addData('trial.started', trial.tStart)
        trial.maxDuration = None
        # keep track of which components have finished
        trialComponents = trial.components
        for thisComponent in trial.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "trial" ---
        thisExp.currentRoutine = trial
        trial.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisMain_loop, 'status') and thisMain_loop.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fixation* updates
            
            # if fixation is starting this frame...
            if fixation.status == NOT_STARTED and frameN >= 0:
                # keep track of start time/frame for later
                fixation.frameNStart = frameN  # exact frame index
                fixation.tStart = t  # local t and not account for scr refresh
                fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation.started')
                # update status
                fixation.status = STARTED
                fixation.setAutoDraw(True)
            
            # if fixation is active this frame...
            if fixation.status == STARTED:
                # update params
                pass
            
            # if fixation is stopping this frame...
            if fixation.status == STARTED:
                if frameN >= (fixation.frameNStart + fixFrames):
                    # keep track of stop time/frame for later
                    fixation.tStop = t  # not accounting for scr refresh
                    fixation.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation.stopped')
                    # update status
                    fixation.status = FINISHED
                    fixation.setAutoDraw(False)
            
            # *prime_text* updates
            
            # if prime_text is starting this frame...
            if prime_text.status == NOT_STARTED and frameN >= fixFrames:
                # keep track of start time/frame for later
                prime_text.frameNStart = frameN  # exact frame index
                prime_text.tStart = t  # local t and not account for scr refresh
                prime_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(prime_text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'prime_text.started')
                # update status
                prime_text.status = STARTED
                prime_text.setAutoDraw(True)
            
            # if prime_text is active this frame...
            if prime_text.status == STARTED:
                # update params
                pass
            
            # if prime_text is stopping this frame...
            if prime_text.status == STARTED:
                if frameN >= (prime_text.frameNStart + primeFrames):
                    # keep track of stop time/frame for later
                    prime_text.tStop = t  # not accounting for scr refresh
                    prime_text.tStopRefresh = tThisFlipGlobal  # on global time
                    prime_text.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'prime_text.stopped')
                    # update status
                    prime_text.status = FINISHED
                    prime_text.setAutoDraw(False)
            
            # *target_text* updates
            
            # if target_text is starting this frame...
            if target_text.status == NOT_STARTED and frameN >= targetFrame:
                # keep track of start time/frame for later
                target_text.frameNStart = frameN  # exact frame index
                target_text.tStart = t  # local t and not account for scr refresh
                target_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(target_text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'target_text.started')
                # update status
                target_text.status = STARTED
                target_text.setAutoDraw(True)
            
            # if target_text is active this frame...
            if target_text.status == STARTED:
                # update params
                pass
            
            # if target_text is stopping this frame...
            if target_text.status == STARTED:
                if frameN >= (target_text.frameNStart + responseFrames):
                    # keep track of stop time/frame for later
                    target_text.tStop = t  # not accounting for scr refresh
                    target_text.tStopRefresh = tThisFlipGlobal  # on global time
                    target_text.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'target_text.stopped')
                    # update status
                    target_text.status = FINISHED
                    target_text.setAutoDraw(False)
            
            # *decision* updates
            waitOnFlip = False
            
            # if decision is starting this frame...
            if decision.status == NOT_STARTED and frameN >= targetFrame:
                # keep track of start time/frame for later
                decision.frameNStart = frameN  # exact frame index
                decision.tStart = t  # local t and not account for scr refresh
                decision.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(decision, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'decision.started')
                # update status
                decision.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(decision.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(decision.clearEvents, eventType='keyboard')  # clear events on next screen flip
            
            # if decision is stopping this frame...
            if decision.status == STARTED:
                if frameN >= (decision.frameNStart + responseFrames):
                    # keep track of stop time/frame for later
                    decision.tStop = t  # not accounting for scr refresh
                    decision.tStopRefresh = tThisFlipGlobal  # on global time
                    decision.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'decision.stopped')
                    # update status
                    decision.status = FINISHED
                    decision.status = FINISHED
            if decision.status == STARTED and not waitOnFlip:
                theseKeys = decision.getKeys(keyList=["f","j"], ignoreKeys=["escape"], waitRelease=False)
                _decision_allKeys.extend(theseKeys)
                if len(_decision_allKeys):
                    decision.keys = _decision_allKeys[0].name  # just the first key pressed
                    decision.rt = _decision_allKeys[0].rt
                    decision.duration = _decision_allKeys[0].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=trial,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                trial.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if trial.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in trial.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "trial" ---
        for thisComponent in trial.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for trial
        trial.tStop = globalClock.getTime(format='float')
        trial.tStopRefresh = tThisFlipGlobal
        thisExp.addData('trial.stopped', trial.tStop)
        # Run 'End Routine' code from trialTiming
        win.recordFrameIntervals = False
        thisExp.addData('dropped_frames', win.nDroppedFrames - dropsAtStart)
        thisExp.addData('recorded_intervals', len(win.frameIntervals) - firstInterval)
        thisExp.addData('trial_last_flip', float(win.lastFrameT))
        # check responses
        if decision.keys in ['', [], None]:  # No response was made
            decision.keys = None
        main_loop.addData('decision.keys',decision.keys)
        if decision.keys != None:  # we had a response
            main_loop.addData('decision.rt', decision.rt)
            main_loop.addData('decision.duration', decision.duration)
        # Run 'End Routine' code from scoreTrial
        expectedKey = wordKey if correct_response == 'word' else nonwordKey
        
        def storeResponse(keyName, keyRT):
            correct = int(keyName == expectedKey)
            thisExp.addData('key', keyName)
            thisExp.addData('rt', keyRT)
            thisExp.addData('accuracy', correct)
            thisExp.addData('timeout', int(keyName == ''))
            if keyName == '':
                return 'Too slow'
            return 'Correct' if correct else 'Incorrect'
        
        pressed = decision.keys in ('f', 'j') and 0 <= decision.rt <= 2.0
        pendingDeadline = not pressed
        if pressed:
            feedbackMessage = storeResponse(decision.keys, decision.rt)
        else:
            feedbackMessage = ''
            def finishResponseWindow():
                # The deadline flip has removed the target. Include queued events
                # through 2.000 s, including ones after the final drawing iteration.
                remaining = 2.0 - decision.clock.getTime()
                if remaining > 0:
                    core.wait(remaining)
                keys = decision.getKeys(keyList=['f', 'j'], waitRelease=False)
                valid = [k for k in keys if 0 <= k.rt <= 2.0]
                event = min(valid, key=lambda k: k.rt) if valid else None
                message = storeResponse(event.name, event.rt) if event else storeResponse('', '')
                currentLoop.addData('decision.keys', event.name if event else None)
                currentLoop.addData('decision.rt', event.rt if event else None)
                currentLoop.addData('decision.duration', event.duration if event else None)
                if phase == 'practice':
                    feedbackText.setText(message)
            win.callOnFlip(finishResponseWindow)
        
        thisExp.addData('prime_shown', prime_text.text)
        thisExp.addData('target_shown', target_text.text)
        thisExp.addData('prime_onset', thisExp.thisEntry['prime_text.started'])
        thisExp.addData('target_onset', thisExp.thisEntry['target_text.started'])
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "interval" ---
        # create an object to store info about Routine interval
        interval = data.Routine(
            name='interval',
            components=[blankScreen],
        )
        interval.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # store start times for interval
        interval.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        interval.tStart = globalClock.getTime(format='float')
        interval.status = STARTED
        thisExp.addData('interval.started', interval.tStart)
        interval.maxDuration = None
        # keep track of which components have finished
        intervalComponents = interval.components
        for thisComponent in interval.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "interval" ---
        thisExp.currentRoutine = interval
        interval.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisMain_loop, 'status') and thisMain_loop.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *blankScreen* updates
            
            # if blankScreen is starting this frame...
            if blankScreen.status == NOT_STARTED and frameN >= 0:
                # keep track of start time/frame for later
                blankScreen.frameNStart = frameN  # exact frame index
                blankScreen.tStart = t  # local t and not account for scr refresh
                blankScreen.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blankScreen, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blankScreen.started')
                # update status
                blankScreen.status = STARTED
                blankScreen.setAutoDraw(True)
            
            # if blankScreen is active this frame...
            if blankScreen.status == STARTED:
                # update params
                pass
            
            # if blankScreen is stopping this frame...
            if blankScreen.status == STARTED:
                if frameN >= (blankScreen.frameNStart + fixFrames):
                    # keep track of stop time/frame for later
                    blankScreen.tStop = t  # not accounting for scr refresh
                    blankScreen.tStopRefresh = tThisFlipGlobal  # on global time
                    blankScreen.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blankScreen.stopped')
                    # update status
                    blankScreen.status = FINISHED
                    blankScreen.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=interval,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                interval.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if interval.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in interval.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "interval" ---
        for thisComponent in interval.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for interval
        interval.tStop = globalClock.getTime(format='float')
        interval.tStopRefresh = tThisFlipGlobal
        thisExp.addData('interval.stopped', interval.tStop)
        # the Routine "interval" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        # mark thisMain_loop as finished
        if hasattr(thisMain_loop, 'status'):
            thisMain_loop.status = FINISHED
        # if awaiting a pause, pause now
        if main_loop.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            main_loop.status = STARTED
        thisExp.nextEntry()
        
    # completed 1 repeats of 'main_loop'
    main_loop.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "endScreen" ---
    # create an object to store info about Routine endScreen
    endScreen = data.Routine(
        name='endScreen',
        components=[endText],
    )
    endScreen.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for endScreen
    endScreen.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    endScreen.tStart = globalClock.getTime(format='float')
    endScreen.status = STARTED
    thisExp.addData('endScreen.started', endScreen.tStart)
    endScreen.maxDuration = None
    # keep track of which components have finished
    endScreenComponents = endScreen.components
    for thisComponent in endScreen.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "endScreen" ---
    thisExp.currentRoutine = endScreen
    endScreen.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *endText* updates
        
        # if endText is starting this frame...
        if endText.status == NOT_STARTED and frameN >= 0:
            # keep track of start time/frame for later
            endText.frameNStart = frameN  # exact frame index
            endText.tStart = t  # local t and not account for scr refresh
            endText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(endText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'endText.started')
            # update status
            endText.status = STARTED
            endText.setAutoDraw(True)
        
        # if endText is active this frame...
        if endText.status == STARTED:
            # update params
            pass
        
        # if endText is stopping this frame...
        if endText.status == STARTED:
            if frameN >= (endText.frameNStart + responseFrames):
                # keep track of stop time/frame for later
                endText.tStop = t  # not accounting for scr refresh
                endText.tStopRefresh = tThisFlipGlobal  # on global time
                endText.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'endText.stopped')
                # update status
                endText.status = FINISHED
                endText.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=endScreen,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            endScreen.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if endScreen.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in endScreen.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "endScreen" ---
    for thisComponent in endScreen.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for endScreen
    endScreen.tStop = globalClock.getTime(format='float')
    endScreen.tStopRefresh = tThisFlipGlobal
    thisExp.addData('endScreen.stopped', endScreen.tStop)
    thisExp.nextEntry()
    # the Routine "endScreen" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    # Run 'End Experiment' code from setupTask
    win.saveFrameIntervals(fileName=thisExp.dataFileName + '_frameIntervals.log')
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    # stop any playback components
    if thisExp.currentRoutine is not None:
        for comp in thisExp.currentRoutine.getPlaybackComponents():
            comp.stop()
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # run any 'at exit' functions
    for fcn in runAtExit:
        fcn()
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
