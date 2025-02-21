import subprocess
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

# Configure LLM with local Ollama instance
llm = OllamaLLM(model="llama3.2", base_url="http://localhost:11434")
prompt = ChatPromptTemplate.from_messages([
    ("system", "Your task is to write a concise commit message according to a given code diff. Your output should only be the commit message with no other information."),
    ("user", "Code Diff: {query_diff} Commit Message:")
])
chain = prompt | llm

def get_diff():
    """Get the Git diff of staged changes."""
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    return result.stdout

def generate_message(qdiff):
    """Generate a commit message using the Ollama LLM."""
    rsp = chain.invoke({"query_diff": qdiff})
    return rsp

if __name__ == "__main__":
    git_diff = get_diff()
    if not git_diff:
        print("No changes staged for commit.")
        exit(1)
    else:
        commit_message = generate_message(git_diff)
        print(commit_message)