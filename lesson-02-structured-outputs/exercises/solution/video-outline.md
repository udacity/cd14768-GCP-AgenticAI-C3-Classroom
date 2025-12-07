# cd14768 - Lesson 2 - exercise
Information Summarizer

- In this exercise, you were asked to develop an agent to process free-form 
  customer feedback and extract key information into a predefined Pydantic schema.
  - Useful for leveraging structured outputs
    for reliable data extraction and downstream processing, particularly for
    tasks like sentiment analysis or database ingestion.
- [agent.py] Define Feedback Summary Pydantic Model (`FeedbackType`, `FeedbackSummary`)
  - Highlight the use of `typing.Literal` to constrain `feedback_type` values.
  - Emphasize `Optional` fields (`customer_name`, `feedback_date`) and the
    `datetime.date` type for consistent date formatting.
  - Explain how the `Field` descriptions guide the LLM in populating each field.
  - This model provides the precise blueprint for the extracted customer feedback.
- [agent-prompt.txt] Craft Agent Instructions for Summarization
  - Explain how the prompt defines the agent's role as a customer service
    assistant tasked with summarizing feedback.
  - Detail how the instructions guide the LLM to identify and extract specific
    information (customer name, feedback date, feedback type, summary).
  - Highlight the instruction to omit optional fields if their values are not
    found, ensuring concise output.
- [agent.py] Configure the ADK Agent with Output Schema (`root_agent = Agent(...)`,
  specifically `output_schema=FeedbackSummary`)
  - Explain that this configuration explicitly instructs the Gemini model to
    adhere to the `FeedbackSummary` Pydantic schema for all its outputs.
  - This establishes the critical link between the desired output structure and
    the LLM's generation capabilities within ADK.
- running the code
  - start `adk web` in another window from the parent directory of the agent
    (i.e., `cd lesson-02-structured-outputs` then `adk web`)
  - navigate to the displayed URL in your browser.
- demonstration
  - In the `adk web` chat interface, provide various customer feedback examples:
    - "I am writing to express my extreme dissatisfaction with the recent service
      I received on October 26, 2023. The technician was late, unhelpful, and did
      not resolve my issue. My name is Alice Smith."
    - "Just wanted to say that the new interface is fantastic! Great work team."
    - "I think it would be great if you could add a dark mode option to your
      mobile app. It would really help with eye strain at night."
  - Observe how the agent consistently outputs structured JSON conforming to the
    `FeedbackSummary` schema.
  - Show how optional fields are correctly omitted when not present in the input.
- conclusion and summary
  - Structured data extraction using LLMs and Pydantic is crucial for automating
    the processing and analysis of unstructured text like customer feedback.
  - Accurate summarization, categorization, and extraction of key details enable
    downstream systems to efficiently analyze sentiment, track trends, and
    automate responses.
  - The combination of a well-defined Pydantic schema, clear agent prompts, and
    ADK's `output_schema` parameter ensures reliable and consistent structured
    output.