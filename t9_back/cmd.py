import typer
import uvicorn

from . import __version__
from .lib.settings import AppSettings
from .lib.setup_app import setup_app


cli_app = typer.Typer(name="t9-back")


@cli_app.command(help="Shows the app version")
def version() -> None:
    typer.echo(__version__)


@cli_app.command(help="Runs a server")
def server() -> None:
    settings = AppSettings()
    app = setup_app(settings)
    uvicorn.run(app, host=settings.host, port=settings.port, debug=settings.debug)
