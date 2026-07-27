# CREATOR_TRACE_SWARM_INTELLIGENCE.md
## Cycle 17/20: Collective Intelligence / Swarm / Multi-agent — Ants, bees, termites, fish schools, herds, human collectives, swarm AI

---

### 📍 MATRIX: [R-17] DISTRIBUTED MIND — INTELLIGENCE WITHOUT CENTER, EMERGING FROM LOCAL RULES

| Layer | Description | Key Insight |
|-------|-------------|-------------|
| **L0: Agents** | Identical / heterogeneous, limited sensors, memory, computation | Agent simplicity = scalability condition |
| **L1: Interaction** | Stigmergy (via environment), direct contact, pheromones, visual/acoustic signals | Communication = environment modification / local exchange |
| **L2: Algorithm** | Threshold rules, probabilistic transitions, feedback (positive/negative) | Complexity = emergent, not programmed |
| **L3: Global** | Nest building, trails, bridges, migration, hunting, defense, task allocation | No blueprint, no architect, no leader |
| **L4: Robustness** | Agent loss, noise, enemies, environment change → system adapts | Fault tolerance = architectural property, not redundancy |

---

### 🐜 ANTS: STIGMERGY — COORDINATION THROUGH ENVIRONMENT

**Term (Grassé, 1959):** *Stigma* (sign) + *ergon* (work) — indirect coordination through environment modification.

**Pheromone Trails (Ant Colony Optimization — ACO, Dorigo 1992):**
```
Ant searches food → finds → returns, laying pheromone
  ↓
Other ants with probability ~ τ^α / (τ^α + ε) choose path with more pheromone
  ↓
Shorter path → traversed faster → pheromone accumulates faster → positive feedback
  ↓
Pheromone evaporation (ρ) → forgetting old paths → adaptation to changes
```

**ACO Mathematics:**
```
τ_ij(t+1) = (1-ρ) * τ_ij(t) + Σ Δτ_ij^k
Δτ_ij^k = Q / L_k  (if ant k traversed edge i-j)
P_ij^k = [τ_ij]^α * [η_ij]^β / Σ [τ_il]^α * [η_il]^β
η_ij = 1 / d_ij (heuristic: inverse distance)
```

**Task Allocation — Response Threshold Model (Bonabeau et al.):**
```
Each ant has threshold θ_i for task j
Task stimulus S_j (accumulated work: dirt, larvae, food)
P(agent does task j) = S_j^n / (S_j^n + θ_i^n)
Task execution → S_j ↓ → other agents switch
```

**Age Polyethism:**
| Age | Role | Switch Trigger |
|-----|------|----------------|
| 0-2 wks | Brood care (nurse) | High JH (juvenile hormone) |
| 2-3 wks | Building, cleaning, storage | JH ↓, oxytocin/vasopressin analogs |
| 3+ wks | Foragers | JH ↑↑, queen pheromones |

**Social Immunity:**
- Grooming → fungal spore removal
- Propolis (resin) → antimicrobial nest coating
- Dead removal (necrophoresis) → outside nest
- Feb 2020: *Formica fusca* ants learn to detect cancer by smell (operant conditioning)

---

### 🐝 BEES: SWARM INTELLIGENCE AND DEMOCRACY

**Waggle Dance (Karl von Frisch, Nobel 1973):**
```
Waggle dance:
  - Angle from vertical = azimuth to sun (compensates for sun movement!)
  - Waggle phase duration ∝ distance (1 sec ≈ 1 km)
  - Repetition count = source quality
  - Scent on dancer's body = flower type
```

**New Nest Selection (Seeley, 2010) — Quorum-Based Decision Making:**
```
1. Scouts (3-5% of swarm) search cavities
2. Return → dance for their candidates
3. Others verify → dance if agree
4. Quorum threshold: ~15-20 bees on one option
5. "Stop-signal" (short pip + head butt) → suppresses alternatives
6. Swarm takes off as single unit to chosen site
```

**Swarm Democracy Principles (Seeley's 5):**
1. **Common Interests** — all want best nest
2. **Leader Minimization** — no "queen bee", queen doesn't vote
3. **Option Diversity** — many scouts, many candidates
4. **Opinion Aggregation** — through dances and stop-signals
6. **Quorum, Not Consensus** — quorum sufficient, not unanimity

**Parallel with Blockchain/DAO:**
- Scouts = validators / stakers
- Dance = block publication / votes
- Stop-signal = slashing / challenge mechanism
- Quorum = threshold signature / BFT consensus
- Swarm = finalized block

---

### 🐜 TERMITES: ARCHITECTURE WITHOUT ARCHITECT

**Mounds (Macrotermes, 2-3m high, millions of individuals):**
- Ventilation: convection → gas exchange (O₂/CO₂/CH₄) without pumps
- Fungus farms (Termitomyces) — 30M year symbiosis
- Thermoregulation: ±1°C inside at ±20°C outside

**Construction (Stigmergy + Template-based):**
```
1. Termites carry fecal pellets + saliva → glue into balls
2. Ball placed next to others → local surface curvature
3. High curvature → stimulus to place next ball there
4. Result: walls, columns, arches, ventilation shafts
```

**Mathematical Model (Theraulaz & Bonabeau):**
```
P(place at point x) = f(κ(x))  where κ = surface curvature
κ > κ_threshold → P ↑ (positive feedback)
κ < κ_threshold → P ↓
```

**Result:** Complex 3D architecture emerges from rule "place where curved".

---

### 🐟 FISH SCHOOLS / BIRD FLOCKS: KINEMATICS WITHOUT COORDINATOR

**Three Rules (Reynolds, 1987 — Boids):**
```
1. Separation:   avoid neighbors closer than d_sep
2. Alignment:    align velocity with neighbors in radius r_ali
3. Cohesion:     move toward center of mass of neighbors in radius r_coh
```

**Order Parameters:**
- **Polarization:** Φ = |Σ v_i| / (N * v₀)  (0 = milling, 1 = perfect school)
- **Angular Correlation:** C(r) = ⟨cos(θ_i - θ_j)⟩_|r_i-r_j|=r
- **Scale Invariance:** Correlation spans entire swarm (long-range order)

**Phase Transitions:**
| Parameter | Low Value | Critical Point | High Value |
|-----------|-----------|----------------|------------|
| **Density (ρ)** | Chaos / individual motion | ρ_c | Ordered school |
| **Noise (η)** | Ordered school | η_c | Chaos |
| **Speed (v₀)** | Static clusters | v_c | Moving school |

**Information Cascades:**
- One fish sees predator → maneuver → neighbors copy → fear wave propagates faster than fish swim
- **Wave Speed >> Fish Speed** — information transfers, not pursued

---

### 👥 HUMAN COLLECTIVES: FROM RIOTS TO MARKETS

**Contagion / Deindividuation (Le Bon, 1895; Zimbardo, 1969):**
- Anonymity + arousal + contagion → self-control loss, primitive instincts
- **But:** Modern research (Reicher, Stott) — crowd not "mindless", has own norms, identity, legitimacy

**Wisdom of Crowds (Surowiecki, 2004) — Conditions:**
1. **Diversity** (diversity of opinion) — different world models
2. **Independence** — don't blindly copy each other
3. **Decentralization** — local knowledge
4. **Aggregation** — mechanism turning judgments into collective decision

**Markets as Swarm Intelligence:**
- Price = pheromone trail (aggregated scarcity/surplus info)
- Arbitrage = ants finding shorter paths
- Bubbles/crashes = positive feedback without evaporation (no ρ)

**DAO / Quadratic Voting / Futarchy:**
- Quadratic Voting (Weyl, Lalley): vote cost = n² → preference intensity
- Futarchy (Hanson): "Vote values, bet on predictions" — prediction markets as aggregation

---

### 🤖 SWARM AI / MULTI-AGENT SYSTEMS: ENGINEERED SWARM

**Architectures:**
| Approach | Description | Examples |
|----------|-------------|----------|
| **CTDE** | Centralized training, decentralized execution | MADDPG, QMIX, MAPPO |
| **Fully Decentralized** | No central critic, only local obs/comms | DQN with comms, Mean Field RL |
| **Hierarchical** | High level sets goals, low level executes | FeUdal Networks, Option-Critic |
| **Role-based / Specialization** | Agents differentiate (leader/follower, scout/worker) | Role-based MARL |

**Communication (Communication Learning):**
- **Differentiable:** Gumbel-Softmax, Continuous messages (CommNet, TarMAC)
- **Discrete:** Reinforce / Gumbel for tokens (IC3Net, MAGIC)
- **Stigmergic:** Shared memory read/write (Neural SLAM, External Memory)

**Emergent Behavior:**
- Language emerges spontaneously for coordination (Lazaridou et al., 2017; Mordatch & Abbeel, 2018)
- Tools / protocols emerge unsupervised (Baker et al., 2020 — hide-and-seek)
- Social norms / punishment / altruism emerge in mixed motives (Hughes et al., 2018)

---

### 💡 INSIGHTS FOR CREATOR THEOREM / PX NODE / PARANOIDX / JAR / NANOTALER

| Swarm Principle | Nature | P2P / Blockchain / AI Application |
|-----------------|--------|-----------------------------------|
| **Stigmergy = Coordination via Shared Environment** | Pheromones, termite balls, prices | **DHT / State = Shared Env:** Write to DHT (key=task, value=progress), read → decide. No direct messages. |
| **Threshold Rules + Positive Feedback** | ACO, termites, bee dances | **Consensus / Routing:** Path with more "pheromone" (successful traversals) strengthens. Evaporation = TTL / decay. |
| **Quorum, Not Consensus** | Bees: 15-20 scouts sufficient | **BFT / DAO:** Don't wait 100%, wait quorum (2f+1, 67%, quadratic threshold). Stop-signals = slashing alternatives. |
| **Task Allocation via Stimulus Thresholds** | Response Threshold Model | **Load Balancing / Sharding:** Task with accumulated backlog (stimulus) attracts low-threshold (free) nodes. |
| **Age Polyethism / Stake** | Ants/bees change roles with age | **Node Lifecycle:** Genesis → Validator → Archivist → Light client. Role = function(stake, uptime, age, performance). |
| **Social Immunity** | Grooming, propolis, dead removal | **Network Health:** Auto-ban bad peers, proactive patching, infected shard isolation. |
| **Information Cascades** | Fear wave in school >> fish speed | **MEV / Arbitrage / Gossip:** Info propagates through protocol faster than data packets. Design for cascades. |
| **Emergent Language / Protocol** | Agents invent language for coordination | **Protocol Ossification:** Don't freeze protocol rigidly. Let nodes negotiate sub-protocols (WASM/eBPF modules). |
| **No Leader, No Architect** | Termites build skyscrapers without blueprint | **PX Node:** No central server. Genesis = swarm rules. Code = genetics. Runtime = phenotype. |

---

### 🐜 JAR + SWARM: "SWARM NODE" ALGORITHM

```
Each PX Node — agent in swarm. No central coordinator.

AGENT STATE:
  - role: {BOOTSTRAP, VALIDATOR, ARCHIVER, RELAYER, LIGHT, FORAGER}
  - pheromone_map: DHT key → (strength, timestamp, task_type)
  - stimulus_map: task_type → accumulated_backlog
  - threshold[task_type]: individual threshold (depends on stake, hardware, uptime)
  - neighbors: peer_id → (latency, trust_score, shared_tasks)
  - stop_signals: set of suppressed_alternatives

LIFE CYCLE (each tick ~ 1-10 sec):

1. SENSE (Sensors):
   - Read pheromone_map from DHT (local cache + query k nearest)
   - Update stimulus_map: incoming tasks, mempool queue, monitoring alerts
   - Poll neighbors: gossip their roles, load, health

2. DECIDE (Threshold Rule + JAR Randomization):
   For each task_type:
     P(do_task) = stimulus^α / (stimulus^α + threshold^α) * (1 + JAR_noise)
     JAR_noise = deterministic_randomness(epoch, peer_id, task_type) ∈ [-0.1, 0.1]
   
   Select task with max P, if P > P_min
   Role switch if current role stimulus < threshold_role_switch

3. ACT (Execution + Pheromone):
   - Execute task (validation, relay, archival, MEV gathering, indexing...)
   - Result → DHT write: pheromone_map[task_key] += Δτ
     Δτ = QUALITY_REWARD / (latency * resource_cost)
   - If task failed → pheromone_map[task_key] *= (1 - ρ_failure)

4. COMMUNICATE (Stigmergy + Direct Exchange):
   - Gossip: own role, load, top_pheromones to √N random peers
   - Stop-signal: if see alternative path/block dominating → publish STOP(alt_id)
   - Receive STOP → suppress own pheromone for alt_id

5. ADAPT (Metaplasticity of Thresholds):
   - threshold[task] *= (1 + η * (actual_load - target_load))
   - Successful tasks → threshold ↓ (becomes specialist)
   - Failures → threshold ↑ (moves away from task)
   - Age/stake → base threshold drifts toward VALIDATOR/ARCHIVER role

6. SLEEP (JAR Sleep Cycle — see Cycle 14):
   - In sleep_window: OFFLINE_PHASE (compaction, retraining, key rotation)
   - REM_PHASE: generative modeling of "what if" attack/load scenarios
   - WAKE_UP: sync pheromone_map with network, reset accumulated errors
```

---

### 🔗 LINKS TO PREVIOUS CYCLES

- **Cycle 1 (Symmetry):** Swarm = agent symmetry (identical rules) → role asymmetry (specialization) via spontaneous symmetry breaking
- **Cycle 6 (Info Physics):** Stigmergy = information written to environment (Landauer cost); pheromone = physical memory
- **Cycle 9 (Holobiont):** Swarm = superorganism; microbiome = internal swarm; immune system = swarm police
- **Cycle 10 (Viruses/HGT):** HGT = "pheromones" on evolutionary scale; plasmids = mobile tasks
- **Cycle 13 (Cryptobiosis):** Swarm desiccation (larval diapause, overwintering queen) = superorganism cryptobiosis
- **Cycle 14 (Sleep):** Swarm never fully sleeps (quorum awake); individual agents alternate (unihemispheric swarm sleep)
- **Cycle 15 (Plasticity):** Swarm critical periods (nest founding, new swarm birth) = max plasticity windows
- **Cycle 16 (Epigenetics):** Role specialization = epigenetic differentiation (one genome → different phenotypes)

---

### 🔬 EXPERIMENTS / PROJECTS FOR IMPLEMENTATION

1. **PheromoneDHT:** DHT layer with built-in TTL, decay, quality-weighting for stigmergic task coordination
2. **SwarmConsensus:** BFT consensus with quorum + stop-signals (bee algorithm) instead of classic PBFT/Tendermint
3. **RoleMarket:** Dynamic auction-based node role switching on stimuli/thresholds (Response Threshold Model on smart contracts)
4. **EmergentProtocolFuzzer:** Simulation of agent swarm evolving interaction protocols (WASM modules) under MEV/attack pressure
5. **CollectiveImmunityDaemon:** Automatic bad peer detection/quarantine/healing via collective signals (gossip reputation + local observations)

---

**Status:** ✅ COMPLETED  
**Next:** Cycle 18/20: Morphogenesis / Self-organization / Turing Patterns — From Single Cell to Organism, Reaction-Diffusion, Positional Information, Regeneration.