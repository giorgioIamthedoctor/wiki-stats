__author__ = 'student'
import matplotlib.pyplot as plt
import numpy as np

# генерируем данные, 5 штук
data1=10*np.random.rand(5)

# видимо это список из аля xrange(1, n + 1)
locs = np.arange(1, len(data1)+1)

# а вот и какаушко ширина столбцов
width = 0.27

# видимо, построение диаграммы: сколько, какая, ширина
plt.bar(locs, data1, width=width)

# подписи столбцов, 5 штук
labels = ['le', 'ku', 'je', 'su', 'ny']

# подписи расположить посередине столбца: номер подписи + ширина столбца/2
plt.xticks(locs,labels)
print(locs)
# показать наплоченное
plt.show()