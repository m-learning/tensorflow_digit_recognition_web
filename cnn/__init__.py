'''
Created on Jun 21, 2016

Files for training data

@author: Levan Tsinadze
'''

import os
from os import walk
import sys

path_is_not_appended = True

# Gets current package directory
def get_current_directory():
  
  global path_is_not_appended
  if path_is_not_appended:
    print 'Appending modules from local packages'
    current_dir = os.path.dirname(__file__)
    for root, _, _ in walk(current_dir):
      sys.path.append(root)
    path_is_not_appended = False
    print 'Modules from local packages appended successfully'
  else:
    print 'Modules from local packages already appended'

print 'Checking modules and dependencies'
get_current_directory()