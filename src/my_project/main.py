#!/usr/bin/env python

import sys
import warnings
from pathlib import Path

from my_project.crew import MyProject

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

CASE_FILE = "case.txt"

def load_case():
"""
Load case description from case.txt
"""
case_path = Path(CASE_FILE)

```
if not case_path.exists():
    raise FileNotFoundError(
        f"{CASE_FILE} not found. Create a case.txt file in the project root."
    )

return case_path.read_text(encoding="utf-8")
```

def run():
"""
Run AI Courtroom Simulator
"""
try:
case_text = load_case()

```
    inputs = {
        "case_text": case_text
    }

    result = MyProject().crew().kickoff(inputs=inputs)

    print("\n" + "=" * 70)
    print("AI COURTROOM SIMULATOR")
    print("=" * 70)
    print(result)

except Exception as e:
    raise Exception(f"An error occurred while running the crew: {e}")
```

def train():
try:
case_text = load_case()

```
    MyProject().crew().train(
        n_iterations=int(sys.argv[1]),
        filename=sys.argv[2],
        inputs={"case_text": case_text}
    )

except Exception as e:
    raise Exception(f"An error occurred while training the crew: {e}")
```

def replay():
try:
MyProject().crew().replay(task_id=sys.argv[1])

```
except Exception as e:
    raise Exception(f"An error occurred while replaying the crew: {e}")
```

def test():
try:
case_text = load_case()

```
    MyProject().crew().test(
        n_iterations=int(sys.argv[1]),
        eval_llm=sys.argv[2],
        inputs={"case_text": case_text}
    )

except Exception as e:
    raise Exception(f"An error occurred while testing the crew: {e}")
```

if **name** == "**main**":
run()
