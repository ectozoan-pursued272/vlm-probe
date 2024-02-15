"""Just dump the model's output text for inspection."""
import json, sys
sys.path.insert(0, ".")

from vlmprobe.model import load_llava, generate
from vlmprobe.tasks import load_task

proc, model = load_llava()
task = load_task(sys.argv[1])
for item in task["items"]:
    out = generate(proc, model, item["image"], item["prompt"])
    print(json.dumps({"image": item["image"], "prompt": item["prompt"],
                      "answer": item["answer"], "pred": out}))
