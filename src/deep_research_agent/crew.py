from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
from loguru import logger

from deep_research_agent.tools.tavily_tool import TavilySearchTool
from dotenv import load_dotenv
load_dotenv(override=True)

@CrewBase
class DeepResearchAgent():
	"""DeepResearchAgent crew - Deep research on a given topic"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self, result_file: str = None):
		self.llm = self.load_llm_model()
		self.MAX_ITER = int(os.getenv('MAX_ITER', 5))
		self.VERBOSE = os.getenv('VERBOSE', 'true').lower() == 'true'
		self.TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', None)
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

	# Agent definitions
	@agent
	def research_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['research_manager'],
			llm=self.llm,
			max_iter=self.MAX_ITER,
			verbose=self.VERBOSE
		)

	@agent
	def web_search_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['web_search_specialist'],
			llm=self.llm,
			max_iter=self.MAX_ITER,
			verbose=self.VERBOSE,
			tools=[self.tavily_search_tool]
		)

	@agent
	def academic_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['academic_researcher'],
			llm=self.llm,
			max_iter=self.MAX_ITER,
			verbose=self.VERBOSE,
			tools=[self.tavily_search_tool]
		)

	@agent
	def news_reports_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['news_reports_analyst'],
			llm=self.llm,
			max_iter=self.MAX_ITER,
			verbose=self.VERBOSE,
			tools=[self.tavily_search_tool]
		)

	@agent
	def source_evaluator(self) -> Agent:
		return Agent(
			config=self.agents_config['source_evaluator'],
			llm=self.llm,
			max_iter=self.MAX_ITER,
			verbose=self.VERBOSE
		)

	@agent
	def research_synthesizer(self) -> Agent:
		return Agent(
			config=self.agents_config['research_synthesizer'],
			llm=self.llm,
			max_iter=self.MAX_ITER,
			verbose=self.VERBOSE
		)

	@agent
	def report_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['report_writer'],
			llm=self.llm,
			max_iter=self.MAX_ITER,
			verbose=self.VERBOSE
		)

	# Task definitions
	@task
	def define_research_scope_task(self) -> Task:
		return Task(
			config=self.tasks_config['define_research_scope_task']
		)

	@task
	def web_information_gathering_task(self) -> Task:
		return Task(
			config=self.tasks_config['web_information_gathering_task'],
			tools=[self.tavily_search_tool]
		)

	@task
	def academic_literature_search_task(self) -> Task:
		return Task(
			config=self.tasks_config['academic_literature_search_task'],
			tools=[self.tavily_search_tool]
		)

	@task
	def news_reports_search_task(self) -> Task:
		return Task(
			config=self.tasks_config['news_reports_search_task'],
			tools=[self.tavily_search_tool]
		)

	@task
	def source_evaluation_task(self) -> Task:
		return Task(
			config=self.tasks_config['source_evaluation_task']
		)

	@task
	def synthesize_findings_task(self) -> Task:
		return Task(
			config=self.tasks_config['synthesize_findings_task']
		)

	@task
	def compile_report_task(self) -> Task:
		return Task(
			config=self.tasks_config['compile_report_task'],
			output_file=self.result_file
		)

	@task
	def final_review_task(self) -> Task:
		return Task(
			config=self.tasks_config['final_review_task']
		)

	@crew
	def crew(self, step_callback=None, task_callback=None) -> Crew:
		"""Creates the DeepResearchAgent crew for comprehensive topic research"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,  # Sequential process as this is a structured research workflow
			manager_llm=self.llm,
			verbose=self.VERBOSE,
			step_callback=step_callback,
			task_callback=task_callback
		)
