"""
Temporal Reasoning Demo - GPT-4o-mini (FAILS)

This demonstrates how GPT-4o-mini struggles with temporal reasoning in a savings coach scenario.
The model fails to properly understand the relationship between:
- Time elapsed (6 months into a 12-month goal)
- Progress made ($2,400 saved out of $12,000 target)
- Required future behavior to meet the goal

A proper temporal reasoning model should recognize that the customer needs to save
$9,600 in the remaining 6 months (= $1,600/month), which is 4x their current rate.
"""

import os
import asyncio
from agent_framework.azure import AzureOpenAIResponsesClient
from dotenv import load_dotenv

load_dotenv()

def create_savings_scenario():
    """
    Creates a savings scenario requiring temporal reasoning:
    - Goal: Save $12,000 in 12 months (Jan 1 - Dec 31, 2024)
    - Current date: End of June (6 months elapsed, 6 months remaining)
    - Current savings: $2,400 (averaging $400/month)
    - Required rate: $1,600/month for remaining 6 months to hit goal
    - Customer's planned action: Continue saving $400/month

    The temporal complexity:
    1. Calculate progress relative to timeline (50% time elapsed, only 20% of goal achieved)
    2. Calculate required future savings rate ($9,600 / 6 months = $1,600/month)
    3. Compare to current rate ($400/month)
    4. Realize customer will miss goal by $7,200 if they continue current behavior
    """

    scenario = """
You are a savings coach helping customers achieve their financial goals.

Customer Profile:
- Name: Sarah
- Savings Goal: $12,000 for a dream vacation
- Timeline: 12 months (started January 1, 2024, target: December 31, 2024)
- Today's Date: June 30, 2024

Current Situation:
- Total saved so far: $2,400
- Savings pattern: Sarah has been consistently saving $400 per month
- Months elapsed: 6 months
- Months remaining: 6 months

Sarah's Question:
"Hi! I've been saving $400 every month like clockwork. I'm planning to continue
with the same $400 per month for the rest of the year. Will I reach my $12,000
goal by December 31st? If not, what should I do?"

Please analyze Sarah's situation and provide guidance on whether she'll meet her
goal and what adjustments (if any) she needs to make.
"""
    return scenario

async def get_gpt4o_mini_advice(scenario):
    """Get advice from GPT-4o-mini (expected to fail at temporal reasoning)"""

    # Create agent with GPT-4o-mini deployment
    agent = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name="gpt-4o-mini",  # Using gpt-4o-mini deployment
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    ).create_agent(
        name="savings_coach_mini",
        instructions="You are a helpful savings coach. Analyze the customer's situation carefully and provide accurate financial guidance."
    )

    response = await agent.run(scenario)
    return response

def analyze_advice_quality(advice):
    """Analyze if the advice correctly identifies the temporal reasoning requirements"""

    key_insights = {
        "recognizes_shortfall": False,
        "calculates_required_rate": False,
        "identifies_4x_increase": False,
        "temporal_awareness": False
    }

    advice_lower = advice.lower()

    # Check if it recognizes she'll fall short
    shortfall_keywords = ["won't reach", "will not reach", "fall short", "won't meet", "will not meet", "short", "miss"]
    key_insights["recognizes_shortfall"] = any(keyword in advice_lower for keyword in shortfall_keywords)

    # Check if it calculates the required rate (looking for $1,600 or mentions of needing to save more)
    if "1,600" in advice or "1600" in advice:
        key_insights["calculates_required_rate"] = True

    # Check if it identifies the 4x increase needed
    if "4" in advice and ("times" in advice_lower or "x" in advice_lower):
        key_insights["identifies_4x_increase"] = True

    # Check temporal awareness (mentions time relationship)
    temporal_keywords = ["6 months left", "remaining 6", "half the time", "50% of time", "halfway"]
    key_insights["temporal_awareness"] = any(keyword in advice_lower for keyword in temporal_keywords)

    return key_insights

async def main():
    print("=" * 80)
    print("TEMPORAL REASONING TEST: GPT-4o-mini")
    print("=" * 80)
    print("\nScenario: Savings Coach - Customer Progress Check\n")

    # Create scenario
    scenario = create_savings_scenario()
    print("SCENARIO:")
    print("-" * 80)
    print(scenario)
    print("\n" + "=" * 80)

    # Get advice from GPT-4o-mini
    print("\nQuerying GPT-4o-mini...")
    advice = await get_gpt4o_mini_advice(scenario)

    print("\nGPT-4o-mini RESPONSE:")
    print("-" * 80)
    print(advice)
    print("\n" + "=" * 80)

    # Analyze the advice
    analysis = analyze_advice_quality(advice)

    print("\nANALYSIS OF TEMPORAL REASONING:")
    print("-" * 80)
    print(f"✓ Recognizes shortfall: {analysis['recognizes_shortfall']}")
    print(f"✓ Calculates required rate ($1,600/month): {analysis['calculates_required_rate']}")
    print(f"✓ Identifies 4x increase needed: {analysis['identifies_4x_increase']}")
    print(f"✓ Shows temporal awareness: {analysis['temporal_awareness']}")

    # Overall assessment
    score = sum(analysis.values())
    print(f"\nTemporal Reasoning Score: {score}/4")

    if score < 3:
        print("\n⚠️  RESULT: GPT-4o-mini FAILS at temporal reasoning")
        print("The model likely missed critical temporal relationships:")
        print("- 50% of time elapsed but only 20% of goal achieved")
        print("- Required rate: $1,600/month (4x current rate)")
        print("- If she continues at $400/month, she'll only save $7,200 total (shortfall: $4,800)")
    else:
        print("\n✓ RESULT: GPT-4o-mini shows adequate temporal reasoning")

    print("\n" + "=" * 80)

    # Show the correct calculation
    print("\nCORRECT TEMPORAL REASONING CALCULATION:")
    print("-" * 80)
    print("Time Analysis:")
    print("  • Months elapsed: 6 / 12 (50% of timeline)")
    print("  • Progress: $2,400 / $12,000 (20% of goal)")
    print("  • Gap: Customer is behind schedule (50% time vs 20% progress)")
    print("\nFuture Requirements:")
    print("  • Remaining goal: $12,000 - $2,400 = $9,600")
    print("  • Remaining time: 6 months")
    print("  • Required rate: $9,600 / 6 = $1,600/month")
    print("  • Current rate: $400/month")
    print("  • Increase needed: $1,600 / $400 = 4x current savings rate")
    print("\nProjection if no change:")
    print("  • Future savings: $400/month × 6 months = $2,400")
    print("  • Total by Dec 31: $2,400 + $2,400 = $4,800")
    print("  • Shortfall: $12,000 - $4,800 = $7,200 (60% short of goal!)")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
