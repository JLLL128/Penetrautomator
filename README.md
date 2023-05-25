# Penetrautomator
An automated penetration testing tool

## 目前实现功能

- CMS查询（调用whatcms的api）
- 路径爆破（调用dirsearch）
- 端口扫描（调用nmap的命令）
- 子域名爆破（调用subDomainBrute）
- **域名反查公司名（调用whois的api）**
- 日志生成

![image-20230522214950754](https://jiangxiaoyyds.com/img/Penetrautomator/image-20230522214950754.png)

## 用法

Penetrautomator.py是命令行模式

```
#在终端里面输入
python Penetrautomator.py -u target_url --all //完整扫描
python Penetrautomator.py -u target_url --cms //只查询cms
#-u是必加参数，后面的参数不带默认完整扫描
```

![image-20230518125803575](https://jiangxiaoyyds.com/img/Penetrautomator/image-20230518125803575.png)

![image-20230518125845146](https://jiangxiaoyyds.com/img/Penetrautomator/image-20230518125845146.png)

Penetrautomator_steady_copy.py是稳定的脚本，没有命令行，直接运行就好

## 
