from plyfile import PlyData, PlyElement
import mcpi.minecraft as minecraft
import mcpi.block as block
import numpy
import sys

# Minecraft coordinates
# It goes from -MAX_XZ to MAX_XZ.
MAX_XZ = 128
MAX_Y = 64

# Clear board
def clear_board(minecraft):
    minecraft.setBlocks(-MAX_XZ, 0, -MAX_XZ, MAX_XZ, MAX_Y, MAX_XZ, 0)

# Can be used to work out extent of .ply file points
def calculate_min_max(plydata):
	global x_min, x_max, y_min, y_max, z_min, z_max

	w_min = plydata['vertex'][0][0]
	l_min = plydata['vertex'][0][1]
	h_min = plydata['vertex'][0][2]

	w_max = plydata['vertex'][0][0]
	l_max = plydata['vertex'][0][1]
	h_max = plydata['vertex'][0][2]

	for v in plydata['vertex']:
		if v[0] < w_min:
			w_min = v[0]
		if v[1] < l_min:
			l_min = v[1]
		if v[2] < h_min:
			h_min = v[2]

		if v[0] > w_max:
			w_max = v[0]
		if v[1] > l_max:
			h_max = v[1]
		if v[2] > h_max:
			h_max = v[2]

		#print(v[0])

	print(w_min, w_max)
	print(l_min, l_max)
	print(h_min, h_max)

# Draw plants
def draw_plant(minecraft, plydata):

	w_range = w_max - w_min
	l_range = l_max - l_min
	h_range = h_max - h_min

	# Array to count point incidence.
	counts = numpy.zeros((2*MAX_XZ,MAX_Y,2*MAX_XZ))

	# Count points within each minecraft block
	for v in plydata['vertex']:
		# planteye has Z for height, minecraft has Y (h).
		# w -> X, l -> Z, h _> Y
		mc_X = (((v[0] - w_min) * (2 * MAX_XZ - 1)) / w_range) + (- MAX_XZ) + MAX_XZ
		mc_Z = (((v[1] - l_min) * (2 * MAX_XZ - 1)) / l_range) + (- MAX_XZ) + MAX_XZ
		mc_Y = (((v[2] - h_min) * (MAX_Y - 1)) / h_range)

		counts[mc_X][mc_Y][mc_Z]+=1

	# Print minecraft blocks with point count > POINT_COUNT
	for i in range(0, 2 * MAX_XZ):
		for j in range(0, MAX_Y):
			for k in range(0, 2 * MAX_XZ):
				if counts[i][j][k] > POINT_COUNT:
					# Colour top half light green, bottom half dark green
					mc.setBlock(i-MAX_XZ, MAX_Y - j, k-MAX_XZ, block.WOOL.id, 13 if j > MAX_Y/2 else 5)



plydata = PlyData.read(sys.argv[1])

# Manually set planteye coordinate space to ensure no aspect-ratio problems
#calculate_mix_max(plydata)
w_min = -750
w_max = 750
l_min = 0
l_max = 1500
h_min = 600
h_max = 1100

# Number of points required in minecraft block to print it.
POINT_COUNT = 1

# Create minecraft connection and draw
mc = minecraft.Minecraft.create()
clear_board(mc)
draw_plant(mc, plydata)
