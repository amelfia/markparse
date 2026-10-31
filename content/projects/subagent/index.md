# Subagent

A command-line coding agent in Python on Google's Gemini API. You give it a task, and it lists, reads, writes and runs files inside one working folder, feeding each result back to the model until it has an answer. [Code on GitHub](https://github.com/amelfia/subagent)

## Why I built it

AI coding tools are everywhere now, and I wanted to understand what actually happens inside one. How does a model decide to read a file? What stops it from writing outside the project? Building Subagent answered both: the agent loop is a model choosing tools and a dispatcher running them, and the boundary is a path check that runs before every file operation.

## How it works

1. You run it with a prompt.
2. The prompt goes to Gemini 2.5 Flash along with a list of four tools.
3. If the model asks for a tool, Subagent runs it and adds the result to the conversation.
4. That repeats until the model answers in plain text, or until 20 turns are used up.

```text
uv run main.py "Read main.py and tell me what it does" --verbose
```

```text
get_files_info     list a folder, with file sizes
get_file_content   read a file (first 10,000 characters)
write_file         write or overwrite a file, creating folders as needed
run_python_file    run a .py file, 30-second timeout, returns stdout, stderr and exit code
```

## Keeping it inside one folder

The model never chooses where it works. A central dispatcher adds the working folder to every tool call and overwrites any folder the model tries to pass in. Each tool then resolves the full path, symlinks included, and rejects anything that isn't inside that folder, so paths like ../ or /etc never reach the filesystem.

That covers file paths, not what a script does once it runs. A Python file the agent runs has the same permissions as me, which is why the README says scripts aren't isolated.

## What was hard

Google's documentation. The agent loop itself is simple once you see it, but working out how the google-genai SDK wants things was a pain: how to describe each tool so the model can call it, and how to hand the result back so the model reads it as the tool's answer. Most of my time went into reading the docs and checking what actually came back.

## Limits

- It only works on the folder set in config.py, which is the sample calculator app by default.
- The tests are scripts that print what each tool returns, not assertions, and there's no CI yet.
- If a call to Gemini fails, it retries, but the failed attempt still uses up one of the 20 turns.
