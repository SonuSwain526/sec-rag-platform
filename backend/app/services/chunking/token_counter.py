import tiktoken

# cl100k_base is OpenAI's GPT-4-era tokenizer. We're not using an OpenAI
# model, but this is a standard, free, "close enough" proxy for estimating
# chunk size across most modern tokenizers — exact token count isn't
# critical here, just a consistent way to judge "is this chunk too big."
_encoding = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """Returns an approximate token count for the given text."""
    return len(_encoding.encode(text))