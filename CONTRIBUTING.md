# Contributing to ARASAKA

Accept the captain's GitHub invitation before cloning this private repository.
Follow the README setup for your operating system and use Python 3.12.

Start a small task in an issue, with an owner and a clear completion condition.
Check which files other teammates are editing before starting.

```text
git switch main
git pull --ff-only
git switch -c feature/describe-your-task
```

Make the change, then run the shared checks from the project root:

```text
python -m unittest discover -s tests -v
git status
git add path/to/changed-file
git commit -m "Describe the change"
git push -u origin feature/describe-your-task
```

Replace the branch and file names with your own. Open a pull request into
`main`, describe your result and validation, and ask the captain to review.
Merge after checks pass and review is complete. Use a new branch for each task.
Keep model reports, datasets, and screenshots out of a PR unless deliberately
needed; never add credentials, `.venv`, or private competition data.

Practice datasets in `data/` are synthetic. Work on copies and retain the
originals. Place competition work in `competition/` only after the real brief
arrives and organizer rules permit this kit. Team roles in `TEAM_PLAYBOOK.md`
are suggestions until agreed by the team.
