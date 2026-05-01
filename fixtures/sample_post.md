# Why I Stopped Hiring VAs

Last quarter I spent $4,200 on a virtual assistant. She was great. But I still
spent two hours every Sunday writing her instructions for the week ahead. The
math caught up with me when I built an inbox-triage agent in 90 minutes that
did 80% of what she did, with no instruction-writing, no scheduling, no PTO.

Three things I learned. First, agents beat humans at deterministic repetition,
not creative work. Pick the boring tasks. Second, the cost guard matters more
than the agent itself; one runaway loop will eat a month of savings. Third,
agents are easier to fire than VAs (you just stop running them) which makes
the experiment cost much lower than people assume.

I'm not anti-VA. I'm anti-paying-someone-to-do-something-deterministic.

The agent I started with cost $0.04 per run, ran 3 times a day, and replaced
about 6 hours of weekly work. The VA cost $1,400/mo. You do the math.

What I'd tell anyone starting: don't build the orchestrator first. Build one
agent that solves one painful task. Live with it for a week. Then build the
next one.
