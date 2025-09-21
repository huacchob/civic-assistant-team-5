"""Main Gradio app for the MAREA project."""

import gradio as gr
from fastapi import FastAPI

from ui_server.api import app
from ui_server.chat import create_interface

# Mount the Gradio interface to FastAPI
demo: gr.Blocks = create_interface()
app: FastAPI = gr.mount_gradio_app(app=app, blocks=demo, path="/")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=8000)
