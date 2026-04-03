# GitHub Secrets Configuration Guide

This guide explains how to configure GitHub Secrets for the DIGIPIN repository workflows.

## Required Secrets

### 1. PYPI_TOKEN
**Purpose:** Publish Python package (digipinpy) to PyPI
**Required for:** `.github/workflows/publish.yml`

**Setup:**
1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `digipin-github-actions`
4. Scope: Select "Entire account" or limit to "digipinpy" project
5. Copy the token (starts with `pypi-`)
6. Add to GitHub: Settings → Secrets and variables → Actions → New repository secret
7. Name: `PYPI_TOKEN`
8. Value: Paste the token

### 2. CODECOV_TOKEN
**Purpose:** Upload test coverage reports
**Required for:** `.github/workflows/tests.yml`, `.github/workflows/unified-ci.yml`

**Setup:**
1. Go to https://codecov.io/gh/DEADSERPENT/digipin
2. Sign in with GitHub
3. Navigate to Settings → General
4. Copy the "Repository Upload Token"
5. Add to GitHub: Settings → Secrets and variables → Actions → New repository secret
6. Name: `CODECOV_TOKEN`
7. Value: Paste the token

### 3. NPM_TOKEN (Optional)
**Purpose:** Publish JavaScript package (digipinjs-lib) to NPM
**Required for:** Manual NPM publishing via Makefile

**Setup:**
1. Go to https://www.npmjs.com/settings/YOUR_USERNAME/tokens
2. Click "Generate New Token" → "Automation"
3. Copy the token (starts with `npm_`)
4. Add to GitHub: Settings → Secrets and variables → Actions → New repository secret
5. Name: `NPM_TOKEN`
6. Value: Paste the token

## Verifying Secrets

Check configured secrets at:
```
https://github.com/DEADSERPENT/digipin/settings/secrets/actions
```

You should see:
- ✅ PYPI_TOKEN
- ✅ CODECOV_TOKEN
- ✅ NPM_TOKEN (if using automated NPM publishing)

## Security Best Practices

### Token Permissions
- **PyPI:** Use project-scoped tokens when possible (limits blast radius)
- **NPM:** Use "Automation" tokens (read/publish only, no user modifications)
- **Codecov:** Token is read-only for the repository

### Token Rotation
Rotate tokens annually or immediately if:
- Team member with access leaves
- Token may have been exposed
- Security incident occurs

### Access Control
- Only repository owner (you) can view/edit secrets
- Workflows can only access secrets they explicitly reference
- Secrets are never exposed in logs or PR comments

## Emergency Procedures

### If Token is Compromised

**PyPI Token:**
1. Immediately revoke at https://pypi.org/manage/account/token/
2. Generate new token
3. Update `PYPI_TOKEN` secret in GitHub
4. Review recent PyPI releases for unauthorized changes

**NPM Token:**
1. Immediately revoke at https://www.npmjs.com/settings/tokens
2. Generate new token
3. Update `NPM_TOKEN` secret in GitHub
4. Check recent NPM package versions

**Codecov Token:**
1. Regenerate at https://codecov.io/gh/DEADSERPENT/digipin/settings
2. Update `CODECOV_TOKEN` secret in GitHub
3. Review coverage reports for anomalies

## Workflow Usage

### Automatic (on events)
```yaml
# .github/workflows/publish.yml
- name: Publish to PyPI
  env:
    TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
```

### Manual (workflow_dispatch)
Workflows can be triggered manually from:
```
https://github.com/DEADSERPENT/digipin/actions
```

Select workflow → "Run workflow" → Choose branch → Run

## Troubleshooting

### "Secret not found" error
- Verify secret name matches exactly (case-sensitive)
- Check secret exists at repository settings
- Ensure workflow has correct reference: `${{ secrets.SECRET_NAME }}`

### PyPI publish fails with 403
- Token may be expired or revoked
- Regenerate PyPI token and update secret

### Codecov upload fails
- Token may be incorrect
- Verify token at Codecov settings
- Check network connectivity in workflow logs

## Additional Resources

- **GitHub Secrets Docs:** https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **PyPI API Tokens:** https://pypi.org/help/#apitoken
- **NPM Access Tokens:** https://docs.npmjs.com/about-access-tokens
- **Codecov Upload:** https://docs.codecov.com/docs/quick-start

## Contact

**Security Issues:** See [SECURITY.md](../../SECURITY.md)
**Maintainer:** @DEADSERPENT
