"""
How to clean the scene explination video: https://youtu.be/3rNqVPtbhzc
Note: I used a slitly different technique in that video
"""

import bpy


def purge_orphans():
    """
    Remove all orphan data blocks

    see this from more info:
    https://youtu.be/3rNqVPtbhzc?t=149
    """
    if bpy.app.version >= (3, 0, 0):
        # run this only for Blender versions 3.0 and higher
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    else:
        # run this only for Blender versions lower than 3.0
        # call purge_orphans() recursively until there are no more orphan data blocks to purge
        result = bpy.ops.outliner.orphans_purge()
        if result.pop() != "CANCELLED":
            purge_orphans()


def recreate_world() -> None:
    """
    Find the existing default world data block and remove it.
    Create a new default world data block.

    In the case when you modify the world shader.
    """
    # delete and recreate the world data block
    world_names = [world.name for world in bpy.data.worlds]
    for name in world_names:
        bpy.data.worlds.remove(bpy.data.worlds[name])

    # create a new world data block
    world_name = "World"
    bpy.context.scene.world = bpy.data.worlds.new(name=world_name)

    # make sure we use nodes to be able to set the background color
    bpy.context.scene.world.use_nodes = True


def clean_scene() -> None:
    """
    A clean scene function that just deletes
    the scene data block and creates a new one.
    """
    scene_name = "Scene"
    assert scene_name in bpy.data.scenes

    # rename the current scene, so the new scene won't have a Scene.001
    old_scene_name = "to_delete"
    bpy.data.scenes[scene_name].name = old_scene_name

    # create a new scene (the name should be just "Scene")
    bpy.data.scenes.new(name=scene_name)

    # remove the old scene
    bpy.data.scenes.remove(bpy.data.scenes[old_scene_name])

    # create a new world data block
    recreate_world()

    purge_orphans()


def main():
    clean_scene()

    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    obj.location.z = 4


if __name__ == "__main__":
    main()
