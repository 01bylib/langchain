"""Tool for the DuckDuckGo search API."""

from pydantic import Field

from langchain.tools.base import BaseTool
from langchain.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
import warnings

class DuckDuckGoSearchRun(BaseTool):
    """Tool that adds the capability to query the DuckDuckGo search API."""

    name = "DuckDuckGo Search"
    description = (
        "A wrapper around DuckDuckGo Search. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query."
    )
    api_wrapper: DuckDuckGoSearchAPIWrapper = Field(
        default_factory=DuckDuckGoSearchAPIWrapper
    )

    def _run(self, query: str) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("DuckDuckGoSearch does not support async")


class DuckDuckGoSearchResults(BaseTool):
    """Tool that has capability to query the Duck Duck Go Search API and get back json."""

    name = "DuckDuckGo Results JSON"
    description = (
        "A wrapper around Duck Duck Go Search. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query. Output is a JSON array of the query results"
    )
    num_results: int = 4
    api_wrapper: DuckDuckGoSearchAPIWrapper = Field(
        default_factory=DuckDuckGoSearchAPIWrapper
    )

    def _run(self, query: str) -> str:
        """Use the tool."""
        return str(self.api_wrapper.results(query, self.num_results))

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("DuckDuckGoSearchResults does not support async")

def DuckDuckGoSearchTool(*args, **kwargs):
    warnings.warn(
        "DuckDuckGoSearchTool will be deprecated in the future. "
        "Please use DuckDuckGoSearchRun instead.",
        DeprecationWarning,
    )
    return DuckDuckGoSearchRun(*args, **kwargs)