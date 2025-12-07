#!/usr/bin/env python3
"""
gitbro - AI-Powered Git CLI Tool
Simplified and streamlined version with clean architecture.
"""

import subprocess
import sys
from functools import wraps
from pathlib import Path

import click
from git import Repo, InvalidGitRepositoryError

from .config import config
from .providers import get_provider


# ============================================================================
# Prompts - All AI prompts in one place for easy customization
# ============================================================================

PROMPTS = {
    "commit": "Write a concise Git commit message. Use imperative mood, ≤50 chars. Output only the message.",
    "commit_conventional": (
        "Write a Conventional Commits message: type(scope): description. "
        "Types: feat, fix, docs, style, refactor, test, chore. Output only the message."
    ),
    "branch": (
        "Suggest a branch name: type/short-description (e.g., feat/add-login). "
        "Use kebab-case, 2-4 words. Output only the branch name."
    ),
    "explain": (
        "Explain these code changes in plain English. "
        "Be concise, use bullet points. Focus on what and why."
    ),
    "changelog": "Create a markdown changelog grouped by type (Features, Fixes, etc.).",
    "release": "Create user-friendly release notes highlighting major changes.",
    "summary": "Summarize this commit history in 2-3 paragraphs.",
    "fix_commit": (
        "Fix this commit message to follow Conventional Commits format. "
        "Output only the improved message."
    ),
    "analyze_chunk": (
        "Briefly analyze this code change. Is it a fix, feature, or refactor? "
        "Give one-sentence recommendation: Stage? (Yes/No)"
    ),
}


# ============================================================================
# Helpers - DRY utilities
# ============================================================================

def git(*args) -> str:
    """Run git command and return output."""
    result = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise click.ClickException(f"Git error: {result.stderr.strip()}")
    return result.stdout


def require_provider(f):
    """Decorator: ensure provider is configured before running command."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except RuntimeError as e:
            raise click.ClickException(str(e))
        except Exception as e:
            raise click.ClickException(f"Error: {e}")
    return wrapper


def ai(prompt_key: str, content: str, custom_prompt: str = None) -> str:
    """Generate AI response using configured provider."""
    provider = get_provider()
    prompt = custom_prompt or PROMPTS.get(prompt_key, "")
    return provider.generate(content, prompt)


# ============================================================================
# CLI Commands
# ============================================================================

@click.group()
@click.version_option(version="2.1.0", prog_name="gitbro")
def cli():
    """🧠 AI-Powered Git CLI Tool"""
    pass


# --- Commit ---
@cli.command("commit")
@click.option("-t", "--temperature", type=float, help="AI creativity (0.0-2.0)")
@click.option("-a", "--auto", is_flag=True, help="Auto-commit without confirmation")
@click.option("-c", "--conventional", is_flag=True, help="Use Conventional Commits")
@require_provider
def commit(temperature, auto, conventional):
    """Generate AI commit message from staged changes."""
    diff = git("diff", "--cached")
    if not diff.strip():
        raise click.ClickException("No staged changes. Use 'git add' first.")

    if temperature:
        config.set_temperature(temperature)

    prompt_key = "commit_conventional" if conventional else "commit"
    msg = ai(prompt_key, diff)

    if auto:
        git("commit", "-m", msg)
        click.echo(f"✅ Committed: {msg}")
    else:
        click.echo(f"📝 {msg}")
        if click.confirm("Commit with this message?"):
            git("commit", "-m", msg)
            click.echo("✅ Done!")


# --- Branch Suggest ---
@cli.command("branch")
@click.option("-c", "--create", is_flag=True, help="Create the suggested branch")
@click.option("--from-commit", type=str, help="Base on specific commit")
@require_provider
def branch_suggest(create, from_commit):
    """Suggest semantic branch name based on changes."""
    if from_commit:
        diff = git("show", "--format=", from_commit)
    else:
        diff = git("diff", "--cached") or git("show", "--format=", "HEAD")

    if not diff.strip():
        raise click.ClickException("No changes to analyze.")

    name = ai("branch", diff).strip()
    click.echo(f"🌿 Suggested: {name}")

    if create and click.confirm("Create this branch?"):
        git("checkout", "-b", name)
        click.echo(f"✅ Switched to {name}")


# --- Explain ---
@cli.command("explain")
@click.option("-s", "--staged", is_flag=True, help="Explain staged changes only")
@click.option("-f", "--file", "filepath", type=str, help="Explain specific file")
@require_provider
def explain(staged, filepath):
    """Get plain English explanation of code changes."""
    if filepath:
        diff = git("diff", filepath)
    elif staged:
        diff = git("diff", "--cached")
    else:
        diff = git("diff")

    if not diff.strip():
        click.echo("No changes to explain.")
        return

    result = ai("explain", diff)
    click.echo(f"📝 {result}")


# --- Summarize ---
@cli.command("summarize")
@click.option("--since", type=str, help="Since date/commit (e.g., '1 week ago')")
@click.option("--author", type=str, help="Filter by author")
@click.option("--branch", type=str, help="Specific branch")
@click.option("--format", "fmt", type=click.Choice(["summary", "changelog", "release"]), default="summary")
@require_provider
def summarize(since, author, branch, fmt):
    """Summarize commit history as changelog or release notes."""
    cmd = ["log", "--oneline"]
    if since:
        cmd.append(f"--since={since}")
    if author:
        cmd.append(f"--author={author}")
    if branch:
        cmd.append(branch)

    logs = git(*cmd)
    if not logs.strip():
        click.echo("No commits found.")
        return

    result = ai(fmt, logs)
    click.echo(f"📊 {result}")


# --- Validate ---
@cli.command("validate")
@click.option("--range", "commit_range", type=str, help="Commit range (e.g., HEAD~5..HEAD)")
@click.option("--fix", is_flag=True, help="Suggest fixes for invalid messages")
@click.option("-c", "--conventional", is_flag=True, help="Check Conventional Commits format")
@require_provider
def validate(commit_range, fix, conventional):
    """Validate commit message formats."""
    cmd = ["log", "--pretty=format:%H|%s"]
    cmd.append(commit_range or "-10")

    logs = git(*cmd)
    if not logs.strip():
        click.echo("No commits found.")
        return

    commits = [(h[:8], m) for line in logs.strip().split("\n") if "|" in line for h, m in [line.split("|", 1)]]

    if not conventional:
        for h, m in commits:
            status = "✅" if len(m) <= 50 else "⚠️"
            click.echo(f"{status} {h}: {m}")
        return

    valid_types = {"feat", "fix", "docs", "style", "refactor", "test", "chore", "perf", "ci", "build", "revert"}
    invalid = []

    for h, m in commits:
        if ":" not in m:
            invalid.append((h, m, "Missing type:"))
        else:
            t = m.split(":")[0].split("(")[0].strip()
            if t not in valid_types:
                invalid.append((h, m, f"Invalid type '{t}'"))

    if not invalid:
        click.echo("✅ All commits follow Conventional Commits!")
        return

    click.echo("❌ Invalid commits:")
    for h, m, reason in invalid:
        click.echo(f"  {h}: {m} ({reason})")

    if fix:
        click.echo("\n🔧 Suggestions:")
        for h, m, _ in invalid[:3]:
            fixed = ai("fix_commit", f"Original: {m}")
            click.echo(f"  {h}: {fixed}")


# --- Interactive Add ---
@cli.command("add")
@require_provider
def interactive_add():
    """AI-assisted interactive staging."""
    diff = git("diff")
    if not diff.strip():
        click.echo("No unstaged changes.")
        return

    # Parse diff into file chunks
    chunks = []
    current_file, current_lines = None, []

    for line in diff.split("\n"):
        if line.startswith("diff --git"):
            if current_file:
                chunks.append((current_file, "\n".join(current_lines)))
            current_file = line.split("b/")[-1] if "b/" in line else "unknown"
            current_lines = []
        current_lines.append(line)

    if current_file:
        chunks.append((current_file, "\n".join(current_lines)))

    click.echo("🤖 AI-Assisted Staging\n")

    for filename, chunk in chunks:
        if not chunk.strip():
            continue

        analysis = ai("analyze_chunk", chunk)
        click.echo(f"📁 {filename}")
        click.echo(f"   {analysis}")

        choice = click.prompt("Stage? [y/n/d(iff)/q(uit)]", type=click.Choice(["y", "n", "d", "q"]), default="y")

        if choice == "q":
            break
        if choice == "d":
            click.echo(chunk)
            choice = click.prompt("Stage?", type=click.Choice(["y", "n"]))
        if choice == "y":
            git("add", filename)
            click.echo(f"   ✅ Staged\n")
        else:
            click.echo()


# --- Clean Branches ---
@cli.command("clean")
@click.option("-r", "--remote", is_flag=True, help="Also delete remote branches")
@click.option("-f", "--force", is_flag=True, help="Skip confirmations")
@click.option("-d", "--dry-run", is_flag=True, help="Preview only")
def clean_branches(remote, force, dry_run):
    """Clean merged branches."""
    try:
        repo = Repo(".")
    except InvalidGitRepositoryError:
        raise click.ClickException("Not a Git repository.")

    # Find main branch
    branches = [b.name for b in repo.branches]
    main = "main" if "main" in branches else ("master" if "master" in branches else None)
    if not main:
        raise click.ClickException("No main/master branch found.")

    current = repo.active_branch.name

    # Switch to main if needed
    if current != main and not dry_run:
        if not force and not click.confirm(f"Switch from '{current}' to '{main}'?"):
            return
        repo.git.checkout(main)
        try:
            repo.git.pull("origin", main)
        except Exception:
            pass

    # Get merged branches
    merged = [b.strip().replace("*", "").strip() for b in repo.git.branch("--merged", main).split("\n")]
    merged = [b for b in merged if b and b not in {main, "master"} and not b.startswith("(")]

    if not merged:
        click.echo(f"✅ No local branches to clean!")
    else:
        click.echo(f"\n🔍 Merged into {main}:")
        for b in merged:
            click.echo(f"  • {b}")

        if dry_run:
            click.echo(f"\n[DRY RUN] Would delete {len(merged)} branch(es)")
        elif force or click.confirm(f"\nDelete {len(merged)} branch(es)?"):
            for b in merged:
                try:
                    repo.git.branch("-d", b)
                    click.echo(f"  ✅ Deleted: {b}")
                except Exception as e:
                    click.echo(f"  ❌ Failed: {b} ({e})")

    # Remote branches
    if remote:
        try:
            remote_merged = repo.git.branch("-r", "--merged", f"origin/{main}").split("\n")
            remote_branches = [
                b.strip().replace("origin/", "") for b in remote_merged
                if b.strip().startswith("origin/") and not b.strip().endswith(f"origin/{main}")
            ]
            remote_branches = [b for b in remote_branches if b not in {main, "master"}]

            if not remote_branches:
                click.echo(f"\n✅ No remote branches to clean!")
            else:
                click.echo(f"\n🔍 Remote merged branches:")
                for b in remote_branches:
                    click.echo(f"  • origin/{b}")

                if dry_run:
                    click.echo(f"\n[DRY RUN] Would delete {len(remote_branches)} remote branch(es)")
                elif force or click.confirm(f"\nDelete {len(remote_branches)} remote branch(es)?"):
                    for b in remote_branches:
                        try:
                            repo.git.push("origin", "--delete", b)
                            click.echo(f"  ✅ Deleted: origin/{b}")
                        except Exception as e:
                            click.echo(f"  ❌ Failed: origin/{b} ({e})")
        except Exception:
            pass

    if not dry_run:
        click.echo("\n🎉 Done!")


# --- Setup ---
@cli.command("setup")
@click.argument("provider", type=click.Choice(["openai", "gemini", "claude", "ollama"]), required=False)
def setup(provider):
    """Configure AI provider."""
    if provider:
        config.setup_provider(provider)
    else:
        # Interactive menu
        providers = config.list_providers()
        click.echo("\nAvailable providers:")
        for i, (name, configured) in enumerate(providers.items(), 1):
            status = "✓" if configured else "✗"
            click.echo(f"  {i}. {name.upper()} [{status}]")

        try:
            choice = click.prompt("Select (1-4)", type=int)
            selected = list(providers.keys())[choice - 1]
            config.setup_provider(selected)
        except (IndexError, ValueError):
            click.echo("Invalid choice.")


# --- Status ---
@cli.command("status")
def status():
    """Show current configuration."""
    p = config.get_provider()
    if not p:
        click.echo("No provider configured. Run 'gitbro setup'.")
        return

    click.echo(f"Provider: {p.upper()}")
    click.echo(f"Model: {config.get_model(p)}")
    click.echo(f"Temperature: {config.get_temperature()}")


# --- Graph ---
@cli.command("graph")
@click.option("-p", "--port", type=int, default=8787, help="Server port")
@click.option("-n", "--limit", type=int, default=100, help="Number of commits")
@click.option("--no-browser", is_flag=True, help="Don't open browser")
def graph(port, limit, no_browser):
    """Open Git graph in browser."""
    from .web_graph import start_server
    start_server(port=port, limit=limit, no_browser=no_browser)


# --- Install Hook ---
@cli.command("hook")
@click.option("--uninstall", is_flag=True, help="Remove the hook")
def install_hook(uninstall):
    """Install/remove pre-commit hook."""
    try:
        repo = Repo(".")
    except InvalidGitRepositoryError:
        raise click.ClickException("Not a Git repository.")

    hook_path = Path(repo.git_dir) / "hooks" / "prepare-commit-msg"

    if uninstall:
        if hook_path.exists():
            hook_path.unlink()
            click.echo("✅ Hook removed.")
        else:
            click.echo("No hook installed.")
        return

    hook_content = '''#!/bin/bash
# gitbro prepare-commit-msg hook
COMMIT_MSG_FILE=$1
COMMIT_SOURCE=$2

# Only run for regular commits (not merge, squash, etc.)
if [ -z "$COMMIT_SOURCE" ]; then
    # Check if message is empty or default
    if [ ! -s "$COMMIT_MSG_FILE" ] || grep -q "^#" "$COMMIT_MSG_FILE"; then
        MSG=$(gitbro commit --auto 2>/dev/null | grep -oP "(?<=Committed: ).*")
        if [ -n "$MSG" ]; then
            echo "$MSG" > "$COMMIT_MSG_FILE"
        fi
    fi
fi
'''

    hook_path.parent.mkdir(exist_ok=True)
    hook_path.write_text(hook_content)
    hook_path.chmod(0o755)
    click.echo("✅ Hook installed!")


# ============================================================================
# Entry point with command aliases
# ============================================================================

class AliasedGroup(click.Group):
    """Support command aliases."""

    def get_command(self, ctx, cmd_name):
        # Try exact match first
        cmd = click.Group.get_command(self, ctx, cmd_name)
        if cmd:
            return cmd

        # Try aliases
        aliases = {
            "c": "commit",
            "b": "branch",
            "e": "explain",
            "s": "summarize",
            "v": "validate",
            "a": "add",
            "g": "graph",
        }
        if cmd_name in aliases:
            return click.Group.get_command(self, ctx, aliases[cmd_name])

        return None


# Replace the default group with aliased version
cli = AliasedGroup(
    name="gitbro",
    help="🧠 AI-Powered Git CLI Tool",
    commands={
        "commit": commit,
        "branch": branch_suggest,
        "explain": explain,
        "summarize": summarize,
        "validate": validate,
        "add": interactive_add,
        "clean": clean_branches,
        "graph": graph,
        "setup": setup,
        "status": status,
        "hook": install_hook,
    }
)


def main():
    cli()


if __name__ == "__main__":
    main()
