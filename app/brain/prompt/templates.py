"""
Prompt templates.
"""


def memory_template(memory: dict) -> str:

    if not memory:
        return ""

    lines = [

        "========== USER PROFILE ==========",

    ]

    for key, value in memory.items():

        key = key.replace("_", " ").title()

        lines.append(f"{key}: {value}")

    lines.append("==============================")

    return "\n".join(lines)