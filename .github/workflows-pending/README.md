# ⚠️ Action required: move this workflow into place

This folder holds a GitHub Actions workflow that could **not** be committed to its
final location (`.github/workflows/`) by the automation agent, because the token
available to the agent lacks GitHub's `workflow` scope. GitHub refuses any push
that creates or edits files under `.github/workflows/` without that scope.

To activate automatic tag indexing, move the file into place with a credential
that has the `workflow` scope (your normal GitHub login in the web UI works):

```bash
git mv .github/workflows-pending/generate-tag-index.yml .github/workflows/generate-tag-index.yml
git rm .github/workflows-pending/README.md   # optional cleanup
git commit -m "Activate automatic tag indexing workflow"
git push
```

Or, in the GitHub web UI: open the file, copy its contents, and create a new file
at `.github/workflows/generate-tag-index.yml` with the same contents.

Once the file lives at `.github/workflows/generate-tag-index.yml`, pushes to `main`
that touch `LOGS/**` or `concepts/**` will regenerate `tags/` automatically.
