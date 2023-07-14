"""
How to clean the scene explination video
https://youtu.be/3rNqVPtbhzc
Note: I used a slitly different technique in that video

Blender Python Tutorial: Linking Objects Across .blend Files
https://youtu.be/ZrN9w8SMFjo
"""

import pathlib

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


def remove_libraries():
    """remove the linked blend files"""
    bpy.data.batch_remove(bpy.data.libraries)


def link_blend_file_objects(blend_file_path, link=False):
    """link the blender file objects into the current blender file"""
    with bpy.data.libraries.load(blend_file_path, link=link) as (data_from, data_to):
        data_to.objects = data_from.objects

    scene = bpy.context.scene

    # link the objects into the scene collection
    for obj in data_to.objects:
        if obj is None:
            continue

        scene.collection.objects.link(obj)


def link_blend_file_scenes(blend_file_path, link=False):
    """link the blender file scenes into the current blender file"""
    with bpy.data.libraries.load(blend_file_path, link=link) as (data_from, data_to):
        data_to.scenes = data_from.scenes


def main():
    remove_libraries()
    clean_scene()

    # define the path to the blend file
    blend_file_path = str(pathlib.Path().home() / "tmp" / "objects.blend")

    link_blend_file_objects(blend_file_path, link=False)

    ico_obj = bpy.data.objects["Icosphere"]
    ico_obj.location.z = 2


if __name__ == "__main__":
    main()
