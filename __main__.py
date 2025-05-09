import uvicorn
import os

if __name__ == "__main__":
    kwargs = {}
    if os.path.exists(".env"):
        kwargs["env_file"] = ".env"
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, **kwargs)
