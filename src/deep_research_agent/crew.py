from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
from loguru import logger

from deep_research_agent.tools.tavily_tool import TavilySearchTool
from dotenv import load_dotenv
load_dotenv(override=True)

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class DeepResearchAgent():
	"""DeepResearchAgent crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self, result_file: str = None):
		self.llm = self.load_llm_model()
		self.MAX_ITER = int(os.getenv('MAX_ITER', 5))
		self.VERBOSE = os.getenv('VERBOSE', 'true').lower() == 'true'
		self.TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', None)
		# Initialize the tool
		# self.code_interpreter = CodeInterpreterTool()
		self.tavily_search_tool = TavilySearchTool(api_key=self.TAVILY_API_KEY)
		self.result_file = result_file

	def load_llm_model(self):
		MODEL = os.getenv("MODEL", "openai/gpt-4o-mini")
		MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", 0.0))
		CONTEXT_WINDOW_SIZE = int(os.getenv("CONTEXT_WINDOW_SIZE", 0))
		model = f"{MODEL}"
		logger.info(f"Loading LLM model: {model} {MODEL_TEMPERATURE} {CONTEXT_WINDOW_SIZE}")
		if CONTEXT_WINDOW_SIZE>0:
			llm = LLM(
				model=model,
				temperature=MODEL_TEMPERATURE,
				max_tokens=CONTEXT_WINDOW_SIZE,                
			)
		else:
			llm = LLM(
				model=model,
				temperature=MODEL_TEMPERATURE,					
			)
		
		return llm

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			llm=self.llm,
            max_iter=self.MAX_ITER,			
            verbose=self.VERBOSE
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			llm=self.llm,
            max_iter=self.MAX_ITER,
            verbose=self.VERBOSE
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			tools=[self.tavily_search_tool], # Add the tool to the agent
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file=self.result_file
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the DeepResearchAgent crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			# process=Process.sequential,
			process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			manager_llm=self.llm,
            verbose=self.VERBOSE,
			
		)
