# Pull Request

## Description

<!-- Provide a brief description of the changes in this PR -->

## Type of Change

Please select the relevant option:

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🎨 Code style update (formatting, renaming)
- [ ] ♻️ Refactoring (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] ✅ Test update
- [ ] 🔧 Build configuration change
- [ ] 🔒 Security fix

## Related Issues

<!-- Link to related issues, e.g., "Fixes #123" or "Relates to #456" -->

Fixes #
Relates to #

## Changes Made

<!-- Provide a detailed list of changes -->

-
-
-

## Testing

<!-- Describe how you tested your changes -->

- [ ] All existing tests pass (`pytest tests/ -v`)
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have added tests for edge cases and boundary conditions

### Test Commands Run

```bash
pytest tests/ -v
pytest tests/ --cov=src/digipin
```

## Code Quality

- [ ] I have run `black src/digipin tests/` to format the code
- [ ] I have run `flake8 src/digipin tests/` and fixed any issues
- [ ] I have run `mypy src/digipin` for type checking
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas

## Specification Compliance

<!-- For changes to core encoding/decoding logic -->

- [ ] This change maintains 100% compliance with the DIGIPIN specification
- [ ] I have verified the change against the official technical document
- [ ] This change does not break backward compatibility
- [ ] N/A - This change does not affect specification compliance

### Specification Reference

<!-- If applicable, cite the section of the DIGIPIN spec this implements -->

Section:
Page:

## Documentation

- [ ] I have updated the README.md (if needed)
- [ ] I have updated DOCUMENTATION.md (if needed)
- [ ] I have updated the CHANGELOG.md
- [ ] I have added docstrings to all new functions/classes
- [ ] I have updated type hints

## Performance Impact

<!-- Describe any performance implications -->

- [ ] No performance impact
- [ ] Performance improved
- [ ] Performance degraded (please explain why this is acceptable)

### Benchmarks

<!-- If applicable, provide before/after performance metrics -->

```
Before:
After:
```

## Breaking Changes

<!-- If this is a breaking change, describe the impact and migration path -->

**Impact:**


**Migration Guide:**


## Screenshots / Examples

<!-- If applicable, add screenshots or code examples -->

```python
# Example usage of the new feature

```

## Checklist

- [ ] My code follows the contributing guidelines
- [ ] I have read the CODE_OF_CONDUCT
- [ ] I have added myself to the contributors list (if this is my first contribution)
- [ ] This PR is ready for review (remove "Draft" status if applicable)

## Additional Notes

<!-- Any additional information for reviewers -->


---

**Thank you for contributing to DIGIPIN-Py!** 🇮🇳
