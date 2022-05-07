from fastapi import FastAPI
import pandas as pd
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/hello")
def hello():
  return {"Hello world!"}

uri = "https://lilablobssc.blob.core.windows.net/snapshotserengeti-unzipped/"

df = pd.read_csv("animal_df_test_real.csv")
print()

@app.get("/random")
def random():
    url = uri + df.sample()["image_id"].values[0] + ".JPG"
    return url

