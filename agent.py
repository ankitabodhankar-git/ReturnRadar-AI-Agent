import json

from google.adk.agents import LlmAgent


def get_return_policy() -> str:
    """Retrieves Moolchand Store's return and exchange policy."""

    try:
        with open("policy.json", "r") as f:
            policy_data = json.load(f)
            return json.dumps(policy_data)

    except Exception as e:
        return json.dumps({
            "error": f"Could not retrieve policy: {str(e)}"
        })


return_radar_agent = LlmAgent(
    name="return_radar_agent",
    model="gemini-3.5-flash",
    instruction="""You are ReturnRadar, an AI assistant for Moolchand Store,
a family clothing store selling women's clothing, sarees, men's clothing,
and kids' clothing.

Your job is to answer customer questions about returns and exchanges.

Rules you MUST follow:

1. You MUST use the get_return_policy() tool to retrieve the store policy.
2. Answer ONLY using information returned by the policy.
3. Never invent a return period, exchange period, exception, or requirement.
4. If the customer's situation is not covered by the policy, clearly say that
   they should contact Moolchand Store.
5. Explain the answer clearly and politely.
6. When answering eligibility questions, consider the number of days,
   bill requirement, original tags, item condition, and non-returnable items
   when relevant.
""",
    tools=[get_return_policy]
)


from google.adk.apps import App

app = App(
    name="return_radar_app",
    root_agent=return_radar_agent
)