def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if block == "":
            continue
        if "\n" in block:
            parts = []
            for part in block.split("\n"):
                if part == "":
                    continue
                parts.append(part.strip())
            blocks.append("\n".join(parts))
        else:
            blocks.append(block)
    return blocks
