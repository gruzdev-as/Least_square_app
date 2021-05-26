''' Docstring '''

from sympy import S, symbols, printing
from matplotlib import pyplot as plt
import numpy as np

#with open('polynom/data.json', 'r') as f:
f = open('polynom/data.json', 'r').read()
lines = f.split('\n')

x_values = []
y_values = []

for line in lines:
    if line == '':
        continue
    else:
        x, y = line.split(' ')
        x_values.append(float(x))
        y_values.append(float(y))

z_3 = np.polyfit(x_values, y_values, 3)
z_5 = np.polyfit(x_values, y_values, 5)

p_3 = np.poly1d(z_3)
p_5 = np.poly1d(z_5)

x_new_3 = np.linspace(x_values[0], x_values[-1], 50)
y_new_3 = p_3(x_new_3)

x_new_5 = np.linspace(x_values[0], x_values[-1], 50)
y_new_5 = p_5(x_new_5)

x = symbols("x")

poly_3 = sum(S("{:6.2f}".format(v))*x**i for i, v in enumerate(z_3[::-1]))
eq_latex_3 = printing.latex(poly_3)

poly_5 = sum(S("{:6.2f}".format(v))*x**i for i, v in enumerate(z_5[::-1]))
eq_latex_5 = printing.latex(poly_5)

plt.plot(x_values, y_values, '.', markersize = 10)
plt.plot(x_new_3, y_new_3, label = "${}$" .format(eq_latex_3))
plt.plot(x_new_5, y_new_5, label = "${}$" .format(eq_latex_5))
plt.legend(fontsize="small")
plt.show()
