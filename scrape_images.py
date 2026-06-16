import urllib.request
import re

html = urllib.request.urlopen("https://lecroisetier.fr").read().decode("utf-8")
images = re.findall(r'<img[^>]+src="([^">]+)"', html)
print("Images found:", images)
