'''
Gompertz-Makeham Survival Model

Author: griffijt
Purpose: 
- Define a set of actuarial functions for a Gompertz-Makeham survival model
- Recreate the Standard Ulitmate Survival Model table from Dickson (2013)

Sources: 
- Actuarial Mathematics for Life Contingent Risks by Dickson, D.C.M. and Hardy, M.R. and Waters, H.R.
- Interpreting Gompertz-Makeham parameters:
    - Accident hazard (A): Mumpar-Victoria, PhD, https://www.soa.org/globalassets/assets/files/resources/essays-monographs/2005-living-to-100/m-li05-1-xiii.pdf
    - Exponential increase in death rates with age (B*c**x): https://en.wikipedia.org/wiki/Gompertz%E2%80%93Makeham_law_of_mortality
    - Effect of parameters: https://papp.iussp.org/sessions/papp103_s02/PAPP103_s02_060_010.html

Notes:
- Accuracy checked based on replicating the Standard Ultimate Survival Model
  from Appendix D, Table D.1 and D.3 of Dickson, Hardy and Waters
- Limiting age of 130, per Example 4.1 from Dickson, page 85
- Acronyms:
    APV = Actuarial Present Value
    PDF = Probability Density Function
    SUSM = Standard Ultimate Survival Model from Dickson
'''
# import libraries
import numpy as np
import pandas as pd

def vt(i, t):
    '''Present value of $1 received at time t.
    
    Args:
        i (float) : Interest rate
        t (float) : Time payment is received
    
    Returns:
        vt (float) : Present value factor for payment at time t
    '''
    vt = 1 / ((1+i)**t)
    return vt

def tPx(A, B, c, x, t):
    '''Probability someone aged x lives until time t
    following a Gompertz-Makeham survival model.

    Args:
        A (float) : Accident hazard (non age-dependent factor)
        B (float) : Scaling factor for c
        c (float) : Age-dependent mortality term
        x (float) : Starting age
        t (float) : Time of survival
    
    Returns:
        tPx (float) : Probability someone aged x lives until time t
    '''
    tPx = np.exp(-A*t - (B/np.log(c)) * (c**x) * (c**t-1))
    return tPx

def m_nqx(A, B, c, x, m, n = 1):
    '''Conditional probability of failure.
    
    Args:
        A (float) : Accident hazard (non age-dependent factor)
        B (float) : Scaling factor for c
        c (float) : Age-dependent mortality term
        x (float) : Starting age
        m (float) : Survive until time m
        n (float) : Failure before time m+n

    Returns: 
        m_nqx (float) : Probability someone aged x survives until m and dies before m+n.
    '''
    m_qx = 1 - tPx(A, B, c, x, t=m) # Pr(Age x dies before m)
    mn_qx = 1 - tPx(A, B, c, x, t=m+n) # Pr(Age x died before m+n)
    m_nqx = mn_qx - m_qx
    return m_nqx

def tfx(A, B, c, x, t):
    '''PDF of someone aged x at time t,
    following a Gompertz-Makeham survival model.

    Args:
        A (float) : Accident term (non age-dependent factor)
        B (float) : Scaling factor for c
        c (float) : Age-dependent mortality term
        x (float) : Starting age
        t (float) : Time
    
    Return:
        tfx (float) : PDF evaluated using x and t
    '''
    # PDF = force of mortality * survival function
    tfx = (A + B*(c**(x+t))) * np.exp(-A*t - (B/np.log(c)) * (c**x) * (c**t-1))
    return tfx

def calc_Ax(A, B, c, x, i):
    '''APV of a $1 whole life policy of someone aged x
    following a Gompertz-Makeham survival model.

    Args:
        A (float) : Accident term (non age-dependent factor)
        B (float) : Scaling factor for c
        c (float) : Age-dependent mortality term
        x (float) : Starting age

    Dependents:
        vt (func) : PV function
        m_nqx (func) : Conditional probability of failure
        tPx (func) : Survival function (indirectly through m_nqx)
    
    Returns:
        Ax (float) : APV of $1 payable at EOY of death (whole life)
    '''
    limAge = 130    # per Example 4.1 from Dickson, page 85
    Ax = 0          # set APV equal to zero

    # sum the product of PV Factor * Pr(Payment) over t
    for k in range(0,limAge):
        Ax = Ax + vt(i, t=k+1) * m_nqx(A, B, c, x, m=k, n=1)

    return Ax

def calc_Ax_2(A, B, c, x, i):
    '''Second moment of a $1 whole life policy of someone aged x
    following a Gompertz-Makeham survival model.

    Args:
        A (float) : Accident term (non age-dependent factor)
        B (float) : Scaling factor for c
        c (float) : Age-dependent mortality term
        x (float) : Starting age

    Dependents:
        vt (func) : PV function
        m_nqx (func) : Conditional probability of failure
        tPx (func) : Survival function (indirectly through m_nqx)
    
    Returns:
        Ax_2 (float) : APV of $1 payable at EOY of death (whole life)
    '''
    limAge = 130    # per Example 4.1 from Dickson, page 85
    Ax_2 = 0          # set APV equal to zero

    # sum the product of PV Factor^2 * Pr(Payment) over k
    for k in range(0,limAge):
        Ax_2 = Ax_2 + vt(i, t=(2*(k+1))) * m_nqx(A, B, c, x, m=k, n=1)

    return Ax_2

def calc_ax(A, B, c, x, i, due = True):
    '''APV of a $1 whole life annuity of someone aged x,
    following a Gompertz-Makeham survival model.

    Args:
        A (float) : Accident term (non age-dependent factor)
        B (float) : Scaling factor for c
        c (float) : Age-dependent mortality term
        x (float) : Starting age

    Dependents:
        vt (func) : PV function
        tPx (func) : Survival function
    
    Returns:
        ax (float) : APV of $1 whole life annuity due
    '''
    limAge = 130    # per Example 4.1 from Dickson, page 85
    ax = 0          # set APV equal to zero

    # sum the product of PV Factor * Pr(Payment) over t
    for t in range(0,limAge):
        ax = ax + vt(i, t) * tPx (A, B, c, x, t)
    
    # if immediate annuity, subtract initial payment
    if due==False:
        ax = ax - 1

    return ax

def nEx(A, B, c, x, n, i):
    '''APV of a $1 pure endowment policy
    following a Gompertz-Makeham survival model.

    Args:
        A (float) : Accident hazard (non age-dependent factor)
        B (float) : Scaling factor for c
        c (float) : Age-dependent mortality term
        x (float) : Starting age
        n (float) : Time until payment
    
    Dependents:
        vt (func) : PV function
        tPx (func) : Survival function
    
    Returns:
        nEx (float) : PV of $1 paid at time n if someone aged x is alive
    '''
    nEx = vt(i, n) * tPx(A, B, c, x, t=n)
    return nEx

#----------Define Model Parameters----------
# Gompertz–Makeham survival model
A = 0.00022
B = 2.7*10**(-6)
c = 1.124

# Other parameters
lx = 100000     # starting number of lives
x = 20          # starting age
t = 1           # live until age x+t
i = 0.05        # interest rate
v = 1/(1+i)     # discount factor
d = i*v         # equivalent discount rate

#-----Age and Number of Lives-----
# initialize life table as list
X = []
L = [lx]

# create age column as list
for j in range(x, 101):
    X.append(j)

# create life column as list
for j in range(x, 101):
    L.append(L[-1]*tPx(A, B, c, j, t))

#-----Whole Life Annuity Due-----
# initialize ax list
ax_due = []

for j in range(x, 101):
    ax_due.append(calc_ax(A, B, c, x=j, i=i, due=True))

#-----Whole Life Policy, Ax (recursively)-----
# Assume terminal age of 130 since q129 is very close to 1
q129 = 1-tPx(A, B, c, x=129, t=1)
#print(q129)

# Per Example 4.1 from Dickson, page 85
A129 = v
Ax_recur = [A129]

# Calculate values of Ax recursively from A129
for j in range(128, x-1, -1):
    px = tPx(A, B, c, x=j, t=1)
    qx = 1-px
    Aj = v * qx + v * px * Ax_recur[0]
    Ax_recur.insert(0, Aj)

#-----Whole Life Policy, Ax (directly)-----
Ax_direct = []

for k in range(x, 101):
    Ax_direct.append(calc_Ax(A, B, c, x=k, i=i))

#-----Second Moment of Whole Life Policy-----
Ax_2 = []

for k in range(x, 101):
    Ax_2.append(calc_Ax_2(A, B, c, x=k, i=i))

#-----Pure Endowment of 5, 10 and 20 years-----
Ex_5 = []
Ex_10 = []
Ex_20 = []

for k in range(x, 101):
    Ex_5.append(nEx(A, B, c, x=k, n=5, i=i))
    Ex_10.append(nEx(A, B, c, x=k, n=10, i=i))
    Ex_20.append(nEx(A, B, c, x=k, n=20, i=i))

#----------Create pandas DataFrame----------
SUSM_df = pd.DataFrame(data=list(zip(X, L, ax_due, Ax_recur, Ax_direct, Ax_2, Ex_5, Ex_10, Ex_20)), 
                              columns=['Age', 'lx', 'ax_due', 'Ax_recur', 'Ax_direct', 'Ax_2', 'Ex_5', 'Ex_10', 'Ex_20'])

# check ages 20-39 and 70-80
print(SUSM_df[0:20])
print(SUSM_df[50:61])