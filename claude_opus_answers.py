 # Multimodal Image Summarizer

A simple, production-grade Python class for summarizing images using a multimodal model (OpenAI's GPT-4 Vision).

```python
"""image_summarizer.py

Production-grade image summarization using a multimodal LLM.
"""

from __future__ import annotations

import base64
import logging
import mimetypes
import time
from pathlib import Path
from typing import Union

import httpx
from openai import OpenAI, APIError, APITimeoutError, RateLimitError

logger = logging.getLogger(__name__)

# Supported image formats by most vision models
_SUPPORTED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


class ImageSummarizerError(Exception):
    """Raised when image summarization fails permanently."""


class ImageSummarizer:
    """Summarize images using a multimodal model.

    Example:
        summarizer = ImageSummarizer(api_key="sk-...")
        summary = summarizer.summarize("photo.jpg")
        print(summary)
    """

    def __init__(
        self,
        api_key: str,
        *,
        model: str = "gpt-4o-mini",
        max_tokens: int = 500,
        timeout: float = 60.0,
        max_retries: int = 3,
        default_prompt: str = "Describe and summarize this image concisely.",
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")

        self._client = OpenAI(api_key=api_key, timeout=timeout)
        self._model = model
        self._max_tokens = max_tokens
        self._max_retries = max_retries
        self._default_prompt = default_prompt

    # ---------- Public API ----------

    def summarize(
        self,
        image: Union[str, Path, bytes],
        *,
        prompt: str | None = None,
    ) -> str:
        """Summarize a single image.

        Args:
            image: A local file path, a public URL, or raw image bytes.
            prompt: Optional custom instruction. Falls back to default.

        Returns:
            The model-generated summary text.

        Raises:
            ImageSummarizerError: If summarization fails after retries.
            ValueError: If the input is invalid or unsupported.
        """
        image_url = self._build_image_url(image)
        prompt = prompt or self._default_prompt

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ]

        return self._call_with_retries(messages)

    # ---------- Internal helpers ----------

    def _build_image_url(self, image: Union[str, Path, bytes]) -> str:
        """Normalize different image inputs into a model-ready URL/data-URI."""
        if isinstance(image, bytes):
            return self._encode_bytes(image)

        if isinstance(image, (str, Path)):
            image_str = str(image)
            if image_str.startswith(("http://", "https://")):
                return image_str  # Public URL — pass through.
            return self._encode_file(Path(image_str))

        raise ValueError(f"Unsupported image type: {type(image)!r}")

    def _encode_file(self, path: Path) -> str:
        if not path.is_file():
            raise ValueError(f"Image file not found: {path}")

        mime_type, _ = mimetypes.guess_type(path.name)
        if mime_type not in _SUPPORTED_MIME_TYPES:
            raise ValueError(
                f"Unsupported image format '{mime_type}'. "
                f"Supported: {sorted(_SUPPORTED_MIME_TYPES)}"
            )

        return self._encode_bytes(path.read_bytes(), mime_type)

    @staticmethod
    def _encode_bytes(data: bytes, mime_type: str = "image/jpeg") -> str:
        if not data:
            raise ValueError("Image bytes are empty")
        b64 = base64.b64encode(data).decode("utf-8")
        return f"data:{mime_type};base64,{b64}"

    def _call_with_retries(self, messages: list[dict]) -> str:
        """Call the API with exponential backoff on transient errors."""
        last_exc: Exception | None = None

        for attempt in range(1, self._max_retries + 1):
            try:
                response = self._client.chat.completions.create(
                    model=self._model,
                    messages=messages,
                    max_tokens=self._max_tokens,
                )
                content = response.choices[0].message.content
                if not content:
                    raise ImageSummarizerError("Model returned empty response")
                return content.strip()

            except (RateLimitError, APITimeoutError, httpx.TransportError) as exc:
                last_exc = exc
                backoff = 2 ** (attempt - 1)
                logger.warning(
                    "Transient error on attempt %d/%d: %s. Retrying in %ss.",
                    attempt, self._max_retries, exc, backoff,
                )
                time.sleep(backoff)

            except APIError as exc:
                # Non-retryable API error (e.g. bad request, auth).
                logger.error("API error: %s", exc)
                raise ImageSummarizerError(f"API error: {exc}") from exc

        raise ImageSummarizerError(
            f"Failed after {self._max_retries} attempts"
        ) from last_exc
```

## Usage

```python
import os
from image_summarizer import ImageSummarizer

summarizer = ImageSummarizer(api_key=os.environ["OPENAI_API_KEY"])

# From a local file
print(summarizer.summarize("diagram.png"))

# From a URL
print(summarizer.summarize("https://example.com/cat.jpg"))

# From raw bytes with a custom prompt