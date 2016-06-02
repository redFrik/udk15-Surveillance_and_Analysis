#make sure to install psutil

#this will list all running processes and their creation time

import psutil

for p in psutil.process_iter():
  print(p.create_time(), p)
