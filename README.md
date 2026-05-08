# ai-skills
codex and claude skills

# mac 配置

## 新的 git 仓库位置：

```
export ai_skills=~/git/ai-skills
```

## claude

### 软连接 skills 目录

```
sudo rm -rf ~/.claude/skills
ln -s $ai_skills/skills ~/.claude/skills
```

### 配置 agent

```
sudo rm -rf ~/.claude/CLAUDE.md
ln -s $ai_skills/agent/CLAUDE.md ~/.claude/CLAUDE.md
```

## codex

### 软连接 skills 目录

```
sudo rm -rf ~/.agents
ln -s $ai_skills/skills ~/.agents
```


### 配置 agent

```
sudo rm -rf ~/.codex/AGENTS.md
ln -s $ai_skills/agent/AGENTS.md ~/.codex/AGENTS.md
```

# 验证 skills 是否配置成功

1. 进入 codex 或者 claude

2. 输入：```test local skill```

3. 若正确输出：```local skill is working.``` 则配置成功。

# skills

## test-skill

验证 skill 是否配置成功

## research

技术论文调研

来源：https://github.com/acking-you/myclaude-skills/blob/main/skills/research/SKILL.md

## web-access

AI Agent 原本的联网能力（WebSearch、WebFetch）缺少调度策略和浏览器自动化能力。这个 Agent Skill 补上的是：联网策略 + CDP 浏览器操作 + 站点经验积累。兼容所有支持 SKILL.md 的 Agent（Claude Code、Cursor、Gemini CLI、Codex CLI 等）。

来源：https://github.com/eze-is/web-access

目前版本：v2.5.0

