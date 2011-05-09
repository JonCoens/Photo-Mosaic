"""
 Color Math Module (colormath) 
 Copyright (C) 2009 Gregory Taylor

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Color Difference Equations
""" 
from math import *

pow_25_7 = pow(25.0, 7.0)

def delta_e_cie1976(color1, color2):
    """
    Calculates the Delta E (CIE1976) of two colors.
    """        
    # Color 1 
    L1 = float(color1.lab_l)
    a1 = float(color1.lab_a)
    b1 = float(color1.lab_b)
    # Color 2
    L2 = float(color2.lab_l)
    a2 = float(color2.lab_a)
    b2 = float(color2.lab_b)
    
    delta_L = pow(L1 - L2, 2)
    delta_a = pow(a1 - a2, 2)
    delta_b = pow(b1 - b2, 2)
    
    return sqrt(delta_L + delta_a + delta_b)

def delta_e_cie1994(color1, color2, K_L=1, K_C=1, K_H=1, K_1=0.045, K_2=0.015):
    """
    Calculates the Delta E (CIE1994) of two colors.
    
    K_l:
      0.045 graphic arts
      0.048 textiles
    K_2:
      0.015 graphic arts
      0.014 textiles
    K_L:
      1 default
      2 textiles
    """        
    # Color 1 
    L1 = float(color1.lab_l)
    a1 = float(color1.lab_a)
    b1 = float(color1.lab_b)
    # Color 2
    L2 = float(color2.lab_l)
    a2 = float(color2.lab_a)
    b2 = float(color2.lab_b)
        
    C_1 = sqrt(pow(a1, 2) + pow(b1, 2))
    C_2 = sqrt(pow(a2, 2) + pow(b2, 2))
    
    S_L = 1
    S_C = 1 + K_1 * C_1 
    S_H = 1 + K_2 * C_1

    delta_L = L1 - L2
    delta_C = C_1 - C_2
    delta_a = a1 - a2
    delta_b = b1 - b2
    
    try:
        delta_H = sqrt(pow(delta_a, 2) + pow(delta_b, 2) - pow(delta_C, 2))
    except ValueError:
        delta_H = 0.0
    
    L_group = pow(delta_L / (K_L * S_L), 2)
    C_group = pow(delta_C / (K_C * S_C), 2)
    H_group = pow(delta_H / (K_H * S_H), 2)
    
    return sqrt(L_group + C_group + H_group)

def delta_e_cie2000(color1, color2, Kl=1, Kc=1, Kh=1):
    """
    Calculates the Delta E (CIE2000) of two colors.
    """        
    # Color 1 
    L1 = float(color1.lab_l)
    a1 = float(color1.lab_a)
    b1 = float(color1.lab_b)
    # Color 2
    L2 = float(color2.lab_l)
    a2 = float(color2.lab_a)
    b2 = float(color2.lab_b)

    avg_Lp = (L1 + L2) / 2.0
    C1 = sqrt(a1*a1 + b1*b1)
    C2 = sqrt(a2*a2 + b2*b2)
    avg_C1_C2 = (C1 + C2) / 2.0 
    
    avg_C1_C2_2 = (avg_C1_C2*avg_C1_C2)
    avg_C1_C2_7 = avg_C1_C2_2 * avg_C1_C2_2 * avg_C1_C2_2 * avg_C1_C2

    G = 0.5 * (1 - sqrt(avg_C1_C2_7 / (avg_C1_C2_7 + pow_25_7)))

    a1p = (1.0 + G) * a1
    a2p = (1.0 + G) * a2
    C1p = sqrt(a1p*a1p + b1*b1)
    C2p = sqrt(a2p*a2p + b2*b2)
    avg_C1p_C2p =(C1p + C2p) / 2.0
   
    degreesB1A1p = degrees(atan2(b1,a1p))
    if degreesB1A1p >= 0:
        h1p = degreesB1A1p
    else:
        h1p = degreesB1A1p + 360
     
    degreesB2A2p = degrees(atan2(b2,a2p))
    if degreesB2A2p >= 0:
        h2p = degreesB2A2p
    else:
        h2p = degreesB2A2p + 360
      
    if fabs(h1p - h2p) > 180:
        avg_Hp = (h1p + h2p + 360) / 2.0
    else:
        avg_Hp = (h1p + h2p) / 2.0

    T = 1 - 0.17 * cos(radians(avg_Hp - 30)) + 0.24 * cos(radians(2 * avg_Hp)) + 0.32 * cos(radians(3 * avg_Hp + 6)) - 0.2  * cos(radians(4 * avg_Hp - 63))

    diff_h2p_h1p = h2p - h1p
    if fabs(diff_h2p_h1p) <= 180:
        delta_hp = diff_h2p_h1p
    elif (fabs(diff_h2p_h1p) > 180) and (h2p <= h1p):
        delta_hp = diff_h2p_h1p + 360
    else:
        delta_hp = diff_h2p_h1p - 360
      
    delta_Lp = L2 - L1
    delta_Cp = C2p - C1p
    delta_Hp = 2 * sqrt(C2p * C1p) * sin(radians(delta_hp) / 2.0)
   
    avg_Lp_2 = (avg_Lp - 50) * (avg_Lp - 50)
    S_L = 1 + ((0.015 * avg_Lp_2) / sqrt(20 + avg_Lp_2))
    S_C = 1 + 0.045 * avg_C1p_C2p
    S_H = 1 + 0.015 * avg_C1p_C2p * T
   
    value = ((avg_Hp - 275) / 25)
    delta_ro = 30 * exp(-(value * value))
    
    avg_C1p_C2p_2 = avg_C1p_C2p * avg_C1p_C2p
    avg_C1p_C2p_7 = avg_C1p_C2p_2 * avg_C1p_C2p_2 * avg_C1p_C2p_2 * avg_C1p_C2p
    
    R_C = sqrt((avg_C1p_C2p_7) / (avg_C1p_C2p_7 + pow_25_7));
    R_T = -2 * R_C * sin(2 * radians(delta_ro))

    delta_Lp_2 = (delta_Lp /(S_L * Kl)) * (delta_Lp /(S_L * Kl))
    delta_Cp_2 = (delta_Cp /(S_C * Kc)) * (delta_Cp /(S_C * Kc))
    delta_Hp_2 = (delta_Hp /(S_H * Kh)) * (delta_Hp /(S_H * Kh))
    delta_E = sqrt(delta_Lp_2 + delta_Cp_2 + delta_Hp_2 + R_T * (delta_Cp /(S_C * Kc)) * (delta_Hp / (S_H * Kh)))

    return delta_E

def delta_e_cmc(color1, color2, pl=2, pc=1):
    """
    Calculates the Delta E (CIE1994) of two colors.
    
    CMC values
      Acceptability: pl=2, pc=1
      Perceptability: pl=1, pc=1
    """        
    # Color 1 
    L1 = float(color1.lab_l)
    a1 = float(color1.lab_a)
    b1 = float(color1.lab_b)
    # Color 2
    L2 = float(color2.lab_l)
    a2 = float(color2.lab_a)
    b2 = float(color2.lab_b)
    
    delta_L = L1 - L2
    delta_a = a1 - a2
    delta_b = b1 - b2
    
    C_1 = sqrt(pow(a1, 2) + pow(b1, 2))
    C_2 = sqrt(pow(a2, 2) + pow(b2, 2))
    
    H_1 = degrees(atan2(b1, a1))
    
    if H_1 < 0:
        H_1 = H_1 + 360
    
    F = sqrt(pow(C_1, 4) / (pow(C_1, 4) + 1900.0))
    if 164 <= H_1 and H_1 <= 345:
        T = 0.56 + abs(0.2 * cos(radians(H_1 + 168)))
    else:
        T = 0.36 + abs(0.4 * cos(radians(H_1 + 35)))
        
    if L1 < 16:
        S_L = 0.511
    else:
        S_L = (0.040975 * L1) / (1 + 0.01765 * L1)
    S_C = ((0.0638 * C_1) / (1 + 0.0131 * C_1)) + 0.638
    S_H = S_C * (F * T + 1 - F)
    
    delta_C = C_1 - C_2
    try:
        delta_H = sqrt(pow(delta_a, 2) + pow(delta_b, 2) - pow(delta_C, 2))
    except ValueError:
        delta_H = 0.0
    
    L_group = delta_L / (pl * S_L)
    C_group = delta_C / (pc * S_C)
    H_group = delta_H / S_H
    
    return sqrt(pow(L_group, 2) + pow(C_group, 2) + pow(H_group, 2))