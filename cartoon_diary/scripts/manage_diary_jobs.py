"""Command-line helper to trigger diary generation jobs."""

import argparse

from apps.generation.pipelines import trigger_cartoon_generation


def main() -> None:
    parser = argparse.ArgumentParser(description="Trigger cartoon generation for a diary entry")
    parser.add_argument("diary_entry_id", type=int)
    args = parser.parse_args()
    trigger_cartoon_generation(diary_entry_id=args.diary_entry_id)


if __name__ == "__main__":
    main()
