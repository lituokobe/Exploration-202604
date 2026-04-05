from utils.load_skill import load_skill_md

skills_text = load_skill_md("skills/equity_signal_analyzer.md")

system_prompt = f"""
You are a helpful agent that answers finance related questions.

Available skills:
{skills_text}

Follow the rules strictly.
"""