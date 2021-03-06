import bpy
import os, sys
import time

def generate():
	render_settings()

	path = sys.argv[-1]
	files = []

	if os.path.isdir(path):
		files = os.listdir(path)
		files = [os.path.join(path, filename)
			for filename in files
			if ".obj" in filename]

	for filename in files:
		render_model(path, filename)

	bpy.ops.wm.quit_blender()

def render_settings():
	for scene in bpy.data.scenes:
		scene.render.resolution_x = 256
		scene.render.resolution_y = 256
		scene.render.resolution_percentage = 100
		scene.render.use_border = False

def render_model(path, filename):
	bpy.ops.import_scene.obj(filepath=filename)
	for obj in bpy.context.selected_objects:
		obj.name = "OBJ"
	OBJ = bpy.data.objects["OBJ"]
	bpy.context.scene.objects.active = bpy.data.objects["OBJ"]
	bpy.ops.object.join()
	bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
	OBJ.delta_rotation_euler[2] = 3.14159 / 2

	# Determine OBJ dimensions
	maxDimension = 1.0
	scaleFactor = maxDimension / max(OBJ.dimensions)

	# Scale uniformly
	OBJ.scale = (scaleFactor,scaleFactor,scaleFactor)

	# Center pivot
	bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='BOUNDS')

	# Move object to origin
	bpy.ops.object.location_clear()

	# Move mesh up by half of Z dimension
	dimX = OBJ.dimensions[0]/2
	dimY = OBJ.dimensions[1]/2
	dimZ = OBJ.dimensions[2]/2
	OBJ.location = (0,0,dimZ)

	# Manual adjustments to CAMERAS
	CAMERAS = bpy.data.objects["cameras"]
	scalevalue = 1
	camScale = 0.5+(dimX*scalevalue+dimY*scalevalue+dimZ*scalevalue)/3
	CAMERAS.scale = (camScale,camScale,camScale)
	CAMERAS.location = (0,0,dimZ)

	# Render thumbnail
	thumbname = bpy.path.basename(bpy.data.filepath)
	thumbname = os.path.splitext(filename)[0]

	if thumbname:
		bpy.context.scene.render.filepath = os.path.join(path, thumbname)

	bpy.ops.render.opengl(write_still=True, view_context=False)

	# Delete OBJ and start over for other .obj's
	bpy.ops.object.delete()
