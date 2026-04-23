#!/bin/bash

# Map of directory names to blog post files
declare -A posts=(
  ["act-wisely-cultivating-meta-cognitive-tool"]="arxiv-act-wisely-cultivating-meta-cognitive-tool.mdx"
  ["ads-in-ai-chatbots-an-analysis"]="arxiv-ads-in-ai-chatbots-an-analysis.mdx"
  ["bas-a-decision-theoretic-approach-to"]="arxiv-bas-a-decision-theoretic-approach-to.mdx"
  ["clawbench-can-ai-agents-complete-everyday"]="arxiv-clawbench-can-ai-agents-complete-everyday.mdx"
  ["demystifying-opd-length-inflation-and-stabilization"]="arxiv-demystifying-opd-length-inflation-and-stabilization.mdx"
  ["faithful-grpo-improving-visual-spatial-reasoning"]="arxiv-faithful-grpo-improving-visual-spatial-reasoning.mdx"
  ["gradient-boosting-within-a-single-attention"]="arxiv-gradient-boosting-within-a-single-attention.mdx"
  ["meta-learning-in-context-enables-training-free"]="arxiv-meta-learning-in-context-enables-training-free.mdx"
  ["openvlthinkerv2-a-generalist-multimodal-reasoning"]="arxiv-openvlthinkerv2-a-generalist-multimodal-reasoning.mdx"
  ["piarena-a-platform-for-prompt-injection"]="arxiv-piarena-a-platform-for-prompt-injection.mdx"
  ["psi-shared-state-for-coherent-ai-instruments"]="arxiv-psi-shared-state-for-coherent-ai-instruments.mdx"
  ["refined-detection-for-gumbel-watermarking"]="arxiv-refined-detection-for-gumbel-watermarking.mdx"
  ["seeing-but-not-thinking-routing-distraction"]="arxiv-seeing-but-not-thinking-routing-distraction.mdx"
  ["supernova-eliciting-general-reasoning-in-llms"]="arxiv-supernova-eliciting-general-reasoning-in-llms.mdx"
  ["target-policy-optimization"]="arxiv-target-policy-optimization.mdx"
  ["textttyc-bench-benchmarking-ai-agents-for"]="arxiv-textttyc-bench-benchmarking-ai-agents-for.mdx"
  ["what-drives-representation-steering-a-mechanistic"]="arxiv-what-drives-representation-steering-a-mechanistic.mdx"
)

echo "Updating blog posts with animations..."
echo ""

for dir in "${!posts[@]}"; do
  post_file="src/content/blog/${posts[$dir]}"

  if [ ! -f "$post_file" ]; then
    echo "✗ Post not found: $post_file"
    continue
  fi

  # Check if animation line already exists
  if grep -q "!\[Concept animation\](/arxiv-visuals/$dir/ConceptScene.gif)" "$post_file"; then
    echo "⊙ Already has animation: ${posts[$dir]}"
    continue
  fi

  # Add animation after the frontmatter (after the second ---)
  # Find the line number of the second ---
  line_num=$(grep -n "^---$" "$post_file" | sed -n '2p' | cut -d: -f1)

  if [ -z "$line_num" ]; then
    echo "✗ Could not find frontmatter end: ${posts[$dir]}"
    continue
  fi

  # Insert animation line after frontmatter
  sed -i '' "${line_num}a\\
\\
![Concept animation](/arxiv-visuals/$dir/ConceptScene.gif)\\
" "$post_file"

  echo "✓ Updated: ${posts[$dir]}"
done

echo ""
echo "Done! All blog posts updated with animations."
