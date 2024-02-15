import sys
from PIL import Image

img = Image.open(sys.argv[1])

pixels2 = list(img.getdata())
pixels = img.load()

for i in range(img.size[0]):
	for j in range(img.size[1]):
		x = j*img.size[0]+i
		if pixels2[x][0] > pixels2[x][1] and pixels2[x][0] > pixels2[x][2]:
			pixels[i,j] = (255, 0 ,0, 255)
		if pixels2[x][0] == pixels2[x][1] and pixels2[x][0] == pixels2[x][2]:
			if pixels2[x] != (187,187,187,255) and pixels2[x] != (255,255,255,255):
				pixels[i,j] = (0, 0 ,0, 255)
img.save(sys.argv[2])

