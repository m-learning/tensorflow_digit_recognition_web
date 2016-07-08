'''
Created on Jul 7, 2016

Utility class for recognizer controller

@author: Levan Tsinadze
'''

# Retrieves host name from arguments or sets defaults
def get_host_info(argv):
    
  if len(argv) > 1:
      host_nm = argv[1]
  else:
      host_nm = '0.0.0.0'
  
  return host_nm

# Retrieves port number from arguments or sets defaults
def get_port_info(argv):
    
  if len(argv) > 2:
      port_nm = argv[1]
  else:
      port_nm = 8080
      
  return port_nm

# Initializes host address and port number    
def get_host_and_port(argv):
    
  # Retrieves host and port from arguments or sets defaults
  host_nm = get_host_info(argv)
  port_nm = get_port_info(argv)
  
  return (host_nm, port_nm)