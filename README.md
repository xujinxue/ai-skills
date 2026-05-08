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
