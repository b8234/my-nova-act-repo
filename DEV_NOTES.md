# Nova Act Exploration - Dev Branch Notes

This file documents my personal exploration of the Amazon Nova Act SDK.
The goal was to get hands-on with the framework, understand how agentic workflows are structured, and validate that the provided sample scripts run successfully.

---

## What I Did

- Cloned the Nova Act SDK repo and created a dedicated **dev branch** for my testing.
- Set up a local Python virtual environment in VS code.
- Added an `example.env` file with placeholder values for AWS and Nova Act variables.
- Successfully ran all sample scripts, including:
  - `order_salad.py` - simulated automated ordering workflow.
  - `s3_writer_example.py` - tested S3 logging and confirmed upload worked with environment variables.
  - Other samples - validated execution and output.

---

## Files I Added

- **`example.env`** -> template with placeholder environment variables (safe to share).
- **`DEV_NOTES.md`** -> this file, capturing setup steps and exploration notes.

---

## Purpose of This Branch

This branch serves as a personal sandbox to:

- Explore how Nova Act structures **atomic actions** (clicks, form fills, navigation).
- Observe how **deterministic Python scaffolding** complements probabilistic model calls.
- Connect learnings to **enterprise-scale orchestration challenges** I've solved in production (e.g., pipeline re-architecture, LLM workflow reliability).

---

## Next Steps

- Experiment with extending one of the sample scripts to add logging and monitoring.
- Continue documenting insights as I go deeper into agentic AI patterns.
