"""Message formatters for project notifications.

Stub — full implementation provided by agentB-core-messages branch.
"""


def format_checkin(slug: str, summary: str, details: str | None = None) -> str:
    text = f"Checkin — {slug}\n{summary}"
    if details:
        text += f"\n\n{details}"
    return text


def format_sprint_merged(
    slug: str,
    sprint: int,
    branches: int = 0,
    status: str = "passed",
    summary: str = "",
) -> str:
    return f"Sprint {sprint} merged — {slug}\n\n{branches} branches · Tests {status}\n\n{summary}"


def format_test_failure(
    slug: str, sprint: int, agent: str = "", exit_code: int = 1
) -> str:
    return f"Sprint {sprint} FAILED — {slug}\n\nAgent {agent} merge failed verification\nExit code: {exit_code}"


def format_event(event: str, **kwargs) -> str:
    dispatch = {
        "checkin": format_checkin,
        "sprint-merged": format_sprint_merged,
        "test-failure": format_test_failure,
    }
    fn = dispatch.get(event)
    if fn is None:
        raise ValueError(f"Unknown event type: {event}")
    return fn(**kwargs)
