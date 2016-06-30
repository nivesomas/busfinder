
"""
	Author : Niveditha Somasundaram
   
   Date:  06/29/2016
   
   
"""

import busfinder


def run_main():
  bus_find_obj = busfinder.BusFinder("301 Howard St, San Francisco, CA 94105")

#  bus_find_obj.print_refpoint()
  bus_find_obj.get_nearest(10)
  







if __name__ == '__main__':
  run_main()