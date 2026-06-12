# ai-skills
codex and claude skills

# skills 配置

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


# hooks 配置

## 增加权限

给 hooks 目录下所有的 hook.sh 文件给 +x 权限。
```
find $ai_skills/hooks -type f -name "hook.sh" -exec chmod +x {} \;
```

单独给某一个文件增加权限：
```
chmod +x hook.sh
```


## claude

软连接 hooks 文件
```
sudo rm -rf ~/.claude/hooks/
ln -s $ai_skills/hooks ~/.claude/hooks

```


## codex

codex 版本：v0.129.0

1. 修改 config.toml 文件

增加配置：
```
[features]
hooks = true
```

2. 撰写 hook.json 文件

3. 软连接 hook 文件
/hooks/hooks.json

```
sudo rm -rf ~/.codex/hooks.json
ln -s $ai_skills/hooks/hooks.json ~/.codex/hooks.json
```



