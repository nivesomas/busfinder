# busfinder
A python package to get a list of buses in close proximity to a given location

Usage:

For tabular display:
==============
python main.py
[STDOUT] ========================================================

[STDOUT] Route 	 | Latitude 	 | Longitude 	 | Dist(m)       |

[STDOUT] ========================================================

[STDOUT] 6	 | 37.7935299	 | -122.39345	 |450.226174402	 |

[STDOUT] 61	 | 37.79361	 | -122.39705	 |514.846529345	 |

[STDOUT] N	 | 37.78261	 | -122.38814	 |938.924797522	 |

[STDOUT] L	 | 37.78515	 | -122.40674	 |1200.54411086	 |

[STDOUT] 8	 | 37.78078	 | -122.40414	 |1302.86489866	 |

[STDOUT] 21	 | 37.78423	 | -122.40795	 |1340.28084337	 |

[STDOUT] F	 | 37.7949399	 | -122.40813	 |1360.1111535	 |

[STDOUT] 31	 | 37.78423	 | -122.41022	 |1522.50073968	 |

[STDOUT] 3	 | 37.78821	 | -122.4165	 |1962.98578658	 |

[STDOUT] 60	 | 37.7937299	 | -122.4174	 |2089.4776954	 |

 
 For realtime refresh(every 60 secs) along with tabular display:
 ===========================================
 python main.py -d
 
 The -d option makes the screipt run as a daemon. It queries NextBus every 60 seconds and stores the 
 location info of the closest buses in a MySQL database. The database can be read by any visualization
 software like Tableau for realtime map display of the buses
