import argparse
import os
import re
from pathlib import Path
from typing import List, Tuple

def check_1_1_bold_spacing(text: str, auto_fix: bool) -> Tuple[str, List[str]]:
    warnings = []
    
    parts = re.split(r'(\*\*.*?\*\*)', text)
    ign = list(' \n\t.,:;!?，。：；！？-[]()（）"\'`<>*')
    has_outside_warning = False
    has_inside_warning = False
    
    new_parts = []
    
    for i in range(len(parts)):
        if i % 2 == 1:
            inner = parts[i][2:-2]
            if inner.startswith(' ') or inner.endswith(' ') or inner.startswith('\t') or inner.endswith('\t') or inner.startswith('\n') or inner.endswith('\n'):
                has_inside_warning = True
                if auto_fix:
                    parts[i] = f"**{inner.strip()}**"
            new_parts.append(parts[i])
        else:
            part = parts[i]
            if i + 1 < len(parts) and part:
                if part[-1] not in ign:
                    has_outside_warning = True
                    if auto_fix:
                        part = part + ' '
            if i - 1 >= 0 and part:
                if part[0] not in ign:
                    has_outside_warning = True
                    if auto_fix:
                        part = ' ' + part
            new_parts.append(part)

    if has_inside_warning:
        warnings.append("1.1 Bold text has spaces inside markers.")
    if has_outside_warning:
        warnings.append("1.1 Bold text missing outside spaces.")

    if auto_fix:
        text = ''.join(new_parts)

    return text, warnings

def check_1_2_header_spacing(text: str, auto_fix: bool) -> Tuple[str, List[str]]:
    warnings = []
    # Check if header is followed by exactly one blank line
    # \n#{1,6}\s+.*\n(?!\n) -> no blank line
    # \n#{1,6}\s+.*\n\n\n+ -> multiple blank lines
    
    lines = text.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        if re.match(r'^#{1,6}\s+.*$', line) and not line.startswith('# ❌') and not line.startswith('# ✅'):
            # It's a header. Count following empty lines.
            empty_count = 0
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                empty_count += 1
                j += 1
            
            if j < len(lines):  # if not end of file
                if empty_count != 1:
                    warnings.append(f"1.2 Header spacing incorrect at line {i+1}: '{line}' has {empty_count} blank lines after it.")
                    if auto_fix:
                        # Skip adding the existing empty lines, just add one.
                        new_lines.append('')
                        i = j - 1 # skip over the empty lines
                    else:
                        pass # just warn
        i += 1
        
    return '\n'.join(new_lines), warnings

def check_1_3_header_hierarchy(text: str) -> List[str]:
    warnings = []
    last_level = 0
    for i, line in enumerate(text.split('\n')):
        match = re.match(r'^(#{1,6})\s+.*$', line)
        if match and not line.startswith('# ❌') and not line.startswith('# ✅'):
            level = len(match.group(1))
            if last_level != 0 and level > last_level + 1:
                warnings.append(f"1.3 Header hierarchy skipped level at line {i+1}: '{line}'. Jumped from H{last_level} to H{level}.")
            last_level = level
    return warnings

def check_1_4_trailing_newline(text: str, auto_fix: bool) -> Tuple[str, List[str]]:
    warnings = []
    if not text.endswith('\n') or text.endswith('\n\n'):
        warnings.append("1.4 File does not end with exactly one newline.")
        if auto_fix:
            text = text.rstrip('\n') + '\n'
    return text, warnings

def check_2_1_and_2_2_header_levels(file_path: str, text: str) -> List[str]:
    warnings = []
    lines = text.split('\n')
    first_header_level = None
    for line in lines:
        match = re.match(r'^(#{1,6})\s+.*$', line)
        if match:
            first_header_level = len(match.group(1))
            break
            
    name = os.path.basename(file_path)
    if name == 'README.md' and first_header_level != 1:
        warnings.append("2.2 README.md first header must be H1.")
    elif name == 'SUMMARY.md':
         pass # SUMMARY.md has relaxed rules per rule 1
    elif name.startswith('summary.md') and first_header_level != 2:
        warnings.append("2.2 summary.md first header must be H2.")
    elif re.match(r'^\d+\.\d+_.*\.md$', name) and first_header_level != 2:
        warnings.append(f"2.2 Section file {name} first header must be H2.")
        
    return warnings

def check_2_2_english_parentheses(text: str) -> List[str]:
    warnings = []
    for i, line in enumerate(text.split('\n')):
        if re.match(r'^#{1,6}\s+.*$', line):
            if re.search(r'\([a-zA-Z\s]+\)', line) or re.search(r'（[a-zA-Z\s]+）', line):
                warnings.append(f"2.2 Header contains English parentheses at line {i+1}: '{line}'.")
    return warnings

def check_2_3_single_child(text: str) -> List[str]:
    warnings = []
    headers = []
    for i, line in enumerate(text.split('\n')):
        match = re.match(r'^(#{1,6})\s+.*$', line)
        if match:
            headers.append((len(match.group(1)), line, i+1))
            
    for i in range(len(headers) - 1):
        level, line, lnum = headers[i]
        children_count = 0
        for j in range(i+1, len(headers)):
            next_level = headers[j][0]
            if next_level == level + 1:
                children_count += 1
            elif next_level <= level:
                break
        if children_count == 1:
            warnings.append(f"2.3 Single child header detected for H{level} at line {lnum}: '{line}'.")
            
    return warnings

def check_2_5_and_3_2_bridge_text(text: str) -> List[str]:
    warnings = []
    lines = text.split('\n')
    for i in range(len(lines)):
        line = lines[i]
        
        # Check bridge text for headers
        match = re.match(r'^(#{1,6})\s+.*$', line)
        if match:
            level = len(match.group(1))
            has_child = False
            # Look ahead for next header or content
            j = i + 1
            content_found = False
            first_child_is_direct = False
            while j < len(lines):
                next_line = lines[j]
                if next_line.strip() == '':
                    j += 1
                    continue
                elif re.match(r'^#{1,6}\s+.*$', next_line):
                    next_level = len(re.match(r'^#{1,6}', next_line).group(0))
                    if next_level > level and not content_found:
                        first_child_is_direct = True
                    break
                else:
                    content_found = True
                j += 1
                
            if first_child_is_direct:
                warnings.append(f"2.5 Missing bridge text after header at line {i+1}: '{line}'.")
                
        # Check text before code block or image
        if line.startswith('```') and not line.startswith('```markdown') and not line.startswith('```diff'):
            # verify previous non-empty line is not a header
            j = i - 1
            prior_content_found = False
            while j >= 0:
                prev_line = lines[j]
                if prev_line.strip() != '':
                    if re.match(r'^#{1,6}\s+.*$', prev_line):
                        warnings.append(f"3.2 Missing introductory text before code block at line {i+1}.")
                    break
                j -= 1
                
        if re.match(r'^!\[.*\]\(.*\)$', line.strip()):
            j = i - 1
            while j >= 0:
                prev_line = lines[j]
                if prev_line.strip() != '':
                    if re.match(r'^#{1,6}\s+.*$', prev_line):
                        warnings.append(f"3.2 Missing introductory text before image at line {i+1}.")
                    break
                j -= 1

    return warnings

def check_3_3_concise_text(text: str, auto_fix: bool) -> Tuple[str, List[str]]:
    warnings = []
    replacements = {
        "我们推荐": "推荐",
        "我们建议": "建议",
        "我们通过": "通过",
        "你可以": "可",
        "你需要": "需",
        "建议你": "建议",
        "推荐你": "推荐"
    }
    
    lines = text.split('\n')
    new_lines = []
    for i, line in enumerate(lines):
        new_line = line
        for bad, good in replacements.items():
            if bad in new_line:
                warnings.append(f"3.3 Concise text at line {i+1}: '{bad}' should be '{good}'.")
                if auto_fix:
                    new_line = new_line.replace(bad, good)
        new_lines.append(new_line)
        
    return '\n'.join(new_lines), warnings

def process_file(file_path: str, auto_fix: bool, verbose: bool) -> bool:
    name = os.path.basename(file_path)
    if not file_path.endswith('.md'):
        return True
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_text = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    text = original_text
    
    # Strip code blocks to avoid false positives on headers within code
    def repl_code(m):
        return re.sub(r'[^\n]', '', m.group(0))
    stripped_text = re.sub(r'```.*?```', repl_code, text, flags=re.DOTALL)
    
    all_warnings = []
    
    # Relaxed rules for README.md and SUMMARY.md
    is_special = name in ['README.md', 'SUMMARY.md']

    # 1.1 Bold Spacing
    text, w = check_1_1_bold_spacing(text, auto_fix)
    all_warnings.extend(w)
    
    # 1.4 Trailing Newline
    text, w = check_1_4_trailing_newline(text, auto_fix)
    all_warnings.extend(w)

    # 3.3 Concise text
    text, w = check_3_3_concise_text(text, auto_fix)
    all_warnings.extend(w)

    if not is_special:
        # 1.2 Header Spacing (apply on full text to auto-fix, but can cause issues if in code)
        text, w = check_1_2_header_spacing(text, auto_fix)
        all_warnings.extend(w)
        
        # 1.3 Header Hierarchy
        all_warnings.extend(check_1_3_header_hierarchy(stripped_text))
        
        # 2.1 & 2.2 Header Levels
        all_warnings.extend(check_2_1_and_2_2_header_levels(file_path, stripped_text))
        
        # 2.2 English Parentheses
        all_warnings.extend(check_2_2_english_parentheses(stripped_text))
        
        # 2.3 Single Child
        all_warnings.extend(check_2_3_single_child(stripped_text))
        
        # 2.5 Bridge Text & 3.2 Content Intro
        all_warnings.extend(check_2_5_and_3_2_bridge_text(stripped_text))

    if all_warnings:
        print(f"\n--- Issues in {file_path} ---")
        for w in all_warnings:
            print(f"  {w}")
            
    if auto_fix and text != original_text:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"  [Fixed automatically applied to {name}]")

    return len(all_warnings) == 0

def main():
    parser = argparse.ArgumentParser(description="Check and fix markdown formatting rules.")
    parser.add_argument('--fix', action='store_true', help="Auto-fix formatting issues where possible.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Show all scanned files.")
    parser.add_argument('path', nargs='?', default='.', help="Directory or file to check.")
    args = parser.parse_args()

    target_path = Path(args.path).resolve()
    has_errors = False
    
    if target_path.is_file():
        if target_path.suffix == '.md':
            success = process_file(str(target_path), args.fix, args.verbose)
            if not success:
                has_errors = True
    elif target_path.is_dir():
        for root, dirs, files in os.walk(target_path):
            if '.git' in dirs:
                dirs.remove('.git')
            if '.agent' in dirs:
                dirs.remove('.agent')
                
            for file in files:
                if file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    if args.verbose:
                        print(f"Scanning {full_path}...")
                    success = process_file(full_path, args.fix, args.verbose)
                    if not success:
                        has_errors = True
    else:
        print(f"Path not found: {args.path}")
        exit(1)

    if has_errors:
         print("\nSome files had formatting warnings/errors.")
    else:
         print("\nAll checks passed!")

if __name__ == '__main__':
    main()
