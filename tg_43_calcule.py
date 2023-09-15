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
    dwell_positions= np.array(dwell_table[...,1:4]/10)

    # Decay
    time_since_calibration = (treatment_date - calibration_date).days
    sk = sk0*exp(-time_since_calibration*log(2)/half_life)
    time_since_calibration

    # Geometry function - GL(r,theta) and GL(0) calculation for line-source approximation
    npos = dwell_positions.shape[0]

    a = np.zeros((npos,3))
    r = np.zeros(npos)
    theta = np.zeros(npos)
    theta_deg = np.zeros(npos)
    beta = np.zeros(npos)

    for index,x in enumerate(dwell_positions):
        # last dwell
        if index == npos-1:
            if dwell_applicator[index] == dwell_applicator[index-1]:
                a[index] = a[index-1]
            else:
                a[index] = np.array([0,0,1])
        # first dwell
        elif index == 0:
            # same applicator 
            if dwell_applicator[index] == dwell_applicator[index+1]:
                a[index] = dwell_positions[index] - dwell_positions[index+1]
            else:
                a[index] = np.array([0,0,1])
        # intermediate dwell
        else:
            if (dwell_applicator[index] == dwell_applicator[index+1]):
                a[index] = dwell_positions[index] - dwell_positions[index+1]
            elif (dwell_applicator[index] == dwell_applicator[index-1]):
                a[index] = a[index-1]
            else:
                a[index] = np.array([0,0,1])
  
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
    # from scipy.interpolate import interp1d

    gl_table = genfromtxt('./SourceData/gl.csv', delimiter=',')
    # gl_interp = interp1d(gl_table[...,0], gl_table[...,1],bounds_error=False,fill_value="extrapolate")

    gl = np.zeros(npos)
    # gl = gl_interp(r)
    
    # Load 2D anisotropy function - F(r,theta) - table and interpolate
    F_table = genfromtxt('./SourceData/F.csv', delimiter=',')
    def inter1d(vy,vx,y):
        return vx[0]+((vx[1]-vx[0])/(vy[1]-vy[0]))*(y-vy[0])
    
    def get_indexes(array, value, lower_extrapolation = "nearest", upper_extrapolation = "nearest"):
        # Find indexes in the table headers for interpolation
        if value < array[0]:
            if(lower_extrapolation == "linear"):
                ind_lowerx = 0
                ind_upperx = 1
            elif(lower_extrapolation == "nearest"):
                ind_lowerx = 0
                ind_upperx = 0
            else:
                ind_lowerx = 0
                ind_upperx = 0               
        elif value > array[-1]:
            if(upper_extrapolation == "linear"):
                ind_lowerx = array.size -2
                ind_upperx = array.size -1
            elif(upper_extrapolation == "nearest"):
                ind_lowerx = array.size -1
                ind_upperx = array.size -1 
            else:
                ind_lowerx = array.size -1
                ind_upperx = array.size -1                            
        else:
            for index,element in enumerate(array):
                if array[index] >= value:
                    ind_upperx = index
                    ind_lowerx = index - 1
                    break
        return ind_lowerx, ind_upperx

    def inter_vect1d(x_array, y_array, x, lower_extrapolation = "nearest", upper_extrapolation = "nearest"):
        header_x = x_array
        header_y = y_array
        # Find X and Y index in the table headers
        if x < header_x[0]:
            if(lower_extrapolation == "linear"):
                ind_lowerx = 0
                ind_upperx = 1
            elif(lower_extrapolation == "nearest"):
                ind_lowerx = 0
                ind_upperx = 0
            else:
                ind_lowerx = 0
                ind_upperx = 0               
        elif x > header_x[-1]:
            if(upper_extrapolation == "linear"):
                ind_lowerx = header_x.size -2
                ind_upperx = header_x.size -1
            elif(upper_extrapolation == "nearest"):
                ind_lowerx = header_x.size -1
                ind_upperx = header_x.size -1 
            else:
                ind_lowerx = header_x.size -1
                ind_upperx = header_x.size -1                            
        else:
            for index,element in enumerate(header_x):
                if header_x[index] >= x:
                    ind_upperx = index
                    ind_lowerx = index - 1
                    break

        val_lowerx = header_x[ind_lowerx]
        val_upperx = header_x[ind_upperx]
        val_lowery = header_y[ind_lowerx]
        val_uppery = header_y[ind_upperx]

        interpolated_value = inter1d([val_lowerx, val_upperx], [val_lowery, val_uppery],x) # ver

        return interpolated_value

    for index,x in enumerate(r):
        gl[index] = inter_vect1d(gl_table[...,0], gl_table[...,1],r[index])
    
    def inter2d_2(matrix,x,y):
        header_x = matrix[0,1:]
        header_y = matrix[1:,0]
        data = matrix[1:,1:]
        # Find X and Y index in the table headers
        if x < header_x[0]:
            ind_lowerx = 0
            ind_upperx = 1
        elif x > header_x[-1]:
            ind_lowerx = header_x.size -2
            ind_upperx = header_x.size -1
        else:
            for index,element in enumerate(header_x):
                if header_x[index] >= x:
                    ind_upperx = index
                    ind_lowerx = index - 1
                    break

        if y < header_y[0]:
            ind_lowery = 0
            ind_uppery = 1
        elif y > header_y[-1]:
            ind_lowery = header_y.size -2
            ind_uppery = header_y.size -1
        else:
            for index,element in enumerate(header_y):
                if header_y[index] >= y:
                    ind_uppery = index
                    ind_lowery = index - 1
                    break
        val_lowerx = header_x[ind_lowerx]
        val_upperx = header_x[ind_upperx]
        val_lowery = header_y[ind_lowery]
        val_uppery = header_y[ind_uppery]

        int_1 = inter1d([val_lowery, val_uppery], [data[ind_lowery, ind_lowerx], data[ind_uppery, ind_lowerx]],y)
        int_2 = inter1d([val_lowery, val_uppery], [data[ind_lowery, ind_upperx], data[ind_uppery, ind_upperx]],y)
        int_3 = inter1d([val_lowerx, val_upperx], [int_1, int_2],x)

        return int_3
    Frt = np.zeros(npos)
    for index,x in enumerate(Frt):
        Frt[index] = inter2d_2(F_table,r[index],theta_deg[index])

    # Calculate dose rate for each dwell and total dose at point P
    total_dose = 0

    for index,x in enumerate(gl):
        dose_rate = (sk*lamda*GL[index])*x*Frt[index]/(GL0)
        total_dose += dwell_time[index]*dose_rate/3600
    
    return total_dose


