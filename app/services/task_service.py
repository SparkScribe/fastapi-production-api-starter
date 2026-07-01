from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, TaskStatus
from app.schemas.task import PaginatedTasks, TaskCreate, TaskUpdate


async def create_task(db: AsyncSession, owner_id: int, data: TaskCreate) -> Task:
    task = Task(owner_id=owner_id, **data.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_task(db: AsyncSession, task_id: int, owner_id: int) -> Task | None:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.owner_id == owner_id)
    )
    return result.scalar_one_or_none()


async def list_tasks(
    db: AsyncSession,
    owner_id: int,
    *,
    page: int,
    page_size: int,
    status: TaskStatus | None,
) -> PaginatedTasks:
    filters = [Task.owner_id == owner_id]
    if status is not None:
        filters.append(Task.status == status)

    count_q = select(func.count()).select_from(Task).where(*filters)
    total = (await db.execute(count_q)).scalar_one()

    offset = (page - 1) * page_size
    items_q = (
        select(Task)
        .where(*filters)
        .order_by(Task.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(items_q)
    items = list(result.scalars().all())

    pages = max(1, (total + page_size - 1) // page_size)
    return PaginatedTasks(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


async def update_task(db: AsyncSession, task: Task, data: TaskUpdate) -> Task:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task: Task) -> None:
    await db.delete(task)
    await db.commit()
