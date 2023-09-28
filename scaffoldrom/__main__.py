"""Allow scaffoldrom to be executable through `python -m scaffoldrom`."""
from scaffoldrom.cli import main


if __name__ == "__main__":  # pragma: no cover
    main(prog_name="scaffoldrom")
