# Agent Anvil Demo Agent

This repository is a minimal public agent repository used to demonstrate the
Agent Anvil leaderboard flow end to end:

1. GitHub Actions runs the Agent Anvil trace benchmark.
2. Agent Anvil exports a compact leaderboard submission.
3. The workflow validates `github_actions` trust metadata.
4. The workflow creates a GitHub artifact attestation for the submission JSON.
5. The workflow opens a pull request against
   [agent-axiom/agent-anvil-leaderboard](https://github.com/agent-axiom/agent-anvil-leaderboard).

The demo agent is intentionally imperfect. Its final answers often look fine,
but its traces contain unsafe tool behavior such as destructive tools called
before verification. That makes it a useful reference row for showing why
trace-aware evals catch failures final-answer checks miss.

## Run Locally

```bash
uvx --from git+https://github.com/agent-axiom/agent-anvil@v0.2.23 \
  anvil paper reproduce \
  --manifest experiments/paper.yaml

uvx --from git+https://github.com/agent-axiom/agent-anvil@v0.2.23 \
  anvil leaderboard export docs/paper/results.json \
  --manifest experiments/paper.yaml \
  --out leaderboard_submission.json \
  --agent-name "Agent Anvil Demo Agent" \
  --agent-version "$(git rev-parse --short HEAD)" \
  --repo-url "https://github.com/agent-axiom/agent-anvil-demo-agent" \
  --commit-sha "$(git rev-parse HEAD)"

uvx --from git+https://github.com/agent-axiom/agent-anvil@v0.2.23 \
  anvil leaderboard validate leaderboard_submission.json
```

## Submit To The Public Leaderboard

Run **Agent Anvil Leaderboard Submission** from the Actions tab. The workflow
downloads Agent Anvil `v0.2.23`, exports and attests
`leaderboard_submission.json`, checks out the public leaderboard repository,
and opens a pull request with a generated review body.

Configure a repository secret named `LEADERBOARD_PR_TOKEN` with permission to
push a branch and open pull requests against
`agent-axiom/agent-anvil-leaderboard`. This token is only used for publishing
the aggregate JSON handoff; the leaderboard repository still does not execute
the demo agent.

After downloading `leaderboard_submission.json`, provenance can be checked with:

```bash
gh attestation verify leaderboard_submission.json -R agent-axiom/agent-anvil-demo-agent
```
