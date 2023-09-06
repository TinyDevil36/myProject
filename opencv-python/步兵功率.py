from time import sleep
import numpy 
import random
a=40
k=0

#第一台步兵
# for i in range(100):
#     a = random.uniform(10,20)
#     sleep(0.06)
#     print(f'超电功率:{a}')
# for i in range(40000):
    

    
#     if 75>k>=50:
        
#         a = random.uniform(5,10)
#     elif k==150:
#         break
#     elif k>=75:
#         a = random.uniform(10,18)
        
    
#     elif k<25:
#         a = random.uniform(35,23)
#     elif 25<=k<50:
#         a = random.uniform(22,10)
#     # a = random.gauss(3,0.5)*10
#     sleep(0.06)
#     k+=1
#     print(f'超电功率:{a}')

#第二台步兵
for i in range(50):
    a = random.uniform(10,20)
    sleep(0.06)
    print(f'超电功率:{a}')
for i in range(40000):
    

    
   
    if k==150:
        break
    elif k>=75:
        a = random.uniform(10,18)
        
    
    elif k<50:
        a = random.uniform(35,23)
    elif 50<=k<75:
        a = random.uniform(5,10)
    # a = random.gauss(3,0.5)*10
    sleep(0.05)
    k+=1
    print(f'超电功率:{a}')
