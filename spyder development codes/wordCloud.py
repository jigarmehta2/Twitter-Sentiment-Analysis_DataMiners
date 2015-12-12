# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 21:35:28 2015

@author: Jigar Mehta
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor





This is a temporary script file.
"""

from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS

d = path.dirname("C:\\Users\\Jigar Mehta\\Downloads")

# Read the whole text.
text = open(path.join(d, 'WC.txt')).read()

# read the mask image
# taken from
# http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
alice_mask = np.array(Image.open(path.join(d, "alice_mask.png")))

wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask,
               stopwords=STOPWORDS.add("said"))
# generate word cloud
wc.generate(text)

# store to file
wc.to_file(path.join(d, "alice.png"))

# show
plt.imshow(wc)
plt.axis("off")
plt.figure()
plt.imshow(alice_mask, cmap=plt.cm.gray)
plt.axis("off")
plt.show()


