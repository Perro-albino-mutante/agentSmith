This is a custom LLM harness that employs models from ollama, giving them the capacity to eecute tools inside of your machine, turning any LLM that supports tools calling into an agent.  
The current tools include:  
- Reading files.  
- Writing files.  
- Editing files.  
- Listing directories.  
- Finding files.  
- Finding patterns in tet.  
- Changing the working directory.  
- Running shell commands.  
- Running python commands.  
- Running commands in a new terminal (kitty by default).  
- Writing to a memory file (~/.agent/memory.tt by default).  
- Reading the memory file.  
  
There is a file called agentconfig.py, inside there are three variables:  
``` python
MODEL = "qwen3:4b-instruct"
TERMINAL = "kitty"
MEMORYFILE = "~/.agent/memory.tet"
```
You can modify any of those variables to your liking.  
 
Requirements:  
-Python  
-Ollama  
-Ollama library for python  
  
Installation:  
Assuming you already have python and ollama installed
``` bash
pip install ollama
ollama pull qwen3:4b-instruct
git clone https://github.com/Perro-albino-mutante/agentSmith.git
```
You can install any model you want as long as it has tool calling capabilities, qwen3:4b-instruct is only an eample.  
