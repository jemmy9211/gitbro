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
    if result.stdout.strip() == "":
        print("No staged changes found. Please use 'git add' to stage your changes first.")
        return None
    return result.stdout

def generate_message(qdiff):
    """Generate a commit message using the Ollama LLM."""
    rsp = chain.invoke({"query_diff": qdiff})
    return rsp

def main():
    """Main function to generate commit message."""
    diff = get_diff()
    if diff is None:
        return 1
    
    try:
        message = generate_message(diff)
        print(message.strip())
        return 0
    except Exception as e:
        print(f"Error generating commit message: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())