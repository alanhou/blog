---
series: "odoo14-cookbook"
seriesOrder: 24
title:
  en: "Chapter 24: Managing the IoT Box"
  zh: "第24章 管理IoT盒子"
description:
  en: "Set up and configure the Odoo 14 IoT Box with Raspberry Pi for connecting printers, cameras, payment devices, and other peripheral devices."
  zh: "使用树莓派设置和配置Odoo 14 IoT盒子，连接打印机、摄像头、支付设备和其他外围设备。"
date: 2021-07-15
tags: ["odoo", "odoo14", "iot", "raspberry-pi", "hardware", "peripherals"]
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080"
---

:::zh
Odoo提供对**物联网**（**IoT**）的支持。IoT是一种通过互联网交换数据的设备/传感器网络。通过将此类设备与系统相连接，你可以使用它们。例如，通过将打印机与Odoo连接，你可以将PDF报表直接发送到打印机。Odoo使用一种称为**IoT盒子**的硬件，用于连接打印机、卡尺、支付设备、脚踏开关等设备。本章中，你将学习如何设置和配置IoT盒子。这里我们将讲解如下课题：

- 为树莓派（Raspberry Pi）闪存IoT盒子镜像
- 通过网络连接IoT盒子
- 向Odoo添加IoT盒子
- 加载驱动及列出已连接设备
- 从设备接收输入
- 通过SSH访问IoT盒子
- 配置销售点（POS）
- 将PDF报表直接发送到打印机

注意本章的目的是安装和配置IoT盒子。开发硬件驱动不在本书的讨论范围之内。如果你想要深入地学习IoT盒子，请研究企业版中的**iot**模块。

## 技术准备

IoT盒子是一个基于树莓派的设备。本章中的各小节基于Raspberry Pi 3 Model B+，可通过 <https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/> 进行购买。IoT盒子是企业版的一部分，因此你需要使用企业版来完成本章中的操作。

本章中的所有代码可在如下GitHub仓库中进行下载：<https://github.com/PacktPublishing/Odoo-14-Development-Cookbook-Fourth-Edition/tree/master/Chapter24/05_capture_image/my_library>。

## 为树莓派（Raspberry Pi）闪存IoT盒子镜像

本节中，你将学习如何通过IoT盒子的镜像闪存microSD卡。注意本节仅适用于那些购买了空白树莓派的人。如果你购买的是Odoo官方的IoT盒子，请跳过这一节，因为它已经预载了IoT盒子镜像。

### 准备工作

树莓派3 Model B+使用microSD卡，因此本节中我们使用了microSD卡。你需要将microSD卡连接到电脑上。

### 如何实现...

执行如下步骤来在SD卡上安装IoT盒子镜像：

1. 将microSD卡插入你的电脑（如果电脑上没有专用卡槽请使用适配器）。
2. 从Odoo的nightly构建中下载IoT盒子镜像。镜像地址为 <https://nightly.odoo.com/master/iotbox/>。
3. 下载并在电脑上安装**balenaEtcher**。下载地址为 <https://www.balena.io/etcher/>。
4. 打开**balenaEtcher**，选择**IoT盒子**镜像（我们使用的是IoT盒子镜像的20.10版本），并选择闪存你的microSD卡。你将看到如下界面：
   ![图24.1 – 使用IoT盒子镜像闪存SD卡](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.1_B15928.jpg)
   图24.1 – 使用IoT盒子镜像闪存SD卡
5. 点击**Flash!**按钮并等待处理完成。
6. 退出microSD卡并将其放入树莓派中。

在完成了这些步骤后，你的microSD卡中就载入了IoT盒子镜像，可以在IoT盒子中使用了。

### 运行原理...

在本节中，我们在microSD卡中安装了IoT盒子镜像。在第2步中，我们从Odoo nightly构建中下载了IoT盒子镜像。在nightly页面上，你可以找到针对IoT盒子的不同镜像。你需要从Odoo nightly构建中选择最新的镜像。在编写本书时，我们使用了最新镜像**iotboxv20_10.zip**。IoT盒子镜像基于Raspbian Stretch Lite OS，并且镜像中加载了将IoT盒子集成到Odoo实例中所需的库和模块。

在*第3步*中，我们下载了**balenaEtcher**工具用于闪存microSD卡。

> **📝注**：在本节中，我们使用**balenaEtcher**来闪存microSD卡，但你也可以使用其它工具来闪存microSD卡。

在*第4步*中，我们通过IoT盒子镜像闪存了microSD卡。注意这个过程可能需要好几分钟。在完成这一过程后，microSD卡就可供使用了。

如果你想要验证闪存是否成功，可执行如下步骤：

1. 将microSD卡挂载到树莓派中。
2. 接通电源并通过HDMI线连接外部显示器（在实际使用中，外部显示器并非必须的，这里我们使用它仅作验证目的）。
3. 系统会启动并显示如下页面：

   ![图24.2 – IoT盒子界面](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.2_B15928.jpg)
   图24.2 – IoT盒子界面

如果你没有使用显示器，只需将IoT盒子接通电源，稍后你会看到IoT盒子的Wi-Fi网络。

### 扩展知识...

在之前的Odoo版本中，PosBox用于销售点（POS）应用。IoT盒子支持PosBox的所有功能，所以如果你使用的是Odoo社区版而又想要集成设备，可以使用相同的IoT盒子镜像来通过不同设备连接Odoo实例。参见*配置销售点（POS）*一节来获取更多信息。

## 通过网络连接IoT盒子

IoT盒子通过网络与Odoo实例进行通讯。连接IoT盒子是很关键的一步，如果操作有误，你会在将IoT盒子连接到Odoo时遇到报错。

### 准备工作

使用IoT盒子镜像将microSD卡挂载到树莓派中，然后将树莓派接通电源。

### 如何实现...

树莓派3 Model B+支持两种类型的网络连接——Ethernet和Wi-Fi。

通过Ethernet连接IoT盒子非常简单，只需将IoT盒子通过RJ45以太网线进行连接，IoT盒子即可使用了。通过Wi-Fi连接IoT盒子则较为复杂，因为你可能没有连接显示设备。执行如下步骤来通过Wi-Fi连接IoT盒子：

1. 为IoT盒子接通电源（如果插上了Ethernet网线，请拔掉网线并重启IoT盒子）。
2. 打开电脑并连接名为**IoTBox**的Wi-Fi网络，如下图所示（无需密码）：
   ![图24.3 – IoT盒子Wi-Fi网络](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.3_B15928.jpg)
   图24.3 – IoT盒子Wi-Fi网络
3. 在连接了Wi-Fi之后，你会看到一个弹出的IoT盒子主页，如下图所示（如未弹出，请在浏览器中打开该盒子的IP地址）：
   ![图24.4 – 连接到IoT盒子](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.4_B15928.jpg)
   图24.4 – 连接到IoT盒子
4. 设置**IoT Box Name**并保留**Server token**为空，然后点击**Next**。这会跳转到一个可以看到Wi-Fi网络列表的页面：
   ![图24.5 – 连接到Wi-Fi](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.5_B15928.jpg)
   图24.5 – 连接到Wi-Fi

> **📝注**：如果你使用的是企业版并且想要立即将IoT盒子与Odoo连接，可以使用服务令牌（Server token）。你可以从Odoo实例中获取服务令牌；参见下一节来了解更多详情。

5. 选择你想要连接的Wi-Fi网络并填入**Password**。然后，点击**Connect**按钮。如果你填写了正确的信息，会跳转到最终页面：

   ![图24.6 – 确认页面](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.6_B15928.jpg)
   图24.6 – 确认页面

在执行了这些步骤之后，你的IoT盒子就已连接到网络，可以与Odoo实例进行集成了。

### 运行原理...

通过Ethernet连接Odoo实例与IoT盒子非常简单，只需通过RJ45以太网线连接IoT盒子即可使用。通过Wi-Fi连接IoT盒子则有所不同，其困难之处在于IoT盒子并没有显示器或图形界面。你没有输入Wi-Fi网络密码的界面。因此，解决这一问题的方法是拔掉IoT盒子的Ethernet网线（如已连接）并进行重启。在这种情况下，IoT盒子会创建其自己的Wi-Fi热点，名为**IoT Box**或类似名称，参见*第2步*。你需要连接名为**IoT Box**的Wi-Fi；所幸无需密码。一旦连接了**IoT Box** Wi-Fi，就会弹出*第3步*中所示的页面。这里你可以将IoT盒子命名为类似**Assembly-line IoT Box**的名称。现在保留服务令牌为空；我们将在*向Odoo添加IoT盒子*一节中进行详细学习。然后点击**Next**按钮。

点击**Next**按钮之后，会显示一个Wi-Fi网络列表，如*第4步*所示。此处你可以将IoT盒子连接到你的Wi-Fi网络。确保选择正确的网络。你需要将IoT盒子连接到与Odoo实例所运行电脑相同的Wi-Fi网络。IoT盒子与Odoo实例在**局域网**（**LAN**）内进行通讯。也就是说如果两者连接到不同的网络上，它们无法进行通讯，IoT将无法正常工作。

在选择了正确的Wi-Fi网络后，点击**Connect**。然后IoT盒子会关闭其热点，重新连接到你所配置的Wi-Fi网络。这样IoT盒子就准备就绪了。

## 向Odoo添加IoT盒子

我们的IoT盒子已连接到本地网络，可供Odoo使用了。在本节中，我们将把IoT盒子与Odoo实例进行连接。

### 准备工作

确保IoT盒子已开启并且已连接到与Odoo实例所在电脑相同的Wi-Fi网络。

需要注意以下几点，否则IoT盒子将无法添加到Odoo：

- 如果你在本地实例上测试IoT盒子，需要使用**http://192.168.\*.\*:8069**（本地IP）来代替**http://localhost:8069**。如果使用localhost，IoT盒子将无法添加到你的Odoo实例。
- 你需要将IoT盒子连接到与Odoo实例所在电脑相同的Wi-Fi/Ethernet网络。否则IoT盒子将无法添加到你的Odoo实例。
- 如果你的Odoo实例运行着多个数据库，IoT盒子不会自动连接到Odoo实例。使用**--db-filter**选项来避免这一问题。

### 如何实现...

为建立IoT盒子与Odoo的连接，首先你需要在Odoo实例中安装**iot**模块：

1. 进入**Apps**菜单并搜索**Internet of Things**模块。该模块如下图所示。安装该模块，即可进行后续操作：
   ![图24.7 – 安装iot模块](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.7_B15928.jpg)
   图24.7 – 安装iot模块
2. 在安装了**iot**模块之后，你可以将实例与IoT盒子进行连接。然后通过点击**IoT**菜单手动将IoT盒子与Odoo实例进行连接。
3. 在控制面板中点击**Connect**按钮。这会显示如下弹窗。复制**Token**值：
   ![图24.8 – 将IoT盒子连接到Odoo的对话框](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.8_B15928.jpg)
   图24.8 – 将IoT盒子连接到Odoo的对话框
4. 以**8069**端口打开IoT盒子的IP地址。这会显示IoT盒子的主页。点击**Name**部分的**configure**按钮：
   ![图24.9 – IoT盒子主页](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.9_B15928.jpg)
   图24.9 – IoT盒子主页
5. 设置**IoT Box Name**并粘贴服务令牌。然后点击**Connect**按钮。这会开始配置IoT盒子。等待处理完成：
   ![图24.10 – IoT盒子主页](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.10_B15928.jpg)
   图24.10 – IoT盒子主页
6. 查看Odoo实例中的**IoT**菜单。你会看到一个新的IoT盒子：

   ![图24.11 – 成功连接的IoT盒子](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.11_B15928.jpg)
   图24.11 – 成功连接的IoT盒子

### 运行原理...

将**IoT盒子**与Odoo连接非常重要。通过这种方式，Odoo将知道IoT盒子的IP地址。该IP地址将被Odoo用于与连接到该设备上的设备进行通讯。在存在多个IoT盒子的情况下，这也将确保Odoo与正确的盒子进行通讯。其余操作都很直观。

如果你想在Wi-Fi配置过程中将IoT盒子添加到Odoo实例，也是可以的。在*通过网络连接IoT盒子*一节中，我们保留了**Server token**字段为空。你只需在该步骤中添加服务令牌即可：

   ![图24.12 – 在Wi-Fi配置时添加服务令牌](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.12_B15928.jpg)
   图24.12 – 在Wi-Fi配置时添加服务令牌

> **📝注**：在使用IoT盒子时，避免使用DHCP网络。这是因为IoT盒子的网络配置是基于IP地址进行添加的。如果你使用DHCP网络，那么IP地址是动态分配的。因此你的IoT盒子有可能因新分配的IP地址而停止响应。要避免这一问题，你可以将IoT盒子的MAC地址映射到固定的IP地址。

### 通过配对码连接IoT盒子

还有一种连接IoT盒子的替代方式，即通过**配对码**。配对码可以在IoT盒子的**销售点**（**POS**）显示页面上找到。有两种方式打开POS客户端显示界面。第一种是将IoT盒子与外部显示器连接。当你启动连接了显示器的IoT盒子时，它将默认打开POS客户端显示界面。第二种方式是通过IoT盒子的IP打开POS客户端。POS客户端显示界面的URL如下：**<IoT盒子IP>:8069/point_of_sale/display**。打开POS客户端显示界面后，你将能看到配对码，如下所示：

   ![图24.13 – IoT盒子的配对码](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.13_B15928.jpg)
   图24.13 – IoT盒子的配对码

然后你只需在Odoo实例中的IoT盒子连接对话框中使用该配对码即可。

> **📝注**：如果你未连接到互联网，配对码将不会显示。

在上图中，我们看到了如何通过POS客户端显示界面获取配对码。但如果你有Ethernet连接和打印机，则无需显示器也可获取配对码。你只需将IoT盒子连接到Ethernet和打印机即可。IoT盒子启动后，它将打印一张带有配对码的小票。然后你只需在Odoo实例中的IoT盒子连接对话框中使用该配对码即可。

### 扩展知识...

如果你想将已有的IoT盒子连接到其它Odoo实例，你需要清除配置。你可以在IoT盒子的Odoo服务器配置页面中通过**Clear**按钮清除IoT盒子配置：

   ![图24.14 – 清除IoT盒子配置](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.14_B15928.jpg)
   图24.14 – 清除IoT盒子配置

## 加载驱动及列出已连接设备

IoT盒子并不仅局限于企业版。你可以在社区版中像PoSBox一样使用它。设备的集成是企业版的一部分，因此**IoT盒子**镜像并不自带设备驱动；你需要手动进行加载。通常，如果你通过企业版Odoo实例连接IoT盒子，IoT盒子会自动加载设备驱动接口。但有时你可能有自定义驱动或未正确加载的驱动。在这种情况下，你可以手动加载驱动。在本节中，我们将了解如何加载驱动并获取已连接设备的列表。

### 准备工作

确保IoT盒子已开启并已将其连接到与Odoo实例所在电脑相同的Wi-Fi网络。

### 如何实现...

执行如下步骤来将设备驱动载入IoT盒子：

1. 打开IoT盒子主页并点击底部的**handlers list**按钮：
   ![图24.15 – 处理器列表](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.15_B15928.jpg)
   图24.15 – 处理器列表
2. **handlers list**按钮会将你重定向到**Handlers list**页面，在此你会看到**Load handlers**按钮。点击该按钮来加载驱动：
   ![图24.16 – 驱动列表](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.16_B15928.jpg)
   图24.16 – 驱动列表
3. 返回**IoT盒子**主页。这里你会看到一个已连接设备的列表：

   ![图24.17 – 已连接设备](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.17_B15928.jpg)
   图24.17 – 已连接设备

在执行了这些步骤之后，IoT盒子对你所指定的设备就准备就绪了，你可以在应用中开始使用这些设备了。

### 运行原理...

你可以从IoT盒子的主页加载驱动。你可以通过底部的**Load handlers**按钮来实现。注意这仅在你的IoT盒子已通过企业版Odoo实例连接时才能使用。在加载完驱动后，你就可以在IoT盒子主页上看到设备列表了。你也可以通过Odoo实例中的**IoT** | **Devices**菜单查看已连接的设备。在该菜单中，你会看到每个IoT盒子的已连接设备列表：

   ![图24.18 – 已连接设备列表](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.18_B15928.jpg)
   图24.18 – 已连接设备列表

目前，IoT盒子支持少数几种硬件设备，如摄像头、脚踏开关、打印机和卡尺。Odoo推荐的设备列表请见：<https://www.odoo.com/page/iot-hardware>。如果你的设备尚未支持，可以付费进行驱动开发。

## 从设备接收输入

IoT盒子仅支持有限的设备。目前这些硬件设备与制造应用相集成。但如果需要，你可以在自己的模块中集成所支持的设备。在本节中，我们将通过IoT盒子从摄像头捕获图片。

### 准备工作

我们将使用[第23章 在Odoo中管理Email](/blog/odoo-14-manage-emails-odoo)中*在聊天器中记录用户修改*一节的**my_library**模块。在本节中，我们将新增一个在借阅者归还图书时捕获和存储图像的字段。确保IoT盒子已开启并且已通过它连接了所支持的摄像头设备。

### 如何实现...

执行如下步骤来通过IoT盒子从摄像头捕获图片：

1. 在声明文件中添加依赖：

   ```python
   ...
   'depends': ['base', 'mail', 'quality_iot'],
   ...
   ```

2. 在**library.book.rent**模型中新增字段：

   ```python
   ...
   device_id = fields.Many2one('iot.device', string='IoT Device',
       domain="[('type', '=', 'camera')]")
   ip = fields.Char(related="device_id.iot_id.ip")
   identifier = fields.Char(related='device_id.identifier')
   picture = fields.Binary()
   ...
   ```

3. 在**library.book.rent**模型的表单视图中添加这些字段：

   ```xml
   <group>
       <field name="book_id" domain="[('state', '=', 'available')]"/>
       <field name="borrower_id"/>
       <field name="ip" invisible="1"/>
       <field name="identifier" invisible="1"/>
       <field name="device_id" required="1"/>
       <field name="picture" widget="iot_picture"
           options="{'ip_field': 'ip', 'identifier': 'identifier'}"/>
   </group>
   ```

4. 更新**my_library**模块来应用这些修改。更新后，你将看到一个捕获图片的按钮：

   ![图24.19 – 通过IoT捕获图像](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.19_B15928.jpg)
   图24.19 – 通过IoT捕获图像

注意如果摄像头未连接到IoT盒子或驱动未加载到IoT盒子中，该按钮将无法捕获图像。

### 运行原理...

在*第1步*中，我们在声明文件中添加了对**quality_iot**模块的依赖。**quality_iot**模块属于企业版，包含一个允许你通过IoT盒子从摄像头请求图像的组件。这将安装**stock**模块，但为简化起见，我们将使用**quality_iot**作为依赖。如果你不想使用这个依赖，可以创建自己的字段组件。参见[第15章 网页客户端开发](/blog/odoo-14-web-client-development)中的*创建自定义组件*一节来了解更多有关组件的知识。

在*第2步*中，我们添加了从摄像头捕获图像所需的字段。捕获图像需要两样东西：设备标识符和IoT盒子的IP地址。我们希望用户能够选择摄像头，因此添加了一个**device_id**字段。用户将选择要用于捕获图像的摄像头，并且基于所选择的摄像头设备，我们通过关联字段提取了IP和设备标识符信息。基于这些字段，在有多个IoT盒子时，Odoo将知道从哪里捕获图像。我们还添加了一个二进制字段**picture**来保存图像。

在*第3步*中，我们在表单视图中添加了字段。注意我们对**picture**字段使用了**iot_picture**组件。我们将**ip**和**identifier**字段添加为隐藏字段，因为不希望向用户显示它们；而是要在**picture**字段的选项中使用它们。该组件将在表单视图中添加按钮；点击按钮时，Odoo会向IoT盒子发出请求来捕获图像。IoT盒子会在响应中返回图像数据。该响应将保存在**picture**二进制字段中。

### 扩展知识...

IoT盒子支持蓝牙卡尺。如果你想要在模块中获取测量数据，可以使用**iot_measure**组件在Odoo中进行获取。注意与**iot_picture**类似，这里也需要在表单视图中添加**ip**和**identifier**隐藏字段：

```xml
<field name="measure" widget="iot_measure"
    options="{'ip_field': 'ip', 'identifier': 'identifier'}"/>
```

这将使用从IoT卡尺捕获的数据填充**measure**字段。

## 通过SSH访问IoT盒子

IoT盒子运行于Raspbian OS之上，可以通过SSH访问IoT盒子。在本节中，我们将学习如何通过SSH访问IoT盒子。

### 准备工作

确保IoT盒子已开启，并且已将IoT盒子连接到与Odoo实例所在电脑相同的Wi-Fi网络。

### 运行原理...

为通过SSH连接IoT盒子，你需要IoT盒子的IP地址。你可以在其表单视图中查看IP地址。作为示例，本节中将使用**192.168.43.6**作为IoT盒子的IP地址，请替换为你自己的IP地址。执行如下步骤来通过SSH访问IoT盒子：

1. 打开终端并执行如下命令：

   ```
   $ ssh pi@192.168.43.6
   pi@192.168.43.6's password:
   ```

2. 终端会询问密码；输入**raspberry**作为密码。
3. 如果你输入了正确的密码，即可通过shell进行访问。执行如下命令来查看目录：

   ```
   total 24
   -rw-r--r-- 1 root root    6 Oct 26 08:12 iotbox_version
   drwxr-xr-x 5 pi   pi   4096 Oct 23 09:05 odoo
   -rw-r--r-- 1 pi   pi     36 Nov 15 13:10 odoo-db-uuid.conf
   -rw-r--r-- 1 pi   pi      0 Nov 15 13:10 odoo-enterprise-code.conf
   -rw-r--r-- 1 pi   pi     26 Nov 15 13:10 odoo-remote-server.conf
   -rw-r--r-- 1 pi   pi     11 Nov 15 13:10 token
   -rw-r--r-- 1 pi   pi     26 Aug 20 12:03 wifi_network.txt
   ```

由于你拥有SSH访问权限，你可以浏览IoT盒子的完整文件系统。

### 如何实现...

我们使用了密码为**raspberry**的Pi用户来通过SSH访问IoT盒子。SSH连接用于需要对IoT盒子进行问题调试的场景。SSH无需过多解释，让我们来看看IoT盒子中Odoo的运行方式。

以下信息可能有助于调试问题：

- IoT盒子内部运行着一些Odoo模块。这些模块的名称通常以**hw_**开头，它们在社区版中可用。你可以在 `/home/pi/odoo/addon` 目录中找到所有模块。
- 如果你想查看Odoo服务器日志，可以通过 `/var/log/odoo/odoo-server.log` 文件进行访问。
- Odoo通过名为**odoo**的服务运行；你可以使用如下命令来**启动**、**停止**或**重启**该**服务**：

  ```
  sudo service odoo start/restart/stop
  ```

- 大多数客户会通过直接断电来关闭IoT盒子。这意味着在这种情况下IoT盒子的操作系统并没有正常关闭。为避免系统损坏，IoT盒子的文件系统是只读的。

### 扩展知识...

注意IoT盒子仅与本地机器相连接。因此，你无法从远程位置（通过互联网）直接访问其shell。如果你想要远程访问IoT盒子，可以在IoT盒子的远程调试页面中粘贴**ngrok**认证令牌密钥，如下图所示。这将在IoT盒子中启用TCP隧道，这样你就可以在任何地方通过SSH连接IoT盒子了。通过 <https://ngrok.com/> 了解更多有关**ngrok**的知识：

   ![图24.20 – 使用ngrok令牌进行调试](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.20_B15928.jpg)
   图24.20 – 使用ngrok令牌进行调试

一旦你添加了令牌，就可以从远程位置访问IoT盒子了。

## 配置销售点（POS）

IoT盒子可用于销售点（POS）应用。在本节中，我们将学习如何为销售点应用配置IoT盒子。

### 准备工作

确保IoT盒子已开启，并且已将IoT盒子连接到与Odoo实例所在电脑相同的Wi-Fi网络。同时，如果尚未安装销售点应用，请进行安装。

### 如何实现...

执行如下步骤来为销售点应用配置IoT盒子：

1. 打开销售点应用，并通过POS会话下拉菜单打开**Settings**：
   ![图24.21 – POS会话设置](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.21_B15928.jpg)
   图24.21 – POS会话设置
2. 点击**Settings**按钮。你将被重定向到**Settings**页面。搜索**Connected Devices**部分并勾选**IoT Box**复选框。这将启用更多选项：
   ![图24.22 – 选择IoT设备](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.22_B15928.jpg)
   图24.22 – 选择IoT设备
3. 选择你想要在销售点会话中使用的设备。如果你准备使用硬件设备（如条码扫描器），请选择相应设备。
4. 通过点击控制面板中的**Save**按钮来保存修改。

配置完成后，你就能够在销售点应用中使用IoT盒子了。

### 运行原理...

IoT盒子可以像PosBox一样用于销售点应用。为了在销售点应用中使用IoT盒子，你需要将IoT盒子连接到Odoo实例。如果你不知道如何连接IoT盒子，请参见*向Odoo添加IoT盒子*一节。一旦将IoT盒子连接到Odoo，你就可以像*第2步*那样在销售点应用中选择IoT盒子了。

在这里你可以选择在销售点会话中使用的硬件。保存修改后，如果你打开销售点会话，就可以在销售点中使用已启用的硬件了。如果你在设置中启用了特定硬件但该硬件未连接到IoT盒子，你将在顶部栏中看到如下警告：

   ![图24.23 – IoT盒子连接问题](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.23_B15928.jpg)
   图24.23 – IoT盒子连接问题

你可以点击这些警告来尝试重新连接。

### 扩展知识...

销售点应用属于社区版。如果你使用的是社区版，在销售点设置中看到的不是**IoT Box**选择框，而是**IoT Box IP Address**字段：

   ![图24.24 – 社区版中的IoT盒子设置](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.24_B15928.jpg)
   图24.24 – 社区版中的IoT盒子设置

如果你想要在社区版中集成硬件，需要在该字段中使用**IoT盒子**的IP地址。

## 将PDF报表直接发送到打印机

IoT盒子默认运行CUPS服务器。CUPS是一种允许计算机充当打印服务器的打印系统。你可以通过 <https://www.cups.org/> 了解更多相关信息。由于IoT盒子内部运行着CUPS，你可以将网络打印机连接到IoT盒子。在本节中，我们将了解如何直接从Odoo打印PDF报表。

### 准备工作

确保IoT盒子已开启并且你已将IoT盒子与Odoo进行了连接。

### 如何实现...

按照以下步骤直接从Odoo打印报表：

1. 通过IP打开IoT盒子主页。
2. 点击底部的**Printer Server**按钮：
   ![图24.25 – 配置打印机的选项](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.25_B15928.jpg)
   图24.25 – 配置打印机的选项
3. 这将打开CUPS配置主页。在此配置你的打印机。
4. 配置好打印机后，你将能够在IoT设备列表中看到该打印机。激活开发者模式，打开**Settings** | **Technical** | **Actions** | **Report**。
5. 搜索你想要打印的报表，打开表单视图，并在**IoT Device**字段中选择打印机，如下图所示：

   ![图24.26 – 选择IoT设备的选项](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_24.26_B15928.jpg)
   图24.26 – 选择IoT设备的选项

完成此配置后，报表PDF将直接发送到打印机。

### 运行原理...

就配置而言，本节非常直观，但有几点你应该了解。IoT盒子使用CUPS服务器来打印报表。你可以通过 **http://<IoT盒子IP>:631** 访问CUPS主页。

通过CUPS，你可以添加/删除打印机。在CUPS主页上，你将能够看到帮助你连接不同类型打印机所需的所有文档。配置好打印机后，你将在IoT设备列表中找到你的打印机。然后，你可以在报表记录中选择该IoT设备（打印机）。通常，当你在Odoo中打印报表时，它会下载报表的PDF文件。但完成此配置后，Odoo将不再下载报表，而是将PDF报表直接发送到所选打印机。注意只有在IoT设备字段中设置了打印机的报表记录才会被发送到打印机。
:::
