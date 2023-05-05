from numpy import cos, sin
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def update_line(num):
    line.set_data(x[:num], y[:num])
    line.set_3d_properties(z[:num])
    return line


data = np.load('data_50_0852g.npz')
robot_positions = data['robot_position']

pi = np.pi
a = [0, 0.4, 0.4, 0, 0, 0]
alpha = [pi / 2, 0, 0, pi / 2, -pi / 2, 0]
d = [0.105, 0, 0, 0.22, 0.2, 0.14]

H_list = []
for theta in robot_positions:
    R = []
    for i in range(6):
        R.append([
            [cos(theta[i])                  , -sin(theta[i]) * cos(alpha[i]) , sin(theta[i]) * sin(alpha[i])  , a[i] * cos(theta[i])],
            [sin(theta[i])                  , cos(theta[i]) * cos(alpha[i])  , -cos(theta[i]) * sin(alpha[i]) , a[i] * sin(theta[i])],
            [0                              , sin(alpha[i])                  , cos(alpha[i])                  , d[i]                ],
            [0                              , 0                              , 0                              , 1                   ]
        ])
    H = np.array(R[0])
    for i in range(5):
        H = np.matmul(H, np.array(R[i+1]))
    H_list.append(H)

x = []
y = []
z = []

for i in range(len(H_list)):
    x.append(H_list[i][0, 3])
    y.append(H_list[i][1, 3])
    z.append(H_list[i][2, 3])

# wyświetlanie całej trajektorii od razu
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.plot3D(x, y, z)
#
# plt.show()

# animacja trajektorii
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
line, = ax.plot(x, y, z)

animate = animation.FuncAnimation(fig, update_line, frames=len(x), interval=1)
plt.show()



