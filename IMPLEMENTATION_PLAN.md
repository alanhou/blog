# Implementation Plan: Multi-Format Image Download

## Problem
Original images are ~10MB. Users need options to download in different formats (PNG, JPEG, WebP) with varying compression levels to balance quality and file size.

## Stage 1: Add Browser-Pica Library for Client-Side Compression
**Goal**: Integrate browser-pica for high-quality image compression
**Success Criteria**:
- Library loaded and available in the tool page
- No breaking changes to existing functionality
**Tests**:
- Verify existing download still works
- Check browser console for library load errors
**Status**: Complete

### Implementation Details
- Add pica library via CDN or npm (prefer CDN for simplicity)
- Use pica to resize/compress with Lanczos3 filter for quality
- Support multiple output formats: PNG, JPEG, WebP

## Stage 2: Generate Multiple Format Versions After Processing
**Goal**: Create PNG, JPEG, and WebP versions with optimized compression
**Success Criteria**:
- After watermark removal, generate three blobs: PNG, JPEG, WebP
- Each format should have appropriate quality settings
- File sizes should show clear differences
**Tests**:
- Process a 10MB image and verify all three blobs exist
- Verify file sizes: PNG (~10MB), JPEG (~1-2MB), WebP (~1-3MB)
- Visual comparison shows acceptable quality for all formats
**Status**: Complete

### Implementation Details
- After processing, generate three versions:
  1. **PNG** - Lossless, original quality (~10MB)
  2. **JPEG** - Quality 92, good for photos (~1-2MB, 80-90% reduction)
  3. **WebP** - Quality 92, best compression (~1-3MB, 70-90% reduction)
- Store blobs: `cleanedBlobs = { png: Blob, jpeg: Blob, webp: Blob }`
- Calculate and store file sizes for each format

## Stage 3: Update UI with Format Selector
**Goal**: Provide format selection with clear size/quality tradeoffs
**Success Criteria**:
- UI shows format selector (dropdown or radio buttons)
- Each option displays format name, file size, and quality description
- Download button updates based on selected format
**Tests**:
- Select PNG → download button shows PNG size
- Select JPEG → download button shows JPEG size
- Select WebP → download button shows WebP size
- Download works correctly for each format with proper filename
**Status**: Complete

### Implementation Details
- Add format selector UI:
  ```
  ○ PNG - Lossless (10.2 MB)
  ○ JPEG - High Quality (1.8 MB) ← Default
  ○ WebP - Best Compression (1.2 MB)
  ```
- Default to JPEG (best balance for most users)
- Update download button text: "Download as [FORMAT]"
- Update filename extension based on selected format

## Stage 4: Add Quality Settings (Optional Enhancement)
**Goal**: Let users fine-tune compression quality
**Success Criteria**:
- Quality slider appears for JPEG/WebP (not PNG)
- Real-time file size estimate updates
- Reasonable defaults (JPEG: 92, WebP: 92)
**Tests**:
- Switch to JPEG → slider appears
- Adjust quality → see file size estimate change
- Download at different qualities → verify file sizes match estimates
**Status**: Not Started (Optional - Deferred)

### Implementation Details
- Add quality slider (70-98 range) that shows only for JPEG/WebP
- Regenerate blob when quality changes (debounced)
- Show estimated file size for selected quality
- This stage is optional - can be deferred if time-constrained

---

## Implementation Summary

### Completed (Stages 1-3)
✅ **Stage 1**: Added Browser-Pica library via CDN
✅ **Stage 2**: Implemented multi-format generation (PNG, JPEG, WebP)
✅ **Stage 3**: Added format selector UI with file size display

### Changes Made
1. **Library Integration**: Added pica.js v9.0.1 from CDN
2. **Format Generation**: Created `generateFormats()` function that produces all three formats using high-quality Lanczos3 resampling
3. **UI Updates**:
   - Added radio button format selector
   - Display file sizes for each format
   - Download button updates based on selection
   - Default to JPEG format

### Testing Required
- [ ] Upload a ~10MB image and verify all three formats generate
- [ ] Check file sizes match expectations (PNG ~10MB, JPEG ~1-2MB, WebP ~1-3MB)
- [ ] Test downloads for all three formats
- [ ] Verify filenames are correct with proper extensions
- [ ] Check visual quality is acceptable for JPEG/WebP
- [ ] Test in Chrome, Firefox, Safari

### Next Steps
- Test the implementation at http://localhost:4321/tools/gemini-watermark
- Verify all formats work correctly
- Stage 4 (quality slider) can be added later if needed

## Technical Notes

### Browser-Pica Usage
```javascript
const pica = window.pica();

// Generate all three formats
async function generateFormats(sourceCanvas) {
  const formats = {};

  // PNG - Lossless (no pica needed, direct from canvas)
  formats.png = await new Promise((resolve) => {
    sourceCanvas.toBlob((blob) => resolve(blob), 'image/png');
  });

  // JPEG - Use pica for quality
  const jpegCanvas = document.createElement('canvas');
  jpegCanvas.width = sourceCanvas.width;
  jpegCanvas.height = sourceCanvas.height;
  await pica.resize(sourceCanvas, jpegCanvas, { quality: 3 });
  formats.jpeg = await new Promise((resolve) => {
    jpegCanvas.toBlob((blob) => resolve(blob), 'image/jpeg', 0.92);
  });

  // WebP - Use pica for quality
  const webpCanvas = document.createElement('canvas');
  webpCanvas.width = sourceCanvas.width;
  webpCanvas.height = sourceCanvas.height;
  await pica.resize(sourceCanvas, webpCanvas, { quality: 3, alpha: true });
  formats.webp = await new Promise((resolve) => {
    webpCanvas.toBlob((blob) => resolve(blob), 'image/webp', 0.92);
  });

  return formats;
}
```

### File Size Expectations
- **PNG**: ~10MB (lossless, largest)
- **JPEG** at quality 92: ~1-2MB (80-90% reduction, good for photos)
- **WebP** at quality 92: ~1-3MB (70-90% reduction, best compression)

### Format Characteristics
- **PNG**: Lossless, supports transparency, largest file size
- **JPEG**: Lossy but high quality, no transparency, widely compatible, good for photos
- **WebP**: Modern format, best compression-to-quality ratio, supports transparency

### Browser Compatibility
- PNG: Universal support
- JPEG: Universal support
- WebP: All modern browsers (Chrome, Firefox, Safari 14+, Edge)
- Fallback: If WebP not supported, hide WebP option

## Rollback Plan
If multi-format causes issues:
1. Keep format selector but disable problematic formats
2. Show "Format temporarily unavailable" message
3. Revert to PNG-only download if needed

## Definition of Done
- [ ] All three formats (PNG, JPEG, WebP) generate correctly
- [ ] File sizes are displayed accurately for each format
- [ ] Format selector UI is intuitiv
- [ ] Download works for all formats with correct filenames
- [ ] JPEG shows 80-90% size reduction from PNG
- [ ] WebP shows 70-90% size reduction from PNG
- [ ] No visual quality loss in JPEG/WebP at quality 92
- [ ] Works in Chrome, Firefox, Safari
- [ ] No console errors
