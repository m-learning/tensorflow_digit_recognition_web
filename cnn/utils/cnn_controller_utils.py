'''
Created on Jul 7, 2016

Utility class for recognizer controller

@author: Levan Tsinadze
'''

def get_host_info(argv):
  """Retrieves host address 
     from arguments or sets defaults
    Args:
      argv - runtime parameters
    Return:
      port_nm - host address
  """
    
  if len(argv) > 1:
      host_nm = argv[1]
  else:
      host_nm = '0.0.0.0'
  
  return host_nm

def get_port_info(argv):
  """Retrieves port number 
     from arguments or sets defaults
    Args:
      argv - runtime parameters
    Return:
      port_nm - port number
  """
    
  if len(argv) > 2:
      port_nm = argv[2]
  else:
      port_nm = 8080
      
  return port_nm

# Initializes host address and port number    
def get_host_and_port(argv):
  """Configures host and port for conreoller
    Args:
      argv - module arguments to mparse
    Return:
      host and port for conreoller
  """
    
  host_nm = get_host_info(argv)
  port_nm = get_port_info(argv)
  
  return (host_nm, port_nm)