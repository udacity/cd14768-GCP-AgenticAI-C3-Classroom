# Building module demos and exercises

Your goal is to assist in writing code for demos and examples for different
modules. Each module has its own folder that is identified by number using
the pattern "lesson-##".
So for Module 1 the name of the folder would be "lesson-01".

What is needed for each demo or example is provided in the
"module-outline.md" file. This file is divided by modules and each module
contains a section about the demo program and the example program that are
required. Pay attention to all the requirements and components of the demo
or exercise that are outlined in their respective sections.

The demo program will be in the "demo" folder under the module folder.
The example program will be under the "exercises/solution" folder under the
module folder.

To assist when building a demo or exercise you should base it on previous
demo or exercise files, either from this module or a previous module, or
from the files in "project/solution".

Other requirements for the code:
* It must be written in python and using the ADK toolkit
* There must be an "__init__.py" file. You can copy it from a previous demo
  or exercise folder. It must not be empty.
* There must be an "agent.py" file that creates the `root_agent`
  * You must look at previous code to see how to structure "agent.py"
  * The name of the adk package is "google.adk".
  * Make sure you add a "name" parameter based on the name of the module,
    with any spaces converted to underscore
  * It should also have a description based on the description of the module
  * The instruction parameter should be read from an "agent-prompt.txt"
    file. You can see other modules to see how this file should be loaded in.
  * Make sure there is a model variable that is set to "gemini-2.5-flash"
    and make sure you include it when constructing the Agent
* You should add a "requirements.txt"
* When creating new module demos and exercises, always include the
  .env file by copying it from a previous module.
* When creating new module demos and exercises, each should also contain a
  README.md file that contains environment information and any additional
  setup information. You can look at the README.md from previous modules for
  examples.
* It should be clear and well documented

# Building the exercise starter

You are an expert technical educator.
You will be helping create starter files that students should build upon.
These files will be in the "exercises/starter" directory and should be based 
on the files that are in "exercises/solution".
Information about the lesson being taught can be found in the 
"module-outline.md" file.

Guidelines:
- The starter files should contain boilerplate code, or other code that is
  incidental to the lesson being taught.
- You should only use code that is present in the solution files. You should 
  not create any new code.
- You should not edit the original solution in any way. Just produce the 
  files in the starter that can be used to create the solution.
- For parts of the files that the student will need to fill in, they should 
  be marked with a comment starting with "TODO:"
- You should create an ".env-sample" file based on the environment 
  information provided in the README.md file in the solution directory.
- The __init__.py file should be copied verbatim
- Prompt files should just have the contents "TODO"

# Generate "CLASSROOM-README.md" from Code Repository

You are an expert technical educator.
Analyze a code repository and generate a README based on the specified type.


## INPUT
- The lesson number
- README type: **demo**, **starter**, or **solution**
- You can get the topic / lesson focus based on the "module-outline.md" file

Based on the lesson number and the type, you will know the root directory of
the files you will be working with.
- For **demo** types, this will be "demo"
- For **starter** types, this will be "exercises/starter"
- For **solution** types, this will be "exercises/solution"

## README TYPES

### Type 1: DEMO README
**Purpose**: Explain and describe existing code walkthrough
**Tone**: Descriptive - "This code does...", "Here's how it works..."

### Type 2: STARTER README
**Purpose**: Give instructions for learners to implement
**Tone**: Instructional - "Build a...", "Implement...", "Your task is..."

### Type 3: SOLUTION README
**Purpose**: Explain and describe the solution code
**Tone**: Descriptive - "The solution works by...", "This implementation..."

---


## OUTPUT STRUCTURE


# {Lesson Title}


{One sentence describing what this lesson teaches}


---


## Overview


### What You'll Learn


{2-3 sentences explaining what learners will be able to do}


Learning objectives:
- {Objective 1}
- {Objective 2}
- {Objective 3}


### Prerequisites


- {Prerequisite 1}
- {Prerequisite 2}


---


## Understanding the Concept


### The Problem


{What problem does this solve? Use a relatable scenario}


### The Solution


{How does this concept/technique solve the problem?}


### How It Works


{Explain the mechanism, architecture, or workflow}


{If multiple components/steps:}


**Step 1: {Name}**
{Explanation}


**Step 2: {Name}**
{Explanation}


### Key Terms


**{Term 1}**: {Definition}


**{Term 2}**: {Definition}


---


## CODE WALKTHROUGH (for demo/solution) OR EXERCISE INSTRUCTIONS (for starter)


---


### IF README TYPE = "demo" OR "solution":


## Code Walkthrough


### Repository Structure


```
{file-structure}
├── {file}  # {Description}
└── {file}  # {Description}
```


### Step 1: {Implementation Step}


{Describe what this code does and why}


```{language}
{Actual code from repository with inline comments}
```


**Key points:**
- {Important detail}
- {Important detail}


### Step 2: {Implementation Step}


{Describe what this code does and why}


```{language}
{Actual code from repository with inline comments}
```


**Key points:**
- {Important detail}
- {Important detail}


### Complete Example


{Show the full working code}


```{language}
{Complete code with comments}
```


**How it works:**
1. {Explanation of key section}
2. {Explanation of key section}
3. {Explanation of key section}


**Expected output:**
```
{What this code produces when run}
```


---


### IF README TYPE = "starter":


## Exercise Instructions


### Your Task


{Clear description of what the learner needs to build}


### Requirements


Your implementation must:
1. {Requirement 1}
2. {Requirement 2}
3. {Requirement 3}
4. {Requirement 4}


### Repository Structure


```
{file-structure}
├── {file}  # {Description - what learner will modify}
└── {file}  # {Description}
```

Make sure you copy ".env-sample" to ".env" and edit it to add the Google
Cloud project you are working with.

{Provide any other instructions about the environment variables necessary}

Remember that you should **never** check-in your .env file to git.

### Starter Code


{Explain what's provided and what needs to be completed}


```{language}
{Partial code with TODO comments}


# TODO: {Instruction for what to implement}


# TODO: {Instruction for what to implement}
```


### Expected Behavior


{Describe what the completed implementation should do}

**Running the agent:**

You will run the agent using the `adk web` tool. This tool launches a chat
environment that lets you test the agent interactively and examine the
internal processing that ADK and Gemini go through.

The `adk web` application is meant to be run from a directory that has a
collection of agents, which is usually the parent directory from where your
agent's code is. Typically, you will run this on the same machine where your
browser is located with a command such as:

```bash
adk web
```

{Provide any other information about starting it that are needed}

**Example usage:**
```
{How to run/test the code}
```


**Expected output:**
```
{What correct implementation produces}
```


### Implementation Hints


1. {Hint without giving away solution}
2. {Hint without giving away solution}
3. {Hint without giving away solution}


---


## Important Details


### Common Misconceptions


**Misconception**: "{Common misunderstanding}"
**Reality**: {Correct explanation}


**Misconception**: "{Common misunderstanding}"
**Reality**: {Correct explanation}


### Best Practices


1. **{Practice 1}**: {Explanation based on repository code}
2. **{Practice 2}**: {Explanation based on repository code}


### Common Errors


**Error**: {Description of typical error}
- **Cause**: {Why it happens}
- **Solution**: {How to fix it}


**Error**: {Description of typical error}
- **Cause**: {Why it happens}
- **Solution**: {How to fix it}


---


## GUIDELINES


- Extract actual code from the repository - do not invent examples
- For demo/solution: Explain what the code does and why it works
- For starter: Give clear instructions on what to build, not how to build it
- Use code blocks with inline comments
- Keep explanations concise (3-5 sentences per section)
- Include expected output examples
- Use the term "customer" when talking about the person who is using the agent

# Building a "video-outline.md"

You are an expert technical educator.
Based on the code for either a module demo or exercise solution, the 
information about a module in the "module-outline.md" file, and the contents 
of the "CLASSROOM-README.md" file for the demo or exercise, you will create 
an outline that will be used to present the demo or solution.

Guidelines:
- This outline will be used by the instructor to create a walk-through of 
  the code and then running and testing the code
- Focus on the new elements that are being introduced and taught
- Each presentation should be about 5 minutes spoken
- The outline will be guidance for the instructor, not a script
- The outline should be presented sequentially, so the instructor can go 
  linearly from point to point
- Be specific - mention specific files, functions, commands, and prompts. 
  Remember that the instructor will be following this to make their 
  presentation.

Format:
- Produce a list of bullet points of the major things to highlight
- Be specific 
  - mention specific files, functions, and line numbers
  - give specific commands to run or prompts to try to illustrate
- Each bullet point should be about one line long
- If there are additional things to mention related to the major point, use 
  an indented sub-list under the bullet
- The title will include the name of the project directory (either "cd14768" 
  or "cd14769")

## Output structure

# {project directory} - Lesson {module number} - {"demo" or "exercise"}
{name of lesson}

- {objective of the lesson}
- [{file with change}] {highlight code or prompt change}
  - {reason for change}
  - {relationship to overall lesson}
- {...repeat above as necessary to show all new code, configuration, and prompts}
- running the code
  - start `adk web` in another window. {other command line parameters as needed}
  - {other startup instructions as needed}
- demonstration
  - {steps to illustrate}
- {...repeat any of the above as necessary to show changes}
- {conclusion and summary}

