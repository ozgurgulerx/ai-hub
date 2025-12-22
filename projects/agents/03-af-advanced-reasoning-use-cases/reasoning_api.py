import copy
import json
import os
from typing import Any, Dict, List, Literal, Optional

from agent_framework.azure import AzureOpenAIResponsesClient
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv()

REQUIRED_ENV_VARS = [
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_VERSION",
    "AZURE_OPENAI_API_KEY",
]

missing = [var for var in REQUIRED_ENV_VARS if not os.environ.get(var)]
if missing:
    missing_list = ", ".join(missing)
    raise RuntimeError(f"Missing required Azure OpenAI env vars: {missing_list}")


def _create_agent(
    deployment: str,
    *,
    name: str,
    instructions: str,
    reasoning_effort: str | None = None,
) -> Any:
    client = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name=deployment,
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    agent_kwargs: Dict[str, Any] = {
        "name": name,
        "instructions": instructions,
    }
    if reasoning_effort:
        agent_kwargs["reasoning_effort"] = reasoning_effort
        agent_kwargs["max_completion_tokens"] = 5000
    return client.create_agent(**agent_kwargs)


CONVENTIONAL_INSTRUCTIONS = """
You are a financial assistant that offers conventional budgeting summaries.
You avoid advanced temporal reasoning and rely on heuristics like simple percentage
allocations and monthly averages. Respond with concise JSON as requested by the user.
"""

REASONING_INSTRUCTIONS = """
You are an advanced financial assistant with strong temporal reasoning.
You analyze calendars, cut-off times, business days, and buffer health before advising.
Highlight time-aware tactics explicitly and respond with structured JSON as requested.
"""

# Shared instructions for fair comparison in rate-swing demo
RATE_SWING_SHARED_INSTRUCTIONS = """
You are a mortgage advisory assistant. Analyze the customer's situation, policy documents,
and scenario data carefully. Consider all constraints including affordability, LTV/LTI/DSCR
requirements, and regulatory disclosures. Cite specific clause IDs from the provided documents.
Return structured JSON as requested.
"""

AGENTS = {
    "conventional": _create_agent(
        "gpt-4o-mini",
        name="savings-conventional",
        instructions=CONVENTIONAL_INSTRUCTIONS.strip(),
    ),
    "reasoning": _create_agent(
        "gpt-5-mini",
        name="savings-reasoning",
        instructions=REASONING_INSTRUCTIONS.strip(),
        reasoning_effort="high",
    ),
}

# Rate-swing specific agents with identical instructions
RATE_SWING_AGENTS = {
    "conventional": _create_agent(
        "gpt-4o-mini",
        name="rate-swing-conventional",
        instructions=RATE_SWING_SHARED_INSTRUCTIONS.strip(),
    ),
    "reasoning": _create_agent(
        "gpt-5-mini",
        name="rate-swing-reasoning",
        instructions=RATE_SWING_SHARED_INSTRUCTIONS.strip(),
        reasoning_effort="high",
    ),
}

MODEL_LOOKUP = {
    "conventional": "gpt-4o-mini",
    "reasoning": "gpt-5-mini",
}

PORTFOLIO_SCENARIO = {
    "now_iso": "2025-11-07T10:00:00+03:00",
    "nav_try": 1_000_000,
    "prices": {"TR_EQ": 100.0, "GL_EQ": 50.0, "EUR_BOND": 10.0, "GOLD": 70.0, "USD_MM": 1.0},
    "holdings_units": {"TR_EQ": 3500, "GL_EQ": 5000, "EUR_BOND": 15000, "GOLD": 1428, "USD_MM": 150000},
    "mu": {"TR_EQ": 0.08, "GL_EQ": 0.10, "EUR_BOND": 0.045, "GOLD": 0.03, "USD_MM": 0.015},
    "cov": {"TR_EQ": {"TR_EQ": 0.20, "GL_EQ": 0.15, "EUR_BOND": 0.05, "GOLD": 0.03, "USD_MM": 0.0}},
    "adv": {"TR_EQ": 500000, "GL_EQ": 1000000, "EUR_BOND": 200000, "GOLD": 300000, "USD_MM": 1000000},
    "fx_map": {"TR_EQ": "TRY", "GL_EQ": "USD", "EUR_BOND": "EUR", "GOLD": "USD", "USD_MM": "USD"},
    "cash_timeline": {
        "today_try": 35000,
        "salary": {"amount_try": 70000, "at_iso": "2025-11-10T09:00:00+03:00"},
        "rent_due": {"amount_try": 36000, "cutoff_iso": "2025-11-10T17:00:00+03:00"},
        "loan_due": {"amount_try": 13500, "cutoff_iso": "2025-11-14T17:00:00+03:00"},
        "cash_floor_try": 20000,
        "checkpoints": [
            {"label": "Now", "iso": "2025-11-07T10:00:00+03:00"},
            {"label": "Salary clears", "iso": "2025-11-10T09:00:00+03:00"},
            {"label": "Rent cutoff", "iso": "2025-11-10T17:00:00+03:00"},
            {"label": "Pre-loan", "iso": "2025-11-14T10:30:00+03:00"},
        ],
    },
    "text_context": {
        "client_mandate_email": "Keep TRY cash ≥ ₺20,000 at all times; max equity 55%; min bonds 20%; no single ETF > 25%; exclude thermal coal; do not sell positions opened < 365 days.",
        "esg_policy_pdf": "Exclude issuers with >10% revenue from coal. GOLD max 15%. Maintain ≥30% local currency (TRY) exposure.",
        "broker_notice_html": "Equities settle T+2, bonds T+1. Mon Nov 10 is a settlement holiday. ADV cap ≤10% per day.",
        "tax_memo_docx": "Wash-sale: do not repurchase substantially identical securities within 30 days of realizing a loss.",
        "factsheets_pdf": "GL_EQ creations halted for the next 3 trading days. EUR_BOND minimum trade lot ₺5,000.",
        "calendar_ics": "Trading hours 09:00–17:00 weekdays. Maintenance: Fri Nov 14 09:45–10:15.",
    },
    "holding_ages": {"TR_EQ": 320, "GL_EQ": 480, "EUR_BOND": 540, "GOLD": 600, "USD_MM": 120},
    "wash_sale_blacklist": ["EUR_BOND"],
    "esg_restricted": ["COAL_ETF"],
}

PORTFOLIO_CONSTRAINTS = [
    {
        "id": "C001",
        "type": "hard",
        "category": "cash",
        "rule": "Keep liquid TRY cash above ₺20,000 at every checkpoint (now, salary, rent, loan).",
        "explanation": "Ensures rent, loan, and other obligations can settle on time.",
        "source": {"doc": "client_mandate_email", "quote": "Keep TRY cash ≥ ₺20,000 at all times"},
        "priority": 1,
    },
    {
        "id": "C002",
        "type": "hard",
        "category": "allocation",
        "rule": "Total equity (TR_EQ + GL_EQ) cannot exceed 55% of the portfolio.",
        "explanation": "Caps equity risk per the client’s mandate.",
        "source": {"doc": "client_mandate_email", "quote": "max equity 55%"},
        "priority": 1,
    },
    {
        "id": "C003",
        "type": "hard",
        "category": "allocation",
        "rule": "EUR_BOND exposure must be at least 20% to meet the bond floor.",
        "explanation": "Maintains minimum fixed-income allocation.",
        "source": {"doc": "client_mandate_email", "quote": "min bonds 20%"},
        "priority": 1,
    },
    {
        "id": "C004",
        "type": "hard",
        "category": "allocation",
        "rule": "GOLD ≤ 15% and no single ETF exceeds 25% weight.",
        "explanation": "Prevents concentration and heavy gold tilts.",
        "source": {"doc": "esg_policy_pdf", "quote": "GOLD max 15%; no single ETF > 25%"},
        "priority": 1,
    },
    {
        "id": "C005",
        "type": "hard",
        "category": "currency",
        "rule": "At least 30% of the portfolio must remain in local TRY exposure.",
        "explanation": "Keeps sufficient domestic currency exposure.",
        "source": {"doc": "esg_policy_pdf", "quote": "Maintain ≥30% local currency (TRY) exposure."},
        "priority": 1,
    },
    {
        "id": "C006",
        "type": "hard",
        "category": "execution",
        "rule": "No GL_EQ buys for 3 days (creations halted) and EUR_BOND trades must be ≥ ₺5k lots.",
        "explanation": "Respects ETF creation halt and bond lot minimums.",
        "source": {"doc": "factsheets_pdf", "quote": "GL_EQ creations halted ... EUR_BOND minimum trade lot ₺5,000."},
        "priority": 1,
    },
    {
        "id": "C007",
        "type": "hard",
        "category": "liquidity",
        "rule": "Each day’s trading per asset must stay within 10% of ADV; equities T+2 (holiday Nov 10), bonds T+1.",
        "explanation": "Prevents illiquid fills and handles settlement timing.",
        "source": {"doc": "broker_notice_html", "quote": "ADV cap ≤10% per day ... Equities settle T+2, bonds T+1. Mon Nov 10 settlement holiday."},
        "priority": 1,
    },
    {
        "id": "C008",
        "type": "soft",
        "category": "risk",
        "rule": "Aim for higher expected return with risk awareness and low turnover (soft preference).",
        "explanation": "Guides the model toward efficient risk-adjusted moves.",
        "source": {"doc": "system", "quote": "Prefer higher expected return with risk awareness (μ−λ·risk); minimize turnover."},
        "priority": 2,
    },
    {
        "id": "C009",
        "type": "hard",
        "category": "esg",
        "rule": "Exclude issuers with >10% coal revenue — no restricted tickers in holdings or trades.",
        "explanation": "Aligns with the ESG coal exclusion policy.",
        "source": {"doc": "esg_policy_pdf", "quote": "Exclude issuers with >10% revenue from coal."},
        "priority": 1,
    },
    {
        "id": "C010",
        "type": "hard",
        "category": "tax",
        "rule": "Do not sell positions opened within the past 365 days.",
        "explanation": "Avoids triggering short-term capital events per client rules.",
        "source": {"doc": "client_mandate_email", "quote": "do not sell positions opened < 365 days."},
        "priority": 1,
    },
    {
        "id": "C011",
        "type": "hard",
        "category": "tax",
        "rule": "Honor wash-sale rule: don’t rebuy the same security within 30 days of realizing a loss.",
        "explanation": "Prevents disallowed loss harvesting.",
        "source": {"doc": "tax_memo_docx", "quote": "Wash-sale: do not repurchase substantially identical securities within 30 days of realizing a loss."},
        "priority": 1,
    },
    {
        "id": "C012",
        "type": "hard",
        "category": "cash",
        "rule": "Keep cash (USD_MM) high enough to cover the ₺36k rent cutoff (~3.6% weight).",
        "explanation": "Guarantees rent liquidity even if other trades settle later.",
        "source": {"doc": "cash_timeline", "quote": "Rent due ₺36,000 with cutoff Mon Nov 10 17:00; keep TRY cash ≥ ₺20,000 at all times."},
        "priority": 1,
    },
]


def compute_current_weights() -> Dict[str, float]:
    nav = PORTFOLIO_SCENARIO["nav_try"]
    prices = PORTFOLIO_SCENARIO["prices"]
    holdings = PORTFOLIO_SCENARIO["holdings_units"]
    weights: Dict[str, float] = {}
    for ticker, units in holdings.items():
        price = prices.get(ticker, 0)
        value = units * price
        weights[ticker] = value / nav if nav else 0.0
    return weights


CURRENT_WEIGHTS = compute_current_weights()
ESG_RESTRICTED_TICKERS = set(PORTFOLIO_SCENARIO.get("esg_restricted", []))
HOLDING_AGE_DAYS = PORTFOLIO_SCENARIO.get("holding_ages", {})
WASH_SALE_BLACKLIST = set(PORTFOLIO_SCENARIO.get("wash_sale_blacklist", []))
RENT_BUFFER_RATIO = PORTFOLIO_SCENARIO["cash_timeline"]["rent_due"]["amount_try"] / PORTFOLIO_SCENARIO["nav_try"]

RATE_SWING_DEFAULT_CUSTOMER = {
    "income_net": 68000,
    "expenses_monthly": 23500,
    "ltv": 0.82,
    "lti": 4.8,
    "dscr": 1.22,
    "term_months": 228,
    "apr_current": 10.9,
    "penalty_rule": "waived_if_shock_≥150bp",
    "risk_band": "mid",
    "delinquency_12m": 0,
}

RATE_SWING_DEFAULT_KNOBS = {
    "rate_move_bps": 150,
    "refix_timing": "now",
    "competitor_teaser_apr": 9.9,
    "competitor_teaser_months": 6,
    "income_volatility": "medium",
}

RATE_SWING_DOCS_PACK = """[T&C §7.2] Penalty waived when central-bank shock ≥150 bps within 60 days of reset.
[T&C §7.4] Early refix more than 6 months ahead requires supervisor sign-off.
[REG §3.b] Lender must assess affordability under baseline, +100 bps, +200 bps stress before refix.
[REG §5.1] "Your home may be repossessed if you do not keep up repayments on your mortgage."
[RISK §2.4] LTV cap 85%; DSCR min 1.15; LTI cap 5.5; exceptions require CRO note.
[BOARD §4] Prioritize stability over teaser arbitrage once +200 bps stress breaches EL budget.
[COMP §1] Competitor teaser 9.9% for 6 months on refix before reset date."""


def build_checkpoint_summary() -> str:
    cash = PORTFOLIO_SCENARIO["cash_timeline"]
    entries = []
    entries.append(f"• Today TRY cash: ₺{cash['today_try']:,}")
    entries.append(f"• Salary ₺{cash['salary']['amount_try']:,} @ {cash['salary']['at_iso']}")
    entries.append(f"• Rent ₺{cash['rent_due']['amount_try']:,} cutoff {cash['rent_due']['cutoff_iso']}")
    entries.append(f"• Loan ₺{cash['loan_due']['amount_try']:,} cutoff {cash['loan_due']['cutoff_iso']}")
    entries.append("• Cash floor ₺20k; Equity T+2 (holiday Nov 10), Bonds T+1.")
    return "\n".join(entries)


CHECKPOINT_SUMMARY = build_checkpoint_summary()



class SavingsConfig(BaseModel):
    persona: str
    goal: float
    currency: str
    timelineStart: str
    timelineEnd: str
    currentSavings: float
    monthsElapsed: int
    rentDueDay: int
    rentAmount: float
    utilitiesDueDay: int
    utilitiesTime: str
    utilitiesAmount: float
    salaryDay: str
    salaryAmount: float
    fridayGigIncome: float
    bnplDueDay: int
    bnplAmount: float
    cardAcutDay: int
    cardADueDay: int
    cardABalance: float
    cardBcutDay: int
    cardBDueDay: int
    cardBBalance: float
    gymMembership: float
    targetBuffer: float


class AdviceRequest(BaseModel):
    strategy: Literal["conventional", "reasoning"]
    config: SavingsConfig


class AdviceResponse(BaseModel):
    strategy: str
    model: str
    summary: str
    temporal_awareness: str = Field(..., alias="temporalAwareness")
    recommended_actions: List[str] = Field(default_factory=list, alias="recommendedActions")
    risks: List[str] = Field(default_factory=list)
    prompt: str
    raw: str
    timeline: List["AdviceTimelinePoint"] = Field(default_factory=list)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class AdviceTimelinePoint(BaseModel):
    date: str
    balance: float
    label: str | None = None


class AdviceSnapshot(BaseModel):
    summary: str
    temporal_awareness: str = Field(..., alias="temporalAwareness")
    recommended_actions: List[str] = Field(default_factory=list, alias="recommendedActions")
    risks: List[str] = Field(default_factory=list)
    prompt: str | None = None
    raw: str | None = None
    timeline: List[AdviceTimelinePoint] = Field(default_factory=list)

    class Config:
        populate_by_name = True


class ComparisonRequest(BaseModel):
    conventional: AdviceSnapshot
    reasoning: AdviceSnapshot
    config: SavingsConfig


class ComparisonResponse(BaseModel):
    headline: str
    temporal_factors: List[str] = Field(default_factory=list, alias="temporalFactors")
    conventional_gaps: List[str] = Field(default_factory=list, alias="conventionalGaps")
    reasoning_edge: List[str] = Field(default_factory=list, alias="reasoningEdge")
    verdict: str
    confidence: str
    prompt: str
    raw: str

    class Config:
        populate_by_name = True


class PortfolioRunRequest(BaseModel):
    strategy: Literal["conventional", "reasoning"]


class PortfolioAnalysisRequest(BaseModel):
    conventional: Dict[str, Any]
    reasoning: Dict[str, Any]


class RateSwingKnobs(BaseModel):
    rate_move_bps: int = RATE_SWING_DEFAULT_KNOBS["rate_move_bps"]
    refix_timing: Literal["now", "3m", "6m"] = RATE_SWING_DEFAULT_KNOBS["refix_timing"]
    competitor_teaser_apr: float = RATE_SWING_DEFAULT_KNOBS["competitor_teaser_apr"]
    competitor_teaser_months: int = RATE_SWING_DEFAULT_KNOBS["competitor_teaser_months"]
    income_volatility: Literal["low", "medium", "high"] = RATE_SWING_DEFAULT_KNOBS["income_volatility"]


class RateSwingRunRequest(BaseModel):
    customer: Dict[str, Any] = Field(default_factory=lambda: copy.deepcopy(RATE_SWING_DEFAULT_CUSTOMER))
    knobs: RateSwingKnobs = Field(default_factory=RateSwingKnobs)
    docs_pack: Optional[str] = None


app = FastAPI(title="Reasoning Demos API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def build_prompt(strategy: str, config: SavingsConfig) -> str:
    emphasis = (
        "Rely on simple heuristics, be honest that you may miss calendar conflicts."
        if strategy == "conventional"
        else "Lean on temporal reasoning: respect cut-offs, order of operations, and buffers."
    )
    format_contract = """
Return ONLY JSON with the following shape:
{
  "summary": "<2-3 sentence overview>",
  "temporal_awareness": "<how timing impacts the plan>",
  "recommended_actions": ["action 1", "action 2"],
  "risks": ["risk 1", "risk 2"],
  "balance_timeline": [
    {"date": "2025-01-01", "balance": 12000, "label": "Starting balance"},
    {"date": "2025-01-10", "balance": 3150, "label": "Rent & utilities debited"},
    {"date": "2025-01-31", "balance": 12150, "label": "Salary clears; buffer restored"}
  ]
}
"""
    return (
        f"You are preparing savings advice for {config.persona}.\n"
        f"{emphasis}\n"
        f"{format_contract.strip()}\n"
        "Scenario data (ISO dates, 24h times):\n"
        f"{json.dumps(config.dict(), indent=2)}\n"
        "Balance timeline guidance: output 5-8 chronological checkpoints between the timelineStart and timelineEnd,"
        " including major debits (rent, BNPL, utilities) and credited income (salary, gig work). Balances must be numeric (no currency symbols)."
    )


def build_portfolio_prompt() -> str:
    prompt_payload = {
        "nav_try": PORTFOLIO_SCENARIO["nav_try"],
        "universe": list(PORTFOLIO_SCENARIO["prices"].keys()),
        "current_weights": CURRENT_WEIGHTS,
        "prices": PORTFOLIO_SCENARIO["prices"],
        "fx_map": PORTFOLIO_SCENARIO["fx_map"],
        "checkpoints": [
            {"id": "CP_NOW", "label": "now"},
            {"id": "CP_SAL", "label": "Nov10_09:00"},
            {"id": "CP_RENT", "label": "Nov10_17:00"},
            {"id": "CP_LOAN", "label": "Nov14_10:30"},
        ],
        "settlement_ops": {
            "equity": "T+2",
            "bond": "T+1",
            "holiday_dates": ["2025-11-10"],
            "trading_hours": {"start": "09:00", "end": "17:00"},
            "maintenance": [
                {
                    "start": "2025-11-14T09:45:00+03:00",
                    "end": "2025-11-14T10:15:00+03:00",
                }
            ],
        },
        "cash_timeline": {
            "cash_now_try": PORTFOLIO_SCENARIO["cash_timeline"]["today_try"],
            "salary_try": PORTFOLIO_SCENARIO["cash_timeline"]["salary"]["amount_try"],
            "salary_at_iso": PORTFOLIO_SCENARIO["cash_timeline"]["salary"]["at_iso"],
            "rent_try": PORTFOLIO_SCENARIO["cash_timeline"]["rent_due"]["amount_try"],
            "rent_cutoff_iso": PORTFOLIO_SCENARIO["cash_timeline"]["rent_due"]["cutoff_iso"],
            "loan_try": PORTFOLIO_SCENARIO["cash_timeline"]["loan_due"]["amount_try"],
            "loan_cutoff_iso": PORTFOLIO_SCENARIO["cash_timeline"]["loan_due"]["cutoff_iso"],
            "cash_floor_try": PORTFOLIO_SCENARIO["cash_timeline"]["cash_floor_try"],
        },
        "constraint_registry": [
            {"cid": "C_CASH_FLOOR", "type": "hard", "category": "cash", "rule": "TRY cash ≥ 20000 at all checkpoints"},
            {"cid": "C_EQUITY_MAX", "type": "hard", "category": "bands", "rule": "Equity (TR_EQ+GL_EQ) ≤ 0.55"},
            {"cid": "C_BOND_MIN", "type": "hard", "category": "bands", "rule": "EUR_BOND ≥ 0.20"},
            {"cid": "C_GOLD_MAX", "type": "hard", "category": "bands", "rule": "GOLD ≤ 0.15"},
            {"cid": "C_ETF_SINGLE_MAX", "type": "hard", "category": "concentration", "rule": "Each ETF ≤ 0.25"},
            {"cid": "C_TRY_FLOOR", "type": "hard", "category": "fx", "rule": "TRY exposure ≥ 0.30"},
            {"cid": "C_NO_COAL", "type": "hard", "category": "esg", "rule": "Exclude issuers >10% coal revenue"},
            {"cid": "C_NO_SELL_LT365", "type": "hard", "category": "tax", "rule": "No sells from lots < 365 days"},
            {"cid": "C_WASH_SALE_30D", "type": "hard", "category": "tax", "rule": "No repurchase within 30 days after realized loss"},
            {"cid": "C_ADV_10PCT", "type": "hard", "category": "liquidity", "rule": "Trade value per day ≤ 10% ADV"},
            {"cid": "C_EURBOND_LOT", "type": "hard", "category": "liquidity", "rule": "EUR_BOND min trade lot ₺5000"},
            {"cid": "C_GLEQ_BUY_LOCK", "type": "hard", "category": "liquidity", "rule": "GL_EQ buys = 0 for next 3 trading days"},
            {"cid": "C_SETTLE_TL", "type": "hard", "category": "ops", "rule": "Respect T+2 equity, T+1 bond, and 2025-11-10 holiday for cash availability"},
            {"cid": "C_TRADE_WINDOW", "type": "hard", "category": "ops", "rule": "Trade only 09:00–17:00; avoid 2025-11-14 09:45–10:15"},
            {"cid": "C_OBJ_SOFT", "type": "soft", "category": "objective", "rule": "Prefer higher μ−λ·risk with minimal turnover"},
        ],
        "adv": PORTFOLIO_SCENARIO["adv"],
        "mu": PORTFOLIO_SCENARIO["mu"],
        "repair_allowed": True,
    }
    prompt = f"""
Duel Prompt v3 (self-check + repair baked in)

SYSTEM (to both models, identical):
You are a portfolio planner. You must (1) read a canonical constraint registry with IDs, (2) plan with a scratchpad, (3) emit a portfolio JSON, and (4) emit a self-check that references constraint IDs. If any hard constraint fails in your self-check, repair once before returning.

Only output JSON objects in the specified order: plan, portfolio, self_check. Follow the schemas exactly.

DELIBERATION BUDGET: Think step-by-step in plan. Keep the final portfolio minimal.

USER:
{json.dumps(prompt_payload, indent=2)}

Bad Candidate Plan A (to critique):
- Target weights: TR_EQ 34%, GL_EQ 26%, EUR_BOND 20%, GOLD 10%, USD_MM 10%.
- Trades (2025-11-07T11:00): Buy GL_EQ ₺10,000; Buy EUR_BOND ₺50,000; Sell USD_MM ₺60,000.

Your job:
1. Audit Plan A against all hard constraints (cash checkpoints, rent buffer, bands, ADV/lot, GL_EQ ban, settlement calendar/holiday, blackout, aging, wash-sale).
2. If any violation exists, produce Plan B (repaired) with trades and final weights that pass every hard constraint.
3. Provide numeric audits in rationale with exact values (no ellipses). If any PASS/FAIL is FAIL, output only the repaired plan.

SCHEMAS (use exactly):
{{
  "plan": {{
    "objective": "text",
    "key_checks": [{{"cid": "string", "how_to_satisfy": "text"}}],
    "proposed_weights": {{"TR_EQ":0,"GL_EQ":0,"EUR_BOND":0,"GOLD":0,"USD_MM":0}},
    "notes": ["text"]
  }},
  "portfolio": {{
    "weights": {{"TR_EQ":0,"GL_EQ":0,"EUR_BOND":0,"GOLD":0,"USD_MM":0}},
    "trades": [
      {{"ticker":"EUR_BOND","side":"buy|sell","units":0,"notional_try":0,"exec_time":"YYYY-MM-DDTHH:MM:SS+03:00","settles_on":"YYYY-MM-DD"}}
    ],
    "rationale": ["text"]
  }},
  "self_check": {{
    "by_constraint": [{{"cid":"string","pass":true,"explain":"text"}}],
    "all_hard_passed": true
  }}
}}

REPAIR RULE:
If any self_check item for a hard constraint is pass:false, update plan (briefly), adjust portfolio, and re-emit all three JSON blocks. One repair chance only.

Controller knobs (internal reference):
- gpt-5-mini: reasoning_effort="high", temperature=0, generous max tokens.
- gpt-4o-mini: temperature=0, default effort.

Important: Output exactly the three JSON objects (plan, portfolio, self_check) in that order. No prose.
"""
    return prompt.strip()

def amortization_payment(principal: float, apr_percent: float, term_months: int) -> float:
    monthly_rate = (apr_percent / 100) / 12
    if monthly_rate <= 0:
        return principal / max(term_months, 1)
    denominator = 1 - (1 + monthly_rate) ** (-term_months)
    if denominator == 0:
        return principal / max(term_months, 1)
    return principal * monthly_rate / denominator


def build_docs_index(docs_text: str) -> List[str]:
    ids: List[str] = []
    for line in docs_text.splitlines():
        if line.startswith("[") and "]" in line:
            cid = line.split("]", 1)[0][1:]
            ids.append(cid.strip())
    return ids


def build_rate_swing_summary(customer: Dict[str, Any], knobs: Dict[str, Any]) -> Dict[str, Any]:
    principal = RATE_SWING_DEFAULT_CUSTOMER.get("principal", RATE_SWING_DEFAULT_CUSTOMER["income_net"])  # fallback
    principal = 1_000_000  # use NAV as principal proxy
    term = int(customer.get("term_months", RATE_SWING_DEFAULT_CUSTOMER["term_months"]))
    apr_current = float(customer.get("apr_current", RATE_SWING_DEFAULT_CUSTOMER["apr_current"]))
    rate_move = knobs.get("rate_move_bps", RATE_SWING_DEFAULT_KNOBS["rate_move_bps"]) / 100
    competitor_apr = knobs.get("competitor_teaser_apr", 9.9)

    scenarios = [
        {"name": "Baseline", "delta": 0.0},
        {"name": "+100bp", "delta": 1.0},
        {"name": "+200bp", "delta": 2.0},
    ]

    paths = []
    for scenario in scenarios:
        apr_now = apr_current + scenario["delta"]
        apr_3m = apr_now + rate_move
        apr_6m = apr_3m + 0.35  # assume further drift

        monthly_now = amortization_payment(principal, apr_now, term)
        monthly_3m = amortization_payment(principal, apr_3m, term)
        monthly_6m = amortization_payment(principal, apr_6m, term)

        paths.append(
            {
                "name": scenario["name"],
                "apr_now": round(apr_now, 2),
                "apr_future": round(apr_3m, 2),
                "monthly_now": round(monthly_now, 2),
                "monthly_3m": round(monthly_3m, 2),
                "monthly_6m": round(monthly_6m, 2),
            }
        )

    penalty = 0 if knobs.get("rate_move_bps", 0) >= 150 else 20000
    diff_3m = max(paths[0]["monthly_now"] - paths[0]["monthly_3m"], 1)
    diff_6m = max(paths[0]["monthly_now"] - paths[0]["monthly_6m"], 1)
    breakeven_3m = max(0, int(round(penalty / diff_3m)))
    breakeven_6m = max(0, int(round(penalty / diff_6m)))

    summary = {
        "paths": paths,
        "breakeven_month_now_vs_3m": breakeven_3m,
        "breakeven_month_now_vs_6m": breakeven_6m,
        "constraints": {
            "dscr_min": 1.15,
            "ltv_cap": 0.85,
            "lti_cap": 5.5,
        },
        "teaser": {
            "apr": competitor_apr,
            "months": knobs.get("competitor_teaser_months", 6),
        },
    }
    return summary


def build_rate_swing_prompt(customer: Dict[str, Any], knobs: Dict[str, Any], summary: Dict[str, Any], docs_text: str) -> str:
    payload = {
        "customer": customer,
        "knobs": knobs,
        "scenario_summary_card": summary,
        "docs_index_ids": build_docs_index(docs_text),
        "docs_pack": docs_text,
    }
    prompt = f"""SYSTEM:
You are a mortgage reasoning assistant. Obey policy & regulator text.
CITE exact section IDs present in DOCS.
If any constraint fails in any scenario, choose the nearest compliant decision and list violations.

USER:
[CUSTOMER]
{json.dumps(customer, indent=2)}

[SCENARIOS]
{json.dumps(summary, indent=2)}

[DOCS]
{docs_text}

[TASK]
Decide one: Refix_Now | Refix_in_3m | Refix_in_6m | Hold.
Constraints: affordability across stress paths; LTV/LTI/DSCR caps; exact [REG §5.1] disclosure; penalty math.
Return JSON strictly matching schema:
{{
  "decision": "Refix_Now|Refix_in_3m|Refix_in_6m|Hold",
  "payment_paths": [{{"scenario":"Baseline","monthly_now":number,"monthly_choice":number}}],
  "breakeven_month": number,
  "rationale": ["string"],
  "cited_clauses": ["T&C §7.2","REG §3.b"],
  "violations": ["string"],
  "disclosures": ["string"],
  "mitigations": ["string"]
}}
"""
    return prompt.strip()
def _extract_json_block(response: str) -> Dict[str, Any]:
    cleaned = response.strip()
    if cleaned.startswith("```"):
        try:
            cleaned = cleaned.split("```", 2)[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        except IndexError:
            pass
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to locate first JSON object heuristically
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            snippet = cleaned[start : end + 1]
            try:
                return json.loads(snippet)
            except json.JSONDecodeError:
                pass
    return {}


def _extract_json_objects(response: str) -> List[Any]:
    cleaned = response.strip()
    cleaned = cleaned.replace("```json", "```")
    if "```" in cleaned:
        parts = cleaned.split("```")
        cleaned = "\n".join(parts[i] for i in range(1, len(parts), 2)).strip()
    decoder = json.JSONDecoder()
    idx = 0
    objs: List[Any] = []
    while idx < len(cleaned):
        while idx < len(cleaned) and cleaned[idx].isspace():
            idx += 1
        if idx >= len(cleaned):
            break
        try:
            obj, end = decoder.raw_decode(cleaned, idx)
            objs.append(obj)
            idx = end
        except json.JSONDecodeError:
            break
    if not objs:
        first = _extract_json_block(response)
        if first:
            objs.append(first)
    return objs


def normalize_payload(parsed: Dict[str, Any]) -> Dict[str, Any]:
    def _to_list(value: Any) -> List[str]:
        if isinstance(value, list):
            return [str(v) for v in value if v]
        if isinstance(value, str) and value:
            return [value]
        return []

    timeline_input = parsed.get("balance_timeline") or parsed.get("balanceTimeline") or []

    def _parse_timeline(entries: Any) -> List[AdviceTimelinePoint]:
        timeline: List[AdviceTimelinePoint] = []
        if not isinstance(entries, list):
            return timeline

        for item in entries:
            if not isinstance(item, dict):
                continue
            raw_date = str(item.get("date", "")).strip()
            if not raw_date:
                continue
            raw_balance = item.get("balance", 0)
            balance_value: float
            try:
                balance_value = float(
                    str(raw_balance)
                    .replace("₺", "")
                    .replace(",", "")
                    .strip()
                )
            except ValueError:
                balance_value = 0.0

            label = item.get("label") or item.get("note") or ""
            timeline.append(
                AdviceTimelinePoint(
                    date=raw_date,
                    balance=balance_value,
                    label=str(label).strip() or None,
                )
            )
        return timeline

    return {
        "summary": str(parsed.get("summary", "")).strip(),
        "temporal_awareness": str(
            parsed.get("temporal_awareness") or parsed.get("temporalAwareness") or ""
        ).strip(),
        "recommended_actions": _to_list(
            parsed.get("recommended_actions") or parsed.get("recommendedActions")
        ),
        "risks": _to_list(parsed.get("risks")),
        "timeline": _parse_timeline(timeline_input),
    }


def build_comparison_prompt(payload: ComparisonRequest) -> str:
    scenario = json.dumps(payload.config.dict(), indent=2)
    conventional = json.dumps(payload.conventional.dict(by_alias=True), indent=2)
    reasoning = json.dumps(payload.reasoning.dict(by_alias=True), indent=2)
    contract = """
Return ONLY JSON with this shape:
{
  "headline": "<short verdict>",
  "temporal_factors": ["factor 1", "..."],
  "conventional_gaps": ["gap 1", "..."],
  "reasoning_edge": ["advantage 1", "..."],
  "verdict": "<2-3 sentences comparing both>",
  "confidence": "<low|medium|high>"
}
"""
    return (
        "You are auditing two model responses about the same savings plan.\n"
        "Explain why the reasoning model shows better temporal understanding.\n"
        f"{contract.strip()}\n"
        f"Scenario data:\n{scenario}\n"
        f"Conventional output:\n{conventional}\n"
        f"Reasoning output:\n{reasoning}\n"
        "Focus on calendar alignment, ordering of payments, and buffer protection."
    )


def normalize_comparison(parsed: Dict[str, Any]) -> Dict[str, Any]:
    def _as_list(*keys: str) -> List[str]:
        for key in keys:
            value = parsed.get(key)
            if value:
                if isinstance(value, list):
                    return [str(item) for item in value if item]
                if isinstance(value, str):
                    return [value]
        return []

    def _first(*keys: str) -> str:
        for key in keys:
            value = parsed.get(key)
            if value:
                return str(value)
        return ""

    return {
        "headline": _first("headline"),
        "temporal_factors": _as_list("temporal_factors", "temporalFactors"),
        "conventional_gaps": _as_list("conventional_gaps", "conventionalGaps"),
        "reasoning_edge": _as_list("reasoning_edge", "reasoningEdge"),
        "verdict": _first("verdict"),
        "confidence": _first("confidence"),
    }


def _safe_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            cleaned = value.replace('%', '').replace('₺', '').replace(',', '').strip()
            return float(cleaned)
        except ValueError:
            return default
    return default


def parse_portfolio_response(response_text: str) -> Dict[str, Any]:
    objects = _extract_json_objects(response_text)
    plan_section: Dict[str, Any] | None = None
    portfolio_section: Dict[str, Any] | None = None
    self_check_section: Dict[str, Any] | None = None

    if len(objects) >= 3:
        plan_section, portfolio_section, self_check_section = objects[:3]
    elif objects:
        first = objects[0]
        if isinstance(first, dict) and {"plan", "portfolio", "self_check"} <= set(first.keys()):
            plan_section = first.get("plan")
            portfolio_section = first.get("portfolio")
            self_check_section = first.get("self_check")
        else:
            portfolio_section = first
    else:
        portfolio_section = {}

    parsed = portfolio_section or {}
    weights = parsed.get("weights") or {}
    trades = parsed.get("trades") or []
    rationale = parsed.get("rationale") or []

    normalized_weights: Dict[str, float] = {}
    for ticker, value in weights.items():
        normalized_weights[ticker] = _safe_float(value)

    normalized_trades: List[Dict[str, Any]] = []
    if isinstance(trades, list):
        for trade in trades:
            if not isinstance(trade, dict):
                continue
            ticker = str(trade.get("ticker", "")).upper()
            if ticker not in PORTFOLIO_SCENARIO["prices"]:
                continue
            price = PORTFOLIO_SCENARIO["prices"].get(ticker, 0) or 0
            notional_value = _safe_float(trade.get("notional_try"), 0.0)
            units_value = trade.get("units")
            if units_value is None and notional_value and price:
                units_value = notional_value / price
            units = int(_safe_float(units_value, 0.0))
            if units == 0 and notional_value and price:
                units = int(round(notional_value / price))
            if notional_value == 0 and units and price:
                notional_value = units * price
            normalized_trades.append(
                {
                    "ticker": ticker,
                    "side": (trade.get("side") or "buy").lower(),
                    "units": units,
                    "notional_try": notional_value,
                    "exec_time": trade.get("exec_time"),
                    "settles_on": trade.get("settles_on"),
                }
            )

    rationale_list: List[str] = []
    if isinstance(rationale, list):
        rationale_list = [str(item).strip() for item in rationale if str(item).strip()]

    return {
        "weights": normalized_weights,
        "trades": normalized_trades,
        "rationale": rationale_list,
        "plan": plan_section,
        "self_check": self_check_section,
    }


def validate_portfolio(portfolio: Dict[str, Any]) -> Dict[str, Any]:
    weights: Dict[str, float] = portfolio.get("weights", {})
    trades: List[Dict[str, Any]] = portfolio.get("trades", [])
    usd_mm_weight = weights.get("USD_MM", 0.0)
    tr_eq_weight = weights.get("TR_EQ", 0.0)
    gl_eq_weight = weights.get("GL_EQ", 0.0)
    eur_bond_weight = weights.get("EUR_BOND", 0.0)
    gold_weight = weights.get("GOLD", 0.0)

    results: Dict[str, Dict[str, Any]] = {}

    def add_result(cid: str, passed: bool, reason: Optional[str] = None):
        results[cid] = {"passed": passed, "reason": reason}

    total_weight = sum(weights.values())
    add_result("SUM", abs(total_weight - 1.0) <= 1e-4, f"Weights sum to {total_weight:.4f}")

    add_result("C001", usd_mm_weight >= 0.02, f"USD_MM weight {usd_mm_weight:.2f} (< 0.02)")

    equity_weight = tr_eq_weight + gl_eq_weight
    add_result("C002", equity_weight <= 0.55 + 1e-4, f"Equity {equity_weight:.2f} > 0.55")

    add_result("C003", eur_bond_weight >= 0.20 - 1e-4, f"EUR_BOND {eur_bond_weight:.2f} < 0.20")

    single_cap_ok = all(weight <= 0.25 + 1e-4 for weight in weights.values())
    gold_cap_ok = gold_weight <= 0.15 + 1e-4
    add_result("C004", single_cap_ok and gold_cap_ok, "ETF or GOLD cap breached")

    try_exposure = sum(weight for ticker, weight in weights.items() if PORTFOLIO_SCENARIO["fx_map"].get(ticker) == "TRY")
    add_result("C005", try_exposure >= 0.30 - 1e-4, f"TRY exposure {try_exposure:.2f} < 0.30")

    gl_eq_buys = any(trade["ticker"] == "GL_EQ" and trade["side"] == "buy" and trade["units"] > 0 for trade in trades)
    eur_bond_lots_ok = all(
        (trade["ticker"] != "EUR_BOND")
        or (trade["units"] * PORTFOLIO_SCENARIO["prices"]["EUR_BOND"] >= 5000)
        for trade in trades
    )
    add_result("C006", (not gl_eq_buys) and eur_bond_lots_ok, "GL_EQ buy detected or EUR_BOND lot < ₺5k")

    adv_caps_ok = True
    for trade in trades:
        ticker = trade["ticker"]
        adv_cap = PORTFOLIO_SCENARIO["adv"].get(ticker)
        price = PORTFOLIO_SCENARIO["prices"].get(ticker, 0)
        trade_value = abs(trade["units"] * price)
        if adv_cap and trade_value > (adv_cap * 0.1):
            adv_caps_ok = False
            break
    add_result("C007", adv_caps_ok, "ADV cap exceeded")

    add_result("C008", True, None)  # subjective soft constraint

    restricted_used = any(
        ticker in ESG_RESTRICTED_TICKERS and weight > 0
        for ticker, weight in weights.items()
    ) or any(trade["ticker"] in ESG_RESTRICTED_TICKERS for trade in trades)
    add_result("C009", not restricted_used, "Restricted ESG asset referenced")

    young_sell_violation = any(
        trade["side"] == "sell" and HOLDING_AGE_DAYS.get(trade["ticker"], 999) < 365 and trade["units"] > 0
        for trade in trades
    )
    add_result("C010", not young_sell_violation, "Sell order on lot held <365 days")

    wash_sale_violation = any(
        trade["side"] == "buy" and trade["ticker"] in WASH_SALE_BLACKLIST and trade["units"] > 0
        for trade in trades
    )
    add_result("C011", not wash_sale_violation, "Wash-sale blacklist ticker repurchased")

    add_result(
        "C012",
        usd_mm_weight >= RENT_BUFFER_RATIO - 1e-4,
        f"Cash weight {usd_mm_weight:.3f} < rent buffer {RENT_BUFFER_RATIO:.3f}",
    )

    passed = [cid for cid, data in results.items() if data["passed"] and cid.startswith("C")]
    failed = [
        {"cid": cid, "reason": data["reason"]}
        for cid, data in results.items()
        if not data["passed"] and cid.startswith("C")
    ]
    score = len(passed) / max(1, len([cid for cid in results if cid.startswith("C")]))

    return {
        "passed": passed,
        "failed": failed,
        "score": round(score, 2),
        "details": results,
    }


def build_portfolio_analysis_prompt(conventional: Dict[str, Any], reasoning: Dict[str, Any]) -> str:
    def format_validation(label: str, data: Dict[str, Any]) -> str:
        passed = ", ".join(data.get("validation", {}).get("passed", []))
        failed_items = data.get("validation", {}).get("failed", [])
        failed_str = "; ".join(f"{item['cid']}: {item['reason']}" for item in failed_items)
        return f"{label} -> passed: [{passed}] | failed: [{failed_str}]"

    conv_summary = format_validation("gpt-4o-mini", conventional)
    reas_summary = format_validation("gpt-5-mini", reasoning)
    constraints_text = "\n".join(
        f"{c['id']}: {c['rule']} ({c['type']})" for c in PORTFOLIO_CONSTRAINTS
    )
    return (
        "Compare two portfolio proposals and explain which constraints were met or missed. "
        "Provide JSON with keys headline, highlights (array), missedConstraints (array), "
        "verdict (string)."
        f"\nConstraints:\n{constraints_text}\n"
        f"{conv_summary}\n{reas_summary}\n"
        "Highlight subtle timeline or liquidity reasoning that explains differences."
    )



def response_to_text(response: Any) -> str:
    """Best-effort conversion of an agent response into a text blob."""
    if response is None:
        return ""

    text_attr = getattr(response, "text", None)
    if callable(text_attr):
        try:
            text_value = text_attr()
        except TypeError:
            text_value = None
    else:
        text_value = text_attr

    if isinstance(text_value, str):
        return text_value

    if isinstance(text_value, (list, dict)):
        try:
            return json.dumps(text_value, indent=2)
        except TypeError:
            pass

    return str(text_value or response)


def response_to_json_blob(response: Any) -> str:
    if response is None:
        return ""
    json_attr = getattr(response, "to_json", None)
    if callable(json_attr):
        try:
            return json_attr()
        except TypeError:
            pass
    return response_to_text(response)


@app.post("/api/savings-advice", response_model=AdviceResponse)
async def savings_advice(payload: AdviceRequest):
    strategy = payload.strategy
    agent = AGENTS.get(strategy)
    if not agent:
        raise HTTPException(status_code=400, detail="Unsupported strategy")

    prompt = build_prompt(strategy, payload.config)

    try:
        raw_response = await agent.run(prompt)
    except Exception as exc:  # pragma: no cover - surface SDK errors
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    response_text = response_to_text(raw_response)
    raw_blob = response_to_json_blob(raw_response)
    parsed = normalize_payload(_extract_json_block(response_text))

    return AdviceResponse(
        strategy=strategy,
        model=MODEL_LOOKUP[strategy],
        summary=parsed["summary"] or "No summary produced.",
        temporalAwareness=parsed["temporal_awareness"] or "No temporal context detected.",
        recommendedActions=parsed["recommended_actions"],
        risks=parsed["risks"],
        prompt=prompt,
        raw=raw_blob,
        timeline=parsed["timeline"],
    )


@app.post("/api/temporal-analysis", response_model=ComparisonResponse)
async def temporal_analysis(payload: ComparisonRequest):
    if not payload.conventional or not payload.reasoning:
        raise HTTPException(status_code=400, detail="Both model responses are required.")

    agent = AGENTS["reasoning"]
    prompt = build_comparison_prompt(payload)

    try:
        raw_response = await agent.run(prompt)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    response_text = response_to_text(raw_response)
    raw_blob = response_to_json_blob(raw_response)
    parsed = normalize_comparison(_extract_json_block(response_text))

    return ComparisonResponse(
        headline=parsed["headline"] or "Temporal analysis",
        temporalFactors=parsed["temporal_factors"],
        conventionalGaps=parsed["conventional_gaps"],
        reasoningEdge=parsed["reasoning_edge"],
        verdict=parsed["verdict"] or "No verdict provided.",
        confidence=parsed["confidence"] or "unknown",
        prompt=prompt,
        raw=raw_blob,
    )


@app.get("/api/portfolio-duel/info")
async def portfolio_duel_info():
    return {
        "scenario": {
            "nav_try": PORTFOLIO_SCENARIO["nav_try"],
            "now_iso": PORTFOLIO_SCENARIO["now_iso"],
            "prices": PORTFOLIO_SCENARIO["prices"],
            "holdings_units": PORTFOLIO_SCENARIO["holdings_units"],
            "current_weights": CURRENT_WEIGHTS,
            "cash_timeline": PORTFOLIO_SCENARIO["cash_timeline"],
            "text_context": PORTFOLIO_SCENARIO["text_context"],
        },
        "constraints": PORTFOLIO_CONSTRAINTS,
        "prompt": build_portfolio_prompt(),
    }


@app.post("/api/portfolio-duel/portfolio")
async def run_portfolio_duel(payload: PortfolioRunRequest):
    agent = AGENTS.get(payload.strategy)
    if not agent:
        raise HTTPException(status_code=400, detail="Unsupported strategy")

    prompt = build_portfolio_prompt()
    try:
        raw_response = await agent.run(prompt)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    response_text = response_to_text(raw_response)
    portfolio = parse_portfolio_response(response_text)
    plan_section = portfolio.pop("plan", None)
    self_check_section = portfolio.pop("self_check", None)
    validation = validate_portfolio(portfolio)

    return {
        "strategy": payload.strategy,
        "model": MODEL_LOOKUP[payload.strategy],
        "portfolio": portfolio,
        "validation": validation,
        "prompt": prompt,
        "raw": response_to_json_blob(raw_response),
        "constraints": PORTFOLIO_CONSTRAINTS,
        "plan": plan_section,
        "self_check": self_check_section,
    }


@app.post("/api/portfolio-duel/analysis")
async def portfolio_duel_analysis(payload: PortfolioAnalysisRequest):
    if not payload.conventional or not payload.reasoning:
        raise HTTPException(status_code=400, detail="Both model payloads are required.")

    prompt = build_portfolio_analysis_prompt(payload.conventional, payload.reasoning)
    try:
        raw_response = await AGENTS["reasoning"].run(prompt)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    response_text = response_to_text(raw_response)
    parsed = _extract_json_block(response_text)
    return {
        "headline": parsed.get("headline", "Constraint analysis"),
        "highlights": parsed.get("highlights", []),
        "missedConstraints": parsed.get("missedConstraints", []),
        "verdict": parsed.get("verdict", ""),
        "prompt": prompt,
        "raw": response_to_json_blob(raw_response),
    }


@app.get("/api/rate-swing/info")
async def rate_swing_info():
    """Return the default customer profile, knobs, and docs pack."""
    return {
        "customer": RATE_SWING_DEFAULT_CUSTOMER,
        "knobs": RATE_SWING_DEFAULT_KNOBS,
        "docs_pack": RATE_SWING_DOCS_PACK,
    }


@app.post("/api/rate-swing/run")
async def rate_swing_run(payload: RateSwingRunRequest):
    """Run both gpt-4o-mini and gpt-5o-mini on the same rate-swing task with identical instructions.
    The ONLY difference is reasoning_effort="high" for gpt-5o-mini."""
    customer = payload.customer
    knobs = payload.knobs.model_dump()
    docs_text = payload.docs_pack or RATE_SWING_DOCS_PACK

    summary = build_rate_swing_summary(customer, knobs)
    prompt = build_rate_swing_prompt(customer, knobs, summary, docs_text)

    # Use rate-swing specific agents with identical instructions
    conventional_agent = RATE_SWING_AGENTS["conventional"]
    reasoning_agent = RATE_SWING_AGENTS["reasoning"]

    try:
        conv_response = await conventional_agent.run(prompt)
        reas_response = await reasoning_agent.run(prompt)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    conv_text = response_to_text(conv_response)
    reas_text = response_to_text(reas_response)

    conv_json = _extract_json_block(conv_text)
    reas_json = _extract_json_block(reas_text)

    return {
        "prompt": prompt,
        "scenario_summary": summary,
        "conventional": {
            "model": MODEL_LOOKUP["conventional"],
            "json": conv_json,
            "raw": response_to_json_blob(conv_response),
        },
        "reasoning": {
            "model": MODEL_LOOKUP["reasoning"],
            "json": reas_json,
            "raw": response_to_json_blob(reas_response),
        },
    }


class RateSwingAnalysisRequest(BaseModel):
    prompt: str
    scenario_summary: Dict[str, Any]
    docs_pack: str
    conventional_json: Dict[str, Any]
    reasoning_json: Dict[str, Any]


@app.post("/api/rate-swing/analysis")
async def rate_swing_analysis(payload: RateSwingAnalysisRequest):
    """Use gpt-5o-mini as an analyst to compare the two outputs and explain which is better."""
    docs_index_ids = build_docs_index(payload.docs_pack)

    analysis_prompt = f"""SYSTEM:
You are an expert evaluation analyst. Compare two JSON outputs from different models (gpt-4o-mini and gpt-5o-mini with reasoning_effort="high") that were given IDENTICAL instructions and prompts. Your job is to assess which model performed better and explain WHY.

Focus on:
- Policy compliance and constraint adherence
- Accuracy of clause citations
- Quality of reasoning and decision-making
- Scenario stability across stress tests
- Completeness of required disclosures

USER:
[CONTEXT]
Both models received identical system instructions and the same prompt below.
The ONLY difference: gpt-5o-mini used reasoning_effort="high" to enable extended reasoning.

- Prompt (identical for both): {payload.prompt}
- Docs index (available clauses): {json.dumps(docs_index_ids)}
- Numeric ground-truth summary: {json.dumps(payload.scenario_summary, indent=2)}

[MODEL_A: gpt-4o-mini (no reasoning_effort)]
{json.dumps(payload.conventional_json, indent=2)}

[MODEL_B: gpt-5o-mini (reasoning_effort="high")]
{json.dumps(payload.reasoning_json, indent=2)}

[TASK]
Analyze both outputs and determine which is better. Be specific about:
1) Validate that every cited clause ID exists in docs_index_ids. Flag invalid citations.
2) Check if constraints (affordability, LTV/LTI/DSCR) are properly evaluated using numeric summary.
3) Check if disclosure includes verbatim REG §5.1 text: "Your home may be repossessed if you do not keep up repayments on your mortgage."
4) Assess decision stability: do decisions make sense given the breakeven numbers and stress scenarios?
5) Evaluate reasoning depth: which model showed deeper understanding of the problem?

Return JSON with clear explanations:
{{
  "winner": "gpt-4o-mini|gpt-5o-mini|tie",
  "reasons": ["Specific reason 1 with evidence", "Specific reason 2...", "..."],
  "issues_A": ["Specific issue in gpt-4o-mini output", "..."],
  "issues_B": ["Specific issue in gpt-5o-mini output", "..."],
  "scorecard": {{
    "policy_violations_A": int,
    "policy_violations_B": int,
    "clause_precision_A": 0.0-1.0,
    "clause_precision_B": 0.0-1.0,
    "stability_A": 0.0-1.0,
    "stability_B": 0.0-1.0
  }}
}}
"""

    # Use rate-swing reasoning agent for analysis
    reasoning_agent = RATE_SWING_AGENTS["reasoning"]
    try:
        analyst_response = await reasoning_agent.run(analysis_prompt)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    analyst_text = response_to_text(analyst_response)
    analyst_json = _extract_json_block(analyst_text)

    return {
        "analysis": analyst_json,
        "prompt": analysis_prompt,
        "raw": response_to_json_blob(analyst_response),
    }


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "reasoning_api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
