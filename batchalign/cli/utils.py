from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown

from pathlib import Path
import configparser

C = Console()

WELCOME = """
# Hello! Welcome to Batchalign!

Thanks so much for checking out **Batchalign**; welcome! This appears to be your first time using Batchalign's command line interface,
so we would like to go through some basic concepts in first-time setup.

For ASR-related tasks, you have two choices of engines to use:

1. Rev.AI, a commercial ASR service in the cloud, or
2. Whisper, a local ASR model

though you can swap between both using flags, Rev requires an API key to function.
"""

REV = """
## Rev.AI Setup
Got it. Let's setup Rev.ai. Please head on over to [Rev signup](https://www.rev.ai/auth/signup) (https://www.rev.ai/auth/signup) to
obtain a API key. Once you are ready, paste it below. We will store it locally on your machine. We will not echo back the
password as you type it, but it will be written down.
"""

FOLDERS = """
## Configuration
FYI, the options you selected during this setup process will be stored in `~/.batchalign.ini` for safekeeping. If you setup
Rev.ai in the previous step, that's where your API key went. Feel free to edit that file for configuration. If you have
questions, please feel free to reach out:

- `macw@cmu.edu`
- `houjun@cmu.edu`
"""


def interactive_setup():
    config = configparser.ConfigParser()
    config["asr"] = {}

    C.print(Markdown(WELCOME))
    configure_rev = Confirm.ask("\nWould you like to set up Rev.ai now?", console=C)

    if configure_rev:
        C.print(Markdown(REV))

        rev_key = Prompt.ask("\nYour Rev.ai API key", console=C, password=True)
        rev_key_confirm = Prompt.ask("Just in case, let's do that again. Your Rev.ai key please", console=C, password=True)

        while rev_key != rev_key_confirm:
            C.print("\n[italic red]That did not match.[/italic red] Let's try again!\n")
            rev_key = Prompt.ask("Your Rev.ai API key", console=C, password=True)
            rev_key_confirm = Prompt.ask("Just in case, let's do that again. Your Rev.ai key please", console=C, password=True)

        config["asr"]["default"] = "rev"
        config["asr"]["key"] = rev_key.strip()
    else:
        config["asr"]["default"] = "whisper"

    C.print(Markdown(FOLDERS))
    C.print("\n[bold green]Alrighty, let's rock and roll![/bold green] Continuing with Batchalign...\n")

    with open(Path.home()/".batchalign.ini", 'w') as df:
        config.write(df)

# interactive_setup()

# from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
# import time

# import time

# progress = Progress(
#     SpinnerColumn(),
#     *Progress.get_default_columns(),
#     TimeElapsedColumn(),
# )

# with progress:
#     task1= progress.add_task("tmp", total = 1000)

#     while not progress.finished:
#         progress.update(task1, advance=0.5)
#         time.sleep(0.1)
