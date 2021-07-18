#!/usr/bin/env python3
### NZBGET SCAN SCRIPT

# Extract filenames from subjects containing [PRiVATE]-[WtFnZb]
#
# This extensions extracts obfuscated filenames from .nzb files
# created by WtFnZb.
#
# Supported subject formats:
#
# - [PRiVATE]-[WtFnZb]-[filename]-[1/5] - "" yEnc 0 (1/1)"
#
# - [PRiVATE]-[WtFnZb]-[5]-[1/filename] - "" yEnc
#
#
# NOTE: Requires Python and lxml (sudo apt install python3-lxml python-lxml)
#

### NZBGET SCAN SCRIPT

import sys
import os
import re

# Exit codes used by NZBGet
POSTPROCESS_SUCCESS = 93
POSTPROCESS_NONE = 95
POSTPROCESS_ERROR = 94

try:
    from lxml import etree
except ImportError:
    print(u'[ERROR] Python lxml required. Please install with "sudo apt install python-lxml" or "pip install lxml".')
    sys.exit(POSTPROCESS_ERROR)

patterns = (
    re.compile(r'^(?P<prefix>.*\[PRiVATE\]-\[WtFnZb\]-)'
               r'\[(?P<total>\d+)\]-\[(?P<segment>\d+)\/(?P<filename>.{3,}?)\]'
               r'\s+-\s+""\s+yEnc\s+',
               re.MULTILINE | re.UNICODE),
    re.compile(r'^(?P<prefix>.*\[PRiVATE\]-\[WtFnZb\]-)'
               r'\[(?P<filename>.{3,}?)\]-\[(?P<segment>\d+)/(?P<total>\d+)\]'
               r'\s+-\s+""\s+yEnc\s+',
               re.MULTILINE | re.UNICODE))

nzb_dir = os.getenv('NZBNP_DIRECTORY')
nzb_filename = os.getenv('NZBNP_FILENAME')
nzb_name = os.getenv('NZBNP_NZBNAME')
nzb_file_naming = os.getenv('NZBOP_FILENAMING')

if nzb_dir is None or nzb_filename is None or nzb_name is None:
    print('Please run as NZBGet plugin')
    sys.exit(POSTPROCESS_ERROR)

if nzb_file_naming is not None and nzb_file_naming.lower() != 'nzb':
    print(u'[ERROR] NZBGet setting FileNaming (under Download Queue) '
          u'must be set to "Nzb" for this extension to work correctly, exiting.')
    sys.exit(POSTPROCESS_ERROR)

if not os.path.exists(nzb_dir):
    print('[ERROR] NZB directory doesn\'t exist, exiting')
    sys.exit(POSTPROCESS_ERROR)

if not nzb_filename.lower().endswith('.nzb'):
    print(u'[ERROR] {} is not a .nzb file.'.format(nzb_filename))
    sys.exit(POSTPROCESS_ERROR)

nzb = os.path.join(nzb_dir, nzb_filename)
if not os.path.exists(nzb):
    print('[ERROR] {nzb} doesn\'t exist, exiting'.format(nzb=nzb))
    sys.exit(POSTPROCESS_ERROR)

with open(nzb, mode='rb') as infile:
    tree = etree.parse(infile)

changed = False
file_count = 0
totals = set()
filenames = set()

for f in tree.getiterator('{http://www.newzbin.com/DTD/2003/nzb}file'):
    subject = f.get('subject')
    if subject is None:
        print(u'[DETAIL] No subject in <file>, skipping')
        continue
    file_count += 1
    result = [re.match(pattern, subject) for pattern in patterns]
    matched = [m for m in result if m is not None]
    if len(matched) == 0:
        print(u'[INFO] No pattern matching subject, exiting.')
        sys.exit(POSTPROCESS_NONE)
    elif len(matched) > 1:
        print(u'[ERROR] Multiple patterns matched, exiting.')
        sys.exit(POSTPROCESS_ERROR)
    else:
        match = matched[0].groupdict()

    if match['filename'].lower().endswith('.par2'):
        print(u'[INFO] par2 exists, exiting')
        sys.exit(POSTPROCESS_NONE)

    if int(match['segment']) > int(match['total']):
        print(u'[DETAIL] Segment index is greater then total, skipping')
        continue

    # NZBGet subject parsing changes when duplicate filenames are present
    # prefix duplicates to avoid that
    if match['filename'] in filenames:
        match['filename'] = u'{}.{}'.format(file_count, match['filename'])

    filenames.add(match['filename'])

    s = u'WtFnZb "{filename}" yEnc ({segment}/{total})'.format(
        filename = match['filename'],
        segment = match['segment'],
        total = match['total'])

    print(u'[INFO] New subject {subject}'.format(subject=s.encode('ascii', 'ignore')))
    f.set('subject', s)
    changed = True
    totals.add(int(match['total']))

if not changed:
    print(u'[WARNING] No subject changed, exiting.')
    sys.exit(POSTPROCESS_NONE)

if len(totals) != 1:
    print(u'[WARNING] Mixed values for number of total segments, exiting.')
    sys.exit(POSTPROCESS_NONE)

if totals.pop() != file_count:
    print(u'[WARNING] Listed segment count does not match <file> count, exiting.')
    sys.exit(POSTPROCESS_NONE)

org = u'{}.wtfnzb.original.processed'.format(nzb)
exists_counter = 0
while os.path.exists(org):
    exists_counter += 1
    org = u'{}.{}.wtfnzb.original.processed'.format(nzb, exists_counter)

print(u'[INFO] Preserving original nzb as {}'.format(org))
os.rename(nzb, org)

print(u'[INFO] Writing {}'.format(nzb))
with open(nzb, mode='wb') as outfile:
    outfile.write(etree.tostring(tree,
        xml_declaration=True,
        encoding=tree.docinfo.encoding,
        doctype=tree.docinfo.doctype))

sys.exit(POSTPROCESS_SUCCESS)
