from dotenv import load_dotenv
from pydantic import BaseModel
import os
load_dotenv()


class Config(BaseModel):
    github_pat_token : str
    github_username : str
    vercel_token : str
    
config = Config(
    github_pat_token=os.getenv("GITHUB_PAT_TOKEN"),
    github_username=os.getenv("GITHUB_USERNAME"),
    vercel_token=os.getenv("VERCEL_TOKEN")
)
