import typer

app = typer.Typer()


@app.command()
def command1():
    """
    First command description
    """
    print("Hello, World! from command1")
    pass


@app.command()
def command2():
    """
    Second command description
    """
    print("Hello, World! from command2")
    pass


if __name__ == "__main__":
    app()
