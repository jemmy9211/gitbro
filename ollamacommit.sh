a#!/bin/bash

# Run Python script to generate the commit message and automatically commit
commit_message=$(python3 - <<END
import subprocess
import requests
import json
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

llm = Ollama(model="phi3.5", base_url="http://localhost:11434")
prompt = ChatPromptTemplate.from_messages([
    ("system", "Your task is to write a concise commit message\
        according a given code di . Your output should only be\
        the commit message with no other information."),
    ("user", "Code Diff: {query_diff} Commit Message:")
])
chain = prompt | llm


def get_git_diff():
    # Get the Git diff of staged changes
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    return result.stdout

def generate_commit_message(diff):
    # Get response from LLM
    rsp = chain.invoke({
        "query_diff": diff
    })
    return rsp

if __name__ == "__main__":
    git_diff = get_git_diff()
    if not git_diff:
        print("No changes staged for commit.")
        exit(1)  # Exit with an error code if there are no staged changes
    else:
        commit_message = generate_commit_message(git_diff)
        print(commit_message)  # Print the commit message to be captured by the shell
END
)

# Check if the commit message was successfully generated
if [ -z "$commit_message" ]; then
    echo "Failed to generate a commit message. Please try again."
    exit 1
fi

# Automatically commit the changes with the generated message
git commit -m "$commit_message"

