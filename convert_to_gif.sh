#!/bin/bash

# Convert all animation.mp4 files to ConceptScene.gif
find public/arxiv-visuals -name "animation.mp4" -type f | while read mp4_file; do
    dir=$(dirname "$mp4_file")
    gif_file="$dir/ConceptScene.gif"

    echo "Converting: $mp4_file -> $gif_file"

    ffmpeg -i "$mp4_file" \
        -vf "fps=10,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
        -loop 0 \
        "$gif_file" \
        -y \
        2>&1 | grep -E "(frame=|error|Error)" | tail -2

    if [ -f "$gif_file" ]; then
        size=$(du -h "$gif_file" | cut -f1)
        echo "✓ Created: $gif_file ($size)"
    else
        echo "✗ Failed: $gif_file"
    fi
    echo "---"
done

echo ""
echo "Summary:"
find public/arxiv-visuals -name "ConceptScene.gif" -type f | wc -l | xargs echo "Total GIFs created:"
