# What is this

There are just so many technical videos on youtube that it takes too much time to watch them. This is a project to analyse those videos and create a `markdown` extract that I can scan through to figure out if it is worth my time.

# What the repo does

## Requirements

- Have [mise](https://mise.jdx.dev/) installed

## How to run it

The project uses [mise](https://mise.jdx.dev/) to make installing dependencies and running tasks easier. Check the `mise.toml` file to see what dependencies are installed and what scripts are being used. The steps to follow:

```sh
mise install
uv venv
uv sync
```

Then have a server running ollama and pull the models that the code uses.

```sh
ollama serve
ollama pull llava # to analyse the video content
ollama pull llama3.2 # to generate summary with diagrams

# Does not hurt checking if the connection is up
nc -zv localhost 11434
# Connection to localhost (127.0.0.1) 11434 port [tcp/*] succeeded!
```

Run the analysis against a youtube video.

```sh
uv run main.py "https://www.youtube.com/watch?v=lvCZk3k4-34"
```

![screenshot-youtube-ai-notetaker-001]("./documentation/screenshot-youtube-ai-notetaker-001.jpg")
