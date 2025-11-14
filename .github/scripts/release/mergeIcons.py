from wand.image import Image
import re
import math
import os

os.chdir('icons')
ls = os.listdir()

folders = []
for items in ls:
	if items[-4:] == ".lua":
		folders.append(items[:-4])


lookup = {}

for folder in folders:
	regex = rf's\[.*?\].*?=(?!.*?{{).*?\"LibCustomIcons/icons/{folder}/([^\"]+)\"' # only get statics
	print("Current folder: " + folder)
	images = []

	foldersFoundIn = []

	for cFolder in folders: ### Find all Static Icons which are in the current folder we are looking at ###
		with open(f"{cFolder}.lua", "r") as fil:
			content = fil.read()
			images += re.findall(regex, content)
			if len(re.findall(regex, content)) != 0:
				foldersFoundIn.append(cFolder)


	images = list(dict.fromkeys(images)) # remove dupes

	numImages = len(images)
	if numImages != 0:

		columns = math.floor(math.sqrt(numImages))
		rows = math.ceil(numImages/columns)

		print(f"Making an image with a dim of {columns}x{rows} for folder {folder}")

		if len(foldersFoundIn) > 1:
			print("Found in folders: " + ', '.join(foldersFoundIn))

		with Image(background=None) as img: ### Merge all images in the folder, and save ###
			for src in images:
				with Image(width=32, height=32, pseudo=f"{folder}/{src}") as item:
					item.border_color = 'none'   # Inner Frame
					item.matte_color = 'none'  # Outer Frame
					item.background_color = "none"
					item.resize(32,32)
					img.image_add(item)
			img.background_color = "none"
			img.montage(mode='concatenate', tile=f'{columns}x{rows}')
			img.compression = "dxt5"
			img.background_color = "none"
			img.format = "dds"
			img.save(filename=f'{folder}/merged.dds')

		for cFolder in folders: ### Look through all lua files and replace their values with the new merged + top bottom left right width height table ###
			with open(f"{cFolder}.lua", "r+") as fil:
				content = fil.read()
				for i in range(len(images)):
					imagePath = images[i]
					column = i%columns
					row = math.floor(i/columns)
					newregex = rf'(s\[.*?\].*?)(\"LibCustomIcons\/icons\/{folder}\/{imagePath}\")'
					newstring = rf'\g<1>{{"LibCustomIcons/icons/{folder}/merged.dds", {column*32}, {(column*32)+31}, {row*32}, {(row*32)+31}, {columns*32-1}, {rows*32-1}}}'
					(content,amnt) = re.subn(newregex, newstring, content)
					if amnt > 1:
						print(f"{folder}/{imagePath} was duplicated {amnt} times in folder {cFolder}")
				fil.seek(0)
				fil.write(content)
				fil.truncate()


		print("")
		
		
		for path in images: ### Delete old images ###
			if os.path.exists(f"{folder}/{path}"):
				os.remove(f"{folder}/{path}")
			else:
				print(f"{folder}/{path} does not exist") 
