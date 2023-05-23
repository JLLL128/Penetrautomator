## git和github

github当中的仓库分支管理需要配合git命令的使用

一些常用的git命令

```bash
git init：初始化一个新的 Git 仓库。
git clone：从远程仓库克隆代码库到本地。
git add：将文件添加到 Git 的暂存区。
git commit：将暂存区的更改提交到本地 Git 仓库。
git push：将本地 Git 仓库的更改推送到远程仓库。
git pull：从远程仓库拉取最新的更改。
git branch：列出本地分支或创建新分支。
git checkout：切换到不同的分支或还原文件。
git merge：将不同分支的更改合并到一起。
git log：查看 Git 仓库的提交历史记录。
git status：查看当前 Git 仓库的状态
```

一般来说，先git clone将远程仓库的某个分支拉取到本地上，然后如果本地分支上有变化的文件或目录，可以使用`git add <目录/文件>`，然后`git commit -m "message"`说明本次的变化包含了哪些信息，最后`git push`将本地分支的变化推到远程的分支上即可

## python——argparse

python的argparse是python标准库的一个用来处理命令行的模块，而且是python的原生库，不需要用pip这样的python包管理工具来安装额外的包依赖。

argparse的用法

**导入模块并创建一个解析器**

```python
import argparse
parser = argparse.ArgumentParser(description='demo1 test program')
```

其中，description是对这个命令行参数的程序的简单说明

**添加一些参数**

```python
parser.add_argument('--name',help='description of name')
parser.add_argument('--age',help='description of age')
```

add_argument是用来添加命令行的参数的，第一个参数是参数的名称，第二个参数help是对当前参数的一个描述

**解析参数**

```python
args = parser.parse_args()
```

parse_args用于解析命令行参数和选项

**使用参数**

```python
print(args.name)
print(args.age)
```

示例代码如下

```python
import argparse

parser = argparse.ArgumentParser(description='description of your program')
parser.add_argument('--name', help='description of name')
parser.add_argument('--age', help='description of age')
args = parser.parse_args()

if __name__ == "__main__":
	print(args.name)
	print(args.age)
```

在命令行输入

```python
python demo1.py John --age 24
```

![image-20230523142801116](/home/nerowander/.config/Typora/typora-user-images/image-20230523142801116.png)