# How could a music app evaluate its recommendations?

**Status:** Illustrative measurement brief. No usage data has been collected and no experiment has been run.

## Question
How could a music app judge whether recommendations are useful, beyond counting plays?

## Purpose and contribution
This brief proposes three candidate measures, identifies the events each would require, and records limitations. It is a planning artifact created for the Make Your Work Visible workshop. It is not analysis of Spotify, Apple Music, or any other service.

## Candidate measures

| Candidate | Possible definition | Data needed | Important limitation |
| --- | --- | --- | --- |
| Listening beyond a chosen threshold | Share of recommendation starts listened to beyond a defined duration | Start, duration, recommendation origin, and autoplay status | Background listening and autoplay can look like interest. The threshold needs a reason. |
| Saving a recommended track | Share of distinct recommended tracks a listener saves within a defined window | Recommendation impressions, track IDs, save events, and timestamps | A listener may enjoy music without saving it. Repeat recommendations need a counting rule. |
| Returning by choice | Share of listeners who intentionally return to recommended tracks within a defined window | Listener/track events, timestamps, and a way to distinguish intentional selection | A return might reflect familiarity rather than discovery; event data may not capture intent. |

## Decisions still needed
Define the feature and decision before choosing a primary measure. Agree on eligible listeners, counting units, observation windows, and which behaviors can actually be observed. Ask what qualitative feedback would add and what data use is permitted.

## What this does not establish
The measures are proposals. They have not been validated against user satisfaction, and they do not show that any service is better than another. This brief does not establish causation, improvement, or business impact.

## A next step
Ask a product-analytics practitioner to critique the definitions and assumptions. Then revise one measure before requesting or collecting data.

## Inspiration and attribution
Figma’s Data Science Intern (2027) posting includes choosing meaningful measures and connecting product analysis to decisions. The music-app example is the workshop author's adaptation, not a Figma task or an analysis of Figma data.
Source: https://job-boards.greenhouse.io/figma/jobs/6178857004 (reviewed October 6, 2026).

If you adapt this teaching example, acknowledge the supplied brief and describe your own changes separately.
