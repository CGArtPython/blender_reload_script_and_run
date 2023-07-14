import bpy


def main():
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    obj.location.z = 4


if __name__ == "__main__":
    main()
