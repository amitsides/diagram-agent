from fastapi import FastAPI

app = FastAPI()

@app.post("/diagram")
async def diagram(query: str):  
    from . import DiagramAgent
    DiagramAgent(query)