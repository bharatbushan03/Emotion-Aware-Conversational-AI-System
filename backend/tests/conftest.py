import os

# Importing the app starts a background model download unless this is set.
os.environ["SKIP_MODEL_WARMUP"] = "1"
