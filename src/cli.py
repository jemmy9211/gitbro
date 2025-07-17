#!/usr/bin/env python3
"""
AI-Powered Git CLI Tool
Main CLI entry point with multiple subcommands for Git workflow enhancement.
"""

import click
import sys
import subprocess
from pathlib import Path
from typing import Optional, List
import git
from git import Repo, InvalidGitRepositoryError

from config import config
from generate_message import MessageGenerator
from providers import get_provider


@click.group()
@click.version_option(version="2.0.0", prog_name="ollamacommit")
@click.pass_context
def cli(ctx):
    """AI-Powered Git CLI Tool for enhanced developer workflow."""
    # Ensure we're in a git repository for most commands
    if ctx.invoked_subcommand not in ['install-hook']:
        try:
            repo = Repo('.')
        except InvalidGitRepositoryError:
            click.echo("Error: Not in a Git repository.", err=True)
            sys.exit(1)


@cli.command()
@click.option('--temperature', '-t', type=float, help='Temperature for AI creativity (0.0-2.0)')
@click.option('--auto', '-a', is_flag=True, help='Auto-commit with generated message')
@click.option('--conventional', '-c', is_flag=True, help='Use Conventional Commits format')
def commit(temperature, auto, conventional):
    """Generate AI-powered commit message from staged changes."""
    try:
        # Check if there are staged changes
        result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
        if result.returncode != 0:
            click.echo(f"Error getting staged changes: {result.stderr.strip()}", err=True)
            sys.exit(1)
        
        if not result.stdout.strip():
            click.echo("No staged changes found. Please use 'git add' to stage your changes first.")
            sys.exit(1)
        
        # Set temperature if provided
        generator = MessageGenerator()
        if temperature is not None:
            config.set_temperature(temperature)
        
        # Generate commit message
        provider = get_provider()
        if not provider:
            click.echo("No AI provider configured. Run 'ollamacommit setup' first.", err=True)
            sys.exit(1)
        
        if conventional:
            # Modify the prompt for conventional commits
            original_prompt = provider._get_system_prompt()
            provider._system_prompt_override = (
                "Generate a commit message following Conventional Commits format. "
                "Use format: type(scope): description. "
                "Types: feat, fix, docs, style, refactor, test, chore. "
                "Keep description concise and imperative. "
                "Output only the commit message, no explanations."
            )
        
        commit_message = generator.generate_message(result.stdout)
        
        if auto:
            # Auto-commit with generated message
            commit_result = subprocess.run(
                ["git", "commit", "-m", commit_message], 
                capture_output=True, text=True
            )
            if commit_result.returncode == 0:
                click.echo(f"✅ Committed with message: {commit_message}")
            else:
                click.echo(f"Error committing: {commit_result.stderr.strip()}", err=True)
        else:
            click.echo(f"Suggested commit message:\n{commit_message}")
            if click.confirm("Do you want to commit with this message?"):
                subprocess.run(["git", "commit", "-m", commit_message])
    
    except Exception as e:
        click.echo(f"Error generating commit message: {str(e)}", err=True)
        sys.exit(1)


@cli.command('branch-suggest')
@click.option('--create', '-c', is_flag=True, help='Auto-create the suggested branch')
@click.option('--from-commit', type=str, help='Generate name from specific commit hash')
def branch_suggest(create, from_commit):
    """Suggest semantic branch name based on changes."""
    try:
        if from_commit:
            # Get diff from specific commit
            result = subprocess.run(
                ["git", "show", "--format=", from_commit], 
                capture_output=True, text=True
            )
        else:
            # Get diff from staged changes or latest commit
            result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
            if not result.stdout.strip():
                # No staged changes, use latest commit
                result = subprocess.run(["git", "show", "--format=", "HEAD"], capture_output=True, text=True)
        
        if result.returncode != 0:
            click.echo(f"Error getting changes: {result.stderr.strip()}", err=True)
            sys.exit(1)
        
        if not result.stdout.strip():
            click.echo("No changes found to analyze.")
            sys.exit(1)
        
        provider = get_provider()
        if not provider:
            click.echo("No AI provider configured. Run 'ollamacommit setup' first.", err=True)
            sys.exit(1)
        
        # Override system prompt for branch naming
        provider._system_prompt_override = (
            "Analyze the code changes and suggest a semantic branch name. "
            "Follow the format: type/short-description (e.g., feat/add-login, fix/api-timeout). "
            "Types: feat, fix, refactor, docs, test, chore, hotfix. "
            "Keep description short (2-4 words), use kebab-case. "
            "Output only the branch name, no explanations."
        )
        
        branch_name = provider.generate_message(result.stdout).strip()
        
        click.echo(f"Suggested branch name: {branch_name}")
        
        if create:
            if click.confirm("Create this branch?"):
                subprocess.run(["git", "checkout", "-b", branch_name])
                click.echo(f"✅ Created and switched to branch: {branch_name}")
        
    except Exception as e:
        click.echo(f"Error suggesting branch name: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--staged', '-s', is_flag=True, help='Explain staged changes only')
@click.option('--file', '-f', type=str, help='Explain changes in specific file')
def explain(staged, file):
    """Generate human-friendly explanation of code changes."""
    try:
        if file:
            # Explain changes in specific file
            result = subprocess.run(
                ["git", "diff", file], capture_output=True, text=True
            )
        elif staged:
            # Explain staged changes
            result = subprocess.run(
                ["git", "diff", "--cached"], capture_output=True, text=True
            )
        else:
            # Explain working directory changes
            result = subprocess.run(
                ["git", "diff"], capture_output=True, text=True
            )
        
        if result.returncode != 0:
            click.echo(f"Error getting diff: {result.stderr.strip()}", err=True)
            sys.exit(1)
        
        if not result.stdout.strip():
            click.echo("No changes found to explain.")
            return
        
        provider = get_provider()
        if not provider:
            click.echo("No AI provider configured. Run 'ollamacommit setup' first.", err=True)
            sys.exit(1)
        
        # Override system prompt for explanation
        provider._system_prompt_override = (
            "Explain the code changes in plain English. "
            "Describe what was changed, added, or removed. "
            "Focus on the functionality and purpose of the changes. "
            "Be concise but comprehensive. Use bullet points for multiple changes. "
            "Avoid technical jargon when possible."
        )
        
        explanation = provider.generate_message(result.stdout)
        click.echo("📝 Change Explanation:")
        click.echo(explanation)
        
    except Exception as e:
        click.echo(f"Error explaining changes: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--since', type=str, help='Summarize commits since date/commit (e.g., "1 week ago", commit hash)')
@click.option('--author', type=str, help='Filter by author')
@click.option('--branch', type=str, help='Summarize specific branch (default: current)')
@click.option('--format', type=click.Choice(['changelog', 'release-notes', 'summary']), default='summary', help='Output format')
def summarize(since, author, branch, format):
    """Generate human-readable summary of commit history."""
    try:
        # Build git log command
        cmd = ["git", "log", "--oneline"]
        
        if since:
            cmd.extend([f"--since={since}"])
        if author:
            cmd.extend([f"--author={author}"])
        if branch:
            cmd.append(branch)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            click.echo(f"Error getting commit history: {result.stderr.strip()}", err=True)
            sys.exit(1)
        
        if not result.stdout.strip():
            click.echo("No commits found for the specified criteria.")
            return
        
        provider = get_provider()
        if not provider:
            click.echo("No AI provider configured. Run 'ollamacommit setup' first.", err=True)
            sys.exit(1)
        
        # Override system prompt based on format
        if format == 'changelog':
            prompt = (
                "Create a changelog from these commit messages. "
                "Group by type (Features, Bug Fixes, Improvements, etc.). "
                "Use markdown formatting with bullet points. "
                "Be concise but informative."
            )
        elif format == 'release-notes':
            prompt = (
                "Create release notes from these commit messages. "
                "Highlight major features, breaking changes, and important fixes. "
                "Use professional tone suitable for end users. "
                "Structure with clear sections."
            )
        else:  # summary
            prompt = (
                "Summarize this commit history in a few paragraphs. "
                "Highlight the main themes and changes. "
                "Be concise but capture the overall development activity."
            )
        
        provider._system_prompt_override = prompt
        
        summary = provider.generate_message(result.stdout)
        click.echo(f"📊 Commit History {format.title()}:")
        click.echo(summary)
        
    except Exception as e:
        click.echo(f"Error summarizing commits: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--range', type=str, help='Validate specific commit range (e.g., HEAD~5..HEAD)')
@click.option('--fix', is_flag=True, help='Suggest improved messages for invalid commits')
@click.option('--conventional', is_flag=True, help='Validate against Conventional Commits format')
def validate(range, fix, conventional):
    """Validate commit message formats and conventions."""
    try:
        # Build git log command
        if range:
            cmd = ["git", "log", "--pretty=format:%H|%s", range]
        else:
            cmd = ["git", "log", "--pretty=format:%H|%s", "-10"]  # Last 10 commits
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            click.echo(f"Error getting commits: {result.stderr.strip()}", err=True)
            sys.exit(1)
        
        if not result.stdout.strip():
            click.echo("No commits found.")
            return
        
        commits = []
        for line in result.stdout.strip().split('\n'):
            if '|' in line:
                hash_part, message = line.split('|', 1)
                commits.append((hash_part[:8], message))
        
        if conventional:
            # Validate against Conventional Commits
            valid_types = ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore', 'perf', 'ci', 'build', 'revert']
            invalid_commits = []
            
            for commit_hash, message in commits:
                # Check if message follows conventional format
                if ':' not in message:
                    invalid_commits.append((commit_hash, message, "Missing type and colon"))
                else:
                    type_part = message.split(':')[0].strip()
                    if '(' in type_part:
                        type_part = type_part.split('(')[0]
                    
                    if type_part not in valid_types:
                        invalid_commits.append((commit_hash, message, f"Invalid type '{type_part}'"))
            
            if invalid_commits:
                click.echo("❌ Invalid commit messages found:")
                for commit_hash, message, reason in invalid_commits:
                    click.echo(f"  {commit_hash}: {message}")
                    click.echo(f"    Issue: {reason}")
                
                if fix:
                    provider = get_provider()
                    if provider:
                        click.echo("\n🔧 Suggested improvements:")
                        provider._system_prompt_override = (
                            "Fix this commit message to follow Conventional Commits format. "
                            "Use format: type(scope): description. "
                            "Types: feat, fix, docs, style, refactor, test, chore. "
                            "Output only the improved commit message."
                        )
                        
                        for commit_hash, message, _ in invalid_commits[:3]:  # Limit to 3
                            improved = provider.generate_message(f"Original: {message}")
                            click.echo(f"  {commit_hash}: {improved}")
            else:
                click.echo("✅ All commits follow Conventional Commits format!")
        else:
            # General validation
            click.echo("📋 Commit Messages:")
            for commit_hash, message in commits:
                status = "✅" if len(message) <= 50 else "⚠️"
                click.echo(f"  {status} {commit_hash}: {message}")
                if len(message) > 50:
                    click.echo(f"     (Message too long: {len(message)} chars)")
        
    except Exception as e:
        click.echo(f"Error validating commits: {str(e)}", err=True)
        sys.exit(1)


@cli.command('interactive-add')
def interactive_add():
    """AI-assisted interactive staging of changes."""
    try:
        # Get unstaged changes
        result = subprocess.run(["git", "diff"], capture_output=True, text=True)
        
        if result.returncode != 0:
            click.echo(f"Error getting changes: {result.stderr.strip()}", err=True)
            sys.exit(1)
        
        if not result.stdout.strip():
            click.echo("No unstaged changes found.")
            return
        
        provider = get_provider()
        if not provider:
            click.echo("No AI provider configured. Run 'ollamacommit setup' first.", err=True)
            sys.exit(1)
        
        # Split diff into chunks (simplified approach)
        diff_lines = result.stdout.split('\n')
        current_file = None
        chunks = []
        current_chunk = []
        
        for line in diff_lines:
            if line.startswith('diff --git'):
                if current_chunk:
                    chunks.append((current_file, '\n'.join(current_chunk)))
                    current_chunk = []
                current_file = line.split('b/')[-1] if 'b/' in line else "unknown"
            current_chunk.append(line)
        
        if current_chunk:
            chunks.append((current_file, '\n'.join(current_chunk)))
        
        click.echo("🤖 AI-Assisted Interactive Add")
        click.echo("Analyzing changes and providing recommendations...\n")
        
        for filename, chunk_diff in chunks:
            if not chunk_diff.strip():
                continue
            
            # Get AI explanation of the chunk
            provider._system_prompt_override = (
                "Briefly explain what this code change does. "
                "Is it a bug fix, new feature, refactoring, or cleanup? "
                "Should it be staged? Give a one-sentence recommendation. "
                "Format: 'EXPLANATION - RECOMMENDATION (Yes/No/Maybe)'"
            )
            
            analysis = provider.generate_message(chunk_diff)
            
            click.echo(f"📁 File: {filename}")
            click.echo(f"🧠 AI Analysis: {analysis}")
            
            choice = click.prompt(
                "Stage this change? [y/n/s(how diff)/q(uit)]", 
                type=click.Choice(['y', 'n', 's', 'q']), 
                default='y'
            )
            
            if choice == 'q':
                break
            elif choice == 's':
                click.echo(chunk_diff)
                choice = click.prompt("Stage this change? [y/n]", type=click.Choice(['y', 'n']))
            
            if choice == 'y':
                subprocess.run(["git", "add", filename])
                click.echo(f"✅ Staged {filename}")
            
            click.echo()
        
    except Exception as e:
        click.echo(f"Error in interactive add: {str(e)}", err=True)
        sys.exit(1)


@cli.command('install-hook')
@click.option('--uninstall', is_flag=True, help='Remove the pre-commit hook')
def install_hook(uninstall):
    """Install or remove Git pre-commit hook for auto-validation."""
    try:
        repo = Repo('.')
        hooks_dir = Path(repo.git_dir) / 'hooks'
        hook_file = hooks_dir / 'pre-commit'
        
        if uninstall:
            if hook_file.exists():
                hook_file.unlink()
                click.echo("✅ Pre-commit hook removed.")
            else:
                click.echo("No pre-commit hook found.")
            return
        
        # Create hook script
        hook_content = f'''#!/bin/bash
# ollamacommit pre-commit hook

# Check if there are staged changes
if git diff --cached --quiet; then
    exit 0
fi

echo "🤖 Running ollamacommit validation..."

# Run commit message validation
{sys.executable} -c "
import sys
sys.path.insert(0, '{Path(__file__).parent.parent / "src"}')
from cli import cli
sys.argv = ['ollamacommit', 'validate', '--range', 'HEAD~1..HEAD', '--conventional']
cli()
"

# If validation fails, offer to generate commit message
if [ $? -ne 0 ]; then
    echo "Would you like to generate a commit message? (y/n)"
    read -r response
    if [ "$response" = "y" ]; then
        {sys.executable} -c "
import sys
sys.path.insert(0, '{Path(__file__).parent.parent / "src"}')
from cli import cli
sys.argv = ['ollamacommit', 'commit']
cli()
"
    fi
fi
'''
        
        hooks_dir.mkdir(exist_ok=True)
        hook_file.write_text(hook_content)
        hook_file.chmod(0o755)
        
        click.echo("✅ Pre-commit hook installed successfully!")
        click.echo("The hook will validate commit messages and offer AI suggestions.")
        
    except Exception as e:
        click.echo(f"Error installing hook: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('provider', type=click.Choice(['openai', 'gemini', 'claude', 'ollama']), required=False)
def setup(provider):
    """Set up AI provider configuration."""
    # Import the original setup functionality
    from generate_message import main as original_main
    
    if provider:
        sys.argv = ['ollamacommit', '--setup', provider]
    else:
        sys.argv = ['ollamacommit', '--setup']
    
    original_main()


@cli.command()
def status():
    """Show current provider configuration status."""
    provider = config.get_provider()
    if provider:
        click.echo(f"Current provider: {provider}")
        click.echo(f"Temperature: {config.get_temperature()}")
        model = config.get_model(provider)
        if model:
            click.echo(f"Model: {model}")
    else:
        click.echo("No provider configured.")


if __name__ == '__main__':
    cli() 