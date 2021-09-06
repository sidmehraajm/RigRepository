s=[]
print("Enter sales for 6 months")
for i in range(0,6):	
	sa=float(input("enter sales value"))
    s.append(sa) 
print
sm=0
for i in range(0,6):
	sm = sm+s[i]
av=sm/6
print(sm)
print(av)