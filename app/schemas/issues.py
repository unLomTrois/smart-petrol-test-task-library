from datetime import datetime
from pydantic import BaseModel


class IssueBookForm(BaseModel):
    book_item_id: int
    user_id: int
    end_of_issue: datetime
