import matplotlib.pyplot as plt
from subprocess import Popen, PIPE

#p = Popen('while true ; do date -Ins ; /sbin/iw wlan0 station dump | grep signal ; done', stdout=PIPE,bufsize=1)
#for line in iter(p.stdout.readline, b''):
#    print line,

p = Popen('cat /proc/net/wireless', stdout=PIPE)
print p.stdout.read()[20:23]
p.stdout.close()
p.wait()
