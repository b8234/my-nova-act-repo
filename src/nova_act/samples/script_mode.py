import os
from dotenv import load_dotenv
from nova_act import NovaAct

load_dotenv()

NOVA_ACT = os.getenv("NOVA_ACT_API_KEY")
if not NOVA_ACT:
    raise RuntimeError("Please set the NOVA_ACT_API_KEY environment variable.")

with NovaAct(starting_page="https://nova.amazon.com/act", headless=False, nova_act_api_key=NOVA_ACT) as nova:
    nova.act("Click learn more. Then, return the title and publication date of the blog.")