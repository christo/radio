import subprocess
import sys
import os

d = os.getenv('RIP_RADIO_HOME', ".") 
if not os.path.isdir(d):
    d = "."
p = subprocess.Popen("streamripper \"http://ice.somafm.com/{0}\" -d \"{1}\" -u 'VLC/2.1.5 LibVLC/2.1.5' -q -r".format(sys.argv[1],d), stdout=subprocess.PIPE, shell=True)
while True:
    out = p.stdout.read(1)
    if out == '' and p.poll() != None:
        break
    if out != '':
        sys.stdout.write(out)
        sys.stdout.flush()
 
