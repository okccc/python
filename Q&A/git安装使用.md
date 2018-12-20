## git基本命令
- 安装：yum install git
- 安装完配置用户和邮箱：  
git config --global user.name "okccc"(这样就不用每次同步到github都输密码)  
git config --global user.email "1573976179@qq.com"(此处email要和github保持一致,不然没有小绿块)    
查看配置列表：git config --global --list  
优先级：--system(系统) < --global(用户) < --local(当前仓库,可单独指定用户邮箱)       
打开配置文件：git config -e --system(/etc/gitconfig ) --global(~/.gitconfig) --local(/project/.git/config)  
解决中文乱码：git config --global core.quotepath false
- 选中某个目录作为仓库：cd mygit
- 初始化仓库：git init
- 将工作区文件(夹)添加到暂存区：git add aaa.txt 或者 git add . 
- 查看工作区状态：git status(多使用可根据提示操作)
- 将暂存区文件提交到版本库：git commit -m '...'  
- 已经在track的文件可以不用添加直接提交：git commit -a -m '...'
- 查看版本记录：git log 或者 git log --pretty=oneline aaa.txt
- 配置别名：git config --global alias.lg 'log --graph --pretty=oneline --abbrev-commit'
- 删除别名：git config --global --unset alias.lg
- 查看操作记录：git reflog
- 版本回退(慎用!)：git reset 38fd442 或者 git reset HEAD^/HEAD~1/HEAD~10(HEAD是指向当前版本的指针默认指向master分支)
- 撤销修改/删除  
场景1：只修改/删除了工作区文件,直接丢弃改动：git checkout -- aaa.txt  (git checkout本质上是用版本库的版本替换工作区的版本)  
场景2：修改/删除了工作区文件并添加到了暂存区,先取消暂存再丢弃改动：git reset HEAD aaa.txt & git checkout -- aaa.txt  
场景3：不仅添加到暂存区还提交到了版本库,先回退版本再丢弃改动：git reset HEAD^ & git checkout -- bbb.txt
- 对比文件  
对比工作区和HEAD版本：git diff HEAD -- aaa.txt  
对比不同HEAD版本：git diff HEAD HEAD^ -- aaa.txt
- 删除文件：git rm aaa.txt & git commit -m 'delete...'
## git分支管理
- 查看分支：git branch
- 创建分支：git branch dev
- 切换分支：git checkout dev
- 创建并切换分支：git checkout -b dev(开发人员平时往dev分支做合并,然后定期合并到master分支发布上线)
- 快速合并某分支到当前分支：git merge dev(当不同分支编辑<font color=red>同一个文件</font>并且都提交后做合并操作会冲突,先解决冲突再重新提交合并)
- 禁用快速合并：git merge --no-ff -m 'no fast-forward' dev  
应用场景：当代码写到一半时突然发现前面有个紧急bug要处理,这时候先保护工作现场此时工作区是干净的,然后创建一个临时的bug分支处理完bug后merge到dev分支,此时最好禁用快速合并,不然删掉临时bug分支后看不到merge修复bug的版本记录,最后再回到工作现场继续工作  
- 保护工作现场：git stash  
- 查看保护工作现场列表：git stash list  
- 创建bug分支：git checkout -b bug001 & ... & git checkout dev & git merge bug001 
- 恢复工作现场：git stash pop  
- 删除已合并的分支：git branch -d bug001(只能删除已经merge过的分支)
- 开发新功能时一般创建feature分支：git branch -b feature & ...
- 强制删除未合并的分支：git branch -D feature
## git标签管理
- 查看所有标签：git tag
- 新建标签,默认打在最新提交的commit上：git tag v0.1
- 新建标签,指定打在某次提交的commit上：git tag v0.1 f52c633
- 新建标签并指定标签信息：git tag -a v0.1 -m '...'
- 查看标签信息：git show v0.1
- 推送指定标签到远程：git push origin v0.1
- 推送所有标签到远程：git push origin --tags
- 删除本地标签：git tag -d v0.1
- 删除远程标签：git tag -d v0.1 & git push origin :refs/tags/v0.1
## github远程仓库
- 在本地生成ssh秘钥: ssh-keygen -t rsa -C "company/personal"  
![](images/git/01_ssh生成秘钥.png)
- 私钥保留,将公钥复制到gitlab账号  
![](images/git/02_复制公钥到github.png) 
- 测试是否成功连接：ssh -T git@github.com 
- github创建新工程
![](images/git/03_github创建新工程.png)
- 场景一：从远程库克隆到本地：git clone git@github.com:okccc/python.git
- 场景二：如果是先有本地仓库,可以在远程github创建一个新仓库(空的,不包含readme.md和.gitignore)  
关联远程库：git remote add origin git@github.com:okccc/python.git  
查看远程库详细信息：git remote -v  
第一次推送本地master分支到远程：git push -u origin master(-u指定origin为默认主机后面就不用加参数直接git push)  
以后再推送本地master分支到远程：git push
## github多人协作流程
- 多台电脑操作同一个github账号时,要在各自电脑ssh-keygen,user.name和user.email可以设置成同样的也可以另外设置
- 甲创建远程origin的dev分支到本地：git checkout -b dev origin/dev
- 推送到远程：git add aaa.txt & git commit -m 'add aaa' & git push origin dev
- 如果此时乙也编辑了aaa.txt那么直接push会冲突,需要先git pull把最新的提交从origin/dev上抓下来在本地合并解决冲突后再推送  
git pull居然也失败了？报错no tracking information：是因为本地的dev分支没有和远程的origin/dev分支建立连接  
建立连接：git branch --set-upstream-to=origin/dev dev  
再次pull：git pull & git status & ... & git commit -m 'fix conflict' & git push origin dev  
- 将分叉的提交历史整理成一条直线：git rebase
#### pycharm拉代码
![](images/git/04_pycharm从gitlab拉代码(ssh).png)
![](images/git/05_pycharm从gitlab拉代码(http).png)



  

