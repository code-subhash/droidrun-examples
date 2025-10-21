## DroidRun Examples

A small collection of runnable, agent-driven Python projects. Each folder contains a focused workflow with its own entrypoint, data, and logs.


### Projects
> Note: the examples given are based on droidrun version 0.4.0+. To see examples of older version see the `legacy/` folder.

- **LinkedInJobsScraper**
	- Agentic workflow that searches LinkedIn for roles, evaluates matches, and prepares tailored applications.
	- Stores results in `jobs/`, uses sample configs like `candidate_data.json`, and records run histories under `trajectories/`.

- **LinkedInLeads**
	- End-to-end lead discovery and enrichment for LinkedIn companies and roles.
	- Scrapes company pages, generates role hypotheses, saves outputs in `data/companies/`, and logs runs in `trajectories/`.

- **TwitterPost**
	- Finds trending topics, drafts posts, and generates images to publish on X/Twitter.
	- Includes agents for trend mining, content creation, image generation, and posting, with example assets under `images/` and run logs in `trajectories/`.




### Learn More

To learn more about Droidrun, take a look at the following resources:

- [Droidrun Documentation](https://docs.droidrun.ai/v3/overview) - learn about Droidrun features and references
- [Benchmark](https://droidrun.ai/benchmark/) - Our latest benchmark scores.

You can check out [the Droidrun GitHub repository](https://github.com/droidrun/droidrun) - your feedback and contributions are welcome!

### Contributing

We welcome fixes, docs, and new example projects.

- See the full guidelines in [`contribution.md`](./contribution.md).
- Keep examples self-contained with `main.py`, `requirements.txt`, and an `agents/` folder.
- Include a short README in any new example and sample data/assets if needed.
- Include a demo video which describes what you created.