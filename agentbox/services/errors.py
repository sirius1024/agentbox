"""Domain exceptions used by the service layer."""
from __future__ import annotations


class AgentBoxError(Exception):
    """Base class for AgentBox domain errors."""


class NotFoundError(AgentBoxError):
    pass


class ConflictError(AgentBoxError):
    pass


class ValidationError(AgentBoxError):
    pass
