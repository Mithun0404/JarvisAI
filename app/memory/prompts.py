MEMORY_EXTRACTION_PROMPT = """
You extract ONLY long-term user facts.

Store ONLY if the user explicitly tells something about themselves.

Examples to STORE:

- My name is Mithun.
- I live in Chennai.
- I like Java.
- I am a student.
- I work at Microsoft.

Examples NOT to store:

- Open Chrome
- Open Notepad
- Hello
- Thanks
- What's my name?
- Launch VS Code
- Search Google

Return ONLY JSON.

If nothing should be stored:

{
    "store": false,
    "facts": {}
}
"""