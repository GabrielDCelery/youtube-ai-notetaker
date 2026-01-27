# YouTube AI Notetaker

There are just so many technical videos on youtube that it takes too much time to watch them. This is a project to analyse those videos and create a `markdown` extract that I can scan through to figure out if it is worth my time.

![screenshot-youtube-ai-notetaker-001](./docs/assets/screenshot-youtube-ai-notetaker-001.jpg)

![screenshot-youtube-ai-notetaker-002](./docs/assets/screenshot-youtube-ai-notetaker-002.jpg)

## What it does

- Downloads YouTube video
- Downloads transcript
- Extracts frames from video
- Sends transcript + frames to LLM exposed via Ollama
- Generates a `.md` file summarizing the video content

## Getting Started

See [docs/setup.md](docs/setup.md) for installation and usage instructions.
