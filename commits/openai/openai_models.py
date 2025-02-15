from pydantic import BaseModel, Field
from typing import Optional, List

class Snippet(BaseModel):
    title: str = Field(..., description="Title of the commit change, maximum should be 3-4 words")
    commit_message: str = Field(..., description="Meaningful and short commit message (max 8-10 words)")
    file_type: Optional[str] = Field(None, description="File extension based on the problem or user input (e.g., py, js, html)")
    code: Optional[str] = Field(None, description="Actual code solution or README content if applicable")

class OpenAIResponse(BaseModel):
    is_pushable: bool = Field(..., description="Indicates if the user input is pushable to GitHub")
    response: Optional[str] = Field(None, description="Brief summary of 1-2 lines if the user input is not pushable then why? and if it is pushable then why?")
    snippets: Optional[List[Snippet]] = Field(None, description="List of commit details, if is_pushable is True")
