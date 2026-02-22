import os
import re

targets = [
    "05_tools_skills/5.2_tool_policy.md",
    "06_context_memory/6.1_sessions.md",
    "06_context_memory/6.2_context_building.md",
    "06_context_memory/6.3_memory_mechanism.md",
    "06_context_memory/6.4_compaction_pruning.md",
    "09_gateway_protocol/9.1_control_plane.md",
    "09_gateway_protocol/9.2_ws_handshake.md",
    "11_reliability_security/11.1_auth_profiles.md",
    "11_reliability_security/11.2_rotation_cooldown.md",
    "11_reliability_security/11.3_fallback_rules.md",
    "11_reliability_security/11.4_guardrails.md"
]

chapters = {}

for target in targets:
    if not os.path.exists(target):
        continue
    with open(target, 'r') as f:
        content = f.read()

    # Match `### X.Y.Z 官方参考\n\n- link1\n- link2\n\n`
    pattern1 = re.compile(r'\n+### \d+\.\d+\.\d+ 官方参考\s*\n+((?:- .*https?://.*(?:\n|$))+)', re.MULTILINE)
    
    # Match `官方参考：\n\n- link1\n- link2\n\n`
    pattern2 = re.compile(r'\n+官方参考：\s*\n+((?:- .*https?://.*(?:\n|$))+)', re.MULTILINE)
    
    # Match `官方参考：https://...\n`
    pattern3 = re.compile(r'\n+官方参考： *(https?://[^\s。]*)[。]*\s*', re.MULTILINE)

    refs = []
    
    def repl1(m):
        for line in m.group(1).strip().split('\n'):
            refs.append(line.strip('- ').strip())
        return '\n\n'

    def repl2(m):
        for line in m.group(1).strip().split('\n'):
            refs.append(line.strip('- ').strip())
        return '\n\n'

    def repl3(m):
        refs.append("参考：" + m.group(1).strip())
        return '\n\n'

    content_new = pattern1.sub(repl1, content)
    content_new = pattern2.sub(repl2, content_new)
    content_new = pattern3.sub(repl3, content_new)

    if content != content_new:
        with open(target, 'w') as f:
            f.write(content_new)
        
        chapter = target.split('/')[0]
        if chapter not in chapters:
            chapters[chapter] = []
        chapters[chapter].extend(refs)

for chapter, refs in chapters.items():
    summary_path = os.path.join(chapter, 'summary.md')
    if not os.path.exists(summary_path):
        continue
        
    with open(summary_path, 'r') as f:
        summary_lines = f.readlines()
        
    # Check if "参考文献汇总" already exists
    content = "".join(summary_lines)
    if "本章参考文献汇总" not in content:
        h3s = [line for line in summary_lines if line.startswith('### ')]
        if h3s:
            last_h3 = h3s[-1]
            m = re.match(r'### (\d+\.\d+)\.(\d+)', last_h3)
            if m:
                next_minor = int(m.group(2)) + 1
                header = f"\n### {m.group(1)}.{next_minor} 本章参考文献汇总\n\n"
            else:
                header = f"\n### 本章参考文献汇总\n\n"
        else:
            header = f"\n### 本章参考文献汇总\n\n"
            
        with open(summary_path, 'a') as f:
            f.write(header)
            unique_refs = []
            for r in refs:
                if r not in unique_refs:
                    unique_refs.append(r)
            for r in unique_refs:
                if "：" in r:
                    f.write(f"- {r}\n")
                else:
                    f.write(f"- {r}\n")
    else:
        # If header exists, append to EOF.
        with open(summary_path, 'a') as f:
            unique_refs = []
            for r in refs:
                if r not in unique_refs:
                    unique_refs.append(r)
            for r in unique_refs:
                f.write(f"- {r}\n")

print(chapters)
