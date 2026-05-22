from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ...schemas.agent import AgentCreate, AgentOut, AgentUpdate
from ...services import agents as svc
from ..deps import get_db, require_admin

router = APIRouter(prefix="/agents", tags=["agents"], dependencies=[Depends(require_admin)])


@router.post("", response_model=AgentOut, status_code=status.HTTP_201_CREATED)
def create_agent(payload: AgentCreate, db: Session = Depends(get_db)) -> AgentOut:
    return AgentOut.model_validate(svc.create_agent(db, payload))


@router.get("", response_model=list[AgentOut])
def list_agents(
    owner_id: str | None = Query(default=None),
    runtime_type: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
) -> list[AgentOut]:
    items = svc.list_agents(
        db, owner_id=owner_id, runtime_type=runtime_type, status=status_filter
    )
    return [AgentOut.model_validate(a) for a in items]


@router.get("/{agent_id}", response_model=AgentOut)
def get_agent(agent_id: str, db: Session = Depends(get_db)) -> AgentOut:
    return AgentOut.model_validate(svc.get_agent(db, agent_id))


@router.patch("/{agent_id}", response_model=AgentOut)
def update_agent(
    agent_id: str, payload: AgentUpdate, db: Session = Depends(get_db)
) -> AgentOut:
    return AgentOut.model_validate(svc.update_agent(db, agent_id, payload))


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(agent_id: str, db: Session = Depends(get_db)) -> None:
    svc.delete_agent(db, agent_id)
