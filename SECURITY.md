# Security Policy

## Supported Versions

| Package | Version | Supported |
|---------|---------|-----------|
| digipinpy (Python) | 1.6.x | ✅ |
| digipinjs-lib (JavaScript) | 1.0.x | ✅ |

## Reporting a Vulnerability

**⚠️ DO NOT report security vulnerabilities through public GitHub issues.**

### Preferred Method
**GitHub Security Advisories:** https://github.com/DEADSERPENT/digipin/security/advisories/new

### Alternative (Email)
- Primary: samarthsmg14@gmail.com
- Secondary: hmrshivu@gmail.com

**Response Time:** Within 48 hours

### What to Include
- Type of issue (injection, overflow, XSS, etc.)
- Affected files/functions (with paths)
- Reproduction steps (detailed)
- Proof-of-concept (if available)
- Impact assessment

### Process
1. Acknowledgment (48 hours)
2. Investigation (5-7 days)
3. Regular updates
4. Coordinated disclosure
5. Credit in release notes (unless anonymous)

## Security Best Practices

### Python
```python
from digipin import encode, is_valid

# Validate input
if not is_valid(user_input):
    raise ValueError("Invalid DIGIPIN code")

# Safe encoding
def safe_encode(lat, lon):
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise ValueError("Invalid coordinates")
    return encode(lat, lon)
```

### JavaScript
```javascript
import { encode, isValid } from 'digipinjs-lib';

// Validate input
if (!isValid(userInput)) {
  throw new Error('Invalid DIGIPIN code');
}

// Safe encoding
function safeEncode(lat, lon) {
  if (lat < -90 || lat > 90 || lon < -180 || lon > 180) {
    throw new Error('Coordinates out of range');
  }
  return encode(lat, lon);
}
```

### API Security
- **Rate limiting** - Implement for public APIs
- **Input sanitization** - Escape output for web display
- **Dependency audits** - Run `pip-audit` (Python) or `npm audit` (JavaScript)

## Security Considerations

### Location Privacy
- DIGIPIN codes decode to approximate coordinates
- Consider privacy before sharing
- Use lower precision for less exact locations

### Not Security Issues
These are **by design**:
- Deterministic encoding (same coords = same code)
- Reversible decoding (feature, not bug)
- No built-in authentication (add at app layer)

### Report These
- Crashes from malformed input
- Memory leaks with large inputs
- Code injection vulnerabilities
- Invalid code generation

## Dependency Security

**Python:**
```bash
pip install pip-audit
pip-audit
```

**JavaScript:**
```bash
npm audit
npm audit fix
```

## Resources

- **Advisories:** https://github.com/DEADSERPENT/digipin/security/advisories
- **Issue Tracker:** https://github.com/DEADSERPENT/digipin/issues

## Contact

**Security Email:** samarthsmg14@gmail.com, hmrshivu@gmail.com
**GitHub:** https://github.com/DEADSERPENT/digipin/security
**Maintainers:** SAMARTHA H V, MR SHIVAKUMAR
