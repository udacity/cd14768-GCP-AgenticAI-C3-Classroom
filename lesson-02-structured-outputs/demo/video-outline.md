# cd14768 - Lesson 2 - demo
Implementing Structured Outputs with Vertex AI Gemini and Pydantic

- This demo illustrates how to take fuzzy, human-like plain text input and 
  convert it into a structured, machine-readable output using Vertex AI 
  Gemini's capabilities and Pydantic models.
- Agents can use structured outputs as a contextual parser
  - This creates a bridge between human-text and traditional computing methods
  - Results are deterministic, which is what existing systems expect
  - Lets the agent work with existing libraries and databases
- [agent.py] Create the ADK Agent with output schema (`root_agent = Agent(...)`,
  specifically `output_schema=RobotCommands`)
  - Explain that setting `output_schema` explicitly tells Gemini to adhere
    to the Pydantic model for its output.
  - This is the core of what enables structured output generation.
- [agent.py] Define Pydantic output schema (`DirectionType`, `DistanceUnitsType`,
  `CommandType`, `Distance`, `RobotCommand`, and `RobotCommands`)
  - Emphasize the use of `typing.Literal` for constrained values.
  - Highlight the `Field` descriptions for guiding the LLM.
  - Explain `RobotCommand` as the model for a single action.
  - **Crucial**: Explain `RobotCommands` as the container for a `list[RobotCommand]`, enabling multi-step instructions.
  - Point out the `error` field for structured error reporting.
  - Explain how this schema provides a strict blueprint for the LLM's output.
- [agent-prompt.txt] Define agent instructions for structured output
  - Explain how the prompt sets the agent's persona as a robot assistant.
  - Detail how the prompt guides the LLM to convert natural language commands
    into the `RobotCommands` structured format.
  - Highlight the instructions for handling ambiguity and reporting errors
    within the structured output.
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
    - **"walk 5 feet then dance"** (Demonstrate multi-step command list)
    - "go somewhere" (to show structured error reporting)
  - Show the request and response to the LLM
    - Point out the response_mime_type
  - Emphasize that the output is now reliably parsable by downstream systems.
- Remove the `optput_schema` line and rerun to illustrate the output changes.
  - It may still obey the instructions, but there is no guarantee
- conclusion and summary
  - Structured outputs are vital for integrating LLMs into automated workflows,
    ensuring reliability and machine interpretability.
  - Pydantic models, combined with clear prompts and ADK's `output_schema`,
    provide a powerful mechanism for enforcing strict output formats.
  - This approach allows LLMs to act as intelligent parsers, translating fuzzy
    natural language into precise, actionable data.