# Working with Branches

## 1. Make Sure You Are Up to Date
```bash
git checkout master
git pull origin master
```

## 2. Create a New Branch
```bash
git checkout -b branch-name
```

## 3. Work, Commit, and Push the Branch
```bash
# Do your changes
git add .
git commit -m "your message"
git push -u origin branch-name
```

## 4. Keep Your Branch Updated with master
```bash
git checkout branch-name
git merge master
```

## 5. Test Thoroughly Before Merging
Before merging back into master, make sure everything works:
- Functionality is equivalent or better than before.
- No regressions.
- Any new dependencies are tested and documented.

## 6. Open a Pull Request (PR)
- Push all changes.
- Go to GitHub.com → Open a pull request from `branch-name` into `master`.
- Optionally request a code review (even if self-review).

## 7. Merge After Review and Tests Pass
- Use **"Squash and merge"** for a clean single commit.
- Use **"Merge"** to preserve full commit history.

## 8. Delete the Branch (Optional but Recommended)
```bash
git branch -d branch-name
git push origin --delete branch-name
```

---

# What If I Am Working on a Branch and Want to Edit Something in master?

## Option 1: Stash Your Work (Safest and Cleanest)
```bash
git stash push -m "WIP: beam drawing logic"

# Switch to master
git checkout master
git pull origin master
# Make your changes
git add .
git commit -m "fix: corrected layer naming bug"
git push origin master

# Return to feature branch
git checkout branch-name
git stash pop
```

## Option 2: Commit Locally, Don’t Push Yet
```bash
# Commit your work
git add .
git commit -m "WIP: partial beam drawing implementation"

# Switch to master
git checkout master

# Return to your branch
git checkout branch-name
```

---

# Change Git User Info

## Global (affects all projects)
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

## Local (current project only)
```bash
git config user.name "Your Name"
git config user.email "your@email.com"
```

---

# Keeping Empty Folders in Git

Git does not track empty folders by default. If your project requires a folder to exist (e.g., `logs/` for log files), you can use a `.gitkeep` file to force Git to track it.

### ✅ Steps to Keep an Empty Folder Tracked:

1. Create the folder:
   ```bash
   mkdir logs
   ```

2. Add a `.gitkeep` file:
   ```bash
   touch logs/.gitkeep
   ```

3. Commit the `.gitkeep` file:
   ```bash
   git add logs/.gitkeep
   git commit -m "chore: keep logs folder in repo"
   ```

4. (Optional) Add a `.gitignore` in the folder to ignore runtime files like logs:
   ```
   # logs/.gitignore
   *
   !.gitkeep
   !.gitignore
   ```

### 📌 Why Not Just Use `*.log` in Root .gitignore?

Using `*.log` in your root `.gitignore` will ignore all `.log` files in the project — not just in `logs/`. To scope it better:
```gitignore
logs/*.log
!logs/.gitkeep
```

This way, you:
- ✅ Ignore only logs in the `logs/` folder
- ✅ Preserve `.gitkeep` so the folder stays in Git
- ✅ Avoid tracking generated logs, keeping your repo clean