from __future__ import annotations

from nova_act import NovaAct
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
import os

# Load environment variables
load_dotenv()

# --- Pydantic Model ---
class BookRequest(BaseModel):
    book: str = Field(..., description="The title of the book to search for.", min_length=1)
    author: str = Field(..., description="The author of the book.", min_length=1)
    format: Literal["Hardcover", "Paperback", "eBook", "Audiobook", "Special"] = Field(
        ..., description="The format of the book."
    )

# --- Collect and validate user input ---
try:
    user_data = BookRequest(
        book=input("Enter the book title (e.g., The Alchemist): ").strip(),
        author=input("Enter the author name (e.g., Paulo Coelho): ").strip(),
        format=input("Enter the format (e.g., Hardcover, Paperback, eBook): ").strip()
    )
except ValidationError as e:
    print("Invalid input:")
    print(e.json(indent=2))
    exit(1)
    
def safe_agent(agent, action: str):
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

# --- NovaAct Steps ---
with NovaAct(
    starting_page="https://www.barnesandnoble.com/",
    nova_act_api_key=os.getenv("NOVA_ACT_API_KEY"),
    record_video=True,
    nova_act_log_level=os.getenv("NOVA_ACT_LOG_LEVEL")
) as agent:
    
    # Step 1: Search for a book
    print(f"Executing: search for '{user_data.book}' by '{user_data.author}'")
    safe_agent(agent, f"search for '{user_data.book}' by '{user_data.author}'")
    
    # Step 2: Select the first result
    print(f"Selecting first result for '{user_data.book}' by '{user_data.author}'")
    safe_agent(agent, f"select the first result for '{user_data.book}' by '{user_data.author}'")
    
    # Step 3: Select requested format if available
    print(f"Selecting '{user_data.format}' format if available for '{user_data.book}'")
    safe_agent(agent, f"select '{user_data.format}' format if available for '{user_data.book}'")
    
    # Step 4: Click the "Add to Cart" button
    print("Executing: click the 'Add to Cart' button")
    safe_agent(agent, "scroll until you see 'Add to Cart', then click 'Add to Cart'")
    
print("Script finished.")
