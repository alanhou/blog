---
title:
  en: "Notes: Deep Dive into LLMs like ChatGPT"
  zh: "笔记：深入理解 ChatGPT 等大语言模型"
description:
  en: "Key takeaways from Andrej Karpathy's 3-hour deep dive into how LLMs are built and how to think about them"
  zh: "Andrej Karpathy 三小时深度讲解大语言模型的核心要点"
date: 2025-02-05
tags: ["ai", "llm", "machine-learning", "andrej-karpathy"]
image: "https://i4.ytimg.com/vi/7xTGNNLPyMI/hqdefault.jpg"
---

::en
This post summarizes Andrej Karpathy's video "Deep Dive into LLMs like ChatGPT" (Feb 2025). The video is freely available for educational use. Watch the original: [YouTube](https://www.youtube.com/watch?v=7xTGNNLPyMI)

## The Three Stages of Training

Building ChatGPT involves three sequential stages:

**1. Pre-training** - Download and process the internet. The FineWeb dataset, for example, contains 44TB of filtered text (15 trillion tokens). This stage teaches the model statistical patterns of language.

**2. Supervised Fine-tuning (SFT)** - Train on conversation datasets. Human labelers (often with LLM assistance) create millions of example conversations following specific instructions. This transforms the base model into an assistant.

**3. Reinforcement Learning (RL)** - The newest and most exciting stage. DeepSeek R1 showed that RL can teach models to "think" - they learn to backtrack, re-evaluate, and try different approaches. This emerges naturally from trial-and-error optimization.

## What You're Actually Talking To

When you chat with ChatGPT, you're not talking to a magical AI. You're getting a statistical simulation of a human labeler who was hired to create training data. The labeler follows instructions, does research, and writes responses. The model learns to imitate this process.

If your exact question exists in the training data, you'll likely get something close to what that labeler wrote. If not, the model combines its pre-training knowledge with the patterns it learned from similar conversations.

## Hallucinations: Why They Happen

Models hallucinate because they imitate the *style* of confident answers, not the *process* of knowing something. In training data, questions like "Who is Tom Cruise?" always get confident answers. So when asked about someone who doesn't exist, the model produces a confident-sounding answer anyway.

Modern models have improved through:
- Adding "I don't know" examples to training data
- Tool use (web search) to verify facts
- Training models to recognize the boundaries of their knowledge

## Models Need Tokens to Think

This is one of the most practical insights. Each token generation involves a fixed amount of computation. Complex problems can't be solved in a single token.

Bad prompt: "What is 23 × 177? Answer in one word."
Good prompt: "What is 23 × 177? Show your work."

The second prompt lets the model spread computation across multiple tokens, creating intermediate results. This is why ChatGPT shows its reasoning - those steps aren't just for you, they're necessary for the model to reach correct answers.

For math and counting tasks, ask the model to use code. Python's arithmetic is more reliable than the model's "mental math."

## The Swiss Cheese Model of Capabilities

LLMs are incredibly capable across many domains but have random holes. A model might solve Olympiad-level math problems but fail at "Is 9.11 bigger than 9.9?" These holes exist because:

- Tokenization obscures character-level information
- Some patterns are rare in training data
- The model's "mental arithmetic" has limits

Don't treat these models as infallible. Use them as tools - for inspiration, first drafts, and assistance. Verify their work.

## Thinking Models (o1, o3, DeepSeek R1)

These models were trained with RL to develop "chains of thought." They don't just produce answers - they reason through problems, backtrack when stuck, and verify from multiple angles.

The thinking process emerges from optimization. No human programmed "wait, let me reconsider" - the model discovered that this strategy improves accuracy.

## What's Coming

- **Multimodality**: Native audio and image handling (tokenize spectrograms and image patches)
- **Agents**: Long-running tasks with human supervision
- **Computer use**: Models taking keyboard/mouse actions
- **Test-time training**: Models that actually learn from their experiences (currently they're frozen after training)

## Practical Takeaways

1. Don't trust models blindly - they hallucinate
2. Give models room to think (show your work, use code)
3. Use tools when available (web search, code interpreter)
4. Understand you're talking to a simulation of a labeler, not magic
5. Expect random failures - the Swiss cheese model
::

::zh
本文总结了 Andrej Karpathy 的视频《深入理解 ChatGPT 等大语言模型》（2025年2月）。该视频可免费用于教育目的。原视频：[YouTube](https://www.youtube.com/watch?v=7xTGNNLPyMI)

## 训练的三个阶段

构建 ChatGPT 需要三个连续阶段：

**1. 预训练** - 下载并处理互联网数据。以 FineWeb 数据集为例，包含 44TB 过滤后的文本（15万亿个 token）。这个阶段让模型学习语言的统计规律。

**2. 监督微调（SFT）** - 在对话数据集上训练。人工标注员（通常借助 LLM）按照特定指令创建数百万条示例对话。这将基础模型转变为助手。

**3. 强化学习（RL）** - 最新也最令人兴奋的阶段。DeepSeek R1 表明，RL 可以教会模型"思考"——它们学会回溯、重新评估、尝试不同方法。这是从试错优化中自然涌现的。

## 你实际在和谁对话

和 ChatGPT 聊天时，你并不是在和神奇的 AI 对话。你得到的是对人工标注员的统计模拟——这些标注员被雇来创建训练数据。标注员遵循指令、做调研、写回复。模型学习模仿这个过程。

如果你的问题恰好在训练数据中，你很可能得到接近那位标注员所写的答案。如果不在，模型会结合预训练知识和从类似对话中学到的模式。

## 幻觉：为什么会发生

模型产生幻觉是因为它们模仿的是自信回答的*风格*，而不是知道某事的*过程*。在训练数据中，"汤姆·克鲁斯是谁？"这类问题总是得到自信的回答。所以当被问到一个不存在的人时，模型也会产生听起来很自信的答案。

现代模型通过以下方式改进：
- 在训练数据中添加"我不知道"的示例
- 使用工具（网络搜索）验证事实
- 训练模型识别自身知识的边界

## 模型需要 Token 来思考

这是最实用的洞见之一。每个 token 的生成涉及固定量的计算。复杂问题无法在单个 token 中解决。

差的提示："23 × 177 等于多少？用一个词回答。"
好的提示："23 × 177 等于多少？展示你的计算过程。"

第二种提示让模型将计算分散到多个 token 上，产生中间结果。这就是为什么 ChatGPT 会展示推理过程——那些步骤不只是给你看的，它们是模型得出正确答案所必需的。

对于数学和计数任务，让模型使用代码。Python 的算术比模型的"心算"更可靠。

## 能力的瑞士奶酪模型

LLM 在许多领域能力惊人，但存在随机的漏洞。一个模型可能解决奥林匹克级别的数学题，却在"9.11 和 9.9 哪个大？"上失败。这些漏洞存在是因为：

- 分词遮蔽了字符级信息
- 某些模式在训练数据中很少见
- 模型的"心算"有局限

不要把这些模型当作万无一失的。把它们当工具用——用于获取灵感、初稿和辅助。验证它们的工作。

## 思考模型（o1、o3、DeepSeek R1）

这些模型通过 RL 训练来发展"思维链"。它们不只是产生答案——它们推理问题、卡住时回溯、从多个角度验证。

思考过程从优化中涌现。没有人编程"等等，让我重新考虑"——模型自己发现这种策略能提高准确率。

## 未来趋势

- **多模态**：原生处理音频和图像（对频谱图和图像块进行分词）
- **智能体**：需要人类监督的长时间运行任务
- **计算机操作**：模型执行键盘/鼠标操作
- **测试时训练**：能从经验中真正学习的模型（目前训练后就固定了）

## 实用要点

1. 不要盲目信任模型——它们会产生幻觉
2. 给模型思考空间（展示过程、使用代码）
3. 有工具时就用（网络搜索、代码解释器）
4. 理解你在和标注员的模拟对话，不是魔法
5. 预期随机失败——瑞士奶酪模型
::
