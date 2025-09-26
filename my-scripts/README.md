# Nova Act Sample Scripts

This repo contains sample scripts I created to explore **Amazon Nova Act** and demonstrate how agents can automate real-world tasks on websites. Each script is a small, focused example of applying Nova Act to a different use case.

---

## Scripts

### `celtics_month.py`
Extracts Boston Celtics games for specific month(s). Handles pop-ups, applies filters, and normalizes messy dates into a consistent format.

- **Why it matters**: Shows how Nova Act can work with dynamic sports schedules and maintain extraction accuracy.  
- **What I learned**: The importance of data normalization (e.g., turning `"Wed, Oct 30"` into `MM-DD-YYYY`).  
- **Future enhancement**: Export results into JSON for easier sharing and analysis, and extend functionality to select a specific game and initiate ticket purchase.  

---

### `book_search.py`
Searches for a book on Barnes & Noble by title and selects the first result by a specific author. Handles closing pop-ups.

- **Why it matters**: Demonstrates search, filtering, and element selection in a real e-commerce flow.  
- **What I learned**: How to combine user input (book, author, format) with Nova Act actions while accounting for unexpected site behaviors like pop-ups.  
- **Future enhancement**: Expand to scrape book details (price, formats, ratings). Improve handling of the “location pop-up,” though this can also be resolved with human input without breaking the script.  

---

### `parallel.py`
Runs multiple Nova Act tasks in parallel, such as checking weather for multiple cities, with the headless browser parameter set to `True`.

- **Why it matters**: Demonstrates that Nova Act can scale across concurrent tasks, not just one at a time.  
- **What I learned**: How to manage concurrency with Nova Act and configure scripts to run in headless mode.  
- **Future enhancement**: Add analysis for comparing weather results and generate a graphical chart for visualization.  

---

## Next Steps

This repo is a starting point. I plan to add more scripts that show:

- Automating data extraction from other domains (e.g., news, finance, retail).  
- Handling more complex interactions like multi-step forms.  
- Integrating results with APIs or databases.  
- Scaling Nova Act using **AgentCore** within AWS.  
