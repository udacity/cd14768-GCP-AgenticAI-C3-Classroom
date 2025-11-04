# Building module demos and exercises

Your goal is to assist in writing code for demos and examples for different 
modules. Each module has its own folder that is identified by number using 
the pattern "module-##". So Module 1 would be in "module-01".

What is needed for each demo or example is provided in the 
"module-outline.md" file. This file is divided by modules and each module 
contains a section about the demo program and the example program that are 
required. Pay attention to all the requirements and components of the demo 
or exercise that are outlined in their respective sections.

The demo program will be in the "demo" folder under the module folder, while 
the example program will be in the "example" folder under the module.folder.

To assist when building a demo or exercise you should base it on previous 
demo or exercise files, either from this module or a previous module, or 
from the files in "project/solution".

Other requirements for the code:
* It must be written in python and using the ADK toolkit
* There must be an "__init__.py" file. You can copy it from a previous demo 
  or exercise folder
* There must be an "agent.py" file that creates the `root_agent`
  * Look at previous code to see how to structure "agent.py" 
  * Make sure you add a "name" parameter based on the name of the module, 
    with any spaces converted to underscore
  * It should also have a description based on the description of the module
  * The instruction parameter should be read from an "agent-prompt.txt" 
    file. You can see other modules to see how this file should be loaded in.
* You should add a "requirements.txt"
* You should copy the .env file from a previous demo or exercise folder
* It should be clear and well documented
