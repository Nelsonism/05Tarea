import matplotlib.pyplot as plt
import numpy as np

h = 0.2
w = 1.9


def LetraN(a, b):
    x = a * h - 5
    y = b * h - 7.5
    if x >= -2.5 and x < -1.5 and y >= -3.5 and y < 3.5:
            return 0.05
    elif x >= 1.5 and x < 2.5 and y >= -3.5 and y < 3.5:
            return 0.05
    elif x >= -1.5 and x < -0.5 and y >= 0.5 and y < 2.5:
            return 0.05
    elif x >= -0.5 and x < 0.5 and y >= -1 and y < 1:
            return 0.05
    elif x >= 0.5 and x < 1.5 and y >= -2.5 and y < -0.5:
            return 0.05
    else:
        return 0


def SobreRelax(V):
    for i in range(1, 10):
        for j in range(1, 75):
            V[i][j] = ((1 - w) * V[i][j] + w / 4 * (V[i+1][j] +
                       V[i-1][j] + V[i][j+1] + V[i][j-1] +
                       h**2 * LetraN(i, j)))
    for i in range(41, 50):
        for j in range(1, 75):
            V[i][j] = ((1 - w) * V[i][j] + w / 4 * (V[i+1][j] +
                       V[i-1][j] + V[i][j+1] + V[i][j-1] +
                       h**2 * LetraN(i, j)))
    for i in range(10, 41):
        for j in range(1, 9):
            V[i][j] = ((1 - w) * V[i][j] + w / 4 * (V[i+1][j] +
                       V[i-1][j] + V[i][j+1] + V[i][j-1] +
                       h**2 * LetraN(i, j)))
        for j in range(9, 10):
            V[i][j] = ((1 - w) * V[i][j] + w / 3 * (V[i+1][j] +
                       V[i-1][j] + V[i][j-1] +
                       h**2 * LetraN(i, j) - h))
        for j in range(10, 11):
            V[i][j] = V[i][j+1] - h
        for j in range(11, 12):
            V[i][j] = V[i][j-1] + h
        for j in range(12, 13):
            V[i][j] = ((1 - w) * V[i][j] + w / 3 * (V[i+1][j] +
                       V[i-1][j] + V[i][j-1] +
                       h**2 * LetraN(i, j) + h))
        for j in range(13, 75):
            V[i][j] = ((1 - w) * V[i][j] + w / 4 * (V[i+1][j] +
                       V[i-1][j] + V[i][j+1] + V[i][j-1] +
                       h**2 * LetraN(i, j)))


def Convergencia(V, NewV):
    QuitaCero = (NewV != 0)
    Dif = (V - NewV)[QuitaCero] / NewV[QuitaCero]
    DifMax = np.max(np.fabs(Dif))
    if DifMax > 1e-3:
        return True
    else:
        return False

Npuntos = []
for a in range(51):
    Npuntos.append([])
    for b in range(76):
        Npuntos[a].append(LetraN(a, b))

Npuntos = np.arcsinh(np.transpose(Npuntos))

fig = plt.figure()
plt.imshow(Npuntos, origin='bottom',
           interpolation='nearest', extent=[-5, 5, -7.5, 7.5])
plt.colorbar()
plt.xlabel('$X[cm]$')
plt.ylabel('$Y[cm]$')
plt.title('$Densidad$ $de$ $Carga$ $[C/cm^2]$')
plt.show()
fig.savefig('Densidad de Carga.png')

V = np.zeros((51, 76))
GuardaV = np.zeros((51, 76))
SobreRelax(V)
N = 0
while N < 3000 and Convergencia(GuardaV, V):
    for a in range(len(GuardaV)):
        for b in range(len(GuardaV[a])):
            GuardaV[a][b] = V[a][b]
    SobreRelax(V)
    N += 1
print ('Para w= '+str(w)+' converge con '+str(N)+' iteraciones.')

Y = V[25]
X = np.linspace(-7.5, 7.5, 76)

V = np.arcsinh(np.transpose(V))

fig = plt.figure()
plt.imshow(V, origin='bottom',
           interpolation='nearest', extent=[-5, 5, -7.5, 7.5])
plt.colorbar()
plt.xlabel('$X[cm]$')
plt.ylabel('$Y[cm]$')
plt.title('$Potencial$ $Electrostático$ $[Volt]$ $w=$ $'+str(w)+'$')
plt.show()
fig.savefig('Potencial Electrostatico w'+str(w)+'.png')

fig = plt.figure()
plt.plot(X, Y)
plt.xlim(-7.5, 7.5)
plt.ylim(-2, 0.5)
plt.xlabel('$Y[cm]$')
plt.ylabel('$[Volt]$')
plt.title('$Perfil$ $de$ $Potencial$')
plt.show()
fig.savefig('Perfil de Potencial.png')
