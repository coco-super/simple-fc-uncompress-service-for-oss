# simple-fc-uncompress-service-for-oss

<a name="QqxEg"></a>
## 背景

阿里云函数计算是事件驱动的全托管计算服务。通过函数计算，您无需管理服务器等基础设施，只需编写代码并上传。函数计算会为您准备好计算资源，以弹性、可靠的方式运行您的代码，并提供日志查询、性能监控、报警等功能。借助于函数计算，您可以快速构建任何类型的应用和服务，无需管理和运维。而且，您只需要为代码实际运行所消耗的资源付费，代码未运行则不产生费用。

这里我们提供一个 fun 模板，帮助我们更快地搭建一个基于函数计算实现对上传的压缩文件自动解压的项目，并预置了编译、打包、调试和发布等开箱即用的功能。

本模板适用于**较小压缩文件**的处理，FC 从内网中拉取 OSS 中的压缩文件，然后一切在内存中完成，将解压后的文件的 bytes 上传到指定 bucket 中目录。关于函数计算实现 oss 上传压缩文件自动压缩的处理，请参照云栖社区文章[函数计算实现 oss 上传超大 zip 压缩文件的自动解压处理](https://yq.aliyun.com/articles/680958)。

另外如果您有超大的 zip 自动解压的需求，请使用另一[流式模板](https://github.com/coco-super/streaming-fc-uncompress-service-for-oss)，适合较大的压缩文件解压。
<a name="cAjUK"></a>
## 快速开始

<a name="lGvKc"></a>
### 1.安装 node 
```bash
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.5/install.sh | bash
nvm install 8
```

<a name="vYqDd"></a>
### 2.安装 fun 工具

```bash
npm install @alicloud/fun -g
```

fun 工具的某些子命令可能会用到 docker，所以你需要安装好 docker，具体参考文档：[Fun 安装教程](https://github.com/aliyun/fun/blob/master/docs/usage/installation-zh.md)。

<a name="dP8XW"></a>
### 3.通过 fun 模板生成项目骨架
使用 fun init 命令可以快捷的将本模板项目初始化到本地，执行命令 ：

```powershell
fun init -n xxx https://github.com/coco-super/simple-fc-uncompress-service-for-oss
```

其中 -n 表示要作为文件夹生成的项目名称。默认值是 fun-app。更多fun init 命令格式选项说明请参考云栖文章[开发函数计算的正确姿势 —— 使用 Fun Init 初始化项目](https://yq.aliyun.com/articles/674363)。

```powershell
PS D:\> fun init -n  simple   https://github.com/coco-super/simple-fc-uncompress-service-for-oss
start cloning...
Cloning into 'simple-fc-uncompress-service-for-oss'...
remote: Enumerating objects: 7, done.
remote: Counting objects: 100% (7/7), done.
remote: Compressing objects: 100% (7/7), done.
remote: Total 7 (delta 0), reused 3 (delta 0), pack-reused 0
Unpacking objects: 100% (7/7), done.
finish cloning.
? Please input oss bucketName? coco-superme
? Please input prefix? source/
? Please input unzip file directory? processed/
? Please choose a file suffix? .zip
Start rendering template...
+ D:\simple
+ D:\simple\index.py
+ D:\simple\template.yml
finish rendering template.
```

上面会提示：

1. 输入一个 OSS 的 bucketName，注意 OSS Bucket 是全球唯一的，请输入提前创建好的 bucketName（已经创建好的，请确保 region 一致）。
1. 输入 OSS 的 bucket 中的指定目录。用户上传压缩文件的目录。注意必须以 `/` 结尾。
1. 输入 OSS 的 bucket 中的指定目录，存放解压后的文件。此目录会以 `prefix` 的父目录作为根目录。注意必须以 `/` 结尾。
1. 选择压缩文件的后缀名。

<a name="ECcD2"></a>
### 4.服务部署

```bash
PS D:\> cd .\simple\
PS D:\simple> fun deploy
using region: cn-shanghai
using accountId: ***********8320
using accessKeyId: ***********vHqQ
using timeout: 10

Waiting for service simple to be deployed...
        Waiting for function simple to be deployed...
                Waiting for packaging function simple code...
                package function simple code done
                Waiting for OSS trigger simple-trigger to be deployed...
                function simple-trigger deploy success
        function simple deploy success
service simple deploy success
```

<a name="qGibX"></a>
## 测试
<a name="rgcDQ"></a>
### 上传压缩文件到 OSS
在 coco-superme 的 bucket 中上传名为 HBuilderX.1.7.0.20190314.zip 的压缩文件。

![image.png](http://cdn-trigger.sunfeiyu.top/img/1558971895176-b6998199-a87f-4c3a-850f-fdfccd09c672.png?Expires=1558977072&OSSAccessKeyId=TMP.AgFo55tRmQU7S8oaW2kM7lMv3gox0FNNyekQhFhyOH1MijeRHxwXHF6lDljTAAAwLAIUCoh6LVBo8CAG4p5kwqbRHpKLvTQCFGqJVJZpEhucGmW8Xn0xIiBY-lyw&Signature=r4pXqxxqyrkGdvrya4DK1JniIxc%3D)


上传成功后，触发函数计算自动压缩 HBuilderX.1.7.0.20190314.zip 文件并上传回 OSS 指定目录。刷新页面，发现 processed/ 目录下已生成解压后文件。

![image.png](http://cdn-trigger.sunfeiyu.top/img/1558972696484-cd92d727-9414-45ab-b8ca-26dd13a0c406.png?Expires=1558977101&OSSAccessKeyId=TMP.AgFo55tRmQU7S8oaW2kM7lMv3gox0FNNyekQhFhyOH1MijeRHxwXHF6lDljTAAAwLAIUCoh6LVBo8CAG4p5kwqbRHpKLvTQCFGqJVJZpEhucGmW8Xn0xIiBY-lyw&Signature=KURqLJ7G7BEGU7he%2FOVv38XI1R0%3D)


存储压缩文件的目录和触发函数计算解压后的文件存储目录为同级目录。

![image.png](http://cdn-trigger.sunfeiyu.top/img/1558972782012-98950807-e2b8-4c38-9f36-36ecd0421b75.png?Expires=1558977127&OSSAccessKeyId=TMP.AgFo55tRmQU7S8oaW2kM7lMv3gox0FNNyekQhFhyOH1MijeRHxwXHF6lDljTAAAwLAIUCoh6LVBo8CAG4p5kwqbRHpKLvTQCFGqJVJZpEhucGmW8Xn0xIiBY-lyw&Signature=3NCjYLxe5G%2FYkyOh%2FQnfp7NtYng%3D)
<a name="2473ec5a"></a>
## 
<a name="PF9c6"></a>
## 参考阅读

1. [Fun (Fun with Serverless) 工具](https://github.com/aliyun/fun/)
1. [Fun Init 自定义模板](https://yq.aliyun.com/articles/674364)