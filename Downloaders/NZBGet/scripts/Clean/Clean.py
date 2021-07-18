#!/usr/bin/env python3
#

##############################################################################
### NZBGET SCAN SCRIPT                                                     ###

# Clean NZB name.
#
# Removes the following suffixes from NZB name:
# NZBgeek / Obfuscated / BUYMORE / Scrambled.
#
# NOTE: This script requires Python to be installed on your system.

### NZBGET SCAN SCRIPT                                                     ###
##############################################################################

from __future__ import print_function
import os, re, sys

# Exit codes used by NZBGet
POSTPROCESS_SUCCESS=93
POSTPROCESS_ERROR=94
POSTPROCESS_SKIP=95

# Check if the script is called from NZBGet 13.0 or later
if not 'NZBOP_SCRIPTDIR' in os.environ:
  print('*** NZBGet post-processing script ***')
  print('This script is supposed to be called from NZBGet (13.0 or later).')
  sys.exit(POSTPROCESS_ERROR)

if not 'NZBNP_NZBNAME' in os.environ:
  print('[WARN] Filename not found in environment')
  sys.exit(POSTPROCESS_ERROR)

fwp = os.environ['NZBNP_NZBNAME']
fwp = re.sub('(?i)-4P\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-4Planet\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-AsRequested\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-AsRequested-xpost\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-BUYMORE\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-Chamele0n\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-GEROV\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-iNC0GNiTO\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-NZBGeek\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-Obfuscated\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-postbot\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-Rakuv\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-Scrambled\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-WhiteRev\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-xpost\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)\[eztv\]\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)\[TGx\]\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)\[TGx\]-xpost\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)\[ettv\]\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-WRTEAM\.nzb$', '.nzb', fwp)
fwp = re.sub('(?i)-CAPTCHA\.nzb$', '.nzb', fwp)
if fwp:
  print('[NZB] NZBNAME=', fwp, sep='')

sys.exit(POSTPROCESS_SUCCESS)
