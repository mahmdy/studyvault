# studyvault/file_manager.py

import os
import markdown2
from rich.console import Console
from rich.rule import Rule
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from markdown2 import markdown
import textwrap

console = Console()
# Constants
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data_libraries')

def ensure_data_directory():
    """Create the data_libraries directory if it doesn't exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        console.print(f"[bold green][+][/bold green] Created data directory at: {DATA_DIR}")
    else:
        console.print("[bold green][+][/bold green] Data library is ready.")

def list_markdown_files():
    """List all .md files in the data_libraries directory."""
    ensure_data_directory()
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.md')]
    return files

def get_library_path(filename):
    """Returns the full path of a .md file in the data_libraries directory."""
    return os.path.join(DATA_DIR, filename)

def append_to_file(path, title, content):
    """Append a new section to the Markdown file."""
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f"\n\n## {title}\n{content}\n")
    console.print(f"[bold green][+][/bold green] Content appended to: [cyan]{os.path.basename(path)}[/cyan]")


def update_text_in_file(path, old_text, new_text):
    """Replace the first occurrence of old_text with new_text in the file."""
    if not os.path.exists(path):
        console.print("[bold red][!][/bold red] File not found.")
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_text not in content:
        console.print("[bold red][!][/bold red] The specified text to update was not found.")

        return

    updated_content = content.replace(old_text, new_text, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    console.print("[bold green][+][/bold green] Content successfully updated.")


def find_lines_containing(path, keyword):
    """Return a list of (line_number, line_content) where keyword is found."""
    results = []
    with open(path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            if keyword in line:
                results.append((idx, line.strip()))
    return results

def delete_keyword_from_lines(path, keyword, target_lines):
    """Delete keyword only from the specified line numbers."""
    if not os.path.exists(path):
        console.print("[bold red][!][/bold red] File not found.")
        return

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified = False
    for idx in target_lines:
        if 1 <= idx <= len(lines):
            if keyword in lines[idx - 1]:
                lines[idx - 1] = lines[idx - 1].replace(keyword, "")
                modified = True

    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        console.print("[bold green][+][/bold green] Keyword deleted from selected lines.")

    else:
        console.print("[bold red][!][/bold red] Keyword was not found in the selected lines.")


def append_to_section(path, section_title, position_type, reference, new_data):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    section_header = f"## {section_title}".strip()
    section_start = None
    section_end = len(lines)

    for i, line in enumerate(lines):
        if line.strip() == section_header:
            section_start = i
            break

    if section_start is None:
        console.print("[bold red][!][/bold red] Section not found.")
        return

    for j in range(section_start + 1, len(lines)):
        if lines[j].strip().startswith("## "):
            section_end = j
            break

    section_lines = lines[section_start + 1:section_end]
    insert_at = None

    if position_type == "start":
        insert_at = section_start + 1
    elif position_type == "end":
        insert_at = section_end
    elif position_type == "line":
        if not isinstance(reference, int):
            console.print("[bold red][!][/bold red] Invalid line reference.")

            return

        if reference < 1 or reference > len(section_lines):
            console.print("[bold red][!][/bold red] Invalid line number inside section.")

            return

        direction = input("Insert 'before' or 'after' that line? ").strip().lower()
        if direction == "before":
            insert_at = section_start + reference
        elif direction == "after":
            insert_at = section_start + reference + 1
        else:
            console.print("[bold red][!][/bold red] Invalid direction. Use 'before' or 'after'.")

            return
    else:
        console.print("[bold red][!][/bold red] Invalid position type.")

        return

    # Simulate the change
    simulated = lines.copy()
    simulated.insert(insert_at, new_data + "\n")

    console.print("\n[bold yellow]🔍 Preview of Section After Change:[/bold yellow]")
    for idx in range(section_start, section_end + 2):  # show a few lines after for context
        if idx < len(simulated):
            line_display = simulated[idx].rstrip()
            prefix = ">> " if idx == insert_at else "   "
            print(f"{prefix}{line_display}")
    console.print("-" * 40, style="dim")

    confirm = input("Apply this change? (yes/no): ").strip().lower()
    if confirm in ["y", "yes"]:
        lines.insert(insert_at, new_data + "\n")
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        console.print("[bold green][+][/bold green] Content appended successfully.")

    else:
        console.print("[bold yellow][*][/bold yellow] Operation cancelled.")



def search_in_file(path, keyword):
    """Search for keyword in the file and return matching lines with line numbers."""
    if not os.path.exists(path):
        console.print("[bold red][!][/bold red] File not found.")
        return []

    matches = []
    with open(path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            if keyword.lower() in line.lower():
                matches.append((idx, line.strip()))
    return matches

def search_sections(path, keyword):
    """
    Returns a list of sections (title + content lines) that contain the keyword.
    Each section is a tuple: (section_title, [lines])
    """
    if not os.path.exists(path):
        console.print("[bold red][!][/bold red] File not found.")
        return []

    results = []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_section_title = "Untitled"
    current_section_lines = []
    match_found = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            if match_found:
                results.append((current_section_title, current_section_lines))
            # Start new section
            current_section_title = stripped
            current_section_lines = []
            match_found = False
        else:
            current_section_lines.append(stripped)
            if keyword.lower() in stripped.lower():
                match_found = True

    # Add final section if matched
    if match_found:
        results.append((current_section_title, current_section_lines))

    return results

def list_sections(path):
    """
    Returns a list of (line_number, section_title) for lines starting with '## '.
    """
    sections = []
    with open(path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            if line.strip().startswith("## "):
                sections.append((idx, line.strip()))
    return sections


def export_to_pdf(markdown_path, output_pdf_path):
    if not os.path.exists(markdown_path):
        console.print("[bold red][!][/bold red] Markdown file not found.")
        return

    with open(markdown_path, 'r', encoding='utf-8') as f:
        raw_md = f.read()

    lines = raw_md.splitlines()
    wrapped_lines = []

    for line in lines:
        # Skip empty lines
        if not line.strip():
            wrapped_lines.append("")
            continue

        # Wrap long lines
        wrapped = textwrap.wrap(line, width=100)
        wrapped_lines.extend(wrapped)

    try:
        c = canvas.Canvas(output_pdf_path, pagesize=letter)
        width, height = letter
        y = height - 40  # Start near top

        for line in wrapped_lines:
            if y < 40:
                c.showPage()
                y = height - 40
            c.drawString(40, y, line)
            y -= 15  # Line spacing

        c.save()
        console.print(f"[bold green][+][/bold green] Exported to PDF: [bold]{output_pdf_path}[/bold]")
    except Exception as e:
        console.print(f"[bold red][!][/bold red] PDF export failed: {e}")
