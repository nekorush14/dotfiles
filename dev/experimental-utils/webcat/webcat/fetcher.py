"""HTTP fetcher module for webcat.

This module handles HTTP requests and response processing.
"""

import ipaddress
import socket
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin, urlparse

import httpx


class UnsafeURLError(Exception):
    """Raised when a URL is considered unsafe (SSRF protection)."""

    pass


class ResponseTooLargeError(Exception):
    """Raised when response exceeds size limit."""

    pass


# Blocked URL schemes
BLOCKED_SCHEMES = {"file", "ftp", "gopher", "data", "javascript"}

# Blocked hostnames
BLOCKED_HOSTNAMES = {"localhost", "127.0.0.1", "::1", "0.0.0.0"}


def is_private_ip(hostname: str) -> bool:
    """Check if hostname resolves to a private IP address.

    Args:
        hostname: Hostname or IP address string

    Returns:
        True if private/local IP, False otherwise
    """
    try:
        # Try to parse as IP address directly
        ip = ipaddress.ip_address(hostname)
        return ip.is_private or ip.is_loopback or ip.is_reserved
    except ValueError:
        pass

    # Try to resolve hostname
    try:
        addr_info = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC)
        for family, _, _, _, sockaddr in addr_info:
            ip_str = sockaddr[0]
            try:
                ip = ipaddress.ip_address(ip_str)
                if ip.is_private or ip.is_loopback or ip.is_reserved:
                    return True
            except ValueError:
                continue
    except socket.gaierror:
        # Cannot resolve, allow it (will fail later anyway)
        pass

    return False


@dataclass
class FetchResult:
    """HTTP response result."""

    url: str
    status_code: int
    content: bytes
    content_type: str
    encoding: Optional[str]
    headers: dict[str, str]

    @property
    def is_html(self) -> bool:
        """Check if content is HTML."""
        return "text/html" in self.content_type.lower()

    @property
    def is_image(self) -> bool:
        """Check if content is an image."""
        return self.content_type.lower().startswith("image/")

    @property
    def is_pdf(self) -> bool:
        """Check if content is a PDF."""
        return "application/pdf" in self.content_type.lower()

    @property
    def text(self) -> str:
        """Decode content as text."""
        encoding = self.encoding or "utf-8"
        return self.content.decode(encoding, errors="replace")


class WebFetcher:
    """HTTP request handler."""

    # Default maximum response size: 50MB
    DEFAULT_MAX_SIZE = 50 * 1024 * 1024

    def __init__(
        self,
        user_agent: str = "webcat/1.0",
        timeout: float = 30.0,
        max_redirects: int = 10,
        max_size: int = DEFAULT_MAX_SIZE,
    ) -> None:
        """Initialize WebFetcher.

        Args:
            user_agent: User-Agent header value
            timeout: Request timeout in seconds
            max_redirects: Maximum number of redirects to follow
            max_size: Maximum response size in bytes
        """
        self.user_agent = user_agent
        self.timeout = timeout
        self.max_redirects = max_redirects
        self.max_size = max_size
        self._client: Optional[httpx.Client] = None
        self._allow_private = False  # For testing only

    @property
    def client(self) -> httpx.Client:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.Client(
                headers={"User-Agent": self.user_agent},
                timeout=self.timeout,
                follow_redirects=True,
                max_redirects=self.max_redirects,
            )
        return self._client

    def _validate_url(self, url: str) -> None:
        """Validate URL for SSRF protection.

        Args:
            url: URL to validate

        Raises:
            UnsafeURLError: If URL is unsafe
        """
        parsed = urlparse(url)

        # Check scheme (always blocked, even in test mode)
        if parsed.scheme.lower() in BLOCKED_SCHEMES:
            raise UnsafeURLError(f"Blocked URL scheme: {parsed.scheme}")

        # Skip hostname/IP checks if private IPs are allowed (testing mode)
        if self._allow_private:
            return

        # Check hostname
        hostname = parsed.hostname or ""

        if hostname.lower() in BLOCKED_HOSTNAMES:
            raise UnsafeURLError(f"Blocked hostname: {hostname}")

        # Check for private IPs
        if is_private_ip(hostname):
            raise UnsafeURLError(f"Private IP address not allowed: {hostname}")

    def fetch(self, url: str) -> FetchResult:
        """Fetch content from URL.

        Args:
            url: URL to fetch

        Returns:
            FetchResult object

        Raises:
            UnsafeURLError: URL is blocked (SSRF protection)
            ResponseTooLargeError: Response exceeds size limit
            httpx.HTTPError: Network error
            httpx.TimeoutException: Timeout
        """
        # SSRF protection
        self._validate_url(url)

        response = self.client.get(url)

        # Check response size from Content-Length header
        content_length = response.headers.get("content-length")
        if content_length and int(content_length) > self.max_size:
            raise ResponseTooLargeError(
                f"Response too large: {content_length} bytes (max: {self.max_size})"
            )

        # Check actual content size
        content = response.content
        if len(content) > self.max_size:
            raise ResponseTooLargeError(
                f"Response too large: {len(content)} bytes (max: {self.max_size})"
            )

        # Extract encoding from response
        encoding = response.encoding if response.encoding else None

        # Build headers dict
        headers = dict(response.headers)

        return FetchResult(
            url=str(response.url),
            status_code=response.status_code,
            content=content,
            content_type=response.headers.get("content-type", ""),
            encoding=encoding,
            headers=headers,
        )

    def fetch_image(self, url: str, base_url: str) -> Optional[bytes]:
        """Fetch image data with relative URL support.

        Args:
            url: Image URL (relative or absolute)
            base_url: Base URL for relative resolution

        Returns:
            Image data bytes, or None on failure
        """
        try:
            resolved_url = self.resolve_url(url, base_url)
            result = self.fetch(resolved_url)
            if result.status_code == 200 and result.is_image:
                return result.content
            return None
        except Exception:
            return None

    def resolve_url(self, url: str, base_url: str) -> str:
        """Resolve a URL against a base URL.

        Args:
            url: URL to resolve (may be relative)
            base_url: Base URL for resolution

        Returns:
            Absolute URL
        """
        # Check if URL is already absolute
        parsed = urlparse(url)
        if parsed.scheme and parsed.netloc:
            return url

        # Resolve relative URL
        return urljoin(base_url, url)

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> "WebFetcher":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()
