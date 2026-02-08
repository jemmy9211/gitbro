#!/usr/bin/env python3
"""
gitbro TUI - Interactive Terminal UI
Run `gitbro` without arguments to launch the interactive menu.
"""

import subprocess
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.syntax import Syntax
from rich import box

from .config import config
from .providers import get_provider

console = Console()

# ============================================================================
# Prompts
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
# Helpers
# ============================================================================


def git(*args) -> str:
    """Run git command and return output."""
    result = subprocess.run(
        ["git", *args], capture_output=True, text=True,
        encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout


def ai(prompt_key: str, content: str) -> str:
    """Generate AI response."""
    provider = get_provider()
    prompt = PROMPTS.get(prompt_key, "")
    return provider.generate(content, prompt)


def show_banner():
    """Show the gitbro banner."""
    banner = Text()
    banner.append("gitbro", style="bold cyan")
    banner.append("  AI-Powered Git Tool", style="dim")
    console.print(Panel(banner, border_style="dim", padding=(0, 2)))


def err(msg: str):
    console.print(f"  [red]x[/red] {msg}")


def ok(msg: str):
    console.print(f"  [green]>[/green] {msg}")


def info(msg: str):
    console.print(f"  [dim]|[/dim] {msg}")


def ask_choice(prompt: str, choices: list[str], default: int = 0) -> int:
    """Show a selection menu and return the chosen index. Returns -1 on cancel."""
    console.print()
    console.print(f"  [bold]{prompt}[/bold]")
    console.print()
    for i, choice in enumerate(choices):
        num_style = "cyan" if i == default else "dim"
        console.print(f"    [{num_style}]{i + 1}[/{num_style}]  {choice}")
    console.print()
    console.print("  [dim]#[/dim] ", end="")

    try:
        raw = input().strip()
    except (KeyboardInterrupt, EOFError):
        return -1

    if raw.lower() in ("q", "quit", "exit", "0"):
        return -1
    try:
        idx = int(raw) - 1
        if 0 <= idx < len(choices):
            return idx
    except ValueError:
        pass

    if raw == "":
        return default

    err("Invalid choice")
    return -1


def ask_confirm(prompt: str, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    console.print(f"  {prompt} [dim]{suffix}[/dim] ", end="")
    try:
        raw = input().strip().lower()
    except (KeyboardInterrupt, EOFError):
        return False
    if raw == "":
        return default
    return raw in ("y", "yes")


def ask_input(prompt: str, default: str = "") -> str:
    if default:
        console.print(f"  {prompt} [dim]({default})[/dim]: ", end="")
    else:
        console.print(f"  {prompt}: ", end="")
    try:
        raw = input().strip()
    except (KeyboardInterrupt, EOFError):
        return default
    return raw or default


# ============================================================================
# Git Basic Operations
# ============================================================================

def action_status():
    """Show git status."""
    console.print()
    console.print("  [bold]Status[/bold]")
    console.print()

    try:
        branch = git("branch", "--show-current").strip()
        console.print(f"  branch  [cyan]{branch}[/cyan]")

        try:
            ab = git("rev-list", "--left-right", "--count", f"HEAD...origin/{branch}").strip()
            ahead, behind = ab.split()
            if int(ahead) > 0 or int(behind) > 0:
                parts = []
                if int(ahead) > 0:
                    parts.append(f"[green]+{ahead} ahead[/green]")
                if int(behind) > 0:
                    parts.append(f"[red]-{behind} behind[/red]")
                console.print(f"  remote  {', '.join(parts)}")
        except Exception:
            pass

        console.print()

        staged = git("diff", "--cached", "--name-status").strip()
        if staged:
            console.print("  [green]Staged:[/green]")
            for line in staged.split("\n"):
                parts = line.split("\t", 1)
                if len(parts) == 2:
                    st, name = parts
                    console.print(f"    [green]{st}[/green]  {name}")
            console.print()

        unstaged = git("diff", "--name-status").strip()
        if unstaged:
            console.print("  [yellow]Modified:[/yellow]")
            for line in unstaged.split("\n"):
                parts = line.split("\t", 1)
                if len(parts) == 2:
                    st, name = parts
                    console.print(f"    [yellow]{st}[/yellow]  {name}")
            console.print()

        untracked = git("ls-files", "--others", "--exclude-standard").strip()
        if untracked:
            console.print("  [red]Untracked:[/red]")
            lines = untracked.split("\n")
            for f in lines[:15]:
                console.print(f"    [red]?[/red]  {f}")
            if len(lines) > 15:
                console.print(f"    [dim]...and {len(lines) - 15} more[/dim]")
            console.print()

        if not staged and not unstaged and not untracked:
            ok("Working tree clean.")

    except RuntimeError as e:
        err(str(e))


def action_stage():
    """Stage files interactively."""
    console.print()
    console.print("  [bold]Stage[/bold]")
    console.print()

    try:
        modified = git("diff", "--name-only").strip().split("\n") if git("diff", "--name-only").strip() else []
        untracked = git("ls-files", "--others", "--exclude-standard").strip().split("\n") if git("ls-files", "--others", "--exclude-standard").strip() else []
        all_files = modified + untracked
    except RuntimeError as e:
        err(str(e))
        return

    if not all_files:
        ok("Nothing to stage.")
        return

    choice = ask_choice("What to stage?", [
        "All files  (git add -A)",
        "Pick files individually",
        "By pattern  (e.g. *.py)",
        "Cancel",
    ], default=0)

    if choice == -1 or choice == 3:
        return
    elif choice == 0:
        try:
            git("add", "-A")
            ok(f"Staged all {len(all_files)} file(s).")
        except RuntimeError as e:
            err(str(e))
    elif choice == 1:
        staged = 0
        for i, f in enumerate(all_files):
            tag = "[red]new[/red]" if f in untracked else "[yellow]mod[/yellow]"
            console.print(f"  ({i+1}/{len(all_files)}) {tag} {f}")
            if ask_confirm("  Stage?"):
                try:
                    git("add", f)
                    staged += 1
                except RuntimeError as e:
                    err(str(e))
        ok(f"Staged {staged} file(s).")
    elif choice == 2:
        pattern = ask_input("Pattern (e.g. src/*.py)")
        if pattern:
            try:
                git("add", pattern)
                ok(f"Staged: {pattern}")
            except RuntimeError as e:
                err(str(e))


def action_unstage():
    """Unstage files."""
    console.print()
    console.print("  [bold]Unstage[/bold]")
    console.print()

    try:
        staged = git("diff", "--cached", "--name-only").strip()
    except RuntimeError as e:
        err(str(e))
        return

    if not staged:
        ok("Nothing is staged.")
        return

    files = staged.split("\n")
    console.print("  Staged files:")
    for f in files:
        console.print(f"    [green]+[/green] {f}")
    console.print()

    choice = ask_choice("Unstage:", [
        "All staged files",
        "Pick individually",
        "Cancel",
    ], default=0)

    if choice == -1 or choice == 2:
        return
    elif choice == 0:
        try:
            git("reset", "HEAD")
            ok("All files unstaged.")
        except RuntimeError as e:
            err(str(e))
    elif choice == 1:
        for f in files:
            if ask_confirm(f"  Unstage {f}?"):
                try:
                    git("reset", "HEAD", f)
                    ok(f"Unstaged: {f}")
                except RuntimeError as e:
                    err(str(e))


def action_commit():
    """Generate AI commit message."""
    console.print()
    console.print("  [bold]AI Commit[/bold]")
    console.print()

    try:
        diff = git("diff", "--cached")
    except RuntimeError as e:
        err(str(e))
        return

    if not diff.strip():
        err("No staged changes.")
        console.print()
        if ask_confirm("Stage all first? (git add -A)"):
            try:
                git("add", "-A")
                diff = git("diff", "--cached")
                if not diff.strip():
                    err("Still no changes.")
                    return
                ok("All changes staged.")
            except RuntimeError as e:
                err(str(e))
                return
        else:
            return

    fmt_choice = ask_choice("Format:", [
        "Standard",
        "Conventional Commits (feat/fix/...)",
    ], default=0)

    if fmt_choice == -1:
        return

    prompt_key = "commit_conventional" if fmt_choice == 1 else "commit"

    console.print()
    with console.status("[dim]generating...[/dim]"):
        try:
            msg = ai(prompt_key, diff)
        except Exception as e:
            err(f"AI error: {e}")
            return

    console.print(Panel(msg, title="message", border_style="green", padding=(0, 2)))
    console.print()

    choice = ask_choice("", [
        "Commit",
        "Edit then commit",
        "Regenerate",
        "Cancel",
    ], default=0)

    if choice == 0:
        try:
            git("commit", "-m", msg)
            ok(f"Committed: {msg}")
        except RuntimeError as e:
            err(str(e))
    elif choice == 1:
        edited = ask_input("Message", default=msg)
        if edited:
            try:
                git("commit", "-m", edited)
                ok(f"Committed: {edited}")
            except RuntimeError as e:
                err(str(e))
    elif choice == 2:
        action_commit()


def action_amend():
    """Amend last commit."""
    console.print()
    console.print("  [bold]Amend Last Commit[/bold]")
    console.print()

    try:
        last_msg = git("log", "-1", "--pretty=%s").strip()
        last_hash = git("log", "-1", "--pretty=%h").strip()
    except RuntimeError as e:
        err(str(e))
        return

    console.print(f"  Last commit: [cyan]{last_hash}[/cyan] {last_msg}")
    console.print()

    choice = ask_choice("Amend how?", [
        "Change message only",
        "Add staged changes + change message",
        "Add staged changes, keep message",
        "Cancel",
    ], default=0)

    if choice == -1 or choice == 3:
        return
    elif choice == 0:
        new_msg = ask_input("New message", default=last_msg)
        if new_msg:
            try:
                git("commit", "--amend", "-m", new_msg)
                ok(f"Amended: {new_msg}")
            except RuntimeError as e:
                err(str(e))
    elif choice == 1:
        new_msg = ask_input("New message", default=last_msg)
        if new_msg:
            try:
                git("commit", "--amend", "-m", new_msg)
                ok(f"Amended with staged changes: {new_msg}")
            except RuntimeError as e:
                err(str(e))
    elif choice == 2:
        try:
            git("commit", "--amend", "--no-edit")
            ok("Amended (message unchanged).")
        except RuntimeError as e:
            err(str(e))


def action_push():
    """Push to remote."""
    console.print()
    console.print("  [bold]Push[/bold]")
    console.print()

    try:
        branch = git("branch", "--show-current").strip()
    except RuntimeError as e:
        err(str(e))
        return

    console.print(f"  branch: [cyan]{branch}[/cyan]")

    try:
        git("rev-parse", "--abbrev-ref", f"{branch}@{{upstream}}")
        has_upstream = True
    except RuntimeError:
        has_upstream = False

    if not has_upstream:
        console.print(f"  [yellow]No upstream set.[/yellow]")
        if ask_confirm(f"Push and set upstream? (git push -u origin {branch})"):
            try:
                result = git("push", "-u", "origin", branch)
                ok(f"Pushed and set upstream: origin/{branch}")
                if result.strip():
                    info(result.strip())
            except RuntimeError as e:
                err(str(e))
        return

    choice = ask_choice("", [
        f"Push to origin/{branch}",
        "Push with force (--force-with-lease)",
        "Cancel",
    ], default=0)

    if choice == 0:
        try:
            result = git("push")
            ok("Pushed.")
            if result.strip():
                info(result.strip())
        except RuntimeError as e:
            err(str(e))
    elif choice == 1:
        if ask_confirm("Force push? This may overwrite remote.", default=False):
            try:
                result = git("push", "--force-with-lease")
                ok("Force pushed.")
                if result.strip():
                    info(result.strip())
            except RuntimeError as e:
                err(str(e))


def action_pull():
    """Pull from remote."""
    console.print()
    console.print("  [bold]Pull[/bold]")
    console.print()

    choice = ask_choice("Strategy:", [
        "Pull (merge)",
        "Pull (rebase)",
        "Fetch only",
        "Cancel",
    ], default=0)

    if choice == -1 or choice == 3:
        return

    try:
        if choice == 0:
            result = git("pull")
            ok("Pulled (merge).")
        elif choice == 1:
            result = git("pull", "--rebase")
            ok("Pulled (rebase).")
        elif choice == 2:
            result = git("fetch", "--all")
            ok("Fetched all remotes.")

        if result.strip():
            info(result.strip())
    except RuntimeError as e:
        err(str(e))


def action_stash():
    """Stash operations."""
    console.print()
    console.print("  [bold]Stash[/bold]")
    console.print()

    try:
        stash_list = git("stash", "list").strip()
    except RuntimeError:
        stash_list = ""

    if stash_list:
        console.print("  Stash list:")
        for line in stash_list.split("\n")[:10]:
            console.print(f"    [dim]{line}[/dim]")
        console.print()

    choice = ask_choice("", [
        "Stash current changes",
        "Stash with message",
        "Stash (include untracked)",
        "Pop latest stash",
        "Apply latest stash (keep in list)",
        "Drop a stash",
        "Cancel",
    ], default=0)

    if choice == -1 or choice == 6:
        return

    try:
        if choice == 0:
            git("stash", "push")
            ok("Stashed.")
        elif choice == 1:
            msg = ask_input("Message")
            if msg:
                git("stash", "push", "-m", msg)
                ok(f"Stashed: {msg}")
        elif choice == 2:
            git("stash", "push", "--include-untracked")
            ok("Stashed (with untracked).")
        elif choice == 3:
            git("stash", "pop")
            ok("Popped latest stash.")
        elif choice == 4:
            git("stash", "apply")
            ok("Applied latest stash.")
        elif choice == 5:
            idx = ask_input("Stash index (0, 1, ...)", default="0")
            if ask_confirm(f"Drop stash@{{{idx}}}?", default=False):
                git("stash", "drop", f"stash@{{{idx}}}")
                ok(f"Dropped stash@{{{idx}}}.")
    except RuntimeError as e:
        err(str(e))


def action_log():
    """Show recent log."""
    console.print()
    console.print("  [bold]Log[/bold]")
    console.print()

    count = ask_input("How many commits?", default="15")

    try:
        entries = git("log", f"-{count}", "--pretty=format:%h|%ar|%s|%an").strip()
    except RuntimeError as e:
        err(str(e))
        return

    if not entries.strip():
        err("No commits.")
        return

    table = Table(box=box.SIMPLE, padding=(0, 1), show_header=False)
    table.add_column("hash", style="cyan", width=8)
    table.add_column("time", style="dim", width=16)
    table.add_column("msg")
    table.add_column("author", style="dim")

    for line in entries.split("\n"):
        parts = line.split("|", 3)
        if len(parts) == 4:
            table.add_row(parts[0], parts[1], parts[2], parts[3])

    console.print(table)


def action_branch_ops():
    """Branch operations."""
    console.print()
    console.print("  [bold]Branches[/bold]")
    console.print()

    try:
        current = git("branch", "--show-current").strip()
    except RuntimeError as e:
        err(str(e))
        return

    console.print(f"  Current: [cyan]{current}[/cyan]")
    console.print()

    try:
        local = [b.strip() for b in git("branch", "--format=%(refname:short)").strip().split("\n") if b.strip()]
        for b in local:
            marker = "[cyan]*[/cyan]" if b == current else " "
            console.print(f"  {marker} {b}")
    except Exception:
        pass

    console.print()

    choice = ask_choice("", [
        "Switch branch",
        "Create new branch",
        "AI suggest branch name",
        "Delete branch",
        "Cancel",
    ], default=0)

    if choice == -1 or choice == 4:
        return

    if choice == 0:
        try:
            local = [b.strip() for b in git("branch", "--format=%(refname:short)").strip().split("\n") if b.strip()]
            branch_choice = ask_choice("Switch to:", local)
            if 0 <= branch_choice < len(local):
                git("checkout", local[branch_choice])
                ok(f"Switched to {local[branch_choice]}")
        except RuntimeError as e:
            err(str(e))

    elif choice == 1:
        name = ask_input("Branch name")
        if name:
            try:
                git("checkout", "-b", name)
                ok(f"Created and switched to {name}")
            except RuntimeError as e:
                err(str(e))

    elif choice == 2:
        try:
            diff = git("diff", "--cached") or git("show", "--format=", "HEAD")
            if not diff.strip():
                err("No changes to analyze.")
                return
            with console.status("[dim]generating...[/dim]"):
                name = ai("branch", diff).strip()
            console.print(Panel(name, title="suggestion", border_style="green", padding=(0, 2)))
            if ask_confirm("Create this branch?"):
                git("checkout", "-b", name)
                ok(f"Switched to {name}")
        except Exception as e:
            err(str(e))

    elif choice == 3:
        try:
            local = [b.strip() for b in git("branch", "--format=%(refname:short)").strip().split("\n")
                     if b.strip() and b.strip() != current]
            if not local:
                ok("No other branches to delete.")
                return
            del_choice = ask_choice("Delete:", local)
            if 0 <= del_choice < len(local):
                if ask_confirm(f"Delete '{local[del_choice]}'?", default=False):
                    git("branch", "-d", local[del_choice])
                    ok(f"Deleted {local[del_choice]}")
        except RuntimeError as e:
            err(str(e))


def action_diff():
    """View diff."""
    console.print()
    console.print("  [bold]Diff[/bold]")
    console.print()

    choice = ask_choice("View:", [
        "Working directory changes",
        "Staged changes",
        "Last commit diff",
        "Cancel",
    ], default=0)

    if choice == -1 or choice == 3:
        return

    try:
        if choice == 0:
            diff = git("diff")
        elif choice == 1:
            diff = git("diff", "--cached")
        elif choice == 2:
            diff = git("show", "--format=", "HEAD")
    except RuntimeError as e:
        err(str(e))
        return

    if not diff.strip():
        ok("No changes.")
        return

    display = diff[:5000]
    if len(diff) > 5000:
        display += f"\n\n... ({len(diff)} bytes total, truncated)"
    console.print(Syntax(display, "diff", theme="monokai", line_numbers=False))


def action_discard():
    """Discard changes."""
    console.print()
    console.print("  [bold]Discard Changes[/bold]")
    console.print()

    choice = ask_choice("Discard:", [
        "All unstaged changes  (git checkout -- .)",
        "Specific file",
        "All changes + untracked  (git clean -fd + reset)",
        "Cancel",
    ], default=0)

    if choice == -1 or choice == 3:
        return

    if choice == 0:
        if ask_confirm("Discard all unstaged changes? Cannot undo.", default=False):
            try:
                git("checkout", "--", ".")
                ok("Discarded all unstaged changes.")
            except RuntimeError as e:
                err(str(e))
    elif choice == 1:
        filepath = ask_input("File path")
        if filepath:
            if ask_confirm(f"Discard changes in {filepath}?", default=False):
                try:
                    git("checkout", "--", filepath)
                    ok(f"Discarded: {filepath}")
                except RuntimeError as e:
                    err(str(e))
    elif choice == 2:
        if ask_confirm("Discard ALL changes including untracked files? Cannot undo.", default=False):
            try:
                git("reset", "--hard", "HEAD")
                git("clean", "-fd")
                ok("Discarded everything.")
            except RuntimeError as e:
                err(str(e))


def action_remove():
    """Remove files from git tracking."""
    console.print()
    console.print("  [bold]Remove[/bold]")
    console.print()

    choice = ask_choice("Remove mode:", [
        "Delete file from repo and disk",
        "Stop tracking only (keep file on disk)",
        "Cancel",
    ], default=0)

    if choice == -1 or choice == 2:
        return

    filepath = ask_input("File or pattern (e.g. *.log)")
    if not filepath:
        return

    if choice == 0:
        if ask_confirm(f"Delete '{filepath}' from repo AND disk?", default=False):
            try:
                git("rm", filepath)
                ok(f"Removed: {filepath}")
            except RuntimeError as e:
                # Try with -r for directories
                try:
                    git("rm", "-r", filepath)
                    ok(f"Removed: {filepath}")
                except RuntimeError:
                    err(str(e))
    elif choice == 1:
        if ask_confirm(f"Stop tracking '{filepath}'? (file stays on disk)"):
            try:
                git("rm", "--cached", filepath)
                ok(f"Untracked: {filepath}")
            except RuntimeError as e:
                try:
                    git("rm", "--cached", "-r", filepath)
                    ok(f"Untracked: {filepath}")
                except RuntimeError:
                    err(str(e))


# ============================================================================
# AI Operations
# ============================================================================

def action_explain():
    """Explain changes."""
    console.print()
    console.print("  [bold]AI Explain[/bold]")
    console.print()

    scope = ask_choice("What to explain?", [
        "Working directory changes",
        "Staged changes",
        "Specific file",
        "Cancel",
    ], default=0)

    if scope == -1 or scope == 3:
        return

    try:
        if scope == 0:
            diff = git("diff")
        elif scope == 1:
            diff = git("diff", "--cached")
        else:
            filepath = ask_input("File path")
            if not filepath:
                return
            diff = git("diff", filepath)
    except RuntimeError as e:
        err(str(e))
        return

    if not diff.strip():
        err("No changes found.")
        return

    with console.status("[dim]analyzing...[/dim]"):
        try:
            result = ai("explain", diff)
        except Exception as e:
            err(f"AI error: {e}")
            return

    console.print()
    console.print(Panel(result, border_style="dim", padding=(1, 2)))


def action_summarize():
    """Summarize commit history."""
    console.print()
    console.print("  [bold]AI Summarize[/bold]")
    console.print()

    fmt = ask_choice("Format:", [
        "Summary",
        "Changelog (grouped by type)",
        "Release Notes",
        "Cancel",
    ], default=0)

    if fmt == -1 or fmt == 3:
        return

    fmt_key = ["summary", "changelog", "release"][fmt]
    since = ask_input("Since (e.g. '1 week ago', 'v1.0', empty=all)")

    cmd = ["log", "--oneline"]
    if since:
        cmd.append(f"--since={since}")

    try:
        logs = git(*cmd)
    except RuntimeError as e:
        err(str(e))
        return

    if not logs.strip():
        err("No commits found.")
        return

    with console.status("[dim]generating...[/dim]"):
        try:
            result = ai(fmt_key, logs)
        except Exception as e:
            err(f"AI error: {e}")
            return

    console.print()
    console.print(Panel(result, border_style="dim", padding=(1, 2)))


def action_validate():
    """Validate commit messages."""
    console.print()
    console.print("  [bold]Validate Commits[/bold]")
    console.print()

    count = ask_input("How many recent commits?", default="10")

    try:
        logs = git("log", f"--pretty=format:%H|%s", f"-{count}")
    except RuntimeError as e:
        err(str(e))
        return

    if not logs.strip():
        err("No commits found.")
        return

    commits = [
        (h[:8], m) for line in logs.strip().split("\n")
        if "|" in line for h, m in [line.split("|", 1)]
    ]

    valid_types = {"feat", "fix", "docs", "style", "refactor", "test", "chore", "perf", "ci", "build", "revert"}
    invalid = []

    table = Table(box=box.SIMPLE, padding=(0, 2))
    table.add_column("", width=3)
    table.add_column("Hash", style="cyan", width=10)
    table.add_column("Message")
    table.add_column("Issue", style="yellow")

    for h, m in commits:
        issue = ""
        status_icon = "[green]ok[/green]"

        if len(m) > 50:
            issue = "too long"
            status_icon = "[yellow]!![/yellow]"

        if ":" not in m:
            issue = "not conventional"
            status_icon = "[yellow]!![/yellow]"
        else:
            t = m.split(":")[0].split("(")[0].strip()
            if t not in valid_types:
                issue = f"unknown type '{t}'"
                status_icon = "[red]xx[/red]"
                invalid.append((h, m))

        table.add_row(status_icon, h, m, issue)

    console.print()
    console.print(table)

    if invalid and ask_confirm("Suggest AI fixes?"):
        console.print()
        with console.status("[dim]generating fixes...[/dim]"):
            for h, m in invalid[:3]:
                try:
                    fixed = ai("fix_commit", f"Original: {m}")
                    info(f"{h}: {m}  ->  [green]{fixed}[/green]")
                except Exception:
                    pass


def action_ai_stage():
    """AI-assisted staging."""
    console.print()
    console.print("  [bold]AI-Assisted Stage[/bold]")
    console.print()

    try:
        diff = git("diff")
    except RuntimeError as e:
        err(str(e))
        return

    if not diff.strip():
        err("No unstaged changes.")
        return

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

    staged_count = 0

    for i, (filename, chunk) in enumerate(chunks):
        if not chunk.strip():
            continue

        console.print(f"\n  ({i+1}/{len(chunks)}) [cyan]{filename}[/cyan]")

        with console.status("[dim]analyzing...[/dim]"):
            try:
                analysis = ai("analyze_chunk", chunk)
            except Exception:
                analysis = "(could not analyze)"

        console.print(f"    [dim]{analysis}[/dim]")

        choice = ask_choice("", [
            "Stage",
            "Show diff first",
            "Skip",
            "Stop",
        ], default=0)

        if choice == 3 or choice == -1:
            break
        elif choice == 1:
            console.print()
            display = chunk[:2000]
            console.print(Syntax(display, "diff", theme="monokai", line_numbers=False))
            if ask_confirm("Stage?"):
                git("add", filename)
                staged_count += 1
                ok(f"Staged: {filename}")
        elif choice == 0:
            try:
                git("add", filename)
                staged_count += 1
                ok(f"Staged: {filename}")
            except RuntimeError as e:
                err(str(e))

    console.print()
    ok(f"Staged {staged_count} file(s).")

    if staged_count > 0 and ask_confirm("Generate commit message now?"):
        action_commit()


def action_quick_commit():
    """Stage all + AI message + commit."""
    console.print()
    console.print("  [bold]Quick Commit[/bold]  stage all > generate > commit")
    console.print()

    try:
        git("add", "-A")
    except RuntimeError as e:
        err(str(e))
        return

    diff = git("diff", "--cached")
    if not diff.strip():
        err("No changes.")
        return

    ok("All changes staged.")

    with console.status("[dim]generating...[/dim]"):
        try:
            msg = ai("commit_conventional", diff)
        except Exception as e:
            err(f"AI error: {e}")
            return

    console.print(Panel(msg, title="message", border_style="green", padding=(0, 2)))
    console.print()

    if ask_confirm("Commit?"):
        try:
            git("commit", "-m", msg)
            ok(f"Done: {msg}")
        except RuntimeError as e:
            err(str(e))
    else:
        info("Cancelled. Changes still staged.")


def action_graph():
    """Open git graph."""
    console.print()
    console.print("  [bold]Git Graph[/bold]  opening in browser...")
    console.print()

    try:
        from .web_graph import start_server
        start_server(port=8787, limit=100, no_browser=False)
    except Exception as e:
        err(str(e))


def action_clean():
    """Clean merged branches."""
    console.print()
    console.print("  [bold]Clean Branches[/bold]")
    console.print()

    from git import Repo, InvalidGitRepositoryError

    try:
        repo = Repo(".")
    except InvalidGitRepositoryError:
        err("Not a git repository.")
        return

    branches = [b.name for b in repo.branches]
    main = "main" if "main" in branches else ("master" if "master" in branches else None)
    if not main:
        err("No main/master branch found.")
        return

    merged = [
        b.strip().replace("*", "").strip()
        for b in repo.git.branch("--merged", main).split("\n")
    ]
    merged = [b for b in merged if b and b not in {main, "master"} and not b.startswith("(")]

    if not merged:
        ok("No merged branches to clean.")
        return

    console.print(f"  Found {len(merged)} merged branch(es):\n")
    for b in merged:
        console.print(f"    [dim]-[/dim] {b}")

    console.print()
    if ask_confirm(f"Delete {len(merged)} branch(es)?"):
        for b in merged:
            try:
                repo.git.branch("-d", b)
                ok(f"Deleted: {b}")
            except Exception as e:
                err(f"Failed: {b} ({e})")

    if ask_confirm("Also clean remote merged branches?", default=False):
        try:
            remote_merged = repo.git.branch("-r", "--merged", f"origin/{main}").split("\n")
            remote_branches = [
                b.strip().replace("origin/", "") for b in remote_merged
                if b.strip().startswith("origin/") and not b.strip().endswith(f"origin/{main}")
            ]
            remote_branches = [b for b in remote_branches if b not in {main, "master"}]

            if not remote_branches:
                ok("No remote branches to clean.")
            else:
                for b in remote_branches:
                    console.print(f"    [dim]-[/dim] origin/{b}")
                if ask_confirm(f"Delete {len(remote_branches)} remote branch(es)?"):
                    for b in remote_branches:
                        try:
                            repo.git.push("origin", "--delete", b)
                            ok(f"Deleted: origin/{b}")
                        except Exception as e:
                            err(f"Failed: origin/{b} ({e})")
        except Exception:
            pass


def action_settings():
    """Configure settings."""
    console.print()
    console.print("  [bold]Settings[/bold]")
    console.print()

    p = config.get_provider()
    if p:
        console.print(f"  provider     [green]{p.upper()}[/green]")
        console.print(f"  model        [cyan]{config.get_model(p)}[/cyan]")
        console.print(f"  temperature  [cyan]{config.get_temperature()}[/cyan]")
    else:
        console.print("  [yellow]No provider configured.[/yellow]")

    console.print()

    choice = ask_choice("", [
        "Change provider",
        "Change model",
        "Change temperature",
        "Back",
    ], default=0)

    if choice == 0:
        provider_choice = ask_choice("Provider:", [
            "OpenAI  (GPT)",
            "Gemini  (Google)",
            "Claude  (Anthropic)",
            "Ollama  (Local, free)",
        ], default=3)

        providers = ["openai", "gemini", "claude", "ollama"]
        if 0 <= provider_choice < len(providers):
            selected = providers[provider_choice]
            config.setup_provider(selected)
            ok(f"Provider: {selected.upper()}")

    elif choice == 1:
        current = config.get_model(p) if p else ""
        model = ask_input("Model name", default=current)
        if model and p:
            config.set_model(p, model)
            ok(f"Model: {model}")

    elif choice == 2:
        current = str(config.get_temperature())
        temp = ask_input("Temperature (0.0-2.0)", default=current)
        try:
            config.set_temperature(float(temp))
            ok(f"Temperature: {temp}")
        except ValueError:
            err("Invalid number.")


# ============================================================================
# Main Menu & TUI Loop
# ============================================================================

# Menu grouped by workflow phase, each row = (label, action, shortcut_hint)
# Sections: header rows have action=None
MENU_SECTIONS = [
    # Section header, then items as (label, action)
    ("workflow", [
        ("status",    action_status),
        ("diff",      action_diff),
        ("add",       action_stage),
        ("commit",    action_commit),
        ("push",      action_push),
    ]),
    ("more git", [
        ("pull",      action_pull),
        ("unstage",   action_unstage),
        ("amend",     action_amend),
        ("stash",     action_stash),
        ("discard",   action_discard),
        ("remove",    action_remove),
        ("branches",  action_branch_ops),
        ("log",       action_log),
    ]),
    ("ai", [
        ("quick commit", action_quick_commit),
        ("ai explain",   action_explain),
        ("ai summarize", action_summarize),
        ("ai stage",     action_ai_stage),
        ("validate",     action_validate),
    ]),
    ("tools", [
        ("graph",     action_graph),
        ("clean",     action_clean),
        ("settings",  action_settings),
    ]),
]

# Column width for grid layout
_COLS = 4


def _render_menu() -> list:
    """Render menu in grid layout and return flat action_map (index -> action)."""
    action_map = []

    for section_name, items in MENU_SECTIONS:
        console.print(f"  [dim]-- {section_name} --[/dim]")

        table = Table(box=None, show_header=False, padding=(0, 2), expand=False)
        for _ in range(_COLS):
            table.add_column(min_width=18)

        row = []
        for label, action in items:
            idx = len(action_map)
            action_map.append(action)
            cell = f"[dim]{idx + 1:>2}[/dim] {label}"
            row.append(cell)

            if len(row) == _COLS:
                table.add_row(*row)
                row = []

        if row:
            while len(row) < _COLS:
                row.append("")
            table.add_row(*row)

        console.print(table)
        console.print()

    console.print(f"   [dim] 0[/dim] exit")
    return action_map


def run_tui():
    """Main interactive TUI loop."""
    show_banner()

    # Check if provider is configured
    p = config.get_provider()
    if not p:
        console.print()
        console.print("  [yellow]No AI provider configured.[/yellow]")
        console.print("  [dim]Let's set one up...[/dim]")
        action_settings()
        console.print()

    while True:
        console.print()
        action_map = _render_menu()
        console.print()
        console.print("  [dim]#[/dim] ", end="")

        try:
            raw = input().strip()
        except (KeyboardInterrupt, EOFError):
            break

        if raw.lower() in ("q", "quit", "exit", "0"):
            console.print("  [dim]bye[/dim]")
            break

        try:
            idx = int(raw) - 1
            if 0 <= idx < len(action_map):
                try:
                    action_map[idx]()
                except KeyboardInterrupt:
                    console.print("\n  [dim]cancelled[/dim]")
                except Exception as e:
                    err(str(e))
            else:
                err("Invalid choice.")
                continue
        except ValueError:
            err("Enter a number.")
            continue

        # Wait before showing menu again
        console.print()
        console.print("  [dim]Press Enter for menu...[/dim]", end="")
        try:
            input()
        except (KeyboardInterrupt, EOFError):
            break
