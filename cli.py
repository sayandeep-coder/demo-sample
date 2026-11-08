import argparse
import re
import sys
import warnings
from colorama import Fore, Style, init

# Silence library warnings in CLI
warnings.filterwarnings("ignore")

# Ensure UTF-8 output when possible on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Initialize colorama
init(autoreset=True)

from src.config import LLM_MODEL
from src.chat_service import KnowledgeChatService


def render_terminal_markdown(text: str) -> str:
    """Converts markdown bolding and headers into terminal ANSI bold styling, removing raw stars."""
    # Triple stars: ***text*** -> Bold
    text = re.sub(r"\*\*\*(.+?)\*\*\*", lambda m: f"{Style.BRIGHT}{m.group(1)}{Style.NORMAL}", text)
    # Double stars: **text** -> Bold
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: f"{Style.BRIGHT}{m.group(1)}{Style.NORMAL}", text)
    # Headers: ### Header -> Bold Header
    text = re.sub(r"^(#{1,6})\s+(.+)$", lambda m: f"{Style.BRIGHT}{m.group(2)}{Style.NORMAL}", text, flags=re.MULTILINE)
    return text



def print_banner():
    banner = f"""
{Fore.MAGENTA}===================================================================={Style.RESET_ALL}
{Fore.GREEN}{Style.BRIGHT}            FIZA'S PA & BEST FRIEND CHAT SYSTEM                    {Style.RESET_ALL}
{Fore.MAGENTA}===================================================================={Style.RESET_ALL}
{Fore.YELLOW}Role:{Style.RESET_ALL}           Fiza's Personal Assistant & Best Friend
{Fore.YELLOW}Model:{Style.RESET_ALL}          {LLM_MODEL}
{Fore.YELLOW}Commands:{Style.RESET_ALL}
  {Fore.CYAN}/help{Style.RESET_ALL}     - Show this help message
  {Fore.CYAN}/clear{Style.RESET_ALL}    - Clear conversation history
  {Fore.CYAN}/exit{Style.RESET_ALL}     - Exit the chat system
{Fore.MAGENTA}--------------------------------------------------------------------{Style.RESET_ALL}
"""
    print(banner)


def safe_print(text: str):
    """Prints text safely to the console, falling back if unicode encoding issues occur."""
    try:
        print(text)
    except UnicodeEncodeError:
        encoding = sys.stdout.encoding or "utf-8"
        print(text.encode(encoding, errors="replace").decode(encoding))


def run_interactive_cli():
    print_banner()

    print(f"{Fore.CYAN}[*] Connecting to Gemini 2.5 Flash via LangChain...{Style.RESET_ALL}")
    try:
        service = KnowledgeChatService()
        print(f"{Fore.GREEN}[OK] Ready! Hey Fiza, your PA & bestie is here! Ask me anything.{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}[X] Initialization error: {e}{Style.RESET_ALL}")
        sys.exit(1)

    while True:
        try:
            user_input = input(f"{Fore.GREEN}{Style.BRIGHT}Fiza > {Style.RESET_ALL}").strip()

            if not user_input:
                continue

            # Command handling
            cmd = user_input.lower()
            if cmd in ["/exit", "exit", "quit", ":q"]:
                print(f"{Fore.CYAN}Talk to you soon, bestie! Bye!{Style.RESET_ALL}")
                break

            elif cmd == "/help":
                print_banner()
                continue

            elif cmd == "/clear":
                service.clear_history()
                print(f"{Fore.CYAN}[OK] Memory cleared for our fresh chat!{Style.RESET_ALL}\n")
                continue

            # Query Gemini
            print(f"{Fore.CYAN}[Thinking for Fiza...]{Style.RESET_ALL}")
            answer = service.ask(user_input)

            print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Your PA & Bestie:{Style.RESET_ALL}")
            safe_print(f"{render_terminal_markdown(answer)}\n")

        except (KeyboardInterrupt, EOFError):
            print(f"\n{Fore.YELLOW}Exiting... Goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}[Error] {e}{Style.RESET_ALL}\n")


def run_one_off_query(query: str):
    """Run a single query from the command line and exit."""
    try:
        service = KnowledgeChatService()
        answer = service.ask(query)
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Your PA & Bestie:{Style.RESET_ALL}")
        safe_print(render_terminal_markdown(answer))
    except Exception as e:
        print(f"{Fore.RED}[Error] {e}{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Knowledge Base Chat System with Gemini 2.5 Flash & LangChain"
    )
    parser.add_argument(
        "-q", "--query", type=str, help="Run a single question query and exit"
    )
    args = parser.parse_args()

    if args.query:
        run_one_off_query(args.query)
    else:
        run_interactive_cli()


if __name__ == "__main__":
    main()
