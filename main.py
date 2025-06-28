import sys
from datetime import date
from loader import load_events
from utils import resolve_event

# Parse CLI arguments (month + year)

def parse_args():
    if len(sys.argv) != 3:
        print("Usage: python main.py <month> <year>")
        sys.exit(1)

    try:
        month = int(sys.argv[1])
        year = int(sys.argv[2])
    except ValueError:
        print("Both month and year must be integers.")
        sys.exit(1)

    if not (1 <= month <= 12):
        print("Month must be between 1 and 12.")
        sys.exit(1)

    if not (1000 <= year <= 9999):
        print("Please use a valid 4-digit year.")
        sys.exit(1)

    return month, year

def main():
    month, year = parse_args()
    events = load_events()

    matching = []
    for ev in events:
        try:
            dt = resolve_event(ev, year)
            if dt.month == month:
                matching.append((dt, ev["name"], ev["category"]))
        except Exception as e:
            print(f"[!] Skipping event: {ev.get('name')} — {e}")

    if not matching:
        print(f"No philosophy-related events found in {month:02}/{year}.")
        return

    # Sort chronologically and display
    matching.sort()
    print(f"Philosophy-related dates for {month:02}/{year}:")
    for dt, name, category in matching:
        print(f"  {dt.strftime('%d %b %Y')} — {name} [{category}]")

if __name__ == "__main__":
    main()
