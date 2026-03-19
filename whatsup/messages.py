"""Message formatting for notifications."""
from __future__ import annotations


def format_checkin(slug: str, summary: str, details: str | None = None) -> str:
    """Format a manual checkin message."""
    msg = f"Checkin — {slug}\n{summary}"
    if details:
        msg += f"\n\n{details}"
    return msg


def format_sprint_merged(
    slug: str,
    sprint: int,
    branches: int = 0,
    status: str = "passed",
    summary: str = "",
) -> str:
    """Format a sprint merged notification."""
    msg = f"Sprint {sprint} merged — {slug}\n\n{branches} branches · Tests {status}"
    if summary:
        msg += f"\n\n{summary}"
    return msg


def format_test_failure(
    slug: str,
    sprint: int,
    agent: str = "",
    exit_code: int = 1,
) -> str:
    """Format a test failure notification."""
    return (
        f"Sprint {sprint} FAILED — {slug}\n\n"
        f"Agent {agent} merge failed verification\n"
        f"Exit code: {exit_code}"
    )


def format_sprint_started(
    slug: str,
    sprint: int,
    goal: str = "",
    agents: str = "",
    phases: int = 1,
) -> str:
    """Format a sprint-started notification."""
    return (
        f"Sprint {sprint} started — {slug}\n\n"
        f"Goal: {goal}\n"
        f"Agents: {agents}\n"
        f"Phases: {phases}"
    )


def format_agent_completed(
    slug: str,
    sprint: int,
    agent: str,
    duration: str = "",
    commits: int = 0,
    remaining: int = 0,
) -> str:
    """Format an agent-completed notification."""
    return (
        f"Agent {agent} completed — {slug} Sprint {sprint}\n\n"
        f"{duration} · {commits} commits\n"
        f"{remaining} agents remaining"
    )


_FORMATTERS: dict[str, callable] = {
    "checkin": format_checkin,
    "sprint-merged": format_sprint_merged,
    "test-failure": format_test_failure,
    "sprint-started": format_sprint_started,
    "agent-completed": format_agent_completed,
}


def format_event(event: str, **kwargs) -> str:
    """Dispatch to the right format function based on event name."""
    formatter = _FORMATTERS.get(event)
    if formatter is None:
        raise ValueError(
            f"Unknown event '{event}'. "
            f"Valid events: {', '.join(sorted(_FORMATTERS))}"
        )
    return formatter(**kwargs)
