from nova_act import NovaAct
from datetime import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()

# --- Utility wrapper ---
def safe_act(agent, action: str):
    try:
        agent.act("Close any pop-ups")
    except Exception as e:
        print(f"Optional pop-up close skipped: {e}")
    try:
        result = agent.act(action)
        return result
    except Exception as e:
        print(f"Action failed: {action} -> {e}")
        return None

def normalize_date(raw_date: str) -> str:
    """Normalize Celtics schedule dates to MM-DD-YYYY with dynamic season year."""
    raw_date = raw_date.strip()
    if not raw_date:
        return None

    current_year = datetime.now().year
    target_format = "%m-%d-%Y"

    # Format: "Wed, Oct 30"
    try:
        dt = datetime.strptime(raw_date, "%a, %b %d")
        season_year = current_year if dt.month >= 10 else current_year + 1
        return dt.replace(year=season_year).strftime(target_format)
    except Exception:
        pass

    # Format: "Oct 30, 2025"
    try:
        dt = datetime.strptime(raw_date, "%b %d, %Y")
        return dt.strftime(target_format)
    except Exception:
        pass

    # Format: "October 8"
    try:
        dt = datetime.strptime(raw_date, "%B %d")
        season_year = current_year if dt.month >= 10 else current_year + 1
        dt = dt.replace(year=season_year)
        return dt.strftime(target_format)
    except Exception:
        pass

    # Format: "10/08" (MM/DD)
    try:
        dt = datetime.strptime(raw_date, "%m/%d")
        season_year = current_year if dt.month >= 10 else current_year + 1
        dt = dt.replace(year=season_year)
        return dt.strftime(target_format)
    except Exception:
        pass

    print(f"Date parse failed for: {raw_date}")
    return None

# --- Main extraction ---
def extract_games_on_screen(months=None):
    """
    Extract games visible on the Celtics schedule page filtered by month.
    - months: list of strings (e.g., ["October", "November"])
    """
    with NovaAct(
        starting_page="https://www.nba.com/celtics",
        nova_act_api_key=os.getenv("NOVA_ACT_API_KEY")
    ) as agent:

        # Navigate to schedule
        safe_act(agent, "Click the 'SCHEDULE' tab on the Celtics site")

        # Apply Month filter if given
        if months:
            month_str = "', '".join(months)
            agent.act("Find and click the 'Month' dropdown on the Celtics SCHEDULE page.")
            agent.act(f"Ensure that '{month_str}' is selected in the Month filter. "
                      "Do not unselect any already selected options.")
            agent.act("Close the Month dropdown to update the schedule.")

        # Extract rows
        result = agent.act(
            "Extract all visible schedule rows including date, opponent and time"
        )

        # Unwrap ActResult
        rows = getattr(result, "parsed_response", None)
        if rows is None and hasattr(result, "response"):
            try:
                rows = json.loads(result.response)
            except Exception:
                print("Could not parse ActResult into JSON. Falling back to empty list.")
                rows = []

        if not rows:
            return []

        games = []
        for row in rows:
            raw_date = (row.get("date") or "").strip()
            opponent = (row.get("opponent") or "").strip()
            time = (row.get("time") or "").strip()

            # Skip junk rows
            if not raw_date or raw_date.lower() in ["date", "tbd"]:
                continue
            if not opponent or opponent.lower() in ["opponent", ""]:
                continue

            parsed_date = normalize_date(raw_date)
            if not parsed_date:
                continue

            games.append({
                "date": parsed_date,
                "opponent": opponent,
                "time": time
            })

        # Deduplication
        unique_games = {(g["date"], g["opponent"], g["time"]): g for g in games}
        return list(unique_games.values())

# --- Runner ---
if __name__ == "__main__":
    months_input = input("Enter Month(s), comma-separated (e.g., October, November): ")
    months = [m.strip() for m in months_input.split(",") if m.strip()]

    games = extract_games_on_screen(months)

    for g in games:
        print(g)
