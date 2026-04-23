# IP Lookup Component

A client-side Astro component for looking up IP address information using the ipinfo.io API.

## Usage

### Inline Mode (default)

```astro
---
import IPLookup from '@/components/IPLookup.astro';
---

<p>Google DNS: <IPLookup ip="8.8.8.8" inline /></p>
```

Output: `8.8.8.8 (Mountain View, US, AS15169 Google LLC)`

### Block Mode

```astro
---
import IPLookup from '@/components/IPLookup.astro';
---

<IPLookup ip="8.8.8.8" />
```

Output:
```
8.8.8.8
📍 Mountain View, California, US
🏢 AS15169 Google LLC
🌐 dns.google
🕐 America/Los_Angeles
```

## Props

- `ip` (required): IP address to lookup
- `inline` (optional): Display inline with minimal info (default: false)

## API Limits

Uses ipinfo.io free tier:
- 50,000 requests/month
- No authentication required
- Rate limited to prevent abuse

## Example in MDX

```mdx
import IPLookup from '@/components/IPLookup.astro';

# Network Analysis

The server is located at <IPLookup ip="1.1.1.1" inline />.

## Full Details

<IPLookup ip="1.1.1.1" />
```

## Styling

The component uses CSS custom properties for theming:
- `--text-primary`: Main text color
- `--text-secondary`: Secondary text color
- `--bg-secondary`: Background color (block mode)
- `--error-color`: Error message color

## Features

- ✅ Client-side lookup (no backend needed)
- ✅ Works with Astro view transitions
- ✅ Loading states
- ✅ Error handling
- ✅ Responsive design
- ✅ Two display modes
