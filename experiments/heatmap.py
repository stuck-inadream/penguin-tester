import matplotlib.pyplot as plt

data = [1.0, 0.6, 0.7]
plt.figure()
plt.plot(data, marker='o')
plt.xticks([0,1,2], ['empty','exception','myth'])
plt.title('Penguin Distortion Spectrum (Modal Fractions)')
plt.ylim(0,1.05)
plt.grid(True)
plt.savefig('heatmap.png', bbox_inches='tight')
print('Saved heatmap.png')
