import pytest
from pydantic import ValidationError

from app.schemas.task import TaskCreate, TaskUpdate


def test_task_create_rejects_blank_title() -> None:
    with pytest.raises(ValidationError):
        TaskCreate(title="   ")


def test_task_update_rejects_blank_title() -> None:
    with pytest.raises(ValidationError):
        TaskUpdate(title="   ")
