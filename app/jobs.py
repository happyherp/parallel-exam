"""In-memory job store keyed by UUID.

v1 design decision: no persistence. Jobs live only in the process heap.
A browser refresh after the process restarts will lose the job. If the
teacher needs durability, add SQLite (Fly volumes) in a later phase.
Jobs are not explicitly expired; in practice scale-to-zero means the
process restarts after idle periods, which clears them automatically.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime

from app.models import Problem, Template, Variant


@dataclass
class Job:
    job_id: str
    created_at: datetime
    filename: str
    problems: list[Problem]
    templates: dict[int, Template | None]
    variants: dict[int, Variant | None]


_store: dict[str, Job] = {}


def create_job(
    filename: str,
    problems: list[Problem],
    templates: dict[int, Template | None],
    variants: dict[int, Variant | None],
) -> Job:
    job = Job(
        job_id=str(uuid.uuid4()),
        created_at=datetime.utcnow(),
        filename=filename,
        problems=problems,
        templates=templates,
        variants=variants,
    )
    _store[job.job_id] = job
    return job


def get_job(job_id: str) -> Job | None:
    return _store.get(job_id)
