import cvxpy as cp
import numpy as np


# Generate a quadratic program with respect to [x1,x2,x3,x4]
N=100
dt=1/N
x1 = cp.Variable(N)
x2 = cp.Variable(N)
x3 = cp.Variable(N)
x4 = cp.Variable(N)
b1 = cp.Variable(N)
b2 = cp.Variable(N)
b3 = cp.Variable(N)
b4 = cp.Variable(N)


x1_0=cp.Parameter()
x2_0=cp.Parameter()
x3_0=cp.Parameter()
x4_0=cp.Parameter()

obje = dt*sum(5*b2+9*b4)+1000*x3[N-1]

cons = [x1[0]==x1_0]\
+[x2[0]==x2_0]\
+[x3[0]==x3_0]\
+[x4[0]==x4_0]\
+[x1[k+1]==x1[k]-b1[k]*dt for k in range(N-1)]\
+[x2[k+1]==x2[k]-b2[k]*dt for k in range(N-1)]\
+[x3[k+1]==x3[k]-b3[k]*dt for k in range(N-1)]\
+[x4[k+1]==x4[k]-b4[k]*dt for k in range(N-1)]\
+[b1[k]==-x2[k] for k in range(N)]\
+[b3[k]==-x4[k] for k in range(N)]\
+[-b2[k]-b4[k]<=0 for k in range(N)]\
+[2*b2[k]+b4[k]<=0 for k in range(N)]\
+[5*b2[k]+9*b4[k]<=1 for k in range(N)]\
+[x2[k]<=0.1 for k in range(N)]\
+[x2[k]>=-0.1 for k in range(N)]


prob = cp.Problem(cp.Minimize(objej),cons)
x1_0.value=0
x2_0.value=0
x3_0.value=0
x4_0.value=0

prob.solve()


####################################################################################
#                                                                                  #
#           Interpolation process for reconstruing a feasible control              #
#                                                                                  #
####################################################################################
t_int=[]
alpha_int=[]
tt=np.arange(0,1,1/N)
for i in range(N):
    beta_2=b2.value[i]
    beta_4=b4.value[i]
    
    t_int.append(tt[i])
    
    B=(beta_4-.25)/(beta_2+.25)
    
    inter=(B*.25+.25)/(-2-B)
    
    lambda_1=abs(beta_2+.25)/abs(inter+.25)

    a=-inter*13


    if lambda_1<10**-3:
        alpha_int.append([1,1])
 
    else:
        alpha_int.append([2,a])
    
    t_int.append(tt[i]+dt*lambda_1)
    alpha_int.append([1,1])
    
####################################################################################
#                                                                                  #
#     Obtaining the trajectory controlled by the feasible control reconstructed    #
#                                                                                  #
####################################################################################    
    
    
def f(x,a1,a2):
    return [x[1],1/(1+3*a1**2)*a2,x[3],-a1/(1+3*a1**2)*a2]

x_initial=[0,0,0,0]
traj=[]

traj.append(x_initial)

traj_aux=x_initial
a1=np.array(alpha_int)[:,0]
a2=np.array(alpha_int)[:,1]

for i in range(0,len(t_int)-1):
    traj_aux=traj_aux+(t_int[i+1]-t_int[i])*np.array(f(traj[i],a1[i],a2[i]))
    
    traj.append(traj_aux)
