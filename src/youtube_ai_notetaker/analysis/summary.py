from pathlib import Path

from .ollama import ollama_client

# Load prompts from instruction files
# Navigate up to project root: analysis -> youtube_ai_notetaker -> src -> project_root
INSTRUCTIONS_DIR = Path(__file__).parent.parent / "instructions"
ANALYSIS_PROMPT_TEMPLATE = (INSTRUCTIONS_DIR / "analysis_prompt.md").read_text()
SYSTEM_PROMPT = (INSTRUCTIONS_DIR / "system_prompt.md").read_text()


def generate_summary_with_diagrams(transcript, visual_context="") -> str | None:
    # Load and format the prompt template with actual data
    prompt = ANALYSIS_PROMPT_TEMPLATE.format(
        transcript=transcript, visual_context=visual_context
    )

    response = ollama_client.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response["message"]["content"]
