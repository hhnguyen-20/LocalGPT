# LocalGPT

## Steps to run the app

1. Create and activate a virtual environment

```terminal
python3 -m venv .venv && source .venv/bin/activate
```

2. Install all requirements

```terminal
pip install -r requirements.txt
```

3. Train the model using the `ollama`

```terminal
ollama create <your-model-name> -f Modelfile
```

4. Check and use the created model in the `app.py` file

- Check if the model is created successfully:

```terminal
ollama list
```

- Use the model in the `app.py` file:

```python
model = Ollama(model="<your-model-name>")
```

5. Run the app using `chainlit`

```terminal
chainlit run app.py
```

6. Optional: (Need connecting to the internet) You can create a database named "LocalGPT" to store the user inputs and chat responses on langchain. Rename the file `example.env` to `.env` and add the following environment variables:

```example.env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="<your-api-key>"
LANGCHAIN_PROJECT="LocalGPT"
```
