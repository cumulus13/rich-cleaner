import re
import logging
from pathlib import Path
from typing import Optional

# Setup standard logging
logger = logging.getLogger(__name__)


class RichCleaner:
    """
    A production-ready class to parse and strip Rich markup from text and files.
    """

    def __init__(self):
        # Pre-compile regex for performance
        self._tag_regex = re.compile(r'^[a-zA-Z0-9_\-\.#\s=:]+$')

    def clean_text(self, text: str) -> str:
        """
        Natively strips all Rich markup, custom tags, colors, emojis, and styling.
        """
        out = []
        length = len(text)
        i = 0

        while i < length:
            char = text[i]

            # Handle escaped brackets: [[ -> [ and ]] -> ]
            if char in ('[', ']'):
                if i + 1 < length and text[i + 1] == char:
                    out.append(char)
                    i += 2
                    continue

            # Look for the start of a tag
            if char == '[':
                end_idx = text.find(']', i + 1)
                if end_idx != -1:
                    tag_content = text[i + 1:end_idx]
                    
                    # Verify tag_content is valid Rich markup before dropping it
                    if self._is_valid_rich_tag(tag_content):
                        i = end_idx + 1
                        continue

            out.append(char)
            i += 1

        return "".join(out)

    def _is_valid_rich_tag(self, tag: str) -> bool:
        if not tag:
            return False

        if tag.startswith('/'):
            return True
        if tag.startswith(':'):
            return True
        if tag.startswith('link') or 'link=' in tag:
            return True

        tokens = tag.split()
        first = tokens[0].lower() if tokens else ""

        if (
            first.startswith('#') or  
            first.startswith('rgb(') or 
            ':' in tag or 
            any(style in tag.lower() for style in ('bold', 'italic', 'underline', 'dim', 'reverse', 'blink', 'strike')) or
            len(tokens) > 1 
        ):
            return True

        # Fallback to compiled regex for standard single-word tags
        if self._tag_regex.match(tag):
            return True

        return False

    def clean_file(self, filepath: Path, dry_run: bool = False) -> bool:
        """
        Cleans a single file in-place.
        Returns True if the file was modified (or would be modified in dry-run).
        """
        try:
            original_text = filepath.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Safely skip binary files or files with unknown encodings
            logger.debug(f"Skipping non-UTF-8/binary file: {filepath}")
            return False
        except Exception as e:
            logger.error(f"Error reading {filepath}: {e}")
            return False

        cleaned_text = self.clean_text(original_text)

        if original_text != cleaned_text:
            if dry_run:
                logger.info(f"[DRY RUN] Would clean: {filepath}")
            else:
                try:
                    filepath.write_text(cleaned_text, encoding="utf-8")
                    logger.info(f"Cleaned: {filepath}")
                except Exception as e:
                    logger.error(f"Failed to write to {filepath}: {e}")
                    return False
            return True

        return False

    def clean_directory(self, dirpath: Path, recursive: bool = False, extension: Optional[str] = None, dry_run: bool = False):
        """
        Cleans files in a directory.
        """
        search_pattern = f"**/*{extension}" if (recursive and extension) else "**/*" if recursive else f"*{extension}" if extension else "*"
        
        modified_count = 0
        for filepath in dirpath.glob(search_pattern):
            if filepath.is_file():
                if self.clean_file(filepath, dry_run=dry_run):
                    modified_count += 1
                    
        return modified_count