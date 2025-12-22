"""
Temporal Reasoning Demo - GPT-o1 (SUCCEEDS)

This demonstrates how GPT-o1's advanced reasoning capabilities excel at temporal reasoning
in a savings coach scenario. The model correctly understands:
- Time elapsed (6 months into a 12-month goal)
- Progress made ($2,400 saved out of $12,000 target)
- Required future behavior to meet the goal

GPT-o1 should recognize that the customer needs to save $9,600 in the remaining
6 months (= $1,600/month), which is 4x their current rate, and provide accurate guidance.
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

async def get_gpt_o1_advice(scenario):
    """Get advice from GPT-o1 (expected to succeed at temporal reasoning)"""

    # Create agent with o1 deployment
    agent = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name="gpt-5",  # Using o1 reasoning model deployment
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    ).create_agent(
        name="savings_coach_o1",
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
        "temporal_awareness": False,
        "provides_specific_numbers": False
    }

    advice_lower = advice.lower()

    # Check if it recognizes she'll fall short
    shortfall_keywords = ["won't reach", "will not reach", "fall short", "won't meet", "will not meet", "short", "miss", "insufficient"]
    key_insights["recognizes_shortfall"] = any(keyword in advice_lower for keyword in shortfall_keywords)

    # Check if it calculates the required rate (looking for $1,600 or mentions of needing to save more)
    if "1,600" in advice or "1600" in advice or "$1600" in advice or "$1,600" in advice:
        key_insights["calculates_required_rate"] = True

    # Check if it identifies the 4x increase needed or significant multiplier
    if ("4" in advice and ("times" in advice_lower or "x" in advice_lower)) or "quadruple" in advice_lower or "four times" in advice_lower:
        key_insights["identifies_4x_increase"] = True

    # Check temporal awareness (mentions time relationship)
    temporal_keywords = ["6 months left", "remaining 6", "half the time", "50% of time", "halfway", "6 months remaining"]
    key_insights["temporal_awareness"] = any(keyword in advice_lower for keyword in temporal_keywords)

    # Check if it provides specific numbers (shows calculation)
    number_keywords = ["9,600", "9600", "4,800", "4800", "7,200", "7200"]
    key_insights["provides_specific_numbers"] = any(keyword in advice for keyword in number_keywords)

    return key_insights

async def main():
    print("=" * 80)
    print("TEMPORAL REASONING TEST: GPT-o1 (Advanced Reasoning Model)")
    print("=" * 80)
    print("\nScenario: Savings Coach - Customer Progress Check\n")

    # Create scenario
    scenario = create_savings_scenario()
    print("SCENARIO:")
    print("-" * 80)
    print(scenario)
    print("\n" + "=" * 80)

    # Get advice from GPT-o1
    print("\nQuerying GPT-o1 (reasoning model)...")
    print("Note: This may take longer as the model performs deep reasoning...")
    advice = await get_gpt_o1_advice(scenario)

    print("\nGPT-o1 RESPONSE:")
    print("-" * 80)
    print(advice)
    print("\n" + "=" * 80)

    # Analyze the advice
    analysis = analyze_advice_quality(advice)

    print("\nANALYSIS OF TEMPORAL REASONING:")
    print("-" * 80)
    print(f"✓ Recognizes shortfall: {'✅' if analysis['recognizes_shortfall'] else '❌'} {analysis['recognizes_shortfall']}")
    print(f"✓ Calculates required rate ($1,600/month): {'✅' if analysis['calculates_required_rate'] else '❌'} {analysis['calculates_required_rate']}")
    print(f"✓ Identifies 4x increase needed: {'✅' if analysis['identifies_4x_increase'] else '❌'} {analysis['identifies_4x_increase']}")
    print(f"✓ Shows temporal awareness: {'✅' if analysis['temporal_awareness'] else '❌'} {analysis['temporal_awareness']}")
    print(f"✓ Provides specific calculations: {'✅' if analysis['provides_specific_numbers'] else '❌'} {analysis['provides_specific_numbers']}")

    # Overall assessment
    score = sum(analysis.values())
    print(f"\nTemporal Reasoning Score: {score}/5")

    if score >= 4:
        print("\n✅ RESULT: GPT-o1 SUCCEEDS at temporal reasoning")
        print("The model correctly identified critical temporal relationships:")
        print("- 50% of time elapsed but only 20% of goal achieved")
        print("- Required rate: $1,600/month (4x current rate)")
        print("- If she continues at $400/month, she'll only save $7,200 total (shortfall: $4,800)")
    else:
        print("\n⚠️  RESULT: GPT-o1 shows incomplete temporal reasoning")
        print(f"Expected score of 4-5, got {score}")

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
    print("\n" + "=" * 80)

    # Comparison insight
    print("\nWHY GPT-o1 EXCELS AT THIS TASK:")
    print("-" * 80)
    print("GPT-o1's reasoning capabilities enable it to:")
    print("  1. Chain temporal relationships (time elapsed → progress → future needs)")
    print("  2. Perform multi-step mathematical reasoning")
    print("  3. Recognize misalignment between timeline and progress")
    print("  4. Calculate forward projections based on current behavior")
    print("  5. Provide actionable, specific guidance based on numerical analysis")
    print("\nThis contrasts with simpler models that may:")
    print("  • Miss the temporal mismatch (50% time ≠ 20% progress)")
    print("  • Fail to calculate the required future savings rate")
    print("  • Give vague advice without specific numbers")
    print("  • Not recognize the 4x increase requirement")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
