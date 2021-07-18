#!/usr/bin/env python3
#
##############################################################################
# Title:         HashRenamer.py                                              #
# Author(s):     l3uddz, desimaniac                                          #
# URL:           https://github.com/l3uddz/nzbgetScripts                     #
# Description:   Renames hashed media files to match the source NZB.         #
# --                                                                         #
#            Part of the Cloudbox project: https://cloudbox.works            #
##############################################################################

##############################################################################
#  Built on top of the NZBGet scripts template created by Clinton Hall       #
#    (https://github.com/clinton-hall).                                      #
#  Released under GNU General Public License v2.0                            #
##############################################################################


##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                          ###

# Rename files with hashes for file name
#
# NOTE: This script requires Python to be installed on your system.
#
##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                          ###
##############################################################################

import os
import re
import shutil
import sys

# NZBGet Exit Codes
NZBGET_POSTPROCESS_PARCHECK = 92
NZBGET_POSTPROCESS_SUCCESS = 93
NZBGET_POSTPROCESS_ERROR = 94
NZBGET_POSTPROCESS_NONE = 95


############################################################
# EXTENSION STUFF
############################################################

def do_check():
    if 'NZBOP_SCRIPTDIR' not in os.environ:
        print("This script can only be called from NZBGet (11.0 or later).")
        sys.exit(0)

    if os.environ['NZBOP_VERSION'][0:5] < '11.0':
        print("[ERROR] NZBGet Version %s is not supported. Please update NZBGet." % (str(os.environ['NZBOP_VERSION'])))
        sys.exit(0)

    print("Script triggered from NZBGet Version %s." % (str(os.environ['NZBOP_VERSION'])))

    status = 0
    if 'NZBPP_TOTALSTATUS' in os.environ:
        if not os.environ['NZBPP_TOTALSTATUS'] == 'SUCCESS':
            print("[ERROR] Download failed with status %s." % (os.environ['NZBPP_STATUS']))
            status = 1
    else:
        # Check par status
        if os.environ['NZBPP_PARSTATUS'] == '1' or os.environ['NZBPP_PARSTATUS'] == '4':
            print("[ERROR] Par-repair failed, setting status \"failed\".")
            status = 1

        # Check unpack status
        if os.environ['NZBPP_UNPACKSTATUS'] == '1':
            print("[ERROR] Unpack failed, setting status \"failed\".")
            status = 1

        if os.environ['NZBPP_UNPACKSTATUS'] == '0' and os.environ['NZBPP_PARSTATUS'] == '0':
            # Unpack was skipped due to nzb-file properties or due to errors during par-check

            if os.environ['NZBPP_HEALTH'] < 1000:
                print("[ERROR] Download health is compromised and Par-check/repair disabled or no .par2 files found. " \
                      "Setting status \"failed\".")
                print("[ERROR] Please check your Par-check/repair settings for future downloads.")
                status = 1

            else:
                print("[ERROR] Par-check/repair disabled or no .par2 files found, and Unpack not required. Health is " \
                      "ok so handle as though download successful.")
                print("[WARNING] Please check your Par-check/repair settings for future downloads.")

    # Check if destination directory exists (important for reprocessing of history items)
    if not os.path.isdir(os.environ['NZBPP_DIRECTORY']):
        print("[ERROR] Nothing to post-process: destination directory", os.environ[
            'NZBPP_DIRECTORY'], "doesn't exist. Setting status \"failed\".")
        status = 1

    # All checks done, now launching the script.
    if status == 1:
        sys.exit(NZBGET_POSTPROCESS_NONE)


def get_file_name(path):
    try:
        file_name = os.path.basename(path)
        extensions = re.findall(r'\.([^.]+)', file_name)
        ext = '.'.join(extensions)
        name = file_name.replace(".%s" % ext, '')
        return name, ext
    except Exception:
        pass
    return None


def is_file_hash(file_name):
    hash_regexp = [
        r'^[a-fA-F0-9]{40}$',
        r'^[a-fA-F0-9]{32}$',
        r'^[a-f0-9]{128}$',
        r'^[a-zA-Z0-9]{42}$'
    ]
    for hash in hash_regexp:
        if re.match(hash, file_name):
            return True
    return False


def find_files(folder, extension=None, depth=None):
    file_list = []
    start_count = folder.count(os.sep)
    for path, subdirs, files in os.walk(folder, topdown=True):
        for name in files:
            if depth and path.count(os.sep) - start_count >= depth:
                del subdirs[:]
                continue
            file = os.path.join(path, name)
            if not extension:
                file_list.append(file)
            else:
                if file.lower().endswith(extension.lower()):
                    file_list.append(file)

    return sorted(file_list, key=lambda x: x.count(os.path.sep), reverse=True)


############################################################
# MAIN
############################################################

# do checks
do_check()

# retrieve required variables
directory = os.path.normpath(os.environ['NZBPP_DIRECTORY'])
nzb_name = os.environ['NZBPP_NZBFILENAME']
if nzb_name is None:
    print("[ERROR] Unable to retrieve NZBPP_NZBFILENAME")
    sys.exit(NZBGET_POSTPROCESS_ERROR)
nzb_name = nzb_name.replace('.nzb', '')

print(("[INFO] Using \"%s\" for hashed filenames" % nzb_name))
print(("[INFO] Scanning \"%s\" for hashed filenames" % directory))

# scan for files
found_files = find_files(directory)
if not found_files:
    print(("[INFO] No files were found in \"%s\"" % directory))
    sys.exit(NZBGET_POSTPROCESS_NONE)
else:
    print(("[INFO] Found %d files to check for hashed filenames" % len(found_files)))
    # loop files checking for file hash
    moved_files = 0
    for found_file_path in found_files:
        # set variable
        dir_name = os.path.dirname(found_file_path)
        file_name, file_ext = get_file_name(found_file_path)

        # is this a file hash
        if is_file_hash(file_name):
            new_file_path = os.path.join(dir_name, "%s.%s" % (nzb_name, file_ext))
            print(("[INFO] Moving \"%s\" to \"%s\"" % (found_file_path, new_file_path)))
            try:
                shutil.move(found_file_path, new_file_path)
                moved_files += 1
            except Exception:
                print(("[ERROR] Failed moving \"%s\" to \"%s\"" % (found_file_path, new_file_path)))

    print(("[INFO] Finished processing \"%s\", moved %d files" % (directory, moved_files)))

sys.exit(NZBGET_POSTPROCESS_SUCCESS)