import subprocess
import sys # Import sys for stderr
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

class MessageGenerator:
    def __init__(self):
        self.base_temperature = 0.7
        self.temperature_increment = 0.1
        self.max_temperature = 1.0
        self.current_temperature = self.base_temperature
        
    def create_llm(self):
        return OllamaLLM(
            model="llama3.2", 
            base_url="http://localhost:11434",
            temperature=self.current_temperature
        )

    def increase_temperature(self):
        self.current_temperature = min(
            self.current_temperature + self.temperature_increment,
            self.max_temperature
        )
        
    def reset_temperature(self):
        self.current_temperature = self.base_temperature

    def generate_message(self, diff):
        llm = self.create_llm()
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Your task is to write a Git commit message based on the provided code diff. The message should follow standard conventions:\n- Start with a short imperative subject line (e.g., 'Fix bug', 'Add feature').\n- The subject line should be 50 characters or less if possible.\n- Optionally, provide a more detailed explanatory text after the subject line, separated by a blank line.\n- Your output should *only* be the commit message content, with no other surrounding text, titles, or explanations."),
            ("user", "Code Diff: {query_diff} Commit Message:")
        ])
        chain = prompt | llm
        raw_message = chain.invoke({"query_diff": diff})
        if hasattr(raw_message, 'content'): # Handling for AIMessage like objects
            return str(raw_message.content)
        return str(raw_message) # Fallback for direct string output

generator = MessageGenerator()

def get_diff():
    """Get the Git diff of staged changes."""
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing 'git diff --cached': {result.stderr.strip()}", file=sys.stderr)
        return None
    if result.stdout.strip() == "":
        print("No staged changes found. Please use 'git add' to stage your changes first.")
        return None
    return result.stdout

def generate_message(qdiff):
    """Generate a commit message using the Ollama LLM."""
    return generator.generate_message(qdiff)

def increase_creativity():
    """Increase the temperature for next generation."""
    generator.increase_temperature()

def reset_creativity():
    """Reset the temperature to base value."""
    generator.reset_temperature()

def main():
    """Main function to generate commit message."""
    diff = get_diff()
    if diff is None:
        return 1
    
    try:
        message = generate_message(diff) # generate_message now returns a string
        print(message) # Print the raw string
        return 0
    except Exception as e:
        print(f"Error generating commit message: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())