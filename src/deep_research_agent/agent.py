#!/usr/bin/env python
import os
import sys
import warnings

from datetime import datetime

from deep_research_agent.crew import DeepResearchAgent
import  deep_research_agent.config as config

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
# Init tracing to Phoenix
config.init_trace()


def run(request, step_callback=None, task_callback=None):
    """
    Run the crew.
    """
    inputs = {
        "topic": request,
        "today": datetime.today().strftime("%Y-%m-%d"),
    }

    result_file = os.getenv('RESULT_FILE', 'result/report.md')

    try:
        return (
            DeepResearchAgent(result_file=result_file)
            .crew(step_callback=step_callback, task_callback=task_callback)
            .kickoff(inputs=inputs)
        )
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
