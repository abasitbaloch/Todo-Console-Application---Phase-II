"""Task endpoints for CRUD operations."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from typing import List
from uuid import UUID

from ..core.database import get_session
from ..models import Task, User
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse
from ..api.deps import get_current_user


router = APIRouter()


@router.get("", response_model=List[TaskResponse])
async def get_all_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Get all tasks for the authenticated user.

    Args:
        current_user: The authenticated user from JWT token
        db: Database session

    Returns:
        List of tasks ordered by creation date (newest first)
    """
    result = await db.execute(
        select(Task)
        .where(Task.user_id == current_user.id)
        .order_by(Task.created_at.desc())
    )
    tasks = result.scalars().all()

    return [TaskResponse.model_validate(task) for task in tasks]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Create a new task for the authenticated user.

    Args:
        task_data: Task creation data (title and optional description)
        current_user: The authenticated user from JWT token
        db: Database session

    Returns:
        The created task
    """
    # Validate title is not empty after trimming
    title = task_data.title.strip()
    if not title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty"
        )

    # Create new task
    new_task = Task(
        user_id=current_user.id,
        title=title,
        description=task_data.description.strip() if task_data.description else None,
        is_completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return TaskResponse.model_validate(new_task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Get a specific task by ID.

    Args:
        task_id: The task UUID
        current_user: The authenticated user from JWT token
        db: Database session

    Returns:
        The requested task

    Raises:
        HTTPException: 404 if task not found or 403 if not owned by user
    """
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify ownership
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Update an existing task.

    Args:
        task_id: The task UUID
        task_data: Task update data (title, description, is_completed)
        current_user: The authenticated user from JWT token
        db: Database session

    Returns:
        The updated task

    Raises:
        HTTPException: 404 if task not found or 403 if not owned by user
    """
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify ownership
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update fields if provided
    if task_data.title is not None:
        title = task_data.title.strip()
        if not title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty"
            )
        task.title = title

    if task_data.description is not None:
        task.description = task_data.description.strip() if task_data.description else None

    if task_data.is_completed is not None:
        task.is_completed = task_data.is_completed

    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Delete a task.

    Args:
        task_id: The task UUID
        current_user: The authenticated user from JWT token
        db: Database session

    Raises:
        HTTPException: 404 if task not found or 403 if not owned by user
    """
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify ownership
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    await db.delete(task)
    await db.commit()
