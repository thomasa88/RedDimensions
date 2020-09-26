#Author-Thomas Axelsson
#Description-Changes Sketch dimension color to red

# This file is part of ThreadKeeper, a Fusion 360 add-in for automatically
# restoring thread definitions after Fusion 360 update.
#
# Copyright (c) 2020 Thomas Axelsson
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import adsk.core, adsk.fusion, adsk.cam

import os
import pathlib
import shutil
import subprocess
import xml.etree.ElementTree as ET

NAME = 'RedDimensions'

# Must import lib as unique name, to avoid collision with other versions
# loaded by other add-ins
from .thomasa88lib import utils
from .thomasa88lib import events
#from .thomasa88lib import timeline
from .thomasa88lib import manifest
from .thomasa88lib import error

# Force modules to be fresh during development
import importlib
importlib.reload(thomasa88lib.utils)
importlib.reload(thomasa88lib.events)
#importlib.reload(thomasa88lib.timeline)
importlib.reload(thomasa88lib.manifest)
importlib.reload(thomasa88lib.error)

app_ = None
ui_ = None

error_catcher_ = thomasa88lib.error.ErrorCatcher()
events_manager_ = thomasa88lib.events.EventsManager(error_catcher_)
manifest_ = thomasa88lib.manifest.read()

def run(context):
    global app_
    global ui_
    with error_catcher_:
        app_ = adsk.core.Application.get()
        ui_ = app_.userInterface

def stop(context):
    with error_catcher_:
        set_color()

def set_color():
    deploy_folder = pathlib.Path(thomasa88lib.utils.get_fusion_deploy_folder())
    prod_folder = deploy_folder.parent

    # This is the file for the current Fusion, but we try to catch the file for the newly downloaded Fusion, after an update.
    #booth_file = (deploy_folder / 'Neutron' / 'Server' / 'Scene' / 'Resources' /
    #              'Environments' / 'PhotoBooth' / 'photobooth.XML')
    
    for booth_file in prod_folder.glob('*/Neutron/Server/Scene/Resources/Environments/PhotoBooth/photobooth.XML'):
        xml = ET.parse(booth_file)
        root = xml.getroot()
        color_element = root.find('./SketchDimensionColor')
        color_element.attrib['ARGB'] = '1 1 0 0'
        xml.write(booth_file)
