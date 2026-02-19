---
series: "odoo14-cookbook"
seriesOrder: 17
title:
  en: "Chapter 17: In-App Purchasing with Odoo"
  zh: "第17章 Odoo的应用内购买"
description:
  en: "Implement Odoo 14 In-App Purchase (IAP) services, create service and client modules, authorize and charge IAP credits."
  zh: "实现Odoo 14应用内购买（IAP）服务，创建服务和客户端模块，授权并收取IAP余额。"
date: 2021-06-01
tags: ["odoo", "odoo14", "iap", "in-app-purchase", "monetization"]
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080"
---

:::zh
Odoo从版本11起就内置了对**应用内购买**（**IAP**）的支持。IAP用于提供无需复杂配置的持续性服务。通常，从应用商店购买的应用只需客户进行一次性付款，因为它们是普通模块，一旦用户购买并开始使用该模块，就不会再给开发者带来任何成本。与此相反，IAP应用用于向用户提供服务，因此提供持续性服务会产生运营成本。在这种情况下，仅靠单次初始购买是无法提供服务的。服务提供者需要一种根据使用量向用户进行持续性收费的方式。Odoo的IAP解决了这些问题，提供了一种基于使用量收费的方式。

本章中，我们将讲解如下小节：

- 应用内购买（IAP）的概念
- 在Odoo中注册一个IAP服务
- 创建一个IAP服务模块
- 授权并收取IAP余额
- 创建一个IAP客户端模块
- 在账户缺少余额时显示报价

使用IAP的场景有很多，如用于发送文档的传真服务或短信服务。在本章中，我们将创建一个小型IAP服务，它将根据我们输入的ISBN号提供图书信息。

## 技术准备

本章的技术要求是Odoo在线平台。

本章中使用的所有代码可从GitHub仓库下载：<https://github.com/PacktPublishing/Odoo-14-Development-Cookbook-Fourth-Edition/tree/master/Chapter17>。

## 应用内购买（IAP）的概念

在本节中，我们将探索IAP流程中各个不同的实体。我们还将了解每个实体的角色以及它们如何组合在一起完成IAP流程。

### 运行原理...

IAP流程中有三个主要实体：**客户**、**服务提供者**和**Odoo**本身。以下是它们的描述：

- **客户**是希望使用服务的终端用户。为了使用服务，客户需要安装服务提供者提供的应用程序。然后客户需要根据其使用需求购买服务方案。之后，客户就可以立即开始使用服务了。这避免了客户遇到的困难，因为无需进行复杂的配置。客户只需为服务付费并开始使用即可。
- **服务提供者**是希望销售服务的开发者（可能就是你，因为你是开发者）。客户会向提供者请求服务，此时服务提供者会检查客户是否购买了有效的方案以及客户账户中是否有足够的余额。如果客户有足够的余额，服务提供者将扣除余额并向客户提供服务。
- **Odoo**在其中充当一种中介角色。它提供了处理支付、余额、方案等的媒介。客户从Odoo购买服务余额，服务提供者在提供服务时提取这些余额。Odoo在客户和服务提供者之间搭建了桥梁，因此客户无需进行复杂的配置，服务提供者也无需设置支付网关、客户账户管理等。作为回报，Odoo从销售中收取佣金。在撰写本书时，Odoo从服务包中收取25%的佣金。

流程中还有一个可选实体，即**外部服务**。在某些情况下，服务提供者会使用一些外部服务。不过，我们在这里将忽略外部服务，因为它们是次要的服务提供者。一个例子是短信服务。如果你正在向Odoo用户提供短信IAP服务，那么你（服务提供者）将在内部使用短信服务。

### IAP服务流

现在，我们将了解所有IAP实体如何协同工作来提供服务。下面的图表说明了IAP流程：

图17.1 – IAP工作流

以下是IAP服务流每一步的说明：

- **客户**向**服务提供者**发起服务请求。在此请求中，**客户**将传递账号令牌，**服务提供者**将使用该令牌来识别用户。（注意客户会在其服务器上安装你的模块。）
- 在收到**客户**的请求后，**服务提供者**将询问**Odoo**该**客户**账户中是否有足够的余额。如果**客户**有足够的余额，则会创建交易以在提供服务之前预留该余额。
- 在预留余额后，**服务提供者**将执行服务。在某些情况下，**服务提供者**会调用外部服务来执行所请求的服务。
- 在执行了**客户**请求的服务后，**服务提供者**返回**Odoo**来获取在*第2步*中预留的余额；如果由于错误而无法提供所请求的服务，**服务提供者**将要求**Odoo**释放已预留的余额。
- 最后，**服务提供者**将回复**客户**，通知其所请求的服务已完成。某些服务可能会返回结果信息；此时你将获得服务的结果。**客户**根据其规格使用该结果信息（取决于具体服务）。

### 扩展知识...

如果客户没有足够的余额，服务流程如下：

- 客户请求服务（与前面的流程相同）。
- 服务提供者收到请求并询问Odoo用户是否有足够的余额。假设客户没有足够的余额。
- 服务提供者返回给客户并告知账户中余额不足，同时显示用户可以在哪里购买服务的信息（Odoo服务包链接）。
- 客户被重定向到Odoo并为服务购买余额。

## 在Odoo中注册一个IAP服务

为了从客户账户中提取余额，服务提供者需要在Odoo上注册其服务。你还需要为服务定义方案。用户将通过这个已注册的服务购买你的方案。在本节中，我们将在Odoo上注册我们的服务并为我们的服务定义方案。

### 准备工作

要从IAP平台销售服务，服务提供者需要向Odoo注册服务和方案。我们将在 <https://iap-sandbox.odoo.com/> 上注册我们的服务。这个IAP端点用于测试目的。你可以免费购买服务包。对于生产环境，你需要在 <https://iap.odoo.com> 注册服务。在本节中，我们将使用沙盒IAP端点。

### 如何实现...

按照以下步骤在Odoo上创建IAP服务：

1. 打开 <https://iap-sandbox.odoo.com/> 并登录（如果没有账户请先注册）。

2. 点击主页上的**My Services**按钮。

3. 点击**Add a Service**按钮创建新服务。

4. 这将打开一个如下截图所示的表单。在此处填写信息，包括**Service Logo**、**Technical Name**（必须唯一）、**Unit Name**和**Privacy Policy**字段：

   图17.2 – 注册IAP服务

5. 保存服务后会给你一个服务密钥，如下截图所示。请在此时记下服务密钥，因为它不会再次显示：

   图17.3 – 新建的IAP服务

6. 通过在**Packs**部分点击**Add a pack**按钮来为服务创建一些服务包（方案）——例如，10欧元获取50条图书信息。下面的截图显示了创建新服务包的页面：

   图17.4 – IAP的新服务包

配置完成后，你的服务页面将如下所示：

图17.5 – 配置服务包后的IAP服务

你可以随时添加新的服务包。也可以随时更改服务包，但在撰写本书时，没有删除服务包的选项。

### 运行原理...

我们在 <https://iap-sandbox.odoo.com/> 上创建了一个IAP服务，因为我们希望在将服务投入生产之前先进行测试。让我们来了解一下创建服务时填写的各字段的用途：

- **Technical Name**值用于标识你的服务，它必须是唯一的名称。我们在这里添加了 `book_isbn` 技术名称。（此后无法更改。）
- **Label**、**Description**和**Service Logo**值用于信息展示。当用户购买服务时，这些信息将显示在网页上。
- **Unit Name**值是你的服务销售的单位。例如，在短信服务中，你的单位名称将是**SMS**（例如，100条短信5美元）。在我们的例子中，我们使用的单位名称是**Books info**。
- **Trial Credit**是为客户提供的用于测试的免费余额。每个客户仅提供一次。此外，试用余额仅在用户拥有有效的企业版合同时才有效，以避免免费余额被滥用。
- **Privacy Policy**是你的服务隐私政策的URL。

提交这些详细信息后，你的服务将被创建，并显示服务密钥。请参阅本节*第5步*中显示的截图以获取更多信息。服务密钥将在服务请求期间用于获取客户余额。请安全保存此密钥，因为它不会再次显示，尽管可以从同一页面生成新密钥；但一旦生成新密钥，旧密钥将停止工作。

我们仍需要为我们的服务创建方案。你需要提供方案名称、描述、徽标、数量和价格。**Amount**字段用于该方案的服务单位数量。**Price**字段用于定义用户获取此方案需要支付的金额。在本节的*第6步*中，我们创建了一个10欧元50条图书信息的方案。这里**Books info**是我们在创建服务时提交的单位类型。这意味着如果用户购买此方案，他们将能够获取50本图书的信息。

> 📝**注：**Odoo从此价格中收取25%的佣金，因此请相应地定义你的服务方案价格。

现在，我们将在以下章节中创建IAP服务模块和IAP客户端模块。

## 创建一个IAP服务模块

在本节中，我们将创建一个供服务提供者使用的服务模块。此模块将接受来自客户的IAP请求并在响应中返回服务结果。

### 准备工作

我们将创建 `iap_isbn_service` 模块。此服务模块将处理客户的IAP请求。客户将发送带有ISBN号的图书信息请求。服务模块将从客户账户中获取余额并返回图书名称、作者和封面图片等信息。

为便于理解，我们将通过两个小节来开发服务模块。在本节中，我们将创建一个基础模块，用于创建图书信息表。在客户请求时，服务提供者将通过搜索此表返回图书信息。在下一节中，我们将添加服务模块的第二部分；在该模块中，我们将添加获取余额和返回图书信息的代码。

### 如何实现...

按照以下步骤生成基础服务模块：

1. 创建一个新的 `iap_isbn_service` 模块并添加 `__init__.py`：

   ```python
   from . import models
   from . import controllers
   ```

2. 添加 `__manifest__.py`，内容如下：

   ```python
   {
       'name': "IAP ISBN service",
       'summary': "Get books information by ISBN number",
       'website': "http://www.example.com",
       'category': 'Uncategorized',
       'version': '14.0.1',
       'author': "Parth Gajjar",
       'depends': ['iap', 'web', 'base_setup'],
       'data': [
           'security/ir.model.access.csv',
           'views/book_info_views.xml',
           'data/books_data.xml',
       ]
   }
   ```

3. 在 `models/book_info.py` 中添加 `book.info` 模型，并包含获取图书数据的方法：

   ```python
   from odoo import models, fields, api

   class BookInfo(models.Model):
       _name = 'book.info'

       name = fields.Char('Books Name', required=True)
       isbn = fields.Char('ISBN', required=True)
       date_release = fields.Date('Release Date')
       cover_image = fields.Binary('BooksCover')
       author_ids = fields.Many2many('res.partner', string='Authors')

       @api.model
       def _books_data_by_isbn(self, isbn):
           book = self.search([('isbn', '=', isbn)], limit=1)
           if book:
               return {
                   'status': 'found',
                   'data': {
                       'name': book.name,
                       'isbn': book.isbn,
                       'date_release': book.date_release,
                       'cover_image': book.cover_image,
                       'authors': [a.name for a in book.author_ids]
                   }
               }
           else:
               return {
                   'status': 'not found',
               }
   ```

4. 在 `controllers/main.py` 文件中添加一个http控制器（不要忘记添加 `controllers/__init__.py` 文件）：

   ```python
   from odoo import http
   from odoo.http import request

   class Main(http.Controller):
       @http.route('/get_book_data', type='json', auth="public")
       def get_book_data(self):
           # 我们将在此获取余额
           return {
               'test': 'data'
           }
   ```

5. 在 `security/ir.model.access.csv` 中添加访问规则并在模块清单文件中列出该文件：

   ```csv
   id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
   acl_book_backend_user,book_info,model_book_info,base.group_user,1,1,1,1
   ```

6. 在 `views/book_info_views.xml` 中添加视图、菜单和动作：

   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <odoo>
       <!-- Form View -->
       <record id="book_info_view_form" model="ir.ui.view">
           <field name="name">Book Info Form</field>
           <field name="model">book.info</field>
           <field name="arch" type="xml">
               <form>
                   <sheet>
                       <field name="cover_image" widget='image'
                           class="oe_avatar"/>
                       <div class="oe_title">
                           <label for="name" class="oe_edit_only"/>
                           <h1>
                               <field name="name" class="oe_inline"/>
                           </h1>
                       </div>
                       <group>
                           <group>
                               <field name="isbn"/>
                               <field name="author_ids"
                                   widget="many2many_tags"/>
                           </group>
                           <group>
                               <field name="date_release"/>
                           </group>
                       </group>
                   </sheet>
               </form>
           </field>
       </record>

       <!-- 在此添加第7和第8步 -->
   </odoo>
   ```

7. 添加图书信息的树形视图：

   ```xml
   <!-- Tree(list) View -->
   <record id="books_info_view_tree" model="ir.ui.view">
       <field name="name">Book Info List</field>
       <field name="model">book.info</field>
       <field name="arch" type="xml">
           <tree>
               <field name="name"/>
               <field name="date_release"/>
           </tree>
       </field>
   </record>
   ```

8. 添加动作和菜单项：

   ```xml
   <!-- action and menus -->
   <record id='book_info_action' model='ir.actions.act_window'>
       <field name="name">Book info</field>
       <field name="res_model">book.info</field>
       <field name="view_mode">tree,form</field>
   </record>

   <menuitem name="Books Data" id="books_info_base_menu" />
   <menuitem name="Books" id="book_info_menu"
       parent="books_info_base_menu" action="book_info_action"/>
   ```

9. 如果你希望的话，可以添加一些示例图书数据。我们通过 `data/books_data.xml` 文件向模块添加了示例数据（不要忘记将封面图片添加到相应目录中）。

安装模块后，你将看到一个带有图书数据的新菜单，如下所示：

图17.6 – IAP服务模块的图书数据

### 运行原理...

我们现在创建了 `iap_isbn_service` 模块。我们创建了一个新的 `book.info` 表。将此表视为主表，我们将在其中存储所有图书的数据。当客户请求图书数据时，我们将在此表中进行搜索。如果找到了所请求的数据，我们将收取余额以换取图书数据。

> 📝**注：**如果你想出于商业目的创建此服务，你需要拥有世界上每本图书的信息。在现实世界中，你需要一个外部服务作为图书信息来源。在我们的练习中，假设我们在 `book.info` 表中拥有所有图书的数据，并且我们仅从此表提供图书数据。

在模型中，我们还创建了 `_books_data_by_isbn()` 方法。此方法将根据ISBN号查找图书并生成适当的数据，以便可以将其发送回客户。结果中的 `status` 键将用于指示是否找到了图书数据。当未找到图书数据时，它将用于释放已预留的余额。

我们还添加了一个 `/get_book_data` 路由。IAP客户将使用此URL发送请求来获取图书详情。我们仍需添加获取IAP余额的代码，这将在下一节中完成。不过，出于测试目的，你可以通过curl发送测试请求，如下所示：

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data "{}" \
  http://localhost:8069/get_book_data
```

这将返回类似这样的结果：

```json
{"jsonrpc": "2.0", "id": null, "result": {"test": "data"}}
```

本节中其余步骤来自之前的章节，不需要详细解释。在下一节中，我们将更新模块以获取客户的余额并将图书数据返回给他们。

## 授权并收取IAP余额

在本节中，我们将完成IAP服务模块。我们将使用IAP平台来授权并从客户账户中获取余额。我们还将添加一个可选配置来保存在本章*在Odoo中注册一个IAP服务*一节中生成的服务密钥。

### 准备工作

在本节中，我们将使用 `iap_isbn_service` 模块。

由于我们使用的是IAP沙盒服务，因此需要在系统参数中设置IAP端点。要设置IAP沙盒端点，请按照以下步骤操作：

1. 启用开发者模式。
2. 打开**Technical | Parameters | System Parameters**。
3. 创建一条新记录并添加键和值，如下所示：

图17.7 – 设置IAP沙盒的端点

### 如何实现...

为了完成服务模块，我们将添加一个配置选项来存储服务密钥。按照以下步骤在通用设置中添加新字段来设置 `isbn_service_key`：

1. 在 `res.config.settings` 中添加 `isbn_service_key` 字段：

   ```python
   from odoo import models, fields

   class ConfigSettings(models.TransientModel):
       _inherit = 'res.config.settings'

       isbn_service_key = fields.Char("ISBN service key",
           config_parameter='iap.isbn_service_key')
   ```

2. 在通用设置视图中添加 `isbn_service_key` 字段：

   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <odoo>
       <record id="view_general_config_isbn_service" model="ir.ui.view">
           <field name="name">Configuration: IAP service key</field>
           <field name="model">res.config.settings</field>
           <field name="inherit_id"
               ref="base_setup.res_config_settings_view_form" />
           <field name="arch" type="xml">
               <div id="business_documents" position="before">
                   <h2>IAP Books ISBN service</h2>
                   <div class="row mt16 o_settings_container">
                       <div class="col-12 col-lg-6 o_setting_box">
                           <div class="o_setting_right_pane">
                               <span class="o_form_label">
                                   IAP service key
                               </span>
                               <div class="text-muted">
                                   Generate service in odoo IAP
                                   and add service key here
                               </div>
                               <div class="content-group">
                                   <div class="mt16 row">
                                       <label for="isbn_service_key"
                                           class="col-3 col-lg-3
                                           o_light_label"/>
                                       <field name="isbn_service_key"
                                           class="oe_inline"
                                           required="1"/>
                                   </div>
                               </div>
                           </div>
                       </div>
                   </div>
               </div>
           </field>
       </record>
   </odoo>
   ```

3. 更新 `iap_isbn_service` 模块。模块更新后，你将在**General Settings**中看到一个用于存储服务密钥的字段，如下截图所示。如果你还记得，我们在本章*在Odoo中注册一个IAP服务*一节中生成了服务密钥。在此字段中添加生成的服务密钥。请参阅以下截图获取更多信息：

   图17.8 – 在配置中设置服务密钥

4. 现在，我们将更新 `/get_book_data` 控制器以获取客户余额。按如下方式更新 `main.py` 文件：

   ```python
   from odoo import http
   from odoo.http import request
   from odoo.addons.iap.tools import iap_tools

   class Main(http.Controller):
       @http.route('/get_book_data', type='json', auth="public")
       def get_book_data(self, account_token, isbn_number):
           service_key = request.env[
               'ir.config_parameter'].sudo().get_param(
               'iap.isbn_service_key', False)
           if not service_key:
               return {
                   'status': 'service is not active'
               }
           credits_to_reserve = 1
           data = {}
           with iap_tools.iap_charge(request.env,
                   service_key, account_token,
                   credits_to_reserve):
               data = request.env[
                   'book.info'].sudo()._books_data_by_isbn(
                   isbn_number)
               if data['status'] == 'not found':
                   raise Exception('Book not found')
           return data
   ```

更新模块以应用这些更改。

### 运行原理...

为了从客户账户中提取余额，我们需要从IAP平台生成的服务密钥。在本章*在Odoo中注册一个IAP服务*一节中，我们生成了服务密钥。（如果你丢失了服务密钥也没关系；可以从服务页面重新生成。）我们在通用设置中添加了 `isbn_service_key` 字段，以便可以在Odoo中存储服务密钥。你可能注意到我们在字段定义中使用了 `config_parameter` 属性。

在字段中使用此属性会将值存储在 `ir.config_parameter` 模型中，也称为**系统参数**。保存后，你可以在开发者模式下的**Technical | Parameters | System Parameters**菜单中检查其值。在获取IAP余额时，我们将从**系统参数**中检索服务密钥。要从**系统参数**中检索值，你可以使用 `get_param()`。例如，你可以像这样获取服务密钥：

```python
self.env['ir.config_parameter'].sudo().get_param(
    'iap.isbn_service_key', False)
```

这里，第一个参数是你想要访问其值的参数键，第二个参数是默认值。如果请求的键在数据库中不存在，则返回默认值。

接下来，我们更新了 `/get_book_data` 路由。现在，它接受两个参数：

- `account_token`，即用于标识用户的客户令牌。客户为服务购买的余额将在IAP平台上与此 `account_token` 关联。服务提供者将在获取余额时发送此令牌。
- `isbn_number` 是客户希望用余额换取信息的图书ISBN号。

> 📝**注：**这些参数在这里并不是固定的。我们的示例服务需要 `isbn_number`，所以我们传递了它。但是，你可以传递任意数量的参数。只需确保传递了 `account_token`，因为没有它，你无法从客户账户中获取余额。

IAP服务提供了 `iap_tools.iap_charge()` 辅助方法，用于处理从客户账户获取余额的过程。`iap_charge()` 方法接受四个参数：环境、提供者服务密钥、客户账号令牌和要获取的余额数量。`iap_charge()` 方法管理以下事项：

- 创建交易对象并预留指定数量的余额。如果客户账户没有足够的余额，则会引发**InsufficientCreditError**。
- 如果在客户账户中找到足够的余额，它将运行 `with` 块中的代码。
- 如果 `with` 块中的代码成功运行，它将获取已预留的余额。
- 如果 `with` 块中的代码产生异常，它将释放已预留的余额，因为无法完成服务请求。

在前面的示例中，我们使用了相同的 `iap_tools.iap_charge()` 方法来获取图书请求的余额。我们使用了我们的服务密钥和客户账号令牌来为图书信息预留一个余额。然后，在 `with` 块中，我们使用 `_books_data_by_isbn()` 方法根据ISBN号获取图书数据。如果找到了图书数据，则 `with` 块将无错误地执行，并且一个预留的余额将从客户账户中扣除。之后，我们将此数据返回给客户。如果未找到图书数据，则我们引发异常，以便释放已预留的余额。

### 扩展知识...

在我们的示例中，我们处理的是只有一本图书数据的请求，获取单个余额很简单；但处理多个余额时情况就变得复杂了。复杂的定价结构可能会引入一些边界情况。让我们通过以下示例来了解这个问题。假设我们想要处理多本图书的请求。在这种情况下，客户请求了10本图书的数据，但我们只有5本图书的数据。这里，如果我们完成 `with` 块而没有遇到任何错误，`iap_charge()` 将获取10个余额，这是不正确的，因为我们只有一定数量的图书数据。此外，如果我们引发异常，则会释放全部10个余额并向客户显示未找到图书信息。为了解决此问题，Odoo在 `with` 块中提供了交易对象。在某些情况下，服务无法完全满足请求。例如，用户请求了10本图书的数据，但你只有5本图书的数据。在这种情况下，你可以动态更改实际余额数量并获取部分余额。请参阅以下示例进一步说明：

```python
...
isbn_list = [<假设为10个ISBN号的列表>]
credits_to_reserve = len(isbn_list)
data_found = []
with iap_tools.iap_charge(request.env, service_key,
        account_token, credits_to_reserve) as transection:
    for isbn in isbn_list:
        data = request.env[
            'books.info']._books_data_by_isbn(isbn)
        if data['status'] == 'found':
            data_found.append(data)
    transection.credit = len(data_found)
return data_found
```

在前面的代码块中，我们根据 `transection.credit` 动态更新了要获取的余额值；这就是我们只对找到的图书数据收取余额的方式。

### 其它内容

- IAP不限于Odoo框架。你可以为任何其他平台或框架开发服务提供者模块。只需确保它可以处理JSON-RPC2（<https://www.jsonrpc.org/specification>）请求。
- 如果你在任何其他平台上开发服务提供者，你还需要通过使用IAP端点手动管理交易。你需要通过请求IAP端点来授权和获取余额。你可以在 <https://www.odoo.com/documentation/12.0/webservices/iap.html#json-rpc2-transaction-api> 获取端点信息。

## 创建一个IAP客户端模块

在上一节中，我们创建了IAP服务模块。现在，我们将创建一个IAP客户端模块来完成IAP服务流程。

### 准备工作

我们需要[第三章 创建Odoo插件模块](/blog/odoo-14-creating-odoo-add-on-modules)中的 `my_library` 模块。我们将在图书表单视图中添加一个新按钮，点击该按钮将创建一个对IAP服务的请求并获取图书数据。

按照IAP服务流程，客户向服务提供者发出请求。这里，为了注册客户的请求，我们需要为IAP服务运行一个单独的服务器。如果你想在同一台机器上进行测试，可以在不同的端口和不同的数据库上运行服务实例，如下所示：

```bash
./odoo-bin -c server-config -d service_db --db-filter=^service_db$ --http-port=8070
```

这将在端口**8070**上运行Odoo服务器。确保你已在此数据库中安装了服务模块并已添加IAP服务密钥。请注意，本节假设你有一个运行在 <http://localhost:8070> 上的IAP服务。

### 如何实现...

我们将创建一个新的 `iap_isbn_client` 模块。此模块将继承 `my_library` 模块并在图书表单视图中添加一个按钮。点击按钮将向运行在端口8070上的IAP服务发送请求。IAP服务将获取余额并返回所请求图书的信息。我们将把这些信息写入图书记录中。按照以下步骤完成IAP客户端模块：

1. 创建一个新的 `iap_isbn_client` 模块并添加 `__init__.py`：

   ```python
   from . import models
   ```

2. 添加 `__manifest__.py`，内容如下：

   ```python
   {
       'name': "Books ISBN",
       'summary': "Get Books Data based on ISBN",
       'website': "http://www.example.com",
       'category': 'Uncategorized',
       'version': '14.0.1',
       'author': "Parth Gajjar",
       'depends': ['iap', 'my_library'],
       'data': [
           'views/library_books_views.xml',
       ]
   }
   ```

3. 添加 `models/library_book.py` 并通过继承 `library.book` 模型添加一些字段：

   ```python
   from odoo import models, fields, api
   from odoo.exceptions import UserError
   from odoo.addons.iap.tools import iap_tools

   class LibraryBook(models.Model):
       _inherit = 'library.book'

       cover_image = fields.Binary('Books Cover')
       isbn = fields.Char('ISBN')
   ```

4. 在同一模型中添加 `fetch_book_data()` 方法。此方法将在按钮点击时被调用：

   ```python
   def fetch_book_data(self):
       self.ensure_one()
       if not self.isbn:
           raise UserError("Please add ISBN number")
       user_token = self.env['iap.account'].get('book_isbn')
       params = {
           'account_token': user_token.account_token,
           'isbn_number': self.isbn
       }
       service_endpoint = 'http://localhost:8070'
       result = iap_tools.iap_jsonrpc(
           service_endpoint + '/get_book_data',
           params=params)
       if result.get('status') == 'found':
           self.write(self.process_result(result['data']))
       return True
   ```

5. 添加 `process_result()` 方法来处理IAP服务的响应：

   ```python
   @api.model
   def process_result(self, result):
       authors = []
       existing_author_ids = []
       for author_name in result['authors']:
           author = self.env['res.partner'].search(
               [('name', '=', author_name)], limit=1)
           if author:
               existing_author_ids.append(author.id)
           else:
               authors.append((0, 0, {'name': author_name}))
       if existing_author_ids:
           authors.append((6, 0, existing_author_ids))
       return {
           'author_ids': authors,
           'name': result.get('name'),
           'isbn': result.get('isbn'),
           'cover_image': result.get('cover_image'),
           'date_release': result.get('date_release'),
       }
   ```

6. 添加 `views/library_books_views.xml`，通过继承图书表单视图添加按钮和字段：

   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <odoo>
       <record id="library_book_view_form_inh" model="ir.ui.view">
           <field name="name">Library Book Form</field>
           <field name="model">library.book</field>
           <field name="inherit_id"
               ref="my_library.library_book_view_form"/>
           <field name="arch" type="xml">
               <xpath expr="//group" position="before">
                   <header>
                       <button name="fetch_book_data"
                           string="Fetch Book Data"
                           type="object"/>
                   </header>
               </xpath>
               <field name="date_release" position="after">
                   <field name="isbn"/>
                   <field name="cover_image" widget="image"
                       class="oe_avatar"/>
               </field>
           </field>
       </record>
   </odoo>
   ```

安装 `iap_isbn_client` 模块。这将在图书表单中添加一个**Fetch Book Data**按钮。完成后，添加一个有效的**ISBN**号（例如**1788392019**）并点击按钮。这将发送请求并从服务中获取数据。如果你是第一次发起IAP服务调用，那么你的Odoo实例不会有关联账户的信息，因此Odoo将弹出一个购买余额的弹窗，如下所示：

图17.9 – 余额不足的警告

点击**Buy credits at Odoo**按钮后，你将被重定向到IAP服务页面，在那里你将看到可供购买的服务包信息。对于我们的示例，你将看到我们在本章*在Odoo中注册一个IAP服务*一节中定义的服务包。请看下面的截图：有一个可供购买的服务包列表：

图17.10 – 可购买的IAP服务包

由于我们使用的是沙盒端点，你可以免费购买任何服务包。之后，你可以从图书表单视图中请求图书信息。

### 运行原理...

我们在服务模块中创建了一个 `/get_book_data` 路由。此路由用于处理客户的IAP请求。因此，从这个客户端模块，我们将向该路由发送JSON-RPC请求。此IAP请求将获取余额并取得图书数据。幸运的是，IAP模块提供了一个 `iap_jsonrpc` 包装器来发送jsonrpc请求，因此我们将使用它。

`my_library` 模块的 `library.book` 模型没有ISBN和 `cover_image` 字段，因此我们通过继承在 `library.book` 模型中添加了额外的字段。请参阅[第四章 应用模型](/blog/odoo-14-application-models)中的*使用继承向模型添加功能*一节。我们通过继承添加字段是因为当 `iap_isbn_client` 模块未安装时我们不想使用这些字段。

为了发起请求，我们通过继承在图书表单视图中添加了一个按钮。按钮点击将触发 `fetch_book_data()` 方法，在该方法中，我们向服务端点发送了jsonrpc请求。在请求中，我们传递了两个参数：客户账号令牌和图书数据的ISBN号。

你可以通过 `iap.account` 模型的 `get()` 方法获取客户账号令牌。令牌生成是自动的。你只需用服务名称调用 `get()` 方法。在我们的例子中，服务名称是 `book_isbn`。这将返回客户IAP账户的记录集，你可以获取客户令牌的 `account_token` 字段。

我们发送了jsonrpc请求来获取图书信息。如果客户没有足够的余额，服务模块将生成**InsufficientCreditError**。现在，jsonrpc将自动处理此异常，并向客户显示一个购买余额的弹窗。弹窗将包含一个链接，指向客户可以购买服务方案的页面。由于我们使用的是沙盒，你可以免费获取任何服务包。但在生产环境中，客户需要为服务付款。

点击按钮后，如果一切顺利，客户有足够的余额，并且我们的数据库中有所请求ISBN的数据，余额将从客户账户中扣除，`iap_jsonrpc` 将返回图书数据。然后，我们简单地将结果传递给 `process_result()` 方法并将数据写入图书记录。

### 扩展知识...

如果你想了解服务的剩余余额数量，可以在仪表盘上提供的链接中查看：

图17.11 – 查看你的活跃服务和余额

此外，`iap_tools.iap_charge()` 方法支持另一个参数 `description`，你可以按如下方式传递：

```python
...
with iap_tools.iap_charge(request.env, service_key,
        account_token, credits_to_reserve,
        description="For the book info"):
    ...
```

如果你在获取余额时传递了 `description`，客户将能够在IAP门户中看到扣除余额的描述信息。

## 在账户缺少余额时显示报价

如果你在所有购买的余额消耗完后发起IAP服务请求，服务模块将生成**InsufficientCreditError**，客户端模块将自动处理此错误并显示弹窗。每当你的IAP账户余额消耗完时，Odoo将显示如下截图所示的弹窗，提示购买更多余额：

图17.12 – 余额不足时显示的警告

默认弹窗过于简单，无法提供足够的信息。在本节中，我们将了解如何用一个更具吸引力的模板来更改此弹窗的内容。

### 准备工作

我们将在本节中使用 `iap_isbn_service` 模块。报价模板是在IAP服务提供者模块上创建的，因此可以随时更改而无需更新客户端模块。

### 如何实现...

按照以下步骤添加自定义余额模板：

1. 在 `views/templates.xml` 中添加带有服务信息的模板：

   ```xml
   <odoo>
       <template id="no_credit_info" name="No credit info">
           <section class="jumbotron text-center bg-primary">
               <div class="container pb32 pt32">
                   <h1 class="jumbotron-heading">
                       Library ISBN
                   </h1>
                   <p class="lead text-muted">
                       Get full book information with cover
                       image just by the ISBN number.
                   </p>
                   <span class="badge badge-warning"
                       style="font-size: 30px;">
                       20% Off
                   </span>
               </div>
           </section>
           <div class="container">
               <div class="row">
                   <div class="col">
                       <div class="card mb-3">
                           <div class="card-header">
                               <i class="fa fa-database"/>
                               Large books database
                           </div>
                           <div class="card-body">
                               <p class="card-text">
                                   We have largest book database.
                                   It contains more then
                                   2500000+ books.
                               </p>
                           </div>
                       </div>
                   </div>
                   <div class="col">
                       <div class="card mb-3">
                           <div class="card-header">
                               <i class="fa fa-image"/>
                               With cover image
                           </div>
                           <div class="card-body">
                               <p class="card-text">
                                   More than 95% of our books
                                   having high quality book
                                   cover images.
                               </p>
                           </div>
                       </div>
                   </div>
               </div>
           </div>
       </template>
   </odoo>
   ```

2. 在 `__manifest__.py` 中添加模板：

   ```python
   ...
   'data': [
       'security/ir.model.access.csv',
       'views/book_info_views.xml',
       'data/books_data.xml',
       'views/res_config_settings.xml',
       'views/templates.xml'
   ]
   ...
   ```

3. 在 `controllers/main.py` 中向 `iap_tools.iap_charge` 添加模板引用：

   ```python
   ...
   with iap_tools.iap_charge(request.env, service_key,
           account_token, credits_to_reserve,
           credit_template=
           'iap_isbn_service.no_credit_info'):
       data = request.env[
           'book.info'].sudo()._books_data_by_isbn(
           isbn_number)
       if data['status'] == 'not found':
           raise Exception('Book not found')
   ```

更新模块以应用更改。

图17.13 – 余额不足时显示的报价

更新后，如果客户的所有余额都已消耗完，你将看到如*图17.13*所示的余额弹窗。

### 运行原理...

为了在客户端显示一个更具吸引力的弹窗，我们需要创建一个QWeb模板。在*第1步*中，我们创建了QWeb模板 `no_credit_info`。这是用简单的Bootstrap内容制作的。请注意它只包含静态HTML内容。在*第2步*中，我们将模板文件添加到了应用清单中。

设计好模板后，你需要将模板XML引用传递给 `iap_tools.iap_charge()` 方法。这可以通过可选的 `credit_template` 参数传递。在*第3步*中，我们向charge方法传递了模板引用。传递模板后，如果引发了**InsufficientCreditError**，则模板将与错误消息一起传递给客户。在客户端，如果收到带有模板主体的错误消息，则此自定义模板将在弹窗中显示，而不是默认弹窗。

### 扩展知识...

我们的模板中没有图片，但如果你想在模板中使用图片，需要格外小心。原因是在这里你不能像通常那样使用绝对图片URL。因为服务模块运行在单独的服务器上，弹窗将无法显示图片。要解决此问题，你需要传递带有域名的完整图片URL，因为此模板将在客户端屏幕上显示。
:::
