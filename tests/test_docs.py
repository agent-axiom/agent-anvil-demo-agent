from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT_ANVIL_RELEASE_REF = "git+https://github.com/agent-axiom/agent-anvil@v0.2.19"


def test_demo_workflow_and_readme_pin_agent_anvil_release() -> None:
    paths = (
        ROOT / ".github" / "workflows" / "agent-anvil-leaderboard.yml",
        ROOT / "README.md",
    )

    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert AGENT_ANVIL_RELEASE_REF in text
        assert "git+https://github.com/agent-axiom/agent-anvil \\" not in text
