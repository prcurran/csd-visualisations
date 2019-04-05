import imageio
import os


filenames = [f for f in os.listdir(os.path.dirname(__file__)) if f.split(".")[1] == 'png']
print filenames

images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('out.gif', images, duration=0.8)