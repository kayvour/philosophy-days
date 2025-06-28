import yaml
import pathlib

#absolute path to the events.yml file
EVENTS_PATH = pathlib.Path(__file__).parent / "data" / "events.yml"

def load_events() -> list[dict]:
    with open(EVENTS_PATH, "r", encoding="utf-8") as f:
        events = yaml.safe_load(f)

    return events
