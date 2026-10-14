import ollama, subprocess, os

from agentconfig import MODEL, TERMINAL, MEMORYFILE

# creating memory file if missing
try:
    with open(MEMORYFILE, "r") as memories:
        memories.read()
execpt FileNotFoundError:
    with open(MEMORYFILE, "w") as memories:
        memories.write("")

os.chdir(os.path.expanduser("~/"))

TOOLS = {}

def tool(fn):
    TOOLS[fn.__name__] = fn
    return fn

@tool
def read_file(path: str) -> str:
    """Read a text file and return its contents."""
    os.system(f"notify-send -u low 'Agent is reading:' '{path}'")
    return open(path).read()[:4000]   # cap output size

@tool
def write_file(path: str, text: str) -> str:
    """Write text to a file."""
    os.system(f"notify-send -u low 'Agent is writing to:' '{path}'")
    return subprocess.run(f"echo {text} >> {path}", shell=True, capture_output=True, text=True)

@tool
def edit_file(path:str, line:str, text:str) -> str:
    """Replace a line in a file with a new text."""
    os.system(f"notify-send -u low 'Agent is editing:' '{path}'")
    return subprocess.run(f"sed -i '{line}s/.*/{text}/' {path}", shell=True, capture_output=True, text=True)

@tool
def list_dir(options:str, path:str) -> str:
    """List contents of a specified path, with options."""
    os.system(f"notify-send -u low 'Agent is listing contents of:' '{path}'")
    p = subprocess.run(f"ls {options} {path}", shell=True, capture_output=True, text=True)
    return p.stdout + p.stderr

@tool
def find(path:str, expression:str) -> str:
    """Find a file in a specified path"""
    os.system(f"notify-send -u low 'Agent is finding:' '{expression} at {path}'")
    p = subprocess.run(f"find {path} -name {expression}", shell=True, capture_output=True, text=True)
    return p.stdout[:400] + p.stderr[:400]

@tool
def grep(options:str, pattern:str, path:str) -> str:
    """Find a pattern in a specified file, with options"""
    os.system(f"notify-send -u low 'Agent is greping for:' '{pattern} at {path}'")
    p = subprocess.run(f"grep {options} {pattern} {path}", shell=True, capture_output=True, text=True)
    return p.stdout + p.stderr

@tool
def change_dir(path: str) -> str:
    """Navigate to a different directory"""
    os.system(f"notify-send -u low 'Agent has cwd into' '{path}'")
    return os.chdir(os.path.expanduser(path))

@tool
def run_shell(command: str) -> str:
    """Run a shell command and return its output."""
    subprocess.run(f"notify-send -u normal 'Agent wants to run' '{command}'", shell=True)
    if input(f"Run {command}? (Y/n): ") != "n":
        p = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        print(p.stdout + p.stderr)
        return (p.stdout + p.stderr)[:4000]
    else:
        return print("Operation rejected by the user, check for security issues or wrong command for user request")

@tool
def run_python(command: str) -> str:
    """Run a python command and return its output."""
    os.system(f"notify-send -u normal 'Agent wants to run' '{command}'")
    if input(f"Run {command}? (Y/n): ") != "n":
        p = subprocess.run(f"python3 -m {command}", shell=True, capture_output=True, text=True)
        print(p.stdout + p.stderr)
        return(p.stdout + p.stderr)[:4000]
    else:
        return print("Operation rejected by the user, check for security issues or wrong command for user request")

@tool
def run_in_new_terminal(command: str) -> str:
    """Runs a command in a separate detached terminal."""
    os.system(f"notify-send -u normal 'Agent wants to run' '{command} in a new terminal'")
    if input(f"Run {command} in a new terminal? (Y/n): ") != "n":
        subprocess.Popen([TERMINAL, "bash", "-c", f"{command}; exec bash"], start_new_session=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return print(f"Ran {command}")
    else:
        return print("User rejected execution")

@tool
def remember(text: str) -> str:
    """Writes text to the memory file."""
    os.system(f"notify-send -u low 'Agent is writing to memory' '{text}'")
    p = subprocess.run(f"echo '{text}' >> /home/gv/.agent/memory.txt", shell=True, capture_output=True, text=True)
    return p.stdout + p.stderr

@tool
def recall_memory() -> str:
    """Retrieves the contents of the memory file."""
    os.system(f"notify-send -u low 'Agent is recalling memory'")
    return open("/home/gv/.agent/memory.txt").read()

messages = []

while True:
    user = input(">>> ")
    if user in ("/bye", "/exit"):
        break
    messages.append({"role": "user", "content": user})

    for _ in range(10):   # inner agent loop, one task
        os.system(f"notify-send -u low 'Agent iteration' 'Number {_}'")
        r = ollama.chat(model=f"{MODEL}", messages=messages, think=False, tools=list(TOOLS.values()))
        messages.append(r.message) 
        if not r.message.tool_calls:
            print(r.message.content)
            break
        for call in r.message.tool_calls:
            name = call.function.name
            try:
                result = TOOLS[name](**call.function.arguments)
            except KeyError:
                result = f"error: no tool named {name}"
            except Exception as e:
                result = f"error: {e}"
            messages.append({"role": "tool", "tool_name": name,
                             "content": str(result)})
    else:
        print("(hit iteration cap)")
        os.system("notify-send -u critical 'hit iteration cap'")
