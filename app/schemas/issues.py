from datetime import datetime, date
from pydantic import BaseModel
from typing import Union


class IssueBookForm(BaseModel):
    book_id: int
    user_id: int
    end_of_issue: Union[datetime, date]
