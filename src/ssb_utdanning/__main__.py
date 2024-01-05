"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """SSB Utdanning Fellesfunksjoner."""


if __name__ == "__main__":
    main(prog_name="ssb-utdanning")  # pragma: no cover
