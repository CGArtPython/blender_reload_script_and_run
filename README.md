# Summary
This is a Blender add-on used to reload/run scripts to quickly iteration on them.

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
