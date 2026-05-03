from rich.console import Console
from rich.prompt imnport Prompt

console = Console()

def register_number():
    while True:
        number = Prompt.ask("Введiть номер телефону")

        if number.replace("+", "").isdigit():
            console.print(f"Номер телефону зареєстровано!", style="green")
            return number
        else:
            console.print("Неправильний номер телефону", style="red")
