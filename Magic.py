def check_spell(spell):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for char in spell:
        if char in '({[':
            stack.append(char)
        elif char in ')}]':
            if not stack or stack[-1] != mapping[char]:
                return f"{spell}:施法失敗"
            stack.pop()

    if not stack:
        return f"{spell}:施法成功"
    else:
        return f"{spell}:施法失敗"

# 測試案例
print(check_spell("()"))  # ():施法成功
print(check_spell("{{}}"))  # {{}}:施法成功
print(check_spell("{()}"))  # {()}:施法成功
print(check_spell("{([])}"))  # {([])}:施法成功
print(check_spell("[)"))  # [):施法失敗
print(check_spell("({[]})"))  # ({[]}):施法失敗
print(check_spell("{{}"))  # {{}:施法失敗
print(check_spell("({)}"))  # ({)}:施法失敗