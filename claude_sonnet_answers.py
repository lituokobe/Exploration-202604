 # Multimodal Image Summarizer

```python
import base64
import logging
from pathlib import Path
from typing import Optional
from urllib.request import urlopen, Request
from urllib.error import URLError

from openai import OpenAI, OpenAIError

logger = logging.getLogger(__name__)


class ImageSummarizer:
    """
    Summarizes images using a multimodal LLM (OpenAI GPT-4o by default).

    Supports local file paths, URLs, and raw base64 strings.
    """

    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    DEFAULT_PROMPT = "Describe this image concisely and accurately."
    DEFAULT_MODEL = "gpt-4o-mini"
    MAX_IMAGE_BYTES = 20 * 1024 * 1024  # 20 MB

    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        max_tokens: int = 512,
        prompt: str = DEFAULT_PROMPT,
        timeout: int = 30,
    ) -> None:
        self.model = model
        self.max_tokens = max_tokens
        self.prompt = prompt
        self.timeout = timeout
        self._client = OpenAI(api_key=api_key, timeout=timeout)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def summarize(self, source: str) -> str:
        """
        Summarize an image from a file path, URL, or base64 string.

        Args:
            source: Local file path, HTTP/HTTPS URL, or base64-encoded image string.

        Returns:
            A natural-language summary of the image.

        Raises:
            ValueError: For unsupported formats or oversized images.
            RuntimeError: For API or network failures.
        """
        image_url = self._resolve_source(source)
        return self._call_model(image_url)

    # ------------------------------------------------------------------
    # Source resolution
    # ------------------------------------------------------------------

    def _resolve_source(self, source: str) -> dict:
        """Return an OpenAI-compatible image_url dict."""
        source = source.strip()

        if source.startswith(("http://", "https://")):
            return self._from_url(source)

        if Path(source).exists():
            return self._from_file(Path(source))

        # Assume raw base64
        return self._from_base64(source)

    def _from_url(self, url: str) -> dict:
        """Validate and return a remote URL image reference."""
        try:
            req = Request(url, method="HEAD")
            with urlopen(req, timeout=self.timeout) as resp:
                content_type = resp.headers.get("Content-Type", "")
                content_length = int(resp.headers.get("Content-Length", 0))
        except URLError as exc:
            raise RuntimeError(f"Failed to reach image URL: {exc}") from exc

        if not content_type.startswith("image/"):
            raise ValueError(f"URL does not point to an image (Content-Type: {content_type})")

        if content_length > self.MAX_IMAGE_BYTES:
            raise ValueError(
                f"Remote image exceeds size limit "
                f"({content_length / 1024 / 1024:.1f} MB > {self.MAX_IMAGE_BYTES / 1024 / 1024:.0f} MB)"
            )

        logger.debug("Resolved remote image: %s", url)
        return {"url": url}

    def _from_file(self, path: Path) -> dict:
        """Read a local image file and encode it as base64."""
        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file extension '{path.suffix}'. "
                f"Supported: {self.SUPPORTED_EXTENSIONS}"
            )

        size = path.stat().st_size
        if size > self.MAX_IMAGE_BYTES:
            raise ValueError(
                f"File '{path.name}' exceeds size limit "
                f"({size / 1024 / 1024:.1f} MB > {self.MAX_IMAGE_BYTES / 1024 / 1024:.0f} MB)"
            )

        mime = self._mime_from_extension(path.suffix.lower())
        data = base64.b64encode(path.read_bytes()).decode("utf-8")
        logger.debug("Resolved local image: %s (%d bytes)", path.name, size)
        return {"url": f"data:{mime};base64,{data}"}

    def _from_base64(self, data: str) -> dict:
        """Wrap a raw base64 string as a PNG data URI (default MIME)."""
        try:
            base64.b64decode(data, validate=True)
        except Exception as exc:
            raise ValueError("Source is not a valid file path, URL, or base64 string.") from exc

        logger.debug("Resolved base64 image (%d chars)", len(data))
        return {"url": f"data:image/png;base64,{data}"}

    # ------------------------------------------------------------------
    # Model call
    # ------------------------------------------------------------------

    def _call_model(self, image_url: dict) -> str:
        """Send the image to the multimodal model and return the summary."""
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": image_url},
                            {"type": "text", "text": self.prompt},
                        ],
                    }
                ],
            )
        except OpenAIError as exc:
            raise RuntimeError(f"Model API call failed: {exc}") from exc

        summary = response.choices[0].message.content
        if not summary:
            raise RuntimeError("Model returned an empty response.")

        logger.info("Summary generated (%d chars)", len(summary))
        return summary.strip()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _mime_from_extension(ext: str) -> str:
        mapping = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        return mapping.get(ext, "image/jpeg")
```

---

## Usage Examples

```python
import os
from image_summarizer import ImageSummarizer

summarizer = ImageSummarizer(api_key=os.environ["OPENAI_API_KEY"])

# From URL
print(summarizer.summarize("https://example.com/photo.jpg"))

# From local file
print(summarizer.summarize("/path/to/image.png"))

# Custom prompt
summarizer.prompt = "List every object visible in this image."
print(summarizer.summarize("https://example.com/scene.webp"))
```

---

## Design Decisions

| Concern | Decision |
|---|---|
| **Single responsibility** | One class, one job — resolve source → call model → return text |
| **Input flexibility** | Auto-detects URL / file path / base64 without extra flags |
| **Safety** | Size limit (20 MB) and extension allow-list before any API call |
| **Error clarity** | `ValueError` for bad input, `RuntimeError` for infrastructure failures |
| **Configurability** | Model, prompt, token limit, and timeout are constructor params |
| **Observability** | `logging` throughout; callers control log level/handler |
| **Testability** | `_resolve_source` and `_call_model` are separate, easily mockable |
| **No hidden state** | Client created once in `__init__`; thread-safe for read-only use |