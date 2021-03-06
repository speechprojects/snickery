'''
## E.g.:
python  script_data/reinsert_silence.py /Users/owatts/data/hybrid_work_2017/afs/inf.ed.ac.uk/group/cstr/projects/blizzard_entries/blizzard2017/parametric_synthesis/benchmark-merlin-data/labels/combilex/label_state_align/ /afs/inf.ed.ac.uk/group/cstr/projects/blizzard_entries/blizzard2017/hybrid_voice/data/predicted_params/train/ /tmp/testpad2
'''


import os, sys
import glob

# modify import path to obtain modules from the script/ directory:
snickery_dir = os.path.split(os.path.realpath(os.path.abspath(os.path.dirname(__file__))))[0]+'/'
sys.path.append(os.path.join(snickery_dir, 'script'))

from speech_manip import get_speech, put_speech
from train_halfphone import read_label, reinsert_terminal_silence
from util import basename, safe_makedir

# labdir = ''
# streams_dir = ''
# outdir = ''

try:
    labdir = sys.argv[1]
    streams_dir = sys.argv[2]
    topoutdir = sys.argv[3]
except:
    print 'called wrong!'

# labdir = '/Users/owatts/data/hybrid_work_2017/afs/inf.ed.ac.uk/group/cstr/projects/blizzard_entries/blizzard2017/parametric_synthesis/benchmark-merlin-data/labels/combilex/label_state_align/'

# ## this is the training data as regenerated by LSTM trained on it (for target cost):
# streams_dir = '/afs/inf.ed.ac.uk/group/cstr/projects/blizzard_entries/blizzard2017/hybrid_voice/data/predicted_params/train/'
 
# topoutdir = '/tmp/testpad'

## -------- 


## HTS style labels used in Blizzard:-
hts_quinphone_regex = '([^~]+)~([^-]+)-([^\+]+)\+([^\=]+)\=([^:]+)'
stream_list = ['mgc','lf0']
stream_dims = {'mgc': 60, 'lf0': 1}


for labfname in glob.glob(labdir + '/*.lab' ):
    print labfname

    lab = read_label(labfname, hts_quinphone_regex)
 
    base = basename(labfname)
    for stream in stream_list:
        stream_file = os.path.join(streams_dir, stream, base+'.'+stream)
        if not os.path.isfile(stream_file):
            print 'skip!'
            continue
        speech = get_speech(stream_file, stream_dims[stream])
        speech = reinsert_terminal_silence(speech, lab)

        outdir = topoutdir + '/' + stream
        safe_makedir(outdir)
        put_speech(speech, outdir + '/' + base + '.' + stream)
     