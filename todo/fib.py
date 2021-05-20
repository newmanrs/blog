#import tabulate
import numpy as np
import matplotlib.pyplot as plt

def fib():
    """ Generator expression for the fibonacci sequence """
    a,b = 0,1
    while True:
        yield a;
        a,b = b, a+b;


f_n = fib(); #Instantiate generator
next(f_n);

N = 50;
fibs = [next(f_n) for n in range(N)];
print(fibs);
fib_rat = [ a / b for (a,b) in zip(fibs[1:], fibs[0:-1])]
print(fib_rat)
fib_err = [ a / b - (1+np.sqrt(5))/2 for (a,b) in zip(fibs[1:], fibs[0:-1])]
print(fib_err)

for i in range(len(fib_rat)):
    print("{} {} {}".format(fibs[i+1], fib_rat[i], fib_err[i]));


plt.figure(1);
plt.subplot(2,1,1)
plt.loglog(range(N),fibs,'-o');
plt.subplot(2,1,2)
plt.semilogy(range(N-1), [abs(i)for i in fib_err],'-o');
#plt.show();

slope, intercept = np.polyfit(range(N),np.log(fibs),1);
print(slope);
print(intercept);
print(np.log10(fibs));
