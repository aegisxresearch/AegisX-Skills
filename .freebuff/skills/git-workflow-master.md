# Git Workflow Master

## Overview
Panduan Git advanced: branching strategies, rebase, cherry-pick, bisect, dan collaboration workflows.

---

## 🌿 Branching Strategies

### GitHub Flow (Recommended for most teams)
```
main ─────────────────────────────────────────▶
  │                                        ▲
  │                                        │
  └─▶ feature/user-auth ───────────────────┘
                    (PR → merge to main)
```

### GitFlow (For release-based projects)
```
main ─────────────────────────────────────────▶
  │                                        ▲
  ├──▶ develop ────────────────────────────┤
  │      │                          │      │
  │      └─▶ feature/login ────────┘      │
  │      │                          │      │
  │      └─▶ release/v1.0 ────────────────┘
  │                                   │
  └───▶ hotfix/critical-bug ──────────┘
```

### Trunk-Based Development
```
main ────●────●────●────●────●────●────▶
         │    │    │    │    │    │
         └─┐  └─┐  └─┐  └─┐  └─┐  └─┐
           └┐   └┐   └┐   └┐   └┐   └┐
            └┐   └┐   └┐   └┐   └┐   └┐
             └┐   └┐   └┐   └┐   └┐   └┐
              Short-lived branches (hours, not days)
```

---

## 🔀 Git Commands Cheat Sheet

### Interactive Rebase (Clean History)
```bash
# Squash last 3 commits
git rebase -i HEAD~3

# In editor:
pick abc1234 feat: add user model
squash def5678 fix: typo in user model
squash ghi9012 update tests
# Result: single clean commit
```

### Cherry-Pick (Select Specific Commits)
```bash
# Apply specific commit to current branch
git cherry-pick abc1234

# Cherry-pick multiple commits
git cherry-pick abc1234 def5678

# Cherry-pick a range
git cherry-pick abc1234..ghi9012
```

### Bisect (Find Bug Introduction)
```bash
# Start bisect
git bisect start
git bisect bad          # Current commit is bad
git bisect good v1.0    # This tag was good

# Git checks out commits automatically
# Test and mark as good/bad
git bisect good    # or
git bisect bad

# Result: finds exact commit that introduced bug
```

### Worktrees (Multiple Branches Simultaneously)
```bash
# Work on feature without stashing
git worktree add ../hotfix-branch hotfix/critical-bug
cd ../hotfix-branch
# Fix bug, commit, push

# Clean up
git worktree remove ../hotfix-branch
```

---

## 📝 Commit Message Convention

### Conventional Commits
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
| Type | Description | Example |
|------|-------------|---------|
| feat | New feature | feat(auth): add OAuth2 login |
| fix | Bug fix | fix(api): handle null response |
| docs | Documentation | docs: update README |
| style | Formatting | style: fix indentation |
| refactor | Code restructure | refactor(auth): extract validation |
| test | Add tests | test: add unit tests for User model |
| chore | Build/tooling | chore: update dependencies |

### Examples
```bash
git commit -m "feat(auth): implement JWT refresh token rotation"

git commit -m "fix(api): handle empty array in search endpoint

Closes #123"

git commit -m "refactor(db): optimize user query performance

- Add index on email column
- Use select_related for foreign keys
- Reduce query count from 5 to 1"
```

---

## 🔧 Useful Aliases

```bash
# Add to ~/.gitconfig
[alias]
  co = checkout
  br = branch
  ci = commit
  st = status
  lg = log --graph --oneline --decorate
  unstage = reset HEAD --
  last = log -1 HEAD
  visual = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
```

---

## 🛠️ Advanced Operations

### Amend Last Commit
```bash
# Change message
git commit --amend -m "New message"

# Add forgotten files
git add forgotten-file.txt
git commit --amend --no-edit
```

### Reset (Careful!)
```bash
# Soft: keep changes staged
git reset --soft HEAD~1

# Mixed: keep changes unstaged (default)
git reset HEAD~1

# Hard: discard all changes (DANGEROUS)
git reset --hard HEAD~1
```

### Stash (Temporary Storage)
```bash
# Stash changes
git stash push -m "WIP: login feature"

# List stashes
git stash list

# Apply stash
git stash apply stash@{0}

# Pop stash (apply + delete)
git stash pop
```

---

## 📋 Workflow Checklist

### Before Starting Work
- [ ] Pull latest from main
- [ ] Create feature branch
- [ ] Name branch descriptively

### During Development
- [ ] Commit often (atomic commits)
- [ ] Write clear commit messages
- [ ] Keep branches short-lived

### Before Merging
- [ ] Rebase on main (clean history)
- [ ] Resolve all conflicts
- [ ] Run tests
- [ ] Update documentation if needed

### Code Review
- [ ] Self-review PR
- [ ] Respond to feedback
- [ ] Squash if needed

---

## 📚 References
- https://git-scm.com/book/en/v2
- https://conventionalcommits.org/
- https://trunkbaseddevelopment.com/
