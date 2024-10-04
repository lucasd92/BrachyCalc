def _inter1d(vy,vx,y):
  return vx[0]+((vx[1]-vx[0])/(vy[1]-vy[0]))*(y-vy[0])

def _get_indexes(array, value, lower_extrapolation = "nearest", upper_extrapolation = "nearest"):
  # Find indexes in the table headers for interpolation
  if value < array[0]:
    if(lower_extrapolation == "linear"):
      ind_lower = 0
      ind_upper = 1
    elif(lower_extrapolation == "nearest"):
      ind_lower = 0
      ind_upper = 0
    else:
      ind_lower = 0
      ind_upper = 0               
  elif value > array[-1]:
    if(upper_extrapolation == "linear"):
      ind_lower = array.size -2
      ind_upper = array.size -1
    elif(upper_extrapolation == "nearest"):
      ind_lower = array.size -1
      ind_upper = array.size -1 
    else:
      ind_lower = array.size -1
      ind_upper = array.size -1                            
  else:
    for index,element in enumerate(array):
      if array[index] >= value:
        ind_upper = index
        ind_lower = index - 1
        break
  return ind_lower, ind_upper

def _inter_vect1d(x_array, y_array, x, lower_extrapolation = "nearest", upper_extrapolation = "nearest"):

  ind_lowerx, ind_upperx = _get_indexes(x_array, x, lower_extrapolation = lower_extrapolation, upper_extrapolation = upper_extrapolation)

  val_lowerx = x_array[ind_lowerx]
  val_upperx = x_array[ind_upperx]
  val_lowery = y_array[ind_lowerx]
  val_uppery = y_array[ind_upperx]

  interpolated_value = _inter1d([val_lowerx, val_upperx], [val_lowery, val_uppery],x) # ver

  return interpolated_value

def _inter2d_2(matrix, x, y, lower_extrapolation = "nearest", upper_extrapolation = "nearest"):
  header_x = matrix[0,1:]
  header_y = matrix[1:,0]
  data = matrix[1:,1:]
  # Find X and Y index in the table headers
  ind_lowerx, ind_upperx = _get_indexes(header_x, x, lower_extrapolation = lower_extrapolation, upper_extrapolation = upper_extrapolation)
  ind_lowery, ind_uppery = _get_indexes(header_y, y, lower_extrapolation = lower_extrapolation, upper_extrapolation = upper_extrapolation)

  val_lowerx = header_x[ind_lowerx]
  val_upperx = header_x[ind_upperx]
  val_lowery = header_y[ind_lowery]
  val_uppery = header_y[ind_uppery]

  int_1 = _inter1d([val_lowery, val_uppery], [data[ind_lowery, ind_lowerx], data[ind_uppery, ind_lowerx]],y)
  int_2 = _inter1d([val_lowery, val_uppery], [data[ind_lowery, ind_upperx], data[ind_uppery, ind_upperx]],y)
  int_3 = _inter1d([val_lowerx, val_upperx], [int_1, int_2],x)

  return int_3


def dose_calculation(P,dwell_table,treatment_date):
  from math import exp, log
  import numpy as np
  from numpy import genfromtxt
  import datetime as date

  # Source data
  f = open("./SourceData/source",'r')
  line = f.readline()
  while(line != ""):
    if line.startswith("lamda"):
      lamda = float(f.readline())
    elif line.startswith("calibration_date"):
      calibration_date = date.datetime.strptime(f.readline(), '%d/%m/%y %H:%M:%S\n')
    elif line.startswith("sk0"):
      sk0 = float(f.readline())
    elif line.startswith("half_life"):
      half_life = float(f.readline())
    elif line.startswith("length"):
      L = float(f.readline())
    line = f.readline()

  # Dwell data
  dwell_time = np.array(dwell_table[...,-1])
  dwell_applicator = np.array(dwell_table[...,0])
  dwell_positions= np.array(dwell_table[...,1:4])

  # Decay
  time_since_calibration = (treatment_date - calibration_date).days
  sk = sk0*exp(-time_since_calibration*log(2)/half_life)

  # Geometry function - GL(r,theta) and GL(0) calculation for line-source approximation
  npos = dwell_positions.shape[0]

  a = np.zeros((npos,3))
  r = np.zeros(npos)
  theta = np.zeros(npos)
  theta_deg = np.zeros(npos)
  beta = np.zeros(npos)

  # for each dwell in the dwell positions vector
  for index,x in enumerate(dwell_positions):
    # last dwell
    if index == npos-1:
      if dwell_applicator[index] == dwell_applicator[index-1]:
        a[index] = a[index-1]
      else:
        a[index] = np.array([1,0,0])
    # first dwell
    elif index == 0:
      # same applicator 
      if dwell_applicator[index] == dwell_applicator[index+1]:
        a[index] = dwell_positions[index] - dwell_positions[index+1]
      else:
        a[index] = np.array([1,0,0])
    # intermediate dwell
    else:
      if (dwell_applicator[index] == dwell_applicator[index+1]):
        a[index] = dwell_positions[index] - dwell_positions[index+1]
      elif (dwell_applicator[index] == dwell_applicator[index-1]):
        a[index] = a[index-1]
      else:
        a[index] = np.array([1,0,0])
  
    # Vector modulus calculation
    a_mod = np.sqrt(np.sum((a[index])**2))
    r[index] = np.sqrt(np.sum((P-x)**2))
    distance_to_tip = (a[index]/a_mod)*L/2
    r1 = np.sqrt(np.sum((P-x-distance_to_tip)**2))
    r2 = np.sqrt(np.sum((P-x+distance_to_tip)**2))
    
    dot_prod_0 = np.dot(P-x,a[index])
    dot_prod_1 = np.dot(P-x-distance_to_tip,a[index])
    dot_prod_2 = np.dot(P-x+distance_to_tip,a[index])
    cos0 = dot_prod_0/(r[index]*a_mod)
    cos1 = dot_prod_1/(r1*a_mod)
    cos2 = dot_prod_2/(r2*a_mod)
    theta[index] = np.arccos(cos0)
    theta1 = np.arccos(cos1)
    theta2 = np.arccos(cos2)

    theta_deg[index] = theta[index]*(180.0/np.pi)
    beta[index] = np.abs(theta2 - theta1)
    
  GL = np.zeros(npos)
  for index,x in enumerate(theta):
    if(x == 0):
      GL[index] = 1/(np.square(r[index])-(np.square(L)/4))
    else:
      GL[index] = beta[index]/(L*r[index]*np.sin(x))

  GL0 = 0.34649133/(L*1*np.sin(np.pi/2))

  # Load Radial dose function - gL(r) - table and interpolate
  from numpy import genfromtxt
  gl_table = genfromtxt('./SourceData/gl.csv', delimiter=',')

  gl = np.zeros(npos)
  for index,x in enumerate(r):
    gl[index] = _inter_vect1d(gl_table[...,0], gl_table[...,1],r[index], lower_extrapolation = "nearest", upper_extrapolation = "linear")

  # Load 2D anisotropy function - F(r,theta) - table and interpolate
  F_table = genfromtxt('./SourceData/F.csv', delimiter=',')

  Frt = np.zeros(npos)
  for index,x in enumerate(Frt):
    Frt[index] = _inter2d_2(F_table,r[index],theta_deg[index], lower_extrapolation = "nearest", upper_extrapolation = "nearest")

  # Calculate dose rate for each dwell and total dose at point P
  total_dose = 0

  for index,x in enumerate(gl):
    dose_rate = (sk*lamda*GL[index])*x*Frt[index]/(GL0)
    total_dose += dwell_time[index]*dose_rate/3600
  # Return dose in Grays with 2 decimals
  return np.round(total_dose/100,2)


