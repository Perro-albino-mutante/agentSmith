This is a custom LLM harness that employs models from ollama, giving them the capacity to execute tools inside of your machine, turning any LLM that supports tools calling into an agent.  
The current tools include:  
- [x]Reading files.  
- [x]Writing files.  
- [x]Editing files.  
- [x]Listing directories.  
- [x]Finding files.  
- [x]Finding patterns in text.  
- [x]Changing the working directory.  
- [x]Running shell commands.  
- [x]Running python commands.  
- [x]Running commands in a new terminal (kitty by default).  
- [x]Writing to a memory file ~/.agent/memory.md.  
- [x]Reading the memory file.  
  
There is a file called agentconfig.py there are three variables:  
``` python
MODEL = "qwen3:4b-instruct"
TERMINAL = "kitty"
MEMORYFILE = "~/.agent/memory.text"
```
You can modify any of this variables to your liking.  
 
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
You can install any model you want as long as it has tool calling capabilities, qwen3:4b-instruct is only an example.  
