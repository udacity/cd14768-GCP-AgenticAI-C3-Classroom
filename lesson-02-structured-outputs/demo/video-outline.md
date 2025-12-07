# cd14768 - Lesson 2 - demo
Implementing Structured Outputs with Vertex AI Gemini and Pydantic

- This demo illustrates how to take fuzzy, human-like plain text input and 
  convert it into a structured, machine-readable output using Vertex AI 
  Gemini's capabilities and Pydantic models.  
- [agent.py] Define Pydantic output schema (`DirectionType`, `DistanceUnitsType`,
  `CommandType`, `Distance`, and `RobotCommands`)
  - Emphasize the use of `typing.Literal` for constrained values.
  - Highlight the `Field` descriptions for guiding the LLM.
  - Point out the `error` field for structured error reporting.
  - Explain how this schema provides a strict blueprint for the LLM's output.
- [agent-prompt.txt] Define agent instructions for structured output
  - Explain how the prompt sets the agent's persona as a robot assistant.
  - Detail how the prompt guides the LLM to convert natural language commands
    into the `RobotCommands` structured format.
  - Highlight the instructions for handling ambiguity and reporting errors
    within the structured output.
- [agent.py] Create the ADK Agent with output schema (`root_agent = Agent(...)`,
  specifically `output_schema=RobotCommands`)
  - Explain that setting `output_schema` explicitly tells Gemini to adhere
    to the Pydantic model for its output.
  - Show how this configuration is central to enabling structured output generation.
- running the code
  - start `adk web` in another window from the parent directory of the agent
    (i.e., `cd lesson-02-structured-outputs` then `adk web`)
  - navigate to the displayed URL in your browser.
- demonstration
  - In the `adk web` chat interface, provide the following prompts and observe
    the structured JSON output:
    - "walk 10 feet to the left"
    - "dance"
    - "turn right"
    - "get the red ball"
    - "go somewhere" (to show structured error reporting)
  - Emphasize that the output is now reliably parsable by downstream systems.
- Remove the `optput_schema` line and rerun to illustrate the output changes.
- conclusion and summary
  - Structured outputs are vital for integrating LLMs into automated workflows,
    ensuring reliability and machine interpretability.
  - Pydantic models, combined with clear prompts and ADK's `output_schema`,
    provide a powerful mechanism for enforcing strict output formats.
  - This approach allows LLMs to act as intelligent parsers, translating fuzzy
    natural language into precise, actionable data.