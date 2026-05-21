# Empathy Map — Senior Leaders Navigating AI

**Version:** 1.0  
**Date:** 2026-05-21  
**Scope:** Senior organisational leaders responsible for ensuring their organisation takes the right actions with AI  
**Structure:** One shared map with C-suite / Function Head splits where perspectives diverge  

---

## Personas

| Dimension | Detail |
|---|---|
| **Persona A** | C-suite: CEO, COO, CDO, CTO |
| **Persona B** | Function heads: CPO, VP Product, VP Engineering |
| **Org size** | Enterprise (1,000+) and Mid-market (100–1,000) |
| **Primary trigger** | Fear of falling behind — competitors shipping AI, board asking questions |
| **Primary info sources** | LinkedIn, newsletters, McKinsey reports, a16z posts, curated exec feeds |

---

## Quadrant 1 — THINK & FEEL
*Inner emotional world — what occupies their mind beneath the surface*

**Shared:**
- "Am I making the right bets, or will I look foolish in 18 months?"
- Anxiety that AI will expose capability gaps in the organisation before they've had time to fix them
- Pride at stake — their reputation is built on reading markets correctly

**C-suite:**
- Guilt about not yet having a coherent AI narrative for the board
- Fear of being outmaneuvered by a competitor who moves faster *and* smarter

**Function heads:**
- "My team is looking to me for direction and I don't fully have it yet"
- Caught between executive pressure to "do AI" and the engineering/product reality of what's actually deliverable
- Fear of shipping something that embarrasses the company or locks them into the wrong stack

---

## Quadrant 2 — SEE
*What they observe in their environment — media, peers, org*

**Shared:**
- Competitors announcing AI features (even superficial ones get press)
- LinkedIn and inboxes full of "AI transformation" stories where it's impossible to separate signal from hype
- New models and tools arriving faster than they can evaluate them
- Their own teams running ad hoc AI experiments without coordination

**C-suite:**
- Board decks with slide 4: "What is our AI strategy?"
- Other CEOs at conferences claiming their transformation is ahead of schedule

**Function heads:**
- Engineers who want to use every new tool the moment it ships
- Product backlogs filling with AI feature requests nobody has prioritised
- Junior PMs and engineers who know more about the latest models than they do

---

## Quadrant 3 — HEAR
*What they're being told — by board, team, peers, media*

**Shared:**
- "We need to move faster on AI"
- "What's our moat once everyone has access to the same models?"
- Contradictory advice from every direction: build vs. buy, which model, which use case first
- "Everything changed again" — every major model release resets the conversation

**C-suite:**
- Board: "What are we doing about AI?" (asked more urgently each quarter)
- Investors: "Your competitors just raised for an AI play"
- Advisors and consultants: high-level frameworks that don't translate into decisions
- Peers at conferences: confident-sounding takes that feel hollow on closer inspection

**Function heads:**
- Engineers: "We should be using [latest model/tool]"
- Their boss: "Why aren't we shipping AI features yet?"
- Customers: mixed signals — some excited, some skeptical, most just waiting to see
- Vendors: every demo looks impressive, none of them look like production

---

## Quadrant 4 — SAY & DO
*What they say publicly and how they behave — including what they won't admit*

**Shared:**
- SAY: "AI is a top strategic priority for us this year"
- DO: Attend AI summits, roundtables, and briefings — actively hunting for clarity
- DON'T: Admit openly that they're uncertain or behind

**C-suite:**
- SAY: "We're evaluating our options carefully" (often a stall)
- DO: Commission a task force or bring in consultants to buy time and cover
- DO: Make a symbolic AI hire (Chief AI Officer) to signal intent to the market

**Function heads:**
- SAY: "We're being deliberate about where AI adds real value"
- DO: Run safe, low-visibility experiments to generate something to show
- DO: Build business cases upward while quietly managing team expectations downward
- DON'T: Push back visibly on executive AI mandates even when privately skeptical

---

## Quadrant 5 — PAINS
*Fears, frustrations, and obstacles*

**Shared:**
- Information overload with no signal — new models, tools, and vendors arrive faster than they can evaluate
- No clear framework for prioritising which AI use cases to pursue first
- Impossible to tell real competitive AI moves from marketing theatre
- Speed pressure creates shortcuts that accumulate as technical and organisational debt

**C-suite:**
- Making a large public commitment before the strategy is solid
- Not knowing enough to evaluate what their own teams are telling them
- Board and investor credibility on the line if AI bets don't pay off
- Organisational resistance when pushing AI transformation downward

**Function heads:**
- Blamed for slow execution when the real problem is unclear direction from above
- Vendor lock-in from rushed decisions made under pressure
- Teams burning out on AI experiments that never ship
- Gap between what models can do in demos vs. in production at scale
- Difficulty measuring ROI in a way that satisfies finance

---

## Quadrant 6 — GAINS
*What success looks and feels like*

**Shared:**
- A clear, defensible point of view on where AI creates value in their specific business
- Confidence to speak credibly about AI — to board, team, press, and peers
- A prioritisation framework that doesn't require tracking every new development

**C-suite:**
- A narrative: "Here's where we're going and why" — for investors, board, and press
- Visible, credible progress that doesn't bet the company
- Being seen as the leader who "got AI right" while peers stumbled or overcorrected

**Function heads:**
- A clear mandate from above with enough room to execute
- Concrete decision criteria: build vs. buy, which use cases first
- Something real shipped — evidence-based wins to point to
- Team retained and motivated, not poached by AI-native companies
- A way to translate executive pressure into a roadmap that's actually deliverable

---

## Machine-Readable JSON

```json
{
  "empathy_map": {
    "title": "Senior Leaders Navigating AI",
    "version": "1.0",
    "date": "2026-05-21",
    "personas": {
      "A": "C-suite: CEO, COO, CDO, CTO",
      "B": "Function heads: CPO, VP Product, VP Engineering"
    },
    "org_size": ["Enterprise (1,000+)", "Mid-market (100–1,000)"],
    "primary_trigger": "Fear of falling behind — competitors shipping AI, board asking questions",
    "primary_info_sources": ["LinkedIn", "Newsletters", "McKinsey reports", "a16z posts", "Curated exec feeds"],
    "quadrants": {
      "think_and_feel": {
        "shared": [
          "Am I making the right bets, or will I look foolish in 18 months?",
          "Anxiety that AI will expose capability gaps in the organisation before they've had time to fix them",
          "Pride at stake — reputation built on reading markets correctly"
        ],
        "c_suite": [
          "Guilt about not yet having a coherent AI narrative for the board",
          "Fear of being outmaneuvered by a competitor who moves faster and smarter"
        ],
        "function_heads": [
          "My team is looking to me for direction and I don't fully have it yet",
          "Caught between executive pressure to do AI and the engineering/product reality of what's actually deliverable",
          "Fear of shipping something that embarrasses the company or locks them into the wrong stack"
        ]
      },
      "see": {
        "shared": [
          "Competitors announcing AI features — even superficial ones get press",
          "LinkedIn and inboxes full of AI transformation stories where it's impossible to separate signal from hype",
          "New models and tools arriving faster than they can evaluate them",
          "Their own teams running ad hoc AI experiments without coordination"
        ],
        "c_suite": [
          "Board decks asking: What is our AI strategy?",
          "Other CEOs at conferences claiming their transformation is ahead of schedule"
        ],
        "function_heads": [
          "Engineers who want to use every new tool the moment it ships",
          "Product backlogs filling with AI feature requests nobody has prioritised",
          "Junior PMs and engineers who know more about the latest models than they do"
        ]
      },
      "hear": {
        "shared": [
          "We need to move faster on AI",
          "What's our moat once everyone has access to the same models?",
          "Contradictory advice: build vs. buy, which model, which use case first",
          "Everything changed again — every major model release resets the conversation"
        ],
        "c_suite": [
          "Board: What are we doing about AI? — asked more urgently each quarter",
          "Investors: Your competitors just raised for an AI play",
          "Advisors and consultants: high-level frameworks that don't translate into decisions",
          "Peers at conferences: confident-sounding takes that feel hollow on closer inspection"
        ],
        "function_heads": [
          "Engineers: We should be using the latest model/tool",
          "Their boss: Why aren't we shipping AI features yet?",
          "Customers: mixed signals — some excited, some skeptical, most just waiting to see",
          "Vendors: every demo looks impressive, none of them look like production"
        ]
      },
      "say_and_do": {
        "shared": {
          "say": ["AI is a top strategic priority for us this year"],
          "do": ["Attend AI summits, roundtables, and briefings — actively hunting for clarity"],
          "dont": ["Admit openly that they're uncertain or behind"]
        },
        "c_suite": {
          "say": ["We're evaluating our options carefully — often a stall"],
          "do": [
            "Commission a task force or bring in consultants to buy time and cover",
            "Make a symbolic AI hire — Chief AI Officer — to signal intent to the market"
          ]
        },
        "function_heads": {
          "say": ["We're being deliberate about where AI adds real value"],
          "do": [
            "Run safe, low-visibility experiments to generate something to show",
            "Build business cases upward while quietly managing team expectations downward"
          ],
          "dont": ["Push back visibly on executive AI mandates even when privately skeptical"]
        }
      },
      "pains": {
        "shared": [
          "Information overload with no signal — new models, tools, and vendors arrive faster than they can evaluate",
          "No clear framework for prioritising which AI use cases to pursue first",
          "Impossible to tell real competitive AI moves from marketing theatre",
          "Speed pressure creates shortcuts that accumulate as technical and organisational debt"
        ],
        "c_suite": [
          "Making a large public commitment before the strategy is solid",
          "Not knowing enough to evaluate what their own teams are telling them",
          "Board and investor credibility on the line if AI bets don't pay off",
          "Organisational resistance when pushing AI transformation downward"
        ],
        "function_heads": [
          "Blamed for slow execution when the real problem is unclear direction from above",
          "Vendor lock-in from rushed decisions made under pressure",
          "Teams burning out on AI experiments that never ship",
          "Gap between what models can do in demos vs. in production at scale",
          "Difficulty measuring ROI in a way that satisfies finance"
        ]
      },
      "gains": {
        "shared": [
          "A clear, defensible point of view on where AI creates value in their specific business",
          "Confidence to speak credibly about AI — to board, team, press, and peers",
          "A prioritisation framework that doesn't require tracking every new development"
        ],
        "c_suite": [
          "A narrative: Here's where we're going and why — for investors, board, and press",
          "Visible, credible progress that doesn't bet the company",
          "Being seen as the leader who got AI right while peers stumbled or overcorrected"
        ],
        "function_heads": [
          "A clear mandate from above with enough room to execute",
          "Concrete decision criteria: build vs. buy, which use cases first",
          "Something real shipped — evidence-based wins to point to",
          "Team retained and motivated, not poached by AI-native companies",
          "A way to translate executive pressure into a roadmap that's actually deliverable"
        ]
      }
    }
  }
}
```
