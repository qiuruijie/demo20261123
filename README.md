# git-practice

一个专门用来走通「分支 → PR → CI → 合并 → CD」的最小仓库。跑完下面的清单，你就能在真实项目里安全地操作了。

## 文件说明

- `hello.py` — 唯一的业务文件，改它来触发 CI。
- `pyproject.toml` — 里面配了 Ruff 的规则（E/F/I/UP）。
- `.github/workflows/ci.yml` — 开 PR 或推 main 时自动跑 `ruff check`。
- `.github/workflows/cd.yml` — 合并进 main 后自动跑一次"假装部署"，打印分支和提交号。

## 第一次跑起来

```powershell
# 1. 本地建仓库（把文件放到这个目录后执行）
git init
git add .
git commit -m "init: practice repo"

# 2. 在 GitHub 上建一个空仓库 git-practice（不要勾选 README / .gitignore）
git remote add origin https://github.com/<你的账号>/git-practice.git
git branch -M main
git push -u origin main
```

推完去仓库的 **Actions** 页面，应该能看到 `CD` 跑了一次并输出 `deploy ok`。

## 练习清单（按顺序做，约 40 分钟）

### 1. 开分支、改代码

```powershell
git switch -c feature/add-lang
# 编辑 hello.py，随便加点东西，比如把 GREETING 改成 "hello, workflow"
git add .
git commit -m "feat: 改一下问候语"
git push -u origin feature/add-lang
```

### 2. 开 PR

网页上会出现黄色条 "Compare & pull request"，点它 → 目标选 `main` → 随便写个标题 → **Create pull request**。

到这一步你应该看到：PR 页面下方出现了 `CI / Lint (Ruff)` 的检查，先是黄点，几秒后变绿勾。

### 3. 故意让检查挂掉

在同一个分支上继续：

```powershell
# 在 hello.py 顶部加一行：import os
git add .
git commit -m "chore: 故意引入未使用的 import"
git push
```

这时候 Ruff 会因 `F401 unused import` 失败 → PR 页面的 CI 变成**红叉**，点 `Details` 能看到具体文件和行号。同时 `CD` 不会跑（因为还没进 main）——这正是"CI 挡住了坏代码"。

### 4. 修好，看它自动变绿

```powershell
# 删掉那行 import os
git commit -am "fix: 移除未使用 import"
git push
```

不用关 PR、不用重开，同一条分支再 push 一次，CI 自动重跑变绿。**这就是 PR 的"活文档"特性。**

### 5. 合并，观察 CD

点 **Merge pull request** → 合并后 main 上有一次新提交 → `CD` 工作流自动触发，Actions 里能看到 `deploy ok` 和提交号。

### 6. 打开分支保护（可选但强烈建议）

仓库 **Settings → Rules → Rulesets** 或 **Branches → Add branch protection rule**：

- 勾选 `Require a pull request before merging`
- 勾选 `Require status checks to pass`，并把 `Lint (Ruff)` 选进去

然后试着直接往 main push 或开一个检查挂掉的 PR 合并，体验"被挡住"的报错。

## 理解要点

| 现象 | 说明 |
| --- | --- |
| 开 PR 就自动跑，不用点按钮 | `on: pull_request` 是事件触发，不是定时 |
| 同一个分支反复 push，检查自动重跑 | CI 绑定的是 PR，不是某一次提交 |
| 合并前 CD 一直没跑 | `cd.yml` 只监听 `push: branches: [main]` |
| 红叉也能合并（默认） | 除非开了 branch protection，GitHub 默认不强制 |

跑完这套，你在 `rj-pro` 里只需要多注意一件事：**别推 `full01`、别发 Release**。
