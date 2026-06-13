# Production-Grade Image Summarization Class

import base64
import logging
from pathlib import Path
from typing import Optional, Union
from dataclasses import dataclass
from enum import Enum

import anthropic

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageFormat(Enum):
    """Supported image formats for the API."""
    JPEG = "image/jpeg"
    PNG = "image/png"
    GIF = "image/gif"
    WEBP = "image/webp"


@dataclass
class SummaryResult:
    """Result of image summarization."""
    summary: str
    image_path: str
    model: str
    tokens_used: Optional[dict] = None


class ImageSummarizer:
    """
    Production-grade image summarization using Claude's vision capabilities.

    Supports both local files and URLs with automatic format detection,
    error handling, and logging.
    """

    # Supported image formats
    SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    MAX_FILE_SIZE_MB = 20

    def __init__(
            self,
            api_key: Optional[str] = None,
            model: str = "claude-3-5-sonnet-20241022",
            timeout: int = 30,
    ):
        """
        Initialize the ImageSummarizer.

        Args:
            api_key: Anthropic API key. If None, uses ANTHROPIC_API_KEY env var.
            model: Claude model to use for summarization.
            timeout: Request timeout in seconds.
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.timeout = timeout
        logger.info(f"ImageSummarizer initialized with model: {model}")

    def _validate_local_file(self, file_path: Union[str, Path]) -> Path:
        """
        Validate that a local file exists and is a supported format.

        Args:
            file_path: Path to the image file.

        Returns:
            Path object if valid.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If format is not supported or file is too large.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Image file not found: {file_path}")

        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format: {path.suffix}. "
                f"Supported: {self.SUPPORTED_FORMATS}"
            )

        file_size_mb = path.stat().st_size / (1024 * 1024)
        if file_size_mb > self.MAX_FILE_SIZE_MB:
            raise ValueError(
                f"File too large: {file_size_mb:.2f}MB. "
                f"Max: {self.MAX_FILE_SIZE_MB}MB"
            )

        return path

    def _get_image_format(self, file_path: Union[str, Path]) -> ImageFormat:
        """Detect image format from file extension."""
        suffix = Path(file_path).suffix.lower()
        format_map = {
            ".jpg": ImageFormat.JPEG,
            ".jpeg": ImageFormat.JPEG,
            ".png": ImageFormat.PNG,
            ".gif": ImageFormat.GIF,
            ".webp": ImageFormat.WEBP,
        }
        return format_map.get(suffix, ImageFormat.JPEG)

    def _encode_image_to_base64(self, file_path: Path) -> str:
        """Encode image file to base64 string."""
        with open(file_path, "rb") as image_file:
            return base64.standard_b64encode(image_file.read()).decode("utf-8")

    def summarize_from_file(
            self,
            file_path: Union[str, Path],
            prompt: Optional[str] = None,
    ) -> SummaryResult:
        """
        Summarize an image from a local file.

        Args:
            file_path: Path to the image file.
            prompt: Custom prompt for summarization. If None, uses default.

        Returns:
            SummaryResult containing the summary and metadata.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If format is unsupported or file is too large.
            anthropic.APIError: If API call fails.
        """
        # Validate file
        file_path = self._validate_local_file(file_path)
        logger.info(f"Processing image: {file_path}")

        # Encode image
        image_data = self._encode_image_to_base64(file_path)
        image_format = self._get_image_format(file_path)

        # Summarize
        return self._call_api(
            image_data=image_data,
            image_format=image_format,
            image_source=str(file_path),
            prompt=prompt,
        )

    def summarize_from_url(
            self,
            image_url: str,
            prompt: Optional[str] = None,
    ) -> SummaryResult:
        """
        Summarize an image from a URL.

        Args:
            image_url: URL of the image.
            prompt: Custom prompt for summarization. If None, uses default.

        Returns:
            SummaryResult containing the summary and metadata.

        Raises:
            anthropic.APIError: If API call fails.
        """
        logger.info(f"Processing image from URL: {image_url}")

        return self._call_api(
            image_url=image_url,
            image_source=image_url,
            prompt=prompt,
        )

    def _call_api(
            self,
            image_source: str,
            prompt: Optional[str] = None,
            image_data: Optional[str] = None,
            image_format: Optional[ImageFormat] = None,
            image_url: Optional[str] = None,
    ) -> SummaryResult:
        """
        Call the Claude API with image content.

        Args:
            image_source: Source identifier for logging.
            prompt: Custom prompt or None for default.
            image_data: Base64 encoded image data (for local files).
            image_format: Image format (for local files).
            image_url: Image URL (for URLs).

        Returns:
            SummaryResult with the summary.
        """
        if prompt is None:
            prompt = (
                "Please provide a concise but comprehensive summary of this image. "
                "Include the main subjects, key details, and any text visible in the image."
            )

        # Build image content
        if image_url:
            image_content = {
                "type": "image",
                "source": {
                    "type": "url",
                    "url": image_url,
                },
            }
        else:
            image_content = {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": image_format.value,
                    "data": image_data,
                },
            }

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            image_content,
                            {
                                "type": "text",
                                "text": prompt,
                            },
                        ],
                    }
                ],
            )

            summary = response.content[0].text
            logger.info(f"Successfully summarized image: {image_source}")

            return S

