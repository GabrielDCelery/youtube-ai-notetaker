TRANSCRIPT:
{transcript}

---

Analyze the transcript above and identify ALL distinct topic segments from beginning to end.

Return segments in this format (one per line):
[START - END] Topic name

Example:
[00:00:00 - 00:02:30] Introduction to the topic
[00:02:30 - 00:05:45] Setting up the project
[00:05:45 - 00:12:00] Deep dive into authentication

Rules:

- Use HH:MM:SS format for all timestamps
- First segment MUST start at 00:00:00
- Last segment MUST end at {duration_formatted}
- Segments must be contiguous (no gaps, no overlaps)
- Keep topic names concise (3-6 words)

Return ONLY the segment list below, nothing else:
