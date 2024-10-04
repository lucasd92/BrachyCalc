
import numpy as np

def parse_dwell_times(path,encode='utf-8'):
  is_right_report = False
  name = ""
  id = ""
  table = np.array([])
  with open(path, 'rb') as f:
    for line in f:
      str_line = str(line,encode)
      if str_line.startswith('  Patient:'):
        splitted = str_line.split(': ')
        name = splitted[1][:-5]
        id = splitted[2][:-12]
      if str_line.startswith(', Dwell Position Report,'):
        is_right_report = True
      if str_line.startswith('  Applicator,'):
        splitted = str_line.split('<')
        n_applicator = splitted[1][:splitted[1].find('>')]
      if str_line[2].isdecimal():
        arr_as_str =(n_applicator + ','+ str_line)
        if table.size > 0:
          table = np.vstack((table,
                             np.asarray(arr_as_str.split(',')[:-2],
                             dtype=float)))
        else:
          table = np.asarray(arr_as_str.split(',')[:-2],
                             dtype=float)
    table_dt = np.stack((table[...,0], #Applicator number
                         table[...,3], #X pos
                         table[...,4], #Y pos
                         table[...,5], #Z pos
                         table[...,-1]), #time in seconds
                         axis=-1)
  return table_dt,name,id,is_right_report

def parse_control_points(path,encode='utf-8'):
    is_right_report = False
    name = ""
    id = ""
    table = np.array([])
    with open(path, 'rb') as f:
        for line in f:
            str_line = str(line,encode)
            if str_line.startswith('  Patient:'):
                splitted = str_line.split(': ')
                name = splitted[1][:-5]
                id = splitted[2][:-12]
            if str_line.startswith(', Dose Control Point Report,'):
                is_right_report = True
            if str_line[2].isdecimal():
                if table.size > 0:
                    table = np.vstack((table,np.asarray(str_line.split(',')[2:-2],dtype=float)))
                else:
                    table = np.asarray(str_line.split(',')[2:-2],dtype=float)

    return table,name,id,is_right_report


