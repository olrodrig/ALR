import numpy as np
    
def select_data_in_range(x, y, err_y, x_range):
  x_sec     = x[x >= min(x_range)]
  y_sec     = y[x >= min(x_range)]
  if hasattr(err_y, '__len__') == True:
      err_y_sec = err_y[x >= min(x_range)]
  y_sec     = y_sec[x_sec <= max(x_range)]
  if hasattr(err_y, '__len__') == True:  
      err_y_sec = err_y_sec[x_sec <= max(x_range)]
  x_sec     = x_sec[x_sec <= max(x_range)]
  
  if hasattr(err_y, '__len__') == True:
      return x_sec, y_sec, err_y_sec
  else:
      return x_sec, y_sec

#read example data
def read_example_data(input_file_name, x_range=[], with_y_errors=True):
    
  #read input data
  x     = np.genfromtxt(input_file_name, usecols=0)
  y     = np.genfromtxt(input_file_name, usecols=1)
  if with_y_errors == True:
      err_y = np.genfromtxt(input_file_name, usecols=2)
  
  x_ref = 0.0
  if len(x_range) != 0:
      
      if len(x_range) == 2:
          if x_range[1] == 'lowest_x':
              x_ref = min(x)
  
      if with_y_errors == True:
          x, y, err_y = select_data_in_range(x, y, err_y, np.array(x_range[0])+x_ref)
      else:
          x, y = select_data_in_range(x, y, 0, np.array(x_range[0])+x_ref)
  
  if with_y_errors == True:
      return x, y, err_y
  else:
      return x, y
