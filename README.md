<!--
 * @Description: 
 * @Author: FlyingRedPig
 * @Date: 2020-07-29 16:49:05
 * @LastEditors: FlyingRedPig
 * @LastEditTime: 2020-08-19 16:51:56
 * @FilePath: \MA_tool\README.md
-->

# **Marketing Automation 工具箱**

<p align="right"><em>edited by</em> Zinan Xu</p>

## **简介**

Maketing Automation 工具箱是为 GC MA team 开发的小工具集合，包含日程管理、报告生成、csv文件格式转换、数据提取等等功能。稍后我将一一介绍这些功能，当您通读这篇文档时，相信您能够感受到我们日常工作的一些缩影。在这里我将简要介绍一下本应用的几个特性：

- 轻量化
- 多人协作
- 多元化

在最初始的时候，这个应用只有一个文件，一百多行代码。所以它最初的设计哲学就是作为一个轻量的工具箱，而绝非一个系统性的应用。我们可以轻易地更改功能，相信这类需求在我们的工作流程中相当常见。当我们在做某些事情，是重复性且费力的，我就希望能够从这个工具箱中取出一个工具来完成。

而到了未来，我们必须面临多人协作的环境。这就要求我们把核心数据库与其他功能隔离开来。比如：在我们以往的认知中，request tracker往往和simple tracker被视为是类似的文档。但实际上，request tracker是主要需求端数据库，而simple tracker只是它的副产品。所以，我们将request tracker和SMC上爬取下来的campaign数据都存在共享文件夹的data文件夹中。

```mermaid
\\cnshag101.sha.global.corp.sap\Restricted\Marketing\Marketing_Automation\data
```

同时，这个应用还处于初级阶段，目前还在不断地改版优化，希望 MA team 的成员们能够使用它们并反馈意见。

## **config 配置**

在我们使用它之前，先期需要做一些个性化的配置。首先，打开config文件夹下的config.json，而后更改如下：

### file_location

- SimpleTracker : simple tracker的存放地址
- reportSave : 数据报告的存放地址
- Analytics : analytics数据的存放地址

### chrome_driver

我们在工具内内置了一个chrome driver，用于爬虫爬取数据。当chrome更新时，我们就需要更新chrome driver的版本。

### username

请在初始化的时候设置用户名。

## **环境配置及打开方式**

我们不支持在共享文件夹内运行此应用，因为此应用多个功能涉及文件的生成与更改，多人同时在同个位置更改文件会导致冲突。我们会将数据库放在共享文件夹中，其他功能尽可能地分离出来，例如simple_tracker以及report都将在各自的本地pc上生成。

### **Windows环境**

点击 Script.bat 即可运行程序。

### **Mac & Linux 环境**

打开bash，进入EDM_project文件夹，然后执行以下命令：

```mermaid
cd EDM
cd EDM-venv
cd Scripts
activate
cd ..
cd ..
cd bin
python edm.py
```

## 使用说明

在这里，我们就真正开始使用 MA 工具箱啦！我们的工具是通过CLI(Command Line Interface) 命令行方式运行的。这需要一点点学习成本，但相信我，这绝对值得，因为命令行交互是所有交互方式中最强大灵活的。同时，此项目中的命令也相当简洁易懂。

在这一章节中，每一个小节都对应一个命令的讲解。我会把命令写在每个小节的最前面。下面我们将一步步地讲解工具的使用过程。

### **第一个命令**

```mermaid
python edm.py 
```

当你敲击这个命令时，它并不会真正执行任何工作，而是会简要地介绍此工具中各命令的功能，就像我下文做的那样。当您对于某个命令的作用不熟悉的时候，相信我，运行它，它会告诉你所有命令的列表。

同时当这个命令运行成功时，证明您的环境配置是没有问题的，这是一个很好的测试。

### **设置我们的username吧！**

```mermaid
python edm.py setting username your_name
```

这个命令用来设置我们的用户名。这是您开始使用此工具的第一步，因为您将访问数据库，我们需要用户名来记录数据库的操作日志。

我们的所有命令都是由python edm.py开头的，这是因为我们要用python解释器运行edm.py文件。如果不想每次都输入它，我们可以按方向键（上）即可复制上一条命令。

### **最重要的命令：routine**

```mermaid
python edm.py routine
```

这条命令是以下命令的集成：

- simple_tracker
- workflow
- write_campaign_id
- report

我们需要每天运行这个命令，来保证我们的daily work正常运转。这听起来很酷，只需要一个命令，就能够保证routine work的正常运转了！接下来我将分别介绍这四个命令的作用。

同时，如果您时间有限，只想学习一个命令。记住这个命令就好了，90%的情况直接运行它就可以解决您的需求。但我同样建议您读下去，下文将介绍它包含命令的具体功能以及我设计它们的思路。

### **日程管理：simple_tracker**

```mermaid
python edm.py simple_tracker
```

当您执行此命令时，它会根据Request_Tracker来生成日程，并保存为一个漂亮的excel表格。我们会根据这个excel表格清晰地看到需求排期。

它会根据星期来变更颜色，文件的开始时间和结束时间是根据现在的时间/需求的排期自动变化的。金黄色代表从今天开始的过去四天，最后一个金黄色是今天。红色代表过去的第五天，我们根据红色可以看到明天campaign需要避让哪些campaign的时间。红色+金黄色代表了所有会占用明天数据的campaign.

在执行方面，这个命令和之前的命令都不同，它有一个新的概念，参数。也就是说，我们可以灵活地操作这个工具了。在这个命令中，我们有一个参数，path，比如：（这里并不是要折行，命令行中没有换行，只有空格，回车键意味着执行）

```mermaid
python edm.py simple_tracker C:/Users/C5293427/Desktop/examples/simple_tracker.xlsx
```

当我们在执行第一个看起来很简洁的命令时，我没有输入路径，那么它实际上在执行一个默认路径，这个路径保存在了edm/config/config.json中，您可以灵活地修改它。

请注意几个特殊的点：

- 当您开始使用您的工具时，在config.json中修改simple_tracker的默认保存地址到您的本地文件夹。如果您把它放在公共文件夹中，速度缓慢，同时多人浏览时无法对其进行变更。
- 输入路径时最后要带上名字 simple_tracker.xlsx ，当然您也可以随便叫它什么，但一定要写上名字，否则它将报错。
- 当您使用windows系统时，默认的文件路径分隔符为 \ 请不要使用使用这个分隔符，因为它恰巧是python中的转义字符（这也是我不太喜欢Windows系统的原因之一），您可以使用 / 或者 \\\ 代替，例如：

```mermaid
python edm.py simple_tracker C:/Users/C5293427/Desktop/examples/simple_tracker.xlsx
```

```mermaid
python edm.py simple_tracker C:\\Users\\C5293427\\Desktop\\examples\\simple_tracker.xlsx
```

但不建议您过多地使用这个参数，在您配置系统时，进入config文件，将它放在您喜欢的本地文件夹中。

最后，routine命令会整合此命令，它将直接保存simple_tracker到默认文件夹。

### **工作计划管理：workflow**

```mermaid
python edm.py workflow
```

此命令主要解决了我们日常工作管理的问题，它的部分功能与simple_tracker重合，并做了丰富的补充。

它的主要内容包括以下五项：

#### 我们未来的工作

这一部分是与simple tracker重合的，但如果您只是想知道明天有哪些需求要完成，它可以在命令行中快速看到，而不必再打开一个excel表格。

#### 待定的工作

有一些需求会因为临时变更，发送日期待定，这部分数据不会在simple_tracker中展示，而是单独在这里展示。

#### 今天要发送的报告

这也是这个工具很聪明的一个功能，它将依据活动日期和发送日期自动计算今天将要发送哪些报告。

#### 我们要检查的campaign

这是一个非常重要的功能，我们的需求填写一般是在接到邮件时进行，但我们无法在接到需求时就填写campaign id. 我们要十分明确：smc campaign id对于本工具而言极为重要，它作为连接几个数据库的纽带，是务必要填写的。

但是，请注意，workflow是一个纯展示命令，它不提供任何交互动作，后续我们会介绍write_campaign_id, 那个时候我们再回过头来看这件事情的完整解决方案。

我们不必要经常运行这个命令，它会作为routine中的一部分呈现。

#### Communication Limited 时间检查

由于traffic control，我们经常想知道五天前的早上，我们到底是什么时候发送的campaign，几点结束的。那么这个表格就将给您明确的提示，您可以根据里面的campaign id去查找相应的时间。当然，simple_tracker中也有相关的提示，红色的格子代表着我们需要时间避让的campaign.

### **smc campaign id，一个campaign的身份证号码**

```mermaid
python edm.py write_campign_id
```

如果您将一个campaign比作婴儿的出生，内容象征着它的容貌，业务指标象征着它的成就，那么smc campaign id就是她的身份证号码。当我们接到需求时，是没有campaign id的，这个时候这个需求是在孕育阶段的，还没有实际执行的。而一旦它执行了，意味着我们的工作进入了下一阶段：数据的收集和报告的生成。

所以，我们要在她有了id之后尽可能快速地将它记录在本地数据库中，但我们依据什么要做这件事呢?我们会提供campaign name，owner， launch time等等需求信息让您判断，它到底是哪个campaign.

此功能的设计思路是：搜索所有今天以前的，没有登记过smc campaign id的campaign，拿出来供您填写。一旦填写后，不能从命令行界面更改，而要到Request Tracker.xlsx (需求数据库) 中修改。

当然您也可以选择不填写此id，跳到下一个campaign,使用命令next:

```mermaid
next
```

直接退出campaign id填写环境：

```mermaid
exit
```

请注意：这两个命令一定是在先执行了 write_campaign_id 命令之后才可以执行的。

### **report，一份体检报告**

```mermaid
python edm.py report 1234
```

执行此命令生成smc campaign id为1234的campaign的数据报告。
此命令接收两个参数：

- smc campaign id
- generate type: static / dynamic

这个命令在后台会运行多项工作。其中最为重要的是，使用浏览器打开SMC，并将数据爬取到我们的sqlite数据库(存储在共享文件夹，这样做的好处一是为了更好的存储整理数据，二是为了在生成报告时不必每次都访问SMC。

想想看，如果没有本地数据库，会出现什么样的状况。想象一下这个场景：团队成员A在本地运行了report命令，程序打开浏览器，花了一分钟才爬取下来数据，生成了报告（生成报告的时间极短，爬取是最耗时的）。过了一个小时，团队成员B又执行了此命令，他又花了一分钟从SMC爬取数据。与此同时，团队成员A的数据还是旧的。这种各自为政的设计显然是低效的，所以这里的设计模式是我们在共享文件夹中有一个sql数据库，所有人的报告实际上都只是数据库数据的再包装。

基于此，就容易理解static和dynamic了。static意味着我们直接从sql数据库生成报告，而不必再次请求SMC。若本地数据库没有数据，我们才请求SMC。而dynamic的意思是，我要更新数据库的内容，我觉得里面的数据太旧了，我想要一个新版本的数据。这个参数会更新sql数据库，同时生成最新版本的report.

```mermaid
python edm.py report 1234
python edm.py report 1234 static
```

我们的默认参数是static，也就是说上述两个命令是一样的。

最后我需要讲一下routine和report的关系，report是routine中的一环。它的原理是根据workflow中计算的，今天需要发送报告的campaign，自动对其执行report，这里的generate type参数用的仍是默认值static. 若想更新数据，则需要再次手动输入：

```mermaid
python edm.py report 1234 dynamic
```

### **transfer -> csv 文件转换器**

```mermaid
python edm.py transfer
```

这个命令会直接调出一个用户界面，按照指示输入路径即可。它的作用是将csv文件转换成excel文件，这个文件最好用于我们的GC standard export模板。这里值得注意的是要在config文件中设置默认的输入输出路径。

### **data, 提取常见数据**

```mermaid
python edm.py data hongkong 20200101 20200630
```

此命令接收三个参数：

- 地区
- 起始时间
- 结束时间

提取的数据维度包括：

- email 总量
- unique email 总量 (不计算第二波第三波)
- touch points: sent 加总
- 平均 open rate
- 平均 click-to-open rate
- 平均 ctr
- 平均 unique ctr

提取后的数据会以excel的形式存储于一个默认文件夹中（在config中配置）。

关于地区名，请使用

- china
- hongkong
- taiwan

关于日期，请使用格式：20200515

通过这个命令，我们就可以轻松应对大家对于数据的基本疑问，例如：HK上半年的平均开信率，CN上半年到底做了多少个EDM等等。

## 联系我们

如有任何issue或comments， 请联系 zinan.xu@sap.com
