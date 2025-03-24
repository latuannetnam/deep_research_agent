#!/usr/bin/env python
import os
import sys
import warnings

from datetime import datetime

from deep_research_agent.crew import DeepResearchAgent
import  deep_research_agent.config as config

# Init tracing to Phoenix
config.init_trace()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    topic = os.getenv('TOPIC', 'AI Agent Trends')
    result_file = os.getenv('RESULT_FILE', 'result/report.md')
    inputs = {
        'topic': topic,
        'current_year': str(datetime.now().year)
    }
    
    try:
        agent = DeepResearchAgent(result_file=result_file).crew()
        result = agent.kickoff(inputs=inputs)
        print(f"Final result:\n {result}")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        DeepResearchAgent().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        DeepResearchAgent().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        DeepResearchAgent().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
