import streamlit as st
import os
import subprocess
import tempfile
from langchain.tools import tool
from crewai import Agent, Task, Crew, Process

# Set up Streamlit Page
st.set_page_config(page_title="AI Code Reviewer", page_icon="💻", layout="wide")
st.title("💻 Autonomous AI Code Reviewer")
st.markdown("Paste your Python code below. The system will run `flake8` for static analysis and use an LLM Agent to generate human-readable suggestions.")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

# --- TOOLS ---
@tool("Run flake8 static analysis")
def flake8_linting_tool(code: str) -> str:
    """
    Takes Python code as a string, writes it to a temporary file,
    runs flake8 static analysis on it, and returns the linting errors.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    try:
        # Run flake8 using subprocess
        result = subprocess.run(
            ['flake8', temp_file_path],
            capture_output=True,
            text=True
        )
        output = result.stdout
        if not output:
            output = "No static analysis errors found by flake8. The code syntax and style look good."
    except Exception as e:
        output = f"Error running flake8: {str(e)}"
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)

    return output

# --- APP LOGIC ---
code_input = st.text_area("Paste Python Code Here:", height=300)

if st.button("Review Code"):
    if not api_key:
        st.error("Please provide your OpenAI API Key in the sidebar.")
    elif not code_input.strip():
        st.warning("Please paste some Python code to review.")
    else:
        with st.spinner("Initializing Agents and running review..."):
            
            # --- AGENTS ---
            static_analysis_agent = Agent(
                role='Static Code Analyzer',
                goal='Analyze the provided Python code using the flake8 tool to find syntax and style errors.',
                backstory="You are a strict code quality inspector who uses static analysis tools like flake8 to catch errors and enforce PEP8 standards.",
                tools=[flake8_linting_tool],
                verbose=True,
                allow_delegation=False
            )

            review_agent = Agent(
                role='Senior Developer & Code Reviewer',
                goal='Translate static analysis errors and the original code into a comprehensive, human-readable code review and suggest improvements or best practices.',
                backstory="You are a friendly and experienced Senior Software Engineer. You review other developer's code. You look at static analysis outputs and the original code, then explain the issues in a clear, constructive way and provide refactored, better code.",
                verbose=True,
                allow_delegation=False
            )

            # --- TASKS ---
            linting_task = Task(
                description=f"Run static analysis on the following Python code using the flake8_linting_tool.\n\nCode to analyze:\n```python\n{code_input}\n```",
                expected_output="The raw output of the flake8 static analysis tool.",
                agent=static_analysis_agent
            )

            review_task = Task(
                description=f"Using the static analysis output from the previous task and considering the following original code, write a comprehensive code review markdown report. Include human-readable explanations of the issues (if any) and provide a refactored version of the code that fixes the issues.\n\nOriginal Code:\n```python\n{code_input}\n```",
                expected_output="A comprehensive Markdown report containing the code review, explanations of issues, and the suggested refactored code.",
                agent=review_agent
            )

            # --- CREW ---
            crew = Crew(
                agents=[static_analysis_agent, review_agent],
                tasks=[linting_task, review_task],
                process=Process.sequential,
                verbose=1
            )

            # Execute
            try:
                result = crew.kickoff()
                st.success("Review Complete!")
                st.markdown("### 📝 Code Review Report")
                st.markdown(result)
            except Exception as e:
                st.error(f"An error occurred during crew execution: {str(e)}")
