from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from datetime import datetime


class CurrentDateToolInput(BaseModel):
    """Input schema for CurrentDateTool."""
    format: str = Field(
        # default="",
        description="The format in which the current date should be returned"
        # description="The format in which the current date should be returned. Default is '%Y-%m-%d'."
    )

class CurrentDateTool(BaseTool):
    name: str = "Current Date Tool"
    description: str = (
        "A tool to return the current date in a specified format. "
        "Provide the desired date format as an argument."
    )
    args_schema: Type[BaseModel] = CurrentDateToolInput

    def _run(self, format: str) -> str:
        if format == "":
            format = "%Y-%m-%d"
        return datetime.now().strftime(format)

