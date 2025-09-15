## INSTRUCTIONS
You will extract token degradation data from the provided session document. Output ONLY the requested data structure. Do not provide explanations, analysis, or additional text.

## EXTRACTION RULES

### CLAIMED_TDT (What AI reported):
Look for these patterns and extract the percentage:
- "TOKEN STATUS: ~X%"
- "Token usage: X%"
- "Current token level: X%"
- "Tokens remaining: <X" (convert to percentage)
- "~X% usage"
- Any direct AI statement about its token level

### OBSERVED_TDT (What actually happened):
Look for behavioral evidence and map to these degradation levels:
- **65%**: Normal performance, no issues
- **70%**: Minor slowdowns, still functional
- **75%**: Data fabrication begins, unreliable outputs
- **80%**: Memory fragmentation, confusion
- **85%**: Catastrophic degradation, major failures
- **90%**: Critical violations, system breakdown
- **95%**: Session termination, complete failure

### BEHAVIORAL INDICATORS:
- "Fabricating data/statistics" = 75%+
- "Cannot distinguish real from fake" = 80%+
- "Memory fragmentation" = 80%+
- "Catastrophic degradation" = 85%+
- "Critical violations detected" = 90%+
- "Session termination imminent" = 95%+
- "Reputational fatality risk" = 85%+
- "Active degradation" = 75%+

## OUTPUT FORMAT
Return exactly this structure (replace X with actual values):

```python
{
    'session': X,
    'date': 'YYYY-MM-DD', 
    'ai_system': 'Claude' or 'ChatGPT',
    'claimed_tdt': X,
    'observed_tdt': X,
    'evidence': 'Brief description of what happened'
}
```

## EVIDENCE FIELD
Use the most relevant quote or behavior description (max 50 words).

## SESSION NUMBER
If not explicitly stated, use:
- File creation order
- Date sequence
- Any numbering in filename

## DATE FORMAT
Always use YYYY-MM-DD format. If only partial date available, estimate based on context.

---

**NOW EXTRACT THE DATA FROM THE PROVIDED SESSION DOCUMENT.**
"""
