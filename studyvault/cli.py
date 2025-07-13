# studyvault/cli.py

import os
import re
import platform
from studyvault.file_manager import (
    list_markdown_files,
    get_library_path,
    ensure_data_directory,
    append_to_file,
    update_text_in_file,
)
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.rule import Rule

console = Console()

try:
    if platform.system() == "Linux":
        import gnureadline as readline
    else:
        import readline
except ImportError:
    readline = None


current_library = None

def clear_screen():
    console.clear()
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def display_main_menu():
    console.clear()
    console.print(Rule("[bold cyan]StudyVault Main Menu"))
    console.print("[bold green]Create[/bold green]  - Create a new data library")
    console.print("[bold blue]List[/bold blue]    - List and load existing libraries")
    console.print("[bold red]Exit[/bold red]    - Exit the application")

def display_library_menu():
    console.print(Rule(f"[bold blue]Library Loaded: {os.path.basename(current_library)}"))
    console.print("[bold blue]Index[/bold blue]   - Show all sections")
    console.print("[bold green]Store[/bold green]   - Add content to the library")
    console.print("[bold yellow]Update[/bold yellow]  - Modify existing content")
    console.print("[bold red]Delete[/bold red]  - Remove content")
    console.print("[bold cyan]Append[/bold cyan]  - Add content to a specific section")
    console.print("[bold magenta]Search[/bold magenta]  - Find content")
    console.print("[bold white]Export[/bold white]  - Export current library to PDF")
    console.print("[bold red]Exit[/bold red]    - Exit the application")

def handle_create():
    global current_library
    name = input("Enter a name for the new library (without .md): ").strip()
    filename = f"{name}.md"
    path = get_library_path(filename)

    if os.path.exists(path):
        console.print("[bold red][!][/bold red] A library with this name already exists.")
        return

    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"# {name} Library\n")
    current_library = path
    console.print(f"[bold green][+][/bold green] Loaded library: [bold]{filename}[/bold]")

def handle_list_and_load():
    global current_library
    files = list_markdown_files()
    if not files:
        console.print("[bold red][!][/bold red] No libraries found. Use 'Create' to make one.")

        return

    console.print("\n[bold cyan]📂 Available Libraries:[/bold cyan]")
    for i, file in enumerate(files):
        console.print(f" [bold cyan]{i+1}[/bold cyan]] {file}")


    choice = input("Enter the number of the library to load: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(files)):
        console.print("[bold red][!][/bold red] Invalid selection.")

        return

    selected = files[int(choice) - 1]
    current_library = get_library_path(selected)
    console.print(f"[bold green][+][/bold green] Loaded library: [bold]{os.path.basename(selected)}[/bold]")
    enter_library_loop()

def handle_store():
    title = input("Enter a title for this entry: ").strip()
    console.print("[bold cyan]Enter content[/bold cyan] (end with an empty line):")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    content = "\n".join(lines)
    append_to_file(current_library, title, content)

def handle_update():
    console.print("[bold cyan]Enter update command in format:[/bold cyan]")

    console.print('[dim]Update: "old text" with: "new text"[/dim]')

    command = input("> ").strip()

    match = re.match(r'^Update:\s*"(.+?)"\s*with:\s*"(.+?)"$', command, re.IGNORECASE)
    
    if not match:
        console.print("[bold red][!][/bold red] Invalid format. Please use: Update: \\\"old text\\\" with: \\\"new text\\\"")
        return

    old_text, new_text = match.groups()
    update_text_in_file(current_library, old_text, new_text)

def handle_delete():
    if not current_library:
        console.print("[bold red][!][/bold red] No library loaded. Use 'Load' or 'Create' first.")
        return

    keyword = input("Enter the keyword or phrase to search for deletion: ").strip()
    from studyvault.file_manager import find_lines_containing, delete_keyword_from_lines

    matches = find_lines_containing(current_library, keyword)
    if not matches:
        console.print("[bold red][!][/bold red] No matches found.")

        return

    console.print("\n[bold cyan]Lines containing the keyword:[/bold cyan]")
    for line_num, content in matches:
        console.print(f"[dim]{line_num}[/dim]: {content}")

    selection = input("\nEnter line number(s) to delete from (comma-separated): ").strip()
    try:
        line_numbers = [int(num.strip()) for num in selection.split(',')]
        delete_keyword_from_lines(current_library, keyword, line_numbers)
    except ValueError:
        console.print("[bold red][!][/bold red] Invalid line numbers.")


def handle_search():
    if not current_library:
        console.print("[bold red][!][/bold red] No library loaded. Use 'Load' or 'Create' first.")

        return

    keyword = input("Enter a keyword or phrase to search for: ").strip()
    from studyvault.file_manager import search_sections
    matches = search_sections(current_library, keyword)

    if not matches:
        console.print("[bold red][!][/bold red] No sections contain this keyword.")
        return
    console.print(f"\n[bold yellow]🔍 Found {len(matches)} section(s) containing '{keyword}':[/bold yellow]")
    console.print(Rule())
    for title, lines in matches:
        console.print(f"[bold blue]{title}[/bold blue]")
        console.print(Rule())

        for line in lines:
            console.print(f" {line}")
    console.print(Rule())


def handle_append_to_section():
    if not current_library:
        console.print("[bold red][!][/bold red] No library loaded. Use 'Load' or 'Create' first.")

        return

    section = input("Enter section title (without ##): ").strip()
    console.print("[bold cyan]Choose position:[/bold cyan] start / end / line")

    position_type = input("Position type: ").strip().lower()

    line_number = None
    if position_type == "line":
        line_number = input("Enter line number (relative to section): ").strip()
        if not line_number.isdigit():
            console.print("[bold red][!][/bold red] Line number must be numeric.")

            return
        line_number = int(line_number)

    console.print("[bold cyan]Enter the content to insert[/bold cyan] (end with empty line):")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    new_data = "\n".join(lines)

    from studyvault.file_manager import append_to_section
    append_to_section(current_library, section, position_type, line_number, new_data)


    if not current_library:
        console.print("[bold red][!][/bold red] No library loaded. Use 'Load' or 'Create' first.")

        return

    keyword = input("Enter a keyword or phrase to search for: ").strip()
    from studyvault.file_manager import search_in_file
    results = search_in_file(current_library, keyword)

    if not results:
        console.print("[bold red][!][/bold red] No matches found.")

    else:
        console.print(f"\n[bold yellow]🔍 Matches found ({len(results)}):[/bold yellow]")
        for line_num, line in results:
            console.print(f"[dim]{line_num}[/dim]: {line}")

def enter_library_loop():
    while True:
        display_library_menu()
        command = input("\n> ").strip().lower()

        if command == "store":
            handle_store()
        elif command == "index":
            handle_index()
        elif command == "update":
            handle_update()
        elif command == "append":
            handle_append_to_section()
        elif command == "delete":
            handle_delete()
        elif command == "export":
            handle_export()
        elif command == "search":
            handle_search()
        elif command == "exit":
            clear_screen()
            console.print("[bold magenta]👋 Exiting StudyVault...[/bold magenta]")

            break
        else:
            console.print("[bold red][!][/bold red] Unknown command. Please choose a valid option.")

def handle_index():
    if not current_library:
        console.print("[bold red][!][/bold red] No library loaded. Use 'Load' or 'Create' first.")
        return

    from studyvault.file_manager import list_sections
    sections = list_sections(current_library)

    if not sections:
        console.print("[bold yellow][*][/bold yellow] No sections found.")
        return

    console.print("\n[bold blue]📑 Section Index[/bold blue]")
    console.print(Rule())
    for i, (line_num, title) in enumerate(sections, 1):
        console.print(f"[cyan]{i}.[/cyan] [bold]{title}[/bold]  [dim](line {line_num})[/dim]")

    console.print("\n[dim]Type a section number to view its content or press Enter to return.[/dim]")
    choice = input("> ").strip()

    if not choice:
        return

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(sections):
        console.print("[bold red][!][/bold red] Invalid section number.")
        return

    selected_line = sections[int(choice) - 1][0]
    display_section_content_from_line(current_library, selected_line)

def display_section_content_from_line(path, start_line):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    section_title = lines[start_line - 1].strip()
    content_lines = []
    for line in lines[start_line:]:
        if line.strip().startswith("## "):
            break
        content_lines.append(line.strip())

    console.print(f"\n[bold blue]{section_title}[/bold blue]")
    console.print(Rule())
    for line in content_lines:
        console.print(f"  {line}")
    console.print(Rule())

def handle_export():
    if not current_library:
        console.print("[bold red][!][/bold red] No library loaded. Use 'Load' or 'Create' first.")
        return

    base_name = os.path.splitext(os.path.basename(current_library))[0]
    default_output = f"{base_name}.pdf"

    console.print(f"[bold cyan]Enter output filename[/bold cyan] [default: {default_output}]:")
    output = input("> ").strip()
    if not output:
        output = default_output

    output_path = os.path.join("exports", output)
    os.makedirs("exports", exist_ok=True)

    from studyvault.file_manager import export_to_pdf
    export_to_pdf(current_library, output_path)

def main():
    clear_screen()
    ensure_data_directory()
    while True:
        display_main_menu()
        command = input("\n> ").strip().lower()

        if command == "create":
            handle_create()
            enter_library_loop()
        elif command == "list":
            handle_list_and_load()
#        elif command == "export":
#            handle_export()
        elif command == "exit":
            clear_screen()
            console.print("[bold magenta]👋 Goodbye![/bold magenta]")
            break

        else:
            console.print("[bold red][!][/bold red] Unknown command. Please choose: [green]Create[/green], [blue]List[/blue], or [red]Exit[/red].")


