# AI Environment Module v3.0.28
#!/usr/bin/env python3
"""
AI Environment Module v3.0.26
Date: 2025-08-14
Time: 10:30
"""

"""
AI Environment - Document Viewer Module
Enhanced viewer with Markdown formatting support for README and PACKAGE_INFO
"""

import os
import re
from pathlib import Path

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    class Fore:
        GREEN = YELLOW = CYAN = WHITE = RED = MAGENTA = BLUE = ""
    class Style:
        RESET_ALL = BRIGHT = ""
    COLORAMA_AVAILABLE = False

class MarkdownFormatter:
    """Formats Markdown text with colors and styling"""
    
    def __init__(self):
        self.in_code_block = False
        self.code_block_lang = ""
    
    def format_line(self, line):
        """Format a single line of Markdown"""
        original_line = line
        
        # Handle code blocks
        if line.strip().startswith("```"):
            if not self.in_code_block:
                self.in_code_block = True
                self.code_block_lang = line.strip()[3:].strip()
                lang_display = self.code_block_lang or "text"
                return f"{Fore.CYAN}┌─ Code Block ({lang_display}) ─{Style.RESET_ALL}"
            else:
                self.in_code_block = False
                self.code_block_lang = ""
                return f"{Fore.CYAN}└─ End Code Block ─{Style.RESET_ALL}"
        
        # If inside code block, return with code formatting
        if self.in_code_block:
            return f"{Fore.GREEN}│ {line}{Style.RESET_ALL}"
        
        # Headers
        if line.startswith("# "):
            sep = "=" * 60
            return f"{Fore.CYAN}{Style.BRIGHT}{sep}{Style.RESET_ALL}\n{Fore.CYAN}{Style.BRIGHT}{line[2:].strip()}{Style.RESET_ALL}\n{Fore.CYAN}{Style.BRIGHT}{sep}{Style.RESET_ALL}"
        elif line.startswith("## "):
            sep = "-" * 40
            return f"{Fore.YELLOW}{Style.BRIGHT}{line[3:].strip()}{Style.RESET_ALL}\n{Fore.YELLOW}{sep}{Style.RESET_ALL}"
        elif line.startswith("### "):
            return f"{Fore.WHITE}{Style.BRIGHT}{line[4:].strip()}{Style.RESET_ALL}"
        elif line.startswith("#### "):
            return f"{Fore.WHITE}{line[5:].strip()}{Style.RESET_ALL}"
        
        # Lists
        if re.match(r"^\s*[-*+]\s", line):
            indent = len(line) - len(line.lstrip())
            content = re.sub(r"^\s*[-*+]\s", "", line)
            indent_str = " " * indent
            return f"{indent_str}{Fore.GREEN}•{Style.RESET_ALL} {self.format_inline(content)}"
        
        # Numbered lists
        if re.match(r"^\s*\d+\.\s", line):
            # Extract the number and content
            match = re.match(r"^(\s*)(\d+)(\.\s)(.*)$", line)
            if match:
                indent, number, dot_space, content = match.groups()
                return f"{indent}{Fore.CYAN}{number}{dot_space}{Style.RESET_ALL}{self.format_inline(content)}"
            else:
                # Fallback if regex doesn\"t match perfectly
                parts = line.split(".", 1)
                if len(parts) == 2:
                    return f"{Fore.CYAN}{parts[0]}.{Style.RESET_ALL}{self.format_inline(parts[1])}"
                else:
                    return line
        
        # Horizontal rules
        if re.match(r"^[-=*]{3,}$", line.strip()):
            sep = "─" * 60
            return f"{Fore.CYAN}{sep}{Style.RESET_ALL}"
        
        # Blockquotes
        if line.startswith("> "):
            return f"{Fore.YELLOW}│ {self.format_inline(line[2:])}{Style.RESET_ALL}"
        
        # Regular text with inline formatting
        return self.format_inline(line)
    
    def format_inline(self, text):
        """Format inline Markdown elements"""
        # Bold text **text** or __text__
        text = re.sub(r"\*\*(.*?)\*\*", Fore.WHITE + Style.BRIGHT + r'\1' + Style.RESET_ALL, text)
        text = re.sub(r"__(.*?)__", Fore.WHITE + Style.BRIGHT + r'\1' + Style.RESET_ALL, text)

        # Italic text *text* or _text_
        text = re.sub(r"\*(.*?)\*", Fore.YELLOW + r'\1' + Style.RESET_ALL, text)
        text = re.sub(r"_(.*?)_", Fore.YELLOW + r'\1' + Style.RESET_ALL, text)

        # Inline code `code`
        text = re.sub(r"`(.*?)`", Fore.GREEN + r'\1' + Style.RESET_ALL, text)

        # Links [text](url)
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", Fore.BLUE + r'\1' + Style.RESET_ALL, text)

        # Checkboxes
        text = re.sub(r"\[x\]", Fore.GREEN + '✓' + Style.RESET_ALL, text, flags=re.IGNORECASE)
        text = re.sub(r"\[ \]", Fore.RED + '☐' + Style.RESET_ALL, text)
        
        return text

class DocumentViewer:
    """Enhanced document viewer with Markdown formatting and pagination"""
    
    def __init__(self, ai_env_path):
        self.ai_env_path = Path(ai_env_path)
        self.lines_per_page = 20
        self.formatter = MarkdownFormatter()
    
    def view_readme(self):
        """View README.md with Markdown formatting"""
        readme_path = self.ai_env_path / "README.md"
        if not readme_path.exists():
            print(f"{Fore.RED}README.md not found at {readme_path}{Style.RESET_ALL}")
            return
        
        self._view_file(readme_path, "README.md", is_markdown=True)
    
    def view_package_info(self):
        """View PACKAGE_INFO.txt with basic formatting"""
        package_info_path = self.ai_env_path / "PACKAGE_INFO.txt"
        if not package_info_path.exists():
            print(f"{Fore.RED}PACKAGE_INFO.txt not found at {package_info_path}{Style.RESET_ALL}")
            return
        
        self._view_file(package_info_path, "PACKAGE_INFO.txt", is_markdown=False)
    
    def _view_file(self, file_path, title, is_markdown=False):
        """View file with pagination and formatting"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Format lines if Markdown
            if is_markdown:
                formatted_lines = []
                for line in lines:
                    formatted = self.formatter.format_line(line.rstrip())
                    # Handle multi-line formatted output (like headers)
                    if '\n' in formatted:
                        formatted_lines.extend(formatted.split('\n'))
                    else:
                        formatted_lines.append(formatted)
                lines = formatted_lines
            else:
                # Basic formatting for non-Markdown files
                lines = [self._format_text_line(line.rstrip()) for line in lines]
            
            total_pages = (len(lines) + self.lines_per_page - 1) // self.lines_per_page
            current_page = 1
            
            while True:
                self._display_page(lines, current_page, total_pages, title)
                
                if total_pages <= 1:
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    break
                
                choice = self._get_navigation_choice(current_page, total_pages)

                if choice == 'q':
                    break
                elif choice == 'n' and current_page < total_pages:
                    current_page += 1
                elif choice == 'p' and current_page > 1:
                    current_page -= 1
                elif choice == 't':
                    current_page = 1
                elif choice == 'b':
                    current_page = total_pages
                elif choice.isdigit():
                    page_num = int(choice)
                    if 1 <= page_num <= total_pages:
                        current_page = page_num
                
        except Exception as e:
            print(f"{Fore.RED}Error reading {title}: {e}{Style.RESET_ALL}")
    
    def _format_text_line(self, line):
        """Basic formatting for non-Markdown text files"""
        # Highlight version numbers
        line = re.sub(r"v?\d+\.\d+\.\d+", Fore.CYAN + r'\g<0>' + Style.RESET_ALL, line)

        # Highlight dates
        line = re.sub(r"\d{4}-\d{2}-\d{2}", Fore.YELLOW + r'\g<0>' + Style.RESET_ALL, line)

        # Highlight SUCCESS/ERROR/WARNING
        line = re.sub(r"\[SUCCESS\]", Fore.GREEN + '[SUCCESS]' + Style.RESET_ALL, line)
        line = re.sub(r"\[ERROR\]", Fore.RED + '[ERROR]' + Style.RESET_ALL, line)
        line = re.sub(r"\[WARNING\]", Fore.YELLOW + '[WARNING]' + Style.RESET_ALL, line)
        line = re.sub(r"\[INFO\]", Fore.CYAN + '[INFO]' + Style.RESET_ALL, line)

        # Highlight file paths
        line = re.sub(r"[A-Za-z]:\\[^\s]+", Fore.BLUE + r'\g<0>' + Style.RESET_ALL, line)

        return line
    
    def _display_page(self, lines, current_page, total_pages, title):
        """Display a single page of content"""
        start_idx = (current_page - 1) * self.lines_per_page
        end_idx = min(start_idx + self.lines_per_page, len(lines))

        # Clear screen and show header
        os.system('cls' if os.name == 'nt' else 'clear')
        sep = "=" * 70
        print(f"{Fore.CYAN}{sep}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{title} - Page {current_page}/{total_pages}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{sep}{Style.RESET_ALL}")
        print()
        
        # Display content
        for i in range(start_idx, end_idx):
            if i < len(lines):
                print(lines[i])
        
        # Add spacing if page is not full
        for _ in range(self.lines_per_page - (end_idx - start_idx)):
            print()
    
    def _get_navigation_choice(self, current_page, total_pages):
        """Get user navigation choice"""
        sep = "─" * 70
        print(f"{Fore.CYAN}{sep}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Navigation:{Style.RESET_ALL}")
        
        nav_options = []
        if current_page > 1:
            nav_options.append(f"{Fore.GREEN}P{Style.RESET_ALL}revious")
        if current_page < total_pages:
            nav_options.append(f"{Fore.GREEN}N{Style.RESET_ALL}ext")
        
        nav_options.extend([
            f"{Fore.GREEN}T{Style.RESET_ALL}op",
            f"{Fore.GREEN}B{Style.RESET_ALL}ottom",
            f"{Fore.GREEN}1-{total_pages}{Style.RESET_ALL} (page number)",
            f"{Fore.GREEN}Q{Style.RESET_ALL}uit"
        ])
        
        print(f"  {' | '.join(nav_options)}")

        while True:
            choice = input(f"\n{Fore.WHITE}Enter choice: {Style.RESET_ALL}").strip().lower()

            if choice in ['q', 'quit', 'exit']:
                return 'q'
            elif choice in ['n', 'next'] and current_page < total_pages:
                return 'n'
            elif choice in ['p', 'prev', 'previous'] and current_page > 1:
                return 'p'
            elif choice in ['t', 'top']:
                return 't'
            elif choice in ['b', 'bottom']:
                return 'b'
            elif choice.isdigit():
                page_num = int(choice)
                if 1 <= page_num <= total_pages:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid page number. Enter 1-{total_pages}.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid choice. Try again.{Style.RESET_ALL}")

def main():
    """Main function for standalone execution"""
    import argparse

    parser = argparse.ArgumentParser(description='AI Environment Document Viewer')
    parser.add_argument('--ai-env-path', default='.',
                       help='Path to AI Environment directory')
    parser.add_argument('--readme', action='store_true',
                       help='View README.md')
    parser.add_argument('--package-info', action='store_true',
                       help='View PACKAGE_INFO.txt')
    
    args = parser.parse_args()
    
    viewer = DocumentViewer(args.ai_env_path)
    
    if args.readme:
        viewer.view_readme()
    elif args.package_info:
        viewer.view_package_info()
    else:
        print("Use --readme or --package-info to view documents")

if __name__ == "__main__":
    main()



