import argparse
import logging
import sys
from pathlib import Path
from rich_cleaner.core import RichCleaner

def main():
    parser = argparse.ArgumentParser(
        description="Production-ready CLI to strip Rich formatting markup from files."
    )
    
    parser.add_argument(
        "target", 
        type=Path, 
        help="Target file or directory to clean."
    )
    
    parser.add_argument(
        "-r", "--recursive", 
        action="store_true", 
        help="Process directories recursively."
    )
    
    parser.add_argument(
        "-d", "--dry-run", 
        action="store_true", 
        help="Show what files would be modified without actually changing them."
    )
    
    parser.add_argument(
        "-e", "--ext", 
        type=str, 
        default=None, 
        help="Only process files with this extension (e.g., .log, .txt). Defaults to all files."
    )
    
    parser.add_argument(
        "-q", "--quiet", 
        action="store_true", 
        help="Suppress standard output, only show errors."
    )

    args = parser.args

    # Configure logging based on verbosity
    log_level = logging.ERROR if args.quiet else logging.INFO
    logging.basicConfig(format="%(message)s", level=log_level)

    if not args.target.exists():
        logging.error(f"Error: Target path '{args.target}' does not exist.")
        sys.exit(1)

    cleaner = RichCleaner()
    
    if args.target.is_file():
        cleaner.clean_file(args.target, dry_run=args.dry_run)
    elif args.target.is_dir():
        modified = cleaner.clean_directory(
            args.target, 
            recursive=args.recursive, 
            extension=args.ext, 
            dry_run=args.dry_run
        )
        verb = "Would modify" if args.dry_run else "Modified"
        logging.info(f"\n{verb} {modified} files.")
    else:
        logging.error(f"Error: Target '{args.target}' is neither a file nor a directory.")
        sys.exit(1)

if __name__ == "__main__":
    main()