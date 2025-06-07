from fastapi import FastAPI

app = FastAPI(title="ecommerce backend using fastapi")

@app.get("/") # it is a decorater that wraps the function
async def root():
  return {"message":"This is the root path to all the api's"}



