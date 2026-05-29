from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT_ANVIL_RELEASE_REF = "git+https://github.com/agent-axiom/agent-anvil@v0.2.23"


def test_demo_workflow_and_readme_pin_agent_anvil_release() -> None:
    paths = (
        ROOT / ".github" / "workflows" / "agent-anvil-leaderboard.yml",
        ROOT / "README.md",
    )

    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert AGENT_ANVIL_RELEASE_REF in text
        assert "git+https://github.com/agent-axiom/agent-anvil \\" not in text


def test_demo_workflow_generates_submission_attestation() -> None:
    workflow = (ROOT / ".github" / "workflows" / "agent-anvil-leaderboard.yml").read_text(
        encoding="utf-8"
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "id-token: write" in workflow
    assert "attestations: write" in workflow
    assert "actions/attest@v4" in workflow
    assert "subject-path: leaderboard_submission.json" in workflow
    assert "leaderboard_submission.json" in workflow
    assert "gh attestation verify leaderboard_submission.json" in readme


def test_demo_workflow_can_open_leaderboard_pr() -> None:
    workflow = (ROOT / ".github" / "workflows" / "agent-anvil-leaderboard.yml").read_text(
        encoding="utf-8"
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "LEADERBOARD_PR_TOKEN" in workflow
    assert "LEADERBOARD_PR_TOKEN_AVAILABLE" in workflow
    assert "Auto-PR skipped" in workflow
    assert "repository: agent-axiom/agent-anvil-leaderboard" in workflow
    assert "path: leaderboard-repo" in workflow
    assert "token: ${{ secrets.LEADERBOARD_PR_TOKEN }}" in workflow
    assert "if: env.LEADERBOARD_PR_TOKEN_AVAILABLE == 'true'" in workflow
    assert "anvil leaderboard pr leaderboard_submission.json" in workflow
    assert "--pr-body-out agent-anvil-leaderboard-pr.md" in workflow
    assert "--force" in workflow
    assert "git push --set-upstream origin" in workflow
    assert "gh pr create" in workflow
    assert "GH_TOKEN: ${{ secrets.LEADERBOARD_PR_TOKEN }}" in workflow
    assert "LEADERBOARD_PR_TOKEN" in readme
