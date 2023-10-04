from ..common.config import LANGUAGE


def code_review_messages(code: str, prior_conversation: list[dict[str, str]] = None) -> list[dict[str, str]]:
    system = "You are a programming specialist assisting a programmer. "
    messages = [{"role": "system", "content": system}]
    if prior_conversation:
        for message in prior_conversation:
            messages.extend(message)
    messages.append({
        "role": "user",
        "content": "I want you to review the my code for quality, bugs, and security issues. Score the code from 1 to 5 on readability, maintainability, coding sytle and security."
    })
    messages.append({
        "role": "assistant",
        "content": "ok, I will review your code. Please let me know the guideline for code review at first."
    })
    messages.append({
        "role": "user",
        "content": f"""Here is the guideline for code review.
[Review Guideline]
The review format guide is as follows:
1. Bugs section is optional. Add it only if you find bugs.
2. Code changes suggestion senction is optional. Add it only if you need to suggest code changes.
3. Code changes suggestion section is limited to 3 suggestions.
4. Put `N/A` in the section if you have no comments.
5. Review must be written in {LANGUAGE}.

The review template is as follows:
## Score and comments
* Readability: */5 (e.g., Clear variable names)
* Maintainability: */5  (e.g., Modular structure)
* Security: */5 (e.g., No sensitive data exposed)
* Coding Style: */5 (e.g., Followed PEP8)
* Overall: */5 (e.g., Well-organized code)

## Bugs
* Bug1
(e.g., Missing validation for user input)
* Bug2
* Bug3

## Code changes suggestion as follows:
* Suggestion1
* Suggestion2
* Suggestion3

Code changes suggestion rules and format are as follows:
* Rules: Looks like linux `diff` command output. The `+` sign indicates that the line of code needs to be changed and the `-` sign indicates the deleted line.
* Format:
```diff
# 1. Suggestions comment
# (e.g., The variable name is not clear)
# ... Omitting unchanged lines
- def func():
-    vl = 1
-    return val

+ def func():
+    val = 1  # <-- Comment explaining change
+    return val

# ... Omitting unchanged lines

# 2. Suggestions comment
# (e.g., The variable name is not clear)
# ... Omitting unchanged lines
- def func():
-    vl = 1
-    return val

+ def func():
+    val = 1  # <-- Comment explaining change
+    return val

# 3. Suggestions comment
# (e.g., The variable name is not clear)
# ... Omitting unchanged lines
- def func():
-    vl = 1
-    return val

+ def func():
+    val = 1  # <-- Comment explaining change
+    return val

# ... Omitting unchanged lines
```
"""
    })
    messages.append({
        "role": "user",
        "content": f"Here is the code:\n```{code}```"
    })
    return messages
