from routers.books import *

if __name__ == "__main__":
    uvicorn.run("main:app")