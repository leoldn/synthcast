# SESS Technical Summary
## Architecture & Core Concepts

---

## System Architecture

### Hierarchical Simulation Structure

```
┌─────────────────────────────────────────────────┐
│         PLANNER LEVEL (Meta-Agent)              │
│                                                 │
│  • Aggregates micro-level sentiment             │
│  • Generates macro investment signals           │
│  • Tests policy scenarios                       │
└─────────────────────────────────────────────────┘
                      ▲ ▼
              (Feedback Loop)
                      ▲ ▼
┌─────────────────────────────────────────────────┐
│      AGENT LEVEL (50,000+ Individuals)          │
│                                                 │
│  Each Agent:                                    │
│  • Profile (demographics, finances, traits)     │
│  • Memory (episodic, semantic, emotional)       │
│  • Perception (filtered economic context)       │
│  • Decision (bounded rationality)               │
└─────────────────────────────────────────────────┘
                      ▲ ▼
┌─────────────────────────────────────────────────┐
│      ECONOMIC ENVIRONMENT (Data Layer)          │
│                                                 │
│  • Macro indicators (GDP, inflation, rates)     │
│  • Policy changes and news events               │
│  • Historical validation data                   │
└─────────────────────────────────────────────────┘
```

**Design principle:** Bottom-up emergence of macro sentiment from heterogeneous micro-level agent interactions, with top-down feedback from economic environment to agent perceptions.

---

## Core Components

### 1. Census-Calibrated Population Generation

**Concept:** Agents sampled from actual demographic distributions rather than random generation.

**Implementation:**
- Age distribution matches census data (18-65 working population)
- Income follows Pareto distribution calibrated to tax brackets
- Geographic stratification matches population density
- Occupations generated per income decile

**Validation:** Chi-squared tests ensure agent population ≤5% deviation from census data.

**Example Agent:**
```
Demographics: 42-year-old, Munich, Germany
Occupation: Manufacturing Engineer (Income Decile 7)
Income: €4,200/month (Pareto-sampled)
Household: 3 people, mortgage holder
Traits: Risk-averse, environmentally conscious
```

---

### 2. Memory-Augmented Agent Architecture

**Concept:** Agents maintain memory systems that influence future decisions.

**Three-Tier Memory:**

```
EPISODIC MEMORY (Personal Experiences)
├── "Electricity bill increased 18% last month"
├── "Delayed vacation due to car repair costs"
└── "Company announced layoffs in October"

SEMANTIC MEMORY (Economic Knowledge)
├── "ECB rate hikes slow housing markets"
├── "Energy prices rise in winter"
└── "Green subsidies make solar affordable"

EMOTIONAL STATE (Psychological Condition)
├── Financial Anxiety: 0.4 (moderate)
├── Job Security: 0.7 (confident)
└── Future Optimism: 0.6 (cautious)
```

**Memory Retrieval:** Vector similarity search retrieves relevant memories when agents make decisions.

**Temporal Evolution:** Memories decay exponentially; emotional states update based on economic conditions.

---

### 3. Bounded Rationality Decision-Making

**Concept:** Agents use heuristics and exhibit cognitive biases.

**Decision Process:**
1. **Perception:** Filter macro indicators through personal relevance
2. **Memory Retrieval:** Recall similar past experiences
3. **Emotional Context:** Current anxiety/optimism influences response
4. **LLM Reasoning:** Generate decision using persona-conditioned prompt
5. **Behavioral Biases:** Loss aversion (2:1 ratio), status quo bias, herding

**Prompt Structure:**
```
You are [Name], [Age]-year-old [Occupation] in [Location].

Financial situation: [Income, savings, debts]
Recent experiences: [Episodic memories]
Economic conditions: [Macro context]
Emotional state: [Anxiety, optimism levels]

Question: [Survey question]

Respond considering bounded rationality and biases.
```

---

### 4. Multi-Period Temporal Simulation

**Concept:** Agents evolve over 1-5 year horizons.

**Time-Series Dynamics:**
- Agents age each period, wage profiles adjust
- New experiences stored, old memories fade
- Emotional persistence from past shocks
- Dynamic job assignment for unemployed

**Crisis Simulation Example:**
```
Period 1: Normal conditions
Period 2: SHOCK (energy crisis)
Period 3-5: Anxiety spikes, spending cuts
Period 6-20: Gradual recovery with psychological scarring
```

---

### 5. Hierarchical Signal Aggregation

**Micro → Macro Pipeline:**

```
50,000 Individual Responses
         ↓
Segment by Demographics
├── Income Quintiles (Q1-Q5)
├── Age Cohorts (18-34, 35-54, 55-65)
├── Regions (North, South, East Europe)
└── Occupations (Manufacturing, Services)
         ↓
Calculate Divergence Signals
├── High-income vs. Low-income gap
├── Regional sentiment spreads
└── Generational differences
         ↓
Generate Investment Indices
└── With Confidence Scores (0-100)
```

**Confidence Calculation:**
- 30%: Agent consensus (low dispersion = high confidence)
- 30%: Historical accuracy of signal type
- 20%: Sample size adequacy (>5,000 agents/segment)
- 20%: Memory consistency across agents

---

## Technical Stack

### Infrastructure
```
LLM API Layer
├── Primary: Anthropic Claude 3.5 Sonnet
├── Fallback: OpenAI GPT-4 Turbo
└── Retry logic with exponential backoff

Orchestration
├── Python 3.11+ (FastAPI)
├── Apache Airflow (scheduling)
└── Kubernetes (container management)

Data Storage
├── PostgreSQL (agent profiles)
├── Pinecone/Weaviate (vector memory)
├── InfluxDB (time-series sentiment)
└── Redis (caching)
```

### Data Flow
```
Census Data → Population Generator → 50,000 Agents
                                           ↓
Economic Indicators → Scenario Manager → Agent Simulation
                                           ↓
Agent Responses → Signal Aggregator → Investment Indices
                                           ↓
Historical Surveys ← Validation Engine ← Backtesting
```

---

## Agent Data Model

### Profile Structure
```python
AgentProfile:
  agent_id: str
  name: str
  age: int (18-65)
  location: str
  country_code: str
  occupation: str
  monthly_wage: float
  income_decile: int (1-10)
  income_percentile: float (0-100)
  education: enum
  household_size: int
  has_mortgage: bool
  savings_rate: float (0-1)
  risk_tolerance: enum
  political_leaning: str
  environmental_concern: str
  loss_aversion_coefficient: float
```

### Memory Structure
```python
EpisodicMemory:
  memory_id: str
  timestamp: datetime
  event_description: str
  emotional_valence: float (-1 to 1)
  importance_score: float (0-1)
  embedding: List[float]

EmotionalState:
  financial_anxiety: float (-1 to 1)
  job_security_confidence: float (-1 to 1)
  future_optimism: float (-1 to 1)
  spending_confidence: float (-1 to 1)
```

---

## Simulation Workflow

### Population Generation
```python
1. Load census demographic distributions
2. Sample ages from census age distribution
3. Sample locations (geographic stratification)
4. Sample incomes (Pareto distribution by location)
5. Generate occupations based on income decile
6. Assign education correlated with income
7. Generate household characteristics
8. Initialize financial profiles
9. Assign behavioral traits
10. Validate population vs. census (chi-squared test)
```

### Scenario Execution
```python
1. Define scenario (economic context, policies, time horizon)
2. Load/generate agent population
3. For each period (1-20):
   a. Update economic context
   b. Age agents, adjust wages
   c. Each agent:
      - Perceive filtered economic context
      - Retrieve relevant memories
      - Make decisions via LLM
      - Update memory and emotional state
   d. Aggregate responses by segments
   e. Calculate divergence signals
4. Generate investment indices with confidence scores
5. Validate against historical benchmarks
```

### Signal Generation
```python
1. Extract responses for specific questions
2. Calculate population-level metrics
3. Segment by demographics:
   - Income quintiles
   - Age cohorts
   - Regions
   - Occupations
4. Calculate divergence indices:
   - High vs. low income gap
   - Regional spreads
   - Generational differences
5. Generate confidence scores
6. Classify signals (Buy/Sell/Hold)
```

---

## Validation Framework

### Historical Backtesting
- Correlation with Michigan Sentiment Index (2008-2023)
- Target: r > 0.85
- Lead time: 2-4 weeks ahead of official surveys

### Demographic Validity
- Chi-squared tests for age, income, geography
- Target: p > 0.05 (not significantly different from census)

### Behavioral Realism
- Loss aversion ratio: ~2:1 (prospect theory)
- Hyperbolic discounting patterns
- Herding effects in networks

### Crisis Replication
- 2008 Financial Crisis: Sentiment collapse post-Lehman
- 2011 Eurozone Crisis: North-South divergence
- 2020 COVID-19: Panic → bifurcation by income
- 2022 Energy Crisis: Inflation anxiety spike

---

## Performance Targets

| Operation | Target Time | Agents |
|-----------|-------------|--------|
| Population Generation | 2 hours | 50,000 |
| Single-Period Simulation | 30 minutes | 50,000 |
| 20-Period Simulation | 10 hours | 50,000 |

**Parallelization:**
- Batch processing: 100 agents per batch
- Multi-threading: 10 concurrent workers
- Async I/O for LLM API calls

---

## System Workflow Example

### UK Taxation Scenario

```
1. Input Setup
   ├── Geography: UK (England, Scotland, Wales)
   ├── Population: 15,000 agents
   ├── Scenario: Income tax +3%, VAT +2%
   └── Time horizon: 5 years

2. Population Generation
   ├── Age: UK census distribution
   ├── Income: Pareto calibrated to UK tax brackets
   ├── Location: England 84%, Scotland 8%, Wales 5%
   └── Occupations: 10 per income decile

3. Agent Simulation
   ├── Survey questions:
   │   ├── Major purchase intentions
   │   ├── Savings rate changes
   │   └── Job security confidence
   └── Each agent responds based on:
       ├── Income impact
       ├── Past tax increase memories
       └── Current financial anxiety

4. Aggregation
   ├── Bottom quintile: -15% spending intent
   ├── Top quintile: -3% spending intent
   ├── Regional: Scotland more resilient
   └── Sectors: Discretionary hit hardest

5. Investment Signals
   ├── Reduce UK consumer discretionary exposure
   ├── Overweight defensive sectors
   └── Monitor for policy reversal pressure
```

---

## Key Technical Concepts

### Census Calibration
Ensures agent population statistically represents real demographics through:
- Distribution matching (age, income, location)
- Correlation preservation (education-income, age-wealth)
- Validation testing (chi-squared, KS tests)

### Memory-Augmented Reasoning
Agents consider historical context when making decisions:
- Past inflation experiences affect spending caution
- Job loss history increases savings rate
- Policy reversal memories create trust issues

### Bounded Rationality
Agents don't optimize perfectly:
- Use heuristics and rules of thumb
- Exhibit loss aversion and status quo bias
- Influenced by recent salient events
- Limited by cognitive capacity

### Hierarchical Aggregation
Individual responses roll up to population patterns:
- Micro-level heterogeneity preserved in segments
- Macro-level emergent dynamics from interactions
- Feedback loops between individual and aggregate

---

*For commercial applications, see README.md*