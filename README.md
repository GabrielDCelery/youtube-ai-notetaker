# What is this project for

There are just so many technical videos on youtube that it takes too much time to watch them. This is a project to analyse those videos and create a `markdown` extract that I can scan through to figure out if it is worth my time.

![screenshot-youtube-ai-notetaker-001](./documentation/screenshot-youtube-ai-notetaker-001.jpg)

![screenshot-youtube-ai-notetaker-002](./documentation/screenshot-youtube-ai-notetaker-002.jpg)

## What it does

- Downloads YouTube video
- Downloads transcript
- Extracts frames from video
- Sends transcript + frames to LLM exposed via Ollama
- generates a `.md` file summarizing the video content

## Requirements

- Have [mise](https://mise.jdx.dev/) installed

## How to run it

The project uses [mise](https://mise.jdx.dev/) to make installing dependencies and running tasks easier. Check the `mise.toml` file to see what dependencies are installed and what scripts are being used. The steps to follow:

1. Install dependencies

```sh
mise install
```

2. Get ollama server running

```sh
ollama serve
ollama pull llava # to analyse the video content
ollama pull llama3.2 # to generate summary with diagrams

# Does not hurt checking if the server is reachable
nc -zv localhost 11434
# Connection to localhost (127.0.0.1) 11434 port [tcp/*] succeeded!
```

3. Package the project and create a CLI command

```sh
uv venv
uv sync
uv pip install .
source .venv/bin/activate

# check if the package was installed and is accessible via your $PATH
which ytainotetaker
```

4. Run it

```sh
ytainotetaker -d downloads -o downloads -H http://10.83.16.99:11434 "https://www.youtube.com/watch?v=pnj3Jbho5Ck" -m full
```
