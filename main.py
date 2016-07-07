
"""
	Author : Niveditha Somasundaram
   
   Date:  06/29/2016
   
   
"""

import busfinder
import sys
import time

def run_main(argv):
  
  bus_find_obj = busfinder.BusFinder("301 Howard St, San Francisco, CA 94105")

#  bus_find_obj.print_refpoint()
  if len(sys.argv) > 1 and sys.argv[1] == '-d':
    while True :
      bus_find_obj.get_nearest(10)
      time.sleep(60)
  else:
    bus_find_obj.get_nearest(10)







if __name__ == '__main__':
  run_main(sys.argv[1:])