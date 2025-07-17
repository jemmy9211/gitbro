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


@cli.command('clean-branches')
@click.option('--remote', '-r', is_flag=True, help='Also delete remote branches (requires confirmation)')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation prompts')
@click.option('--dry-run', '-d', is_flag=True, help='Show what would be deleted without actually deleting')
@click.option('--generate-alias', '-g', is_flag=True, help='Generate shell alias for quick reuse')
def clean_branches(remote, force, dry_run, generate_alias):
    """Clean up local and remote branches that have been merged into main."""
    try:
        repo = Repo('.')
        
        # Ensure we're on main and up to date
        current_branch = repo.active_branch.name
        
        # Check if main branch exists
        if 'main' not in [branch.name for branch in repo.branches]:
            if 'master' in [branch.name for branch in repo.branches]:
                main_branch = 'master'
                click.echo("Using 'master' as the main branch.")
            else:
                click.echo("Error: Neither 'main' nor 'master' branch found.", err=True)
                sys.exit(1)
        else:
            main_branch = 'main'
        
        if current_branch != main_branch:
            if not force and not dry_run:
                if not click.confirm(f"You're currently on '{current_branch}'. Switch to '{main_branch}'?"):
                    click.echo("Aborted.")
                    return
            
            if not dry_run:
                click.echo(f"Switching to {main_branch}...")
                repo.git.checkout(main_branch)
        
        if not dry_run:
            click.echo(f"Updating {main_branch} from origin...")
            try:
                repo.git.pull('origin', main_branch)
            except Exception as e:
                click.echo(f"Warning: Could not pull from origin: {e}")
        
        # Get merged branches (excluding main/master and current branch)
        try:
            merged_output = repo.git.branch('--merged', main_branch)
            merged_branches = []
            
            for line in merged_output.split('\n'):
                branch = line.strip().replace('*', '').strip()
                if branch and branch not in [main_branch, 'master'] and not branch.startswith('('):
                    merged_branches.append(branch)
            
            if not merged_branches:
                click.echo(f"✅ No local branches to clean up! All branches are either unmerged or are the {main_branch} branch.")
            else:
                click.echo(f"\n🔍 Local branches merged into {main_branch}:")
                for branch in merged_branches:
                    click.echo(f"  • {branch}")
                
                if dry_run:
                    click.echo(f"\n[DRY RUN] Would delete {len(merged_branches)} local branch(es)")
                else:
                    if not force:
                        if not click.confirm(f"\nDelete {len(merged_branches)} local branch(es)?"):
                            click.echo("Skipped local branch deletion.")
                        else:
                            for branch in merged_branches:
                                try:
                                    repo.git.branch('-d', branch)
                                    click.echo(f"  ✅ Deleted local branch: {branch}")
                                except Exception as e:
                                    click.echo(f"  ❌ Could not delete {branch}: {e}")
                    else:
                        for branch in merged_branches:
                            try:
                                repo.git.branch('-d', branch)
                                click.echo(f"  ✅ Deleted local branch: {branch}")
                            except Exception as e:
                                click.echo(f"  ❌ Could not delete {branch}: {e}")
        
        except Exception as e:
            click.echo(f"Error getting merged branches: {e}", err=True)
        
        # Handle remote branches
        if remote:
            try:
                remote_merged_output = repo.git.branch('-r', '--merged', f'origin/{main_branch}')
                remote_branches = []
                
                for line in remote_merged_output.split('\n'):
                    branch = line.strip()
                    if branch and not branch.endswith(f'origin/{main_branch}') and branch.startswith('origin/'):
                        branch_name = branch.replace('origin/', '')
                        if branch_name not in [main_branch, 'master']:
                            remote_branches.append(branch_name)
                
                if not remote_branches:
                    click.echo(f"\n✅ No remote branches to clean up!")
                else:
                    click.echo(f"\n🔍 Remote branches merged into origin/{main_branch}:")
                    for branch in remote_branches:
                        click.echo(f"  • origin/{branch}")
                    
                    if dry_run:
                        click.echo(f"\n[DRY RUN] Would delete {len(remote_branches)} remote branch(es)")
                    else:
                        if not force:
                            if click.confirm(f"\nDelete {len(remote_branches)} remote branch(es)?"):
                                for branch in remote_branches:
                                    try:
                                        repo.git.push('origin', '--delete', branch)
                                        click.echo(f"  ✅ Deleted remote branch: origin/{branch}")
                                    except Exception as e:
                                        click.echo(f"  ❌ Could not delete origin/{branch}: {e}")
                            else:
                                click.echo("Skipped remote branch deletion.")
                                click.echo(f"\n💡 You can manually delete remote branches with:")
                                for branch in remote_branches:
                                    click.echo(f"  git push origin --delete {branch}")
                        else:
                            for branch in remote_branches:
                                try:
                                    repo.git.push('origin', '--delete', branch)
                                    click.echo(f"  ✅ Deleted remote branch: origin/{branch}")
                                except Exception as e:
                                    click.echo(f"  ❌ Could not delete origin/{branch}: {e}")
            
            except Exception as e:
                click.echo(f"Error getting remote merged branches: {e}", err=True)
        
        # Generate alias if requested
        if generate_alias:
            _generate_alias()
            
        if not dry_run:
            click.echo(f"\n🎉 Branch cleanup completed!")
        
    except InvalidGitRepositoryError:
        click.echo("Error: Not in a Git repository.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error during branch cleanup: {e}", err=True)
        sys.exit(1)


def _generate_alias():
    """Generate shell alias for the git clean-branches command."""
    click.echo(f"\n📋 Shell Alias Generation")
    click.echo("Add the following alias to your shell configuration (~/.bashrc, ~/.zshrc, etc.):")
    click.echo("")
    
    # Basic alias
    basic_alias = "alias git-clean-branches='ollamacommit clean-branches'"
    click.echo(f"# Basic cleanup alias")
    click.echo(basic_alias)
    click.echo("")
    
    # Advanced alias with options
    advanced_alias = "alias git-clean-all='ollamacommit clean-branches --remote'"
    click.echo(f"# Advanced cleanup (includes remote branches)")
    click.echo(advanced_alias)
    click.echo("")
    
    # Dry run alias
    dry_run_alias = "alias git-clean-preview='ollamacommit clean-branches --dry-run --remote'"
    click.echo(f"# Preview what would be cleaned")
    click.echo(dry_run_alias)
    click.echo("")
    
    click.echo("💡 After adding to your shell config, run: source ~/.bashrc (or ~/.zshrc)")


if __name__ == '__main__':
    cli() 