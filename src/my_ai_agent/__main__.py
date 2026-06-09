"""Allow `python -m my_ai_agent` execution without installing console scripts."""

from .cli import main

raise SystemExit(main())
