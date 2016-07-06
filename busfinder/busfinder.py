
import sys
import os
import requests
import operator
import xml.etree.ElementTree as ET
import _mysql
from geopy import geocoders
from geopy.distance import great_circle
from geopy.distance import vincenty

GMAPS_KEY = "AIzaSyAakxt7yFSijY2r7alEHtZKBww2j0E0hMA"
NEXT_BUS_REST_QUERY = "http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=sf-muni&t=0"



class Vehicle:
  def __init__(self, curr_lon, curr_lat, route_name, dist_from_ref):
    self.curr_lon = curr_lon
    self.curr_lat = curr_lat
    self.route_name = route_name
    self.dist_from_ref = 0
    
  def print_vehicle(self):
    print ("%s\t | %s\t | %s\t |%s\t |" %(self.route_name, self.curr_lat, self.curr_lon, self.dist_from_ref))

  @classmethod
  def delete_table_from_db(cls):
    dbid = _mysql.connect("localhost","root","","mysql")
    dbid.query("delete from nearestbuses")
    dbid.commit()
    dbid.close()

  def add_vehicle_to_db(self):
    dbid = _mysql.connect("localhost","root","","mysql")
    #curs = dbid.cursor()
    try:
      dbid.query("insert into nearestbuses values ('%s','%f','%f','%f')" % \
                   (self.route_name, self.curr_lat, self.curr_lon, self.dist_from_ref))
      dbid.commit()
    except:
      dbid.rollback()
      dbid.close()

  def compute_dist_from_ref(self, ref_lat, ref_lon):
    ref_coord = (ref_lat, ref_lon) # (lat, lon)
    bus_coord = (self.curr_lat, self.curr_lon) # (lat, lon) 
    self.dist_from_ref = vincenty(ref_coord, bus_coord).meters
    
class BusFinder:
  
  def __init__(self, address):
    self.ref_address = address
    self.bus_map = dict()
    self.sorted_bus_map = []
    goog_hdl = geocoders.GoogleV3(api_key=GMAPS_KEY)
    self.ref_lat, self.ref_lon = goog_hdl.geocode(address, timeout=10)[1]
  
  
  def __print_tabular_header(self):
    print "\n\n"
    print "========================================================" 
    print "Route \t | Latitude \t | Longitude \t | Dist(m)       |"
    print "========================================================"
    
  def get_nearest(self, num_buses):
    
    self.__get_bus_locations() 
    self.__compute_distances()
    self.__print_tabular_header()
    Vehicle.delete_table_from_db()
    self.sorted_bus_map = sorted(self.bus_map.values(), key=operator.attrgetter('dist_from_ref'))
    
    for index, vehicle in enumerate(self.sorted_bus_map):
      if index <= num_buses-1:
        vehicle.print_vehicle()
        vehicle.add_vehicle_to_db()
    
    
  def __get_bus_locations(self):
    """
        Sample XML response line from Nextbus
        <vehicle id="8719" routeTag="L_OWL" dirTag="L____I_N00" lat="37.7421099" lon="-122.49576" secsSinceReport="11" predictable="true" heading="88" speedKmHr="33"/>
        Check for vehicle tag and populate the dict
    """
    xml_response = requests.get(NEXT_BUS_REST_QUERY)
    xml_root = ET.fromstring( xml_response.text)
    
    for child in xml_root:
      if child.tag == 'vehicle':
        curr_lat = child.attrib['lat']
        curr_lon = child.attrib['lon']
        route_name = child.attrib['routeTag']
        self.bus_map[route_name] = Vehicle(float(curr_lon), float(curr_lat), route_name, 0)
      
  def __compute_distances(self):
    for key,value in self.bus_map.iteritems():
      value.compute_dist_from_ref(self.ref_lat, self.ref_lon)
    
  def tabulate(self, num_buses):
    pass
    
  def print_refpoint(self):
    print "Reference Address   : ",self.ref_address
    print "Reference Latitude  : ",self.ref_lat
    print "Reference Longitude : ",self.ref_lon
  