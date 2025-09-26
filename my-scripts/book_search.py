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
    """Wrapper to attempt an action and skip if unavailable."""
    try:
        agent.act("Close any pop-ups")
    except Exception:
        pass
    try:
        result = agent.act(action)
        return result
    except Exception as e:
        print(f"Action failed: {action} -> {e}")
        return None

# --- NovaAct Steps ---
with NovaAct(
    starting_page="https://www.barnesandnoble.com/",
    nova_act_api_key=os.getenv("NOVA_ACT_API_KEY")
) as agent:
    try: 
        # Step 1: Search with "in Books"
        print(f"Searching for: {user_data.book} in Books")
        search_query = f"{user_data.book} in Books"
        safe_agent(agent, f"Enter '{search_query}' into the search box and hit Enter")
        
        # Step 2: Filter by author and select first match
        print(f"Looking for first result by author: {user_data.author}")
        safe_agent(agent, f"Locate the first book result where the author is '{user_data.author}' and click it")
    
        # Step 3: Select requested format if available
        print(f"Selecting '{user_data.format}' format")
        safe_agent(agent, f"Select '{user_data.format}' format if available")
    
        # Step 4: Click the "Add to Cart" button
        print("Adding to cart")
        safe_agent(agent, "Scroll until you see 'Add to Cart' and click it")
        
    except Exception as e:
        print(f"Act call failed: {e}")
        agent.page.reload()
    
print("Script finished.")
