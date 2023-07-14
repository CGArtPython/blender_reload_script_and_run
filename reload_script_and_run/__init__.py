"""
This is a Blender add-on used to reload/run scripts.

This add-on can be used with the Blender Development Visual Studio Code extension.
https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development

# Why?

This allows for fast development and debugging without having to run commands from VSCode
(after you started Blender with Blender Development Visual Studio Code extension)

# How?

1. Install VSCode and the Blender Development Visual Studio Code extension
2. Run `Blender: Start` while this file is open
3. Start modifying the `my_script.py` script and adding breakpoints
4. Each time you save `my_script.py` this add-on will reload and run the script

"""

import importlib
import logging
import os
import pathlib
import sys

import bpy

bl_info = {
    "name": "Reload Script and Run",
    "author": "Viktor Stepanov",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "description": "Reloads and runs a script in Blender after a script is modified and saved",
    "category": "Development",
}


def get_file_modification_time(path: str) -> float:
    stat = os.stat(path)
    return stat.st_mtime


class ScriptRunner:
    TARGET_SCRIPT_NAME: str = "my_script"
    TARGET_SCRIPT_PATH: str = str(pathlib.Path(__file__).parent.absolute() / f"{TARGET_SCRIPT_NAME}.py")
    TARGET_SCRIPT_FUNCTION: str | None = "main"  # this can be None if you just want to run the whole script

    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def delete_instance(cls):
        cls.__instance = None

    def __init__(self) -> None:
        self.__file_modification_time: float = 0.0
        self.__refresh_interval_seconds: float = 1.0
        self.__running = False

    def start(self):
        self.__running = True

    def stop(self):
        self.__running = False

    def run_target_script(self) -> None:
        """Import or reload the target script"""
        target_module_name = f"{__name__}.{ScriptRunner.TARGET_SCRIPT_NAME}"
        if target_module_name in sys.modules:
            module_obj = importlib.import_module(target_module_name)
            importlib.reload(module_obj)
        else:
            module_obj = importlib.import_module(target_module_name)

        if not ScriptRunner.TARGET_SCRIPT_FUNCTION:
            return

        target_function = getattr(module_obj, ScriptRunner.TARGET_SCRIPT_FUNCTION, None)
        if target_function:
            target_function()
        else:
            logging.error("the %s() function does not exist in %s", ScriptRunner.TARGET_SCRIPT_FUNCTION, target_module_name)

    def run_script_if_modified(self) -> float | None:
        if not self.__running:
            return None

        current_file_modification_time = get_file_modification_time(ScriptRunner.TARGET_SCRIPT_PATH)
        if current_file_modification_time != self.__file_modification_time:
            self.__file_modification_time = current_file_modification_time
            logging.info("run the target script")
            try:
                self.run_target_script()
            except:  # pylint: disable=bare-except
                logging.exception("target script failed to execute with the following error")

        # since we are registering a callback we need to return when this method will be called
        # see https://docs.blender.org/api/current/bpy.app.timers.html#bpy.app.timers.register
        return self.__refresh_interval_seconds


def register() -> None:
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s - %(message)s", datefmt="%H:%M:%S")

    logging.info("register script watcher for %s", ScriptRunner.TARGET_SCRIPT_PATH)

    script_runner = ScriptRunner()
    script_runner.start()

    bpy.app.timers.register(script_runner.run_script_if_modified, first_interval=2.0)


def unregister() -> None:
    logging.info("unregister script watcher for %s", ScriptRunner.TARGET_SCRIPT_PATH)

    script_runner = ScriptRunner()
    script_runner.stop()
    ScriptRunner.delete_instance()


if __name__ == "__main__":
    register()
