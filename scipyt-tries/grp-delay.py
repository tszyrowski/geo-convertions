
from scipy import signal
import matplotlib.pyplot as plt

b, a = signal.iirdesign(0.1, 0.3, 5, 50, ftype='cheby1')
w, gd = signal.group_delay((b, a))


plt.title('Digital filter group delay')
plt.plot(w, gd)
plt.ylabel('Group delay [samples]')
plt.xlabel('Frequency [rad/sample]')
plt.show()