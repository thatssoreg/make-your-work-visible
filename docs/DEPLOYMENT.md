# Running and publishing the static release

## Use it immediately as a file

Open the generated `index.html` in a full browser. `artifact.html` starts directly in the integrated collection. Each file includes its own CSS, JavaScript, data, and reference text. There is no installation step for a participant. Send the actual file, not a path on your own machine.

## Publish only the reviewed output

A static host should publish `public/`. This directory contains the two self-contained HTML entry points and printable PDFs. It excludes the owner's untouched Artifact provenance, the job-board workbook, and any learner content. The PDF facilitator guide is included intentionally; remove it from that folder before publishing when only student materials should be public.

The repository being public does not itself enable a running site. GitHub Pages must be configured separately. A Vercel project must likewise be intentionally created and pointed at the output. No such hosting configuration is performed by this release.

Use a hosting plan that fits university work. Vercel's Hobby policy restricts its use to noncommercial personal projects; verify the current terms rather than assuming eligibility. GitHub Pages availability and source/site visibility depend on plan and configuration. These are hosting questions, not model-credit questions.

Official references:
- https://vercel.com/docs/limits/fair-use-guidelines
- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages

## Runtime costs and data

The app does not call a model or use an API key. Opening it cannot run the optional prompts against the owner's account. Choosing an external link opens another service, whose account, privacy, and pricing terms apply independently. Hosting bandwidth or build services can have separate limits or costs.

The card's optional browser storage is local to that browser/origin. Moving from a local file to a hosted URL will not automatically migrate it. Export/import is available for that purpose. Do not clear or relocate a student's actual project files as part of publishing this site.

## Verify after deployment

Check both entry points, relative PDF downloads, the content security policy, one route, a help reveal, card save/reload on that origin, and the browser Back button. Open a source link and confirm it is the expected external page. Confirm the intended people can open the site while signed out. Record the actual tested URL and commit; do not invent a live URL from the repository name.
