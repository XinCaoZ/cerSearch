通过（Certificate Transparency）证书透明去查找公开的子域名

#### 使用
```
查看使用帮助
python3 cerSearch.py -h

HTTP OPTIONS:
  -d                  查找单个域名.
  -i                  根据文件内容查找多个域名
  -o                  指定输出的目录名（不使用默认生成output目录）

```
#### 常用命令
```
查找单个目标
python -d test.com

查找多个目标
python -i domains.txt
python -i domains.txt -o subdomains
```
