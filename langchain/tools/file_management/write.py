from pathlib import Path
from typing import Optional, Type

from pydantic import BaseModel, Field

from langchain.tools.file_management.utils import get_validated_relative_path
from langchain.tools.structured import BaseStructuredTool


class WriteFileInput(BaseModel):
    """Input for WriteFileTool."""

    file_path: str = Field(..., description="name of file")
    text: str = Field(..., description="text to write to file")


class WriteFileTool(BaseStructuredTool[str, WriteFileInput]):
    name: str = "write_file"
    args_schema: Type[WriteFileInput] = WriteFileInput
    description: str = "Write file to disk"
    root_dir: Optional[str] = None
    """Directory to write file to.

    If specified, raises an error for file_paths oustide root_dir."""

    def _run(self, tool_input: WriteFileInput) -> str:
        write_path = (
            get_validated_relative_path(Path(self.root_dir), tool_input.file_path)
            if self.root_dir
            else Path(tool_input.file_path)
        )
        try:
            write_path.parent.mkdir(exist_ok=True, parents=False)
            with write_path.open("w", encoding="utf-8") as f:
                f.write(tool_input.text)
            return f"File written successfully to {tool_input.file_path}."
        except Exception as e:
            return "Error: " + str(e)

    async def _arun(self, tool_input: WriteFileInput) -> str:
        # TODO: Add aiofiles method
        raise NotImplementedError
