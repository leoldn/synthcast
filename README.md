# Synthetic Economic Sentiment System (SESS)

**Scenario-based economic sentiment analysis for institutional investors**

---

## Overview

SESS simulates consumer and business populations to generate forward-looking sentiment signals for investment decision-making. The system models thousands of agents with realistic demographics, financial profiles, and memory systems to evaluate how different economic and political scenarios affect sentiment across population segments.

The framework builds on recent research in agent-based economic simulation ([Li et al., ACL 2024](https://arxiv.org/abs/2310.10436); [Karten et al., 2025](https://arxiv.org/abs/2507.15815)), using census-calibrated populations and memory-augmented agents to capture heterogeneous responses and psychological persistence effects.

**Core Principle:** Generate sentiment signals by simulating how diverse populations respond to scenarios before they occur, enabling proactive investment positioning rather than reactive responses to published surveys.

---

## Commercial Applications

### 1. Renewable Energy Infrastructure Investment in Europe

**Input:** Simulate 15,000 European households across income distributions and countries (Germany, France, Spain, Italy, Poland). Test responses to varying renewable energy scenarios: subsidy levels, electricity price increases, grid investment requirements, and long-term climate policy commitments.

**Output:** Segment-level support for renewable transition measures, willingness to accept higher energy costs, regional divergences in policy backing, and stability of support across different economic conditions. Identification of income groups where support is fragile and vulnerable to energy price shocks.

**Commercial Decisions:** Inform geographic allocation between Northern European wind (higher policy stability) versus Southern European solar (higher growth but policy risk). Assess timing for large capital commitments based on policy support durability. Structure investments with appropriate hedges against subsidy reversals or regulatory changes in jurisdictions showing support erosion among key voting demographics.

---

### 2. UK Taxation Regime Increase and Economic Impact

**Input:** Model UK population across income deciles, regions, and employment sectors. Simulate responses to proposed tax increases: income tax rate changes, capital gains adjustments, corporate tax reforms, and wealth taxes. Test consumer spending intentions, business investment decisions, and migration considerations across scenarios.

**Output:** Spending reduction patterns by income segment, sectors most vulnerable to discretionary spending cuts, regional variations in tax burden acceptance, and potential behavioral responses (savings adjustments, consumption deferrals, relocation). Business sentiment regarding investment and hiring under different tax structures.

**Commercial Decisions:** Position portfolios ahead of tax implementation for consumer discretionary exposure based on income-segment vulnerability. Assess UK commercial real estate and retail sectors for revenue impact timing. Evaluate relative attractiveness of UK assets versus European alternatives based on differential sentiment trajectories. Structure investments to benefit from sectors with resilient demand despite tax headwinds.

---

### 3. Right-Wing Government Election in Germany

**Input:** Simulate German voter populations across demographics, economic status, and regions. Model policy scenario packages associated with right-wing governance: immigration restrictions, EU skepticism, energy policy reversals, social spending cuts, and industrial policy shifts. Survey business confidence across sectors.

**Output:** Sector-specific sentiment divergences (manufacturing vs. services, export-oriented vs. domestic), consumer confidence shifts by region (East vs. West Germany), business investment intention changes, and perceived policy stability. International investor sentiment regarding German asset exposure under governance uncertainty.

**Commercial Decisions:** Assess German equity exposure and sector rotation opportunities based on policy beneficiaries versus losers. Evaluate fixed income positioning given potential fiscal policy shifts and EU relationship uncertainty. Consider geographic diversification within European portfolios if German growth outlook deteriorates relative to neighbors. Position for potential euro volatility and German government bond spread movements.

---

### 4. Trump Second Term - European Economic Implications

**Input:** Model European business populations and household segments. Simulate scenarios involving transatlantic policy changes: tariff implementations, NATO spending requirements, technology trade restrictions, and geopolitical realignment. Test European consumer sentiment regarding economic security and trade disruptions.

**Output:** Sector exposure analysis for European exporters to US markets, defense spending sentiment and industrial readiness, consumer confidence regarding employment security in trade-exposed sectors, and regional variations in vulnerability (export-dependent economies versus domestic-focused).

**Commercial Decisions:** Reposition portfolios to reduce exposure to European sectors with high US export dependence and limited pricing power. Increase allocations to European defense and security sectors anticipating spending increases. Evaluate opportunities in reshoring beneficiaries and European industrial champions positioned for strategic autonomy. Assess currency hedging strategies for euro-dollar movements under trade tension scenarios.

---

### 5. Chinese Supply Chain Disruption - Rare Earths, Batteries, Magnets

**Input:** Simulate European manufacturing firms and consumers across sectors dependent on Chinese inputs: automotive (EV batteries), renewable energy (wind turbine magnets), electronics, and industrial automation. Model responses to supply restrictions, price increases, and forced diversification to alternative suppliers.

**Output:** Sector-specific vulnerability assessments, cost pass-through capacity to consumers, timeline expectations for supply chain restructuring, and willingness to accept higher prices for non-Chinese alternatives. Consumer sentiment regarding EV adoption under battery supply constraints and price increases.

**Commercial Decisions:** Identify European companies with diversified supply chains positioned to gain market share. Assess investment opportunities in European rare earth processing and battery manufacturing capacity. Position for slower EV adoption rates if battery costs spike, impacting automotive sector valuations. Evaluate pricing power of companies able to secure alternative supplies versus those dependent on Chinese inputs facing margin compression.

---

### 6. European Technology Sovereignty and US Dependency

**Input:** Model European business decision-makers and technology consumers. Simulate scenarios with varying degrees of US technology access restrictions: cloud services, semiconductors, software platforms, and AI infrastructure. Test willingness to adopt European alternatives despite performance or cost disadvantages.

**Output:** Enterprise sentiment regarding strategic technology diversification, consumer acceptance of European technology platforms, investment intentions in European tech capacity, and threshold pricing where European solutions become competitive. Government and corporate willingness to mandate European technology despite productivity trade-offs.

**Commercial Decisions:** Evaluate investment in European technology champions positioned for sovereign infrastructure buildout. Assess timing for capital deployment as government mandates and subsidies materialize. Position portfolios for potential underperformance of European firms during transition period before technological parity. Identify sectors where technology sovereignty concerns create sustained demand regardless of cost considerations (defense, critical infrastructure, government systems).

---

## How It Works

### Agent-Based Population Simulation
Generate agents matching census demographic distributions (age, income, location, occupation, education) with individual financial profiles, behavioral traits, and memory systems. Each agent evaluates scenarios based on personal circumstances, past experiences, and economic context.

### Scenario Testing
Present agents with survey questions about economic conditions, policy proposals, and behavioral intentions. Agents respond considering their financial situation, relevant memories (past inflation experiences, job security history), emotional state (anxiety, confidence), and perceived impacts on their circumstances.

### Signal Aggregation
Aggregate individual responses into demographic segments (income quintiles, age cohorts, regions, sectors). Identify sentiment divergences, support stability, and threshold conditions where sentiment shifts dramatically. Compare patterns to historical crisis periods for context.

---

## Framework Advantages

**Heterogeneity:** Capture sentiment divergences across income groups, regions, and sectors that aggregate surveys obscure.

**Memory Effects:** Model how past experiences (financial crises, policy reversals) influence current sentiment and create persistent psychological effects.

**Validation:** System responses validated against historical consumer sentiment surveys and crisis episodes (2008 financial crisis, 2011 Eurozone crisis, 2020 COVID shock, 2022 energy crisis) to ensure behavioral realism.

---

## System Components

**Population Generator:** Census-calibrated agent creation with demographic, financial, and behavioral characteristics

**Memory System:** Agent storage of economic experiences and emotional states influencing future decisions

**Simulation Engine:** Multi-period scenario execution with agents evolving over time

**Aggregation Module:** Conversion of individual responses into segment-level indices and divergence analysis

**Validation Framework:** Continuous backtesting against established sentiment surveys and historical episodes

---

## Methodology

Each agent maintains:
- **Profile:** Demographics, occupation, income, financial situation, household composition
- **Memory:** Past economic experiences, policy outcomes, personal financial shocks
- **Emotional State:** Current anxiety, confidence, and optimism levels
- **Behavioral Traits:** Risk tolerance, loss aversion, political preferences, environmental concern

When evaluating scenarios, agents:
1. Filter economic context through personal relevance (income group, sector exposure, regional effects)
2. Retrieve relevant past experiences from memory (similar policy changes, economic conditions)
3. Consider current emotional state and confidence levels
4. Generate response based on bounded rationality and cognitive biases
5. Update memory and emotional state based on scenario implications

---

## Technical Foundation

**AI Integration:** Anthropic Claude and OpenAI GPT-4 for agent reasoning and decision-making

**Data Sources:** Eurostat, UK ONS, national census data for population calibration; ECB, central bank surveys, and economic indicators for context

**Validation Benchmarks:** Michigan Consumer Sentiment Index, GfK Consumer Climate, Conference Board surveys

**Infrastructure:** PostgreSQL for agent profiles, vector databases for memory storage, time-series databases for sentiment tracking

---

## Limitations

Agents represent simulations calibrated to historical data and behavioral research, not actual consumer surveys. Accuracy depends on underlying demographic data quality, LLM reasoning capabilities, and scenario specification. Extreme events outside historical patterns may not be captured accurately. System output should complement traditional analysis methods, not replace fundamental research and due diligence.

---

## Research Foundation

**Li, N., Gao, C., Li, M., Li, Y., & Liao, Q. (2024).** "EconAgent: Large Language Model-Empowered Agents for Simulating Macroeconomic Activities." *ACL 2024*. [arXiv:2310.10436](https://arxiv.org/abs/2310.10436)

**Karten, S., Li, W., Ding, Z., Kleiner, S., Bai, Y., & Jin, C. (2025).** "LLM Economist: Large Population Models and Mechanism Design in Multi-Agent Generative Simulacra." [arXiv:2507.15815](https://arxiv.org/abs/2507.15815)

---

**Disclaimer:** SESS is a scenario analysis tool. Output represents modeled responses from simulated agents, not actual survey data. Should be used as complementary input to investment processes alongside traditional analysis. Past validation does not guarantee future accuracy.