#!/usr/bin/env python3
"""IP address lookup utility using ipinfo.io API."""

import argparse
import json
import sys

import requests


def lookup_ip(ip_address, token=None):
    """Look up IP address information.

    Args:
        ip_address: IP address to lookup
        token: Optional ipinfo.io API token for higher rate limits

    Returns:
        dict: IP information including location, org, etc.
    """
    url = f"https://ipinfo.io/{ip_address}/json"
    params = {"token": token} if token else {}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to lookup IP: {e}")


def format_output(data):
    """Format IP data for human-readable output."""
    lines = []

    # Basic info
    if "ip" in data:
        lines.append(f"IP Address: {data['ip']}")

    # Location
    if "city" in data or "region" in data or "country" in data:
        location_parts = []
        if "city" in data:
            location_parts.append(data["city"])
        if "region" in data:
            location_parts.append(data["region"])
        if "country" in data:
            location_parts.append(data["country"])
        lines.append(f"Location: {', '.join(location_parts)}")

    # Coordinates
    if "loc" in data:
        lines.append(f"Coordinates: {data['loc']}")

    # Organization/ISP
    if "org" in data:
        lines.append(f"Organization: {data['org']}")

    # Hostname
    if "hostname" in data:
        lines.append(f"Hostname: {data['hostname']}")

    # Postal code
    if "postal" in data:
        lines.append(f"Postal Code: {data['postal']}")

    # Timezone
    if "timezone" in data:
        lines.append(f"Timezone: {data['timezone']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="IP address lookup utility",
        epilog="Free tier: 50k requests/month. Get token at https://ipinfo.io/signup"
    )
    parser.add_argument("ip", help="IP address to lookup")
    parser.add_argument(
        "--token",
        help="ipinfo.io API token (or set IPINFO_TOKEN env var)",
        default=None
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON response"
    )

    args = parser.parse_args()

    # Check for token in environment if not provided
    token = args.token
    if not token:
        import os
        token = os.environ.get("IPINFO_TOKEN")

    try:
        data = lookup_ip(args.ip, token)

        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(format_output(data))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
