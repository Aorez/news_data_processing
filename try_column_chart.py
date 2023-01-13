import matplotlib.pyplot as plt


plt.style.use('ggplot')  # 加载'ggplot'风格
plt.figure()

total = [3, 5, 6, 7, 8, 6, 4, 3, 3, 22, 4, 8, 7, 13, 7, 7, 15, 10, 6, 52, 8, 2, 3, 26, 1, 1, 0, 2, 0, 3]
x = [1, 2, 3]
y = [1, 2, 3]
# 以下两种写法等价，
plt.plot(x, y, color='green', marker='o', linestyle='dashed', linewidth=2, markersize=12)

plt.bar(range(len(total)), total)
plt.show()
