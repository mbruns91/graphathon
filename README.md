# graphathon

A template repository for setting up an environment where nodes for a workflow using `pyiron_workflow` can be developed by different people in parallel.

Usage goes like so:
- the team sets up a dummy workflow using placeholder-versions of the involved nodes
- the team creates a repository using *this* repo as a template (especially anything located in `.github/` and `.ci_support/`)
- add dependencies to `.ci_support/environment.yml`!
- each dev opens a branch + PR for her work
- as soon as the `run_workflow` label is added to the PR, each push triggers workflow execution via actions.
- the updated notebook is uploaded as a github action artifact (Actions -> select CI run -> Artifacts). You may 
  - download (unzip) and view it locally
  - navigate to the directory `ci_output` and view theredered workflow directly in your browser. After each workflow execution, a link to this file is posted as a comment in the correspoinding PR.
