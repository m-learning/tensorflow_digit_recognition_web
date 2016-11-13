"""
Created on Jul 7, 2016

Utility class for recognizer controller

@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from cnn.transfer import cnn_flags as flags


def get_host_info():
  """Retrieves host address 
     from arguments or sets defaults
    Args:
      argv - runtime parameters
    Returns:
      port_nm - host address
  """
  return flags.host_nm

def get_port_info():
  """Retrieves port number 
     from arguments or sets defaults
    Args:
      argv - runtime parameters
    Returns:
      port_nm - port number
  """
  return flags.port_nm

# Initializes host address and port number    
def get_host_and_port():
  """Configures host and port for conreoller
    Args:
      argv - module arguments to mparse
    Returns:
      host and port for conreoller
  """
    
  host_nm = get_host_info()
  port_nm = get_port_info()
  
  return (host_nm, port_nm)