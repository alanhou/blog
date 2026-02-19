---
series: "odoo14-cookbook"
seriesOrder: 22
title:
  en: "Chapter 22: Point of Sale"
  zh: "第22章 POS（销售点）"
description:
  en: "Customize the Odoo 14 Point of Sale application with OWL components, action buttons, RPC calls, UI modifications, and receipt customization."
  zh: "使用OWL组件、动作按钮、RPC调用、UI修改和收据自定义来定制Odoo 14销售点应用。"
date: 2021-06-25
tags: ["odoo", "odoo14", "pos", "point-of-sale", "owl", "javascript"]
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080"
---

:::zh
截至目前在本书中我们探讨了两种不同的基础代码。一种是用于创建视图、动作、菜单、向导等的后端基础代码。第二种是用于创建网页、控制器、小插件等的前端基础代码。本章中我们将探讨第三种基础代码，用于Point of Sale（销售点）应用。你可能会好奇为什么Point of Sale应用需要一种不同的基础代码。这是因为它使用不同的架构，使其也可以离线运行。本章中我们将学习如何修改Point of Sale应用。

本章中，我们将讲解如下内容：

- 添加自定义JavaScript/SCSS文件
- 在键盘上添加动作按钮
- 做RPC调用
- 修改POS界面UI
- 修改已有业务逻辑
- 修改客户收据

> **📝注**：Point of Sale应用大多使用JavaScript编写。本章中假定你已有JavaScript的基础知识。本章还使用了OWL框架，因此如果不了解这些JavaScript术语的话，请学习[第16章 Odoo Web Library (OWL)](/blog/odoo-14-odoo-web-library-owl)。

整章中我们使用一个名为 `pos_demo` 的插件模块。这个 `pos_demo` 模块会依赖于 `point_of_sale`，因为我们将要对Point of Sale应用进行自定义。为快速上手本章，我们准备了一个 `pos_demo` 的初始模块，可通过本书GitHub仓库的 `Chapter21/r0_initial_module/pos_demo` 目录进行获取。

## 技术准备

本章中使用的所有代码可通过如下GitHub仓库进行下载：<https://github.com/PacktPublishing/Odoo-14-Development-Cookbook-Fourth-Edition/tree/master/Chapter22>。

## 添加自定义JavaScript/SCSS文件

Point of Sale应用使用不同的资源包来管理JavaScript和样式文件。本节中，我们将学习如何向POS资源包中添加SCSS和JavaScript文件。

### 准备工作

本节中，我们将把SCSS样式文件和JavaScript文件加载到Point of Sale应用中。

### 如何实现...

按照如下步骤来在Point of Sale应用中加载资源：

1. 新增SCSS文件 `/pos_demo/static/src/scss/pos_demo.scss` 并加入如下代码：

   ```scss
   .pos .pos-content {
       .price-tag {
           background: #00abcd;
           width: 100%;
           right: 0;
           left: 0;
           top:0;
       }
   }
   ```

2. 新增JavaScript文件 `/pos_demo/static/src/js/pos_demo.js` 并加入如下代码：

   ```javascript
   console.log('Point of Sale JavaScript loaded');
   ```

3. 将这些JavaScript和SCSS文件注册到 `point_of_sale` 资源中：

   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <odoo>
       <template id="assets" inherit_id="point_of_sale.assets">
           <xpath expr="." position="inside">
               <script type="text/javascript"
                   src="/pos_demo/static/src/js/pos_demo.js"></script>
               <link rel="stylesheet"
                   href="/pos_demo/static/src/scss/pos_demo.scss"/>
           </xpath>
       </template>
   </odoo>
   ```

安装 `pos_demo` 模块。要查看实时的修改，可通过 **Point of Sale** | **Dashboard** 菜单打开新的POS会话。

### 运行原理...

本节中，我们将一个JavaScript文件和一个SCSS文件加载到了Point of Sale应用中。第1步中，我们修改了产品卡片价格标签的背景色和边框半径。在安装了 `pos_demo` 模块之后，你将能看到价格标签的更改：

![Figure 22.1 – Updated price label](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_22.1_B15928.jpg)

图22.1 - 更新后的价格标签

第2步中，我们添加了JavaScript文件。其中我们向控制台添加了一条日志。为查看该消息，你需要打开浏览器的开发者工具。在 **Console** 标签中，可以看到如下的日志。这表明你的JavaScript文件已成功加载。现在，我们仅在JavaScript文件中添加了日志，但在接下来的小节中，我们会添加更多代码：

![Figure 22.2 – JavaScript loaded (log in the console)](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_22.2_B15928.jpg)

图22.2 - JavaScript已加载（控制台中的日志）

第3步中，我们向Point of Sale资源中添加了前述的JavaScript和SCSS文件。Point of Sale资源的外部ID为 `point_of_sale.assets`。此处仅有外部ID不同，其它部分和常规资源相同。如果不知道Odoo中资源如何运作，请参见[第14章 CMS网站开发](/blog/odoo-14-cms-website-development)中的*管理静态资源*一节。

### 扩展知识...

Odoo还有针对餐厅POS解决方案的插件模块。注意这个Point of Sale餐厅模块仅是对POS应用的扩展。如果想要在餐厅模块中进行自定义，你将需要在相同的 `point_of_sale.assets` 资源包中添加JavaScript和SCSS文件。

## 在键盘上添加动作按钮

如我们在前一节所讨论的，POS应用的设计使其可在离线状况下使用。因此POS应用的代码结构和其余的Odoo应用都不同。POS应用的代码库大多使用JavaScript编写并且提供了自定义的不同工具。本节中，我们将使用一个这类工具来在键盘面板的顶部创建一个动作按钮。

### 准备工作

本节我们将继续使用*添加自定义JavaScript/SCSS文件*一节中所创建的 `pos_demo` 模块。我们将在键盘面板的顶部添加一个按钮。该按钮是对订单行应用折扣的一个快捷方式。

### 如何实现...

按照如下步骤来在Point of Sale应用的键盘面板中添加一个5%折扣的动作按钮：

1. 在 `/static/src/js/pos_demo.js` 文件中添加如下代码，它会定义一个动作按钮：

   ```javascript
   odoo.define('pos_demo.custom', function (require) {
       "use strict";
       const PosComponent = require('point_of_sale.PosComponent');
       const ProductScreen = require('point_of_sale.ProductScreen');
       const Registries = require('point_of_sale.Registries');
       class PosDiscountButton extends PosComponent {
           async onClick() {
               const order = this.env.pos.get_order();
               if (order.selected_orderline) {
                   order.selected_orderline.set_discount(5);
               }
           }
       }
       PosDiscountButton.template = 'PosDiscountButton';
       ProductScreen.addControlButton({
           component: PosDiscountButton,
           condition: function () {
               return true;
           },
       });
       Registries.Component.add(PosDiscountButton);
       return PosDiscountButton;
   });
   ```

2. 在 `/static/src/xml/pos_demo.xml` 文件中为该按钮添加OWL模板：

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <templates id="template" xml:space="preserve">
       <t t-name="PosDiscountButton" owl="1">
           <span class="control-button "
                 t-on-click="onClick">
               <i class="fa fa-gift"></i>
               <span>5%</span>
               <span>Discount</span>
           </span>
       </t>
   </templates>
   ```

3. 在声明文件中注册QWeb模板如下：

   ```javascript
   'qweb': [        'static/src/xml/pos_demo.xml'     ]
   ```

4. 更新 `pos_demo` 模块来应用修改。然后，你就会在键盘的顶部看到一个 **5% Discount** 按钮：

   ![Figure 22.3 – Discount button](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_22.3_B15928.jpg)

   图22.3 - 折扣按钮

   点击该按钮后，会对所选的订单行应用折扣。

### 运行原理...

在Odoo v14中，Point of Sale应用的代码库使用OWL框架完全重写了。你可以在[第16章 Odoo Web Library (OWL)](/blog/odoo-14-odoo-web-library-owl)中了解更多有关OWL框架的知识。

要在Point of Sale应用中创建动作按钮，需要继承PosComponent。PosComponent在 `point_of_sale.PosComponent` 命名空间中定义，因此要在代码中使用它，需要进行导入。第1步中，我们使用 `require('point_of_sale.PosComponent')` 导入了组件。然后我们通过继承PosComponent创建了 `PosDiscountButton`。如果想要学习Odoo JavaScript中require的运行机制，请参见[第14章 CMS网站开发](/blog/odoo-14-cms-website-development)中的*为网站扩展CSS和JavaScript*一节。第1步中我们还导入了 `point_of_sale.ProductScreen` 和 `point_of_sale.Registries`。其中 `point_of_sale.ProductScreen` 用于通过 `addControlButton` 方法向POS界面添加按钮。最后，我们将注册后的按钮添加到了 `point_of_sale.Registries` 中，这是包含所有OWL组件的全局注册表。

PosComponent有一些内置工具，可以访问有用的信息，如订单详情、POS配置等。可以通过 `this.env` 变量进行访问。在我们的示例中，我们通过 `this.env.pos.get_order()` 方法获取了当前订单信息。然后使用 `set_discount()` 方法设置了5%的折扣。

第2步和第3步中，我们添加了OWL模板，该模板会渲染到POS键盘上方。如果想了解更多，请参见[第16章 Odoo Web Library (OWL)](/blog/odoo-14-odoo-web-library-owl)。

### 扩展知识...

`addControlButton()` 方法支持另一个参数 `condition`。这个参数用于根据某一条件隐藏/显示该按钮。这个参数的值是一个返回布尔值的函数。根据所返回的值，POS系统会隐藏或显示这个按钮。参见下例来获取更多信息：

```javascript
ProductScreen.addControlButton({
    component: POSDiscountButton,
    condition: function() {
        return this.env.pos.config.module_pos_discount;
    },
});
```

上述 `condition` 函数表示折扣按钮仅在POS配置中启用了折扣功能时才显示。

## 做RPC调用

虽然Point of Sale应用可离线使用，它仍然可以对服务端进行RPC调用。RPC调用可用于任意操作，你可以使用它来进行CRUD操作或对服务端执行某个动作。本节中，我们将进行RPC调用来获取客户最近5个订单的信息。

### 准备工作

本节中，我们将使用*在键盘上添加动作按钮*一节中所创建的 `pos_demo` 模块。我们将定义动作按钮。在用户点击这个动作按钮时，我们会进行RPC调用来获取订单信息并在弹窗中展示。

### 如何实现...

按照如下步骤来显示所选择客户的最近5张订单：

1. 在 `/static/src/js/pos_demo.js` 文件中添加如下代码来创建并注册一个新的动作按钮：

   ```javascript
   class PosLastOrderButton extends PosComponent {
           // 在此处放置第2步的代码
   }
   PosLastOrderButton.template = 'PosLastOrderButton';
   ProductScreen.addControlButton({
       component: PosLastOrderButton,
       condition: function () {
           return true;
       },
   });
   Registries.Component.add(PosLastOrderButton);
   ```

2. 在 `PosLastOrderButton` 类中添加如下点击处理函数：

   ```javascript
   async onClick() {
       var self = this;
       const order = this.env.pos.get_order();
       if (order.attributes.client) {
           var domain = [['partner_id', '=', order.attributes.client.id]];
           this.rpc({
               model: 'pos.order',  method: 'search_read',
               args: [domain, ['name', 'amount_total']],
               kwargs: { limit: 5 },
           }).then(function (orders) {
               if (orders.length > 0) {
                   var order_list = _.map(orders, function (o) {
                       return { 'label': _.str.sprintf("%s - TOTAL: %s", o.name, o.amount_total) };
                   });
                   self.showPopup('SelectionPopup', { title: 'Last 5 orders', list:order_list });
               } else {
                   self.showPopup('ErrorPopup', { body: 'No previous orders found' });
               }
           });
       } else {
           self.showPopup('ErrorPopup', { body: 'Please select the customer' });
       }
   }
   ```

3. 在 `/static/src/xml/pos_demo.xml` 文件中为按钮添加OWL模板：

   ```xml
   <t t-name="PosLastOrderButton" owl="1">
       <span class="control-button" t-on-click="onClick">
           <i class="fa fa-shopping-cart"></i>
           <span></span>
           <span>Last Orders</span>
       </span>
   </t>
   ```

4. 更新 `pos_demo` 模块来应用修改。然后，你将能在键盘面板上方看到一个 **Last Orders** 按钮。在点击这个按钮时，会在弹窗中显示订单信息：

   ![Figure 22.4 – Last five orders of a customer](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_22.4_B15928.jpg)

   图22.4 - 客户最近5张订单

   如果没有找到之前的订单，则会显示一条警告消息而不是订单列表。

### 运行原理...

第1步中，我们创建并注册了动作按钮。如果想了解动作按钮更多的相关知识，请参见本章的*在键盘上添加动作按钮*一节。在深入技术细节之前，让我们来理解通过这个动作按钮我们希望完成的操作。在点击后，我们希望显示所选客户最近5张订单的信息。有一些情况是未选中客户或者客户此前没有订单。在这些情况下，我们需要在弹窗中显示相应的信息。

RPC工具可通过组件的 `this.rpc` 属性使用。第2步中，我们添加了点击处理函数。在点击动作按钮时，会调用该处理函数。这个函数会向服务端发送RPC调用来获取订单信息。我们使用了 `rpc()` 方法来进行RPC调用。以下是你可以在 `rpc()` 方法中传递的参数列表：

- **model**：你希望对其执行操作的模型名称
- **method**：你所希望调用的方法名称
- **args**：方法所能接受的必填位置参数列表
- **kwargs**：方法所接收的可选参数字典

本节中，我们使用了 `search_read` 方法来通过RPC获取数据。我们传递了客户域来过滤订单。我们还传递了 `limit` 关键字参数来仅获取5个订单。`rpc()` 是一个异步方法，返回Promise对象，因此要处理该结果，你需要使用 `then()` 方法，也可以使用await关键字。

> **📝注**：RPC调用不可在离线模式下使用。如果你有良好的网络连接并且不常使用离线模式，那么可以使用RPC。虽然Odoo的Point of Sale应用可以离线使用，有些操作，如创建或更新客户，需要有网络连接，因为这些功能在内部使用了RPC调用。

我们在弹窗中显示了之前的订单信息。我们使用了 `SelectionPopup`，它用于显示可选列表；我们用它来展示最近5张订单。我们还使用了 `ErrorPopup` 来在未选中客户或没有找到之前订单时显示警告消息。

第3步中，我们为动作按钮添加了QWeb模板。POS应用会渲染这个模板来显示动作按钮。

### 扩展知识...

还有很多其它的弹窗工具可以使用。例如，`NumberPopup` 用于从用户获取数字输入。请查看 `addons/point_of_sale/static/src/xml/Popups` 目录中的文件来了解所有这些工具。

## 修改POS界面UI

POS应用的用户界面使用OWL QWeb模板编写。本节中，我们将学习如何在POS应用中修改UI元素。

### 准备工作

本节我们将使用*做RPC调用*一节中所创建的 `pos_demo` 模块。我们会修改产品卡片的UI并显示每个产品的边际利润。

### 如何实现...

按照如下步骤来在产品卡片中显示边际利润：

1. 在 `/static/src/js/pos_demo.js` 文件中添加如下代码来获取产品的实际价格的额外字段：

   ```javascript
   const pos_model = require('point_of_sale.models');
   pos_model.load_fields("product.product", ["standard_price"]);
   ```

2. 在 `/static/src/xml/pos_demo.xml` 中添加如下代码来在产品卡片中显示边际利润：

   ```xml
   <t t-name="ProductItem" t-inherit="point_of_sale.ProductItem"    t-inherit-mode="extension" owl="1">
       <xpath expr="//span[hasclass('price-tag')]" position="after">
           <span t-if="props.product.standard_price"
                 class="sale_margin">
               <t t-set="margin"                t-value="props.product.get_price(pricelist, 1) - props.product.standard_price"/>
               <t t-esc="env.pos.format_currency(margin)"/>
           </span>
       </xpath>
   </t>
   ```

3. 为利润文本添加如下的样式：

   ```scss
   .sale_margin {
       top: 21px;
       line-height: 15px;
       right: 2px;
       background: #CDDC39;
       position: absolute;
       border-radius: 10px;
       padding: 0px 5px;
   }
   ```

更新 `pos_demo` 模块来应用修改。然后，你将能够在产品卡片中看到边际利润：

![Figure 22.5 – Profit margins for products](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_22.5_B15928.jpg)

图22.5 - 产品的边际利润

如果产品未设置产品成本，那么产品卡片将不会显示边际利润，因此请确保设置了产品成本。

### 运行原理...

本节中，我们希望使用 `standard_price` 字段作为产品的购买价格。这个字段默认在POS应用中并没有加载。第1步中，我们为 `product.product` 模型添加了 `standard_price` 字段。然后产品数据会多一个字段：`standard_price`。

第2步中，我们扩展了默认的产品卡片模板。你将需要使用 `t-inherit` 属性来继承已有QWeb模板。然后你需要使用XPath来选择你想要执行操作的元素。如果想了解更多有关XPath的知识，请参见[第9章 后端视图](/blog/odoo-14-backend-views)中的*修改已有视图 - 视图继承*一节。

为获取产品的销售价格，我们使用了从父级OWL组件传递过来的 `product` 属性。`get_price()` 是 `product` 模型的一个方法，我们在ProductItem组件中接收到 `product` 属性。然后我们通过产品价格和产品成本计算出了边际利润。如果想了解更多，请参见[第16章 Odoo Web Library (OWL)](/blog/odoo-14-odoo-web-library-owl)。

第3步中，我们添加了样式来修改利润元素的位置。这会为利润元素添加背景色并将其放到价格标签的下方。

## 修改已有业务逻辑

在前面的小节中，我们学习了如何通过RPC获取数据以及如何修改POS应用的UI界面。本节中我们将学习如何修改或继承已有的业务逻辑。

### 准备工作

本节我们将继续使用*修改POS界面UI*一节中所创建的 `pos_demo` 模块，其中我们获取了产品的购买价格并显示了产品利润。现在，本节中我们将在用户以低于产品利润的价格出售产品时向用户发送警告。

### 如何实现...

POS应用的大部分业务逻辑使用JavaScript编写，因此我们仅需对其进行修改来实现本节的目标。在 `/static/src/js/pos_demo.js` 中添加如下代码来在用户以低于购买价格出售产品时发送警告：

```javascript
const UpdatedProductScreen = ProductScreen =>
    class extends ProductScreen {
        _setValue(val) {
            super._setValue(val);
            const orderline = this.env.pos.get_order().selected_orderline;
            if (orderline && orderline.product.standard_price) {
                var price_unit = orderline.get_unit_price() * (1.0 - (orderline.get_discount() / 100.0));
                if (orderline.product.standard_price > price_unit) {
                    this.showPopup('ErrorPopup', { title: 'Warning', body: 'Product price set below cost of product.' });
                }
            }
        }
    };
Registries.Component.extend(ProductScreen, UpdatedProductScreen);
```

更新 `pos_demo` 模块来应用修改。在更新后，对订单行添加折扣，使产品价格低于购买价格。会弹出如下警告：

![Figure 22.6 – Warning on a big discount](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_22.6_B15928.jpg)

图22.6 - 大折扣时的警告

注意，当你将产品价格设置为低于实际成本时，会显示警告，并且每次执行操作（如更改产品订单的数量）时都会持续弹出。

### 运行原理...

POS组件注册表提供了 `extend` 方法来修改已有的函数。在内部，它是对实际组件定义进行猴子补丁（monkey patching）。

在我们的示例中，我们修改了 `_setValue()` 方法。ProductScreen的 `_setValue()` 方法在用户对订单行进行更改时被调用。我们希望在用户将产品价格设置为低于产品成本时显示警告。因此我们定义了一个新的 `_setValue()` 方法并调用了super方法；这会确保用户执行的任何操作都被应用。在调用super方法之后，我们编写了自己的逻辑，检查产品的销售价格是否高于实际成本。如果不是，则向用户显示警告。

> **📝注**：使用super时如不谨慎会破坏一些事物。如果方法从多个文件中继承，你必须调用super方法，否则它会在随后的继承中跳过该逻辑。这有时会导致崩溃的内部数据状态。

我们将自己的业务逻辑放到了默认实现（super）调用之后。如果想要在默认实现之前编写业务逻辑，可以通过将super调用放到函数的最后来实现。

## 修改客户收据

在你自定义Point of Sale应用时，从客户获取到的常见请求是修改客户收据。本节我们将学习如何修改客户收据。

### 准备工作

本节我们将继续使用*修改已有业务逻辑*一节中所创建的 `pos_demo` 模块。我们将在POS收据中添加一行来显示客户在订单中节省了多少钱。

### 如何实现...

按照如下步骤来在Point of Sale应用中修改客户收据：

1. 在 `/static/src/js/pos_demo.js` 文件中添加如下代码。这会在收据环境中添加额外的数据：

   ```javascript
   var models = require('point_of_sale.models');
   var _super_order = models.Order.prototype;
   models.Order = models.Order.extend({
       export_for_printing: function () {
           var result = _super_order.export_for_printing.apply(this, arguments);
           var savedAmount = this.saved_amount();
           if (savedAmount > 0) {
               result.saved_amount = this.pos.format_currency(savedAmount);
           }
           return result;
       },
       saved_amount: function() {
           const order = this.pos.get_order();
           return _.reduce(order.orderlines.models,
               function (rem, line) {
                   var diffrence = (line.product.lst_price * line.quantity) - line.get_base_price();
                   return rem + diffrence;
               }, 0);
       }
   });
   ```

2. 在 `/static/src/xml/pos_demo.xml` 中添加如下代码。这会继承默认的收据模板并添加我们的自定义内容：

   ```xml
   <t t-name="OrderReceipt" t-inherit="point_of_sale.OrderReceipt"   t-inherit-mode="extension" owl="1">
       <xpath expr="//div[hasclass('before-footer')]" position="before">
           <div style="text-align:center;">
               <div t-if="receipt.saved_amount">
                   You saved
                   <t t-esc="receipt.saved_amount"/>
                   on this order.
               </div>
           </div>
       </xpath>
   </t>
   ```

更新 `pos_demo` 模块来应用修改。然后，添加一个带有折扣的产品并查看收据，会在收据上看到多了一行：

![Figure 22.7 – Updated receipt](/api/v2/epubs/urn:orm:book:9781800200319/files/image/Figure_22.7_B15928.jpg)

图22.7 - 更新后的收据

如果节省金额为零或为负数，收据将不会显示**节省金额**信息。

### 运行原理...

本节中并没有什么新的内容。我们只是通过使用前面小节的知识更新了收据。第1步中，我们重载了 `export_for_printing()` 函数来向收据环境发送了更多数据。通过 `export_for_printing()` 方法发送的所有内容都可以在收据的QWeb模板中使用。我们对比了产品的基准价格和收据上的价格来计算为客户节省了多少钱。我们通过 `saved_amount` 键将这一数据发送到了收据环境中。

第2步中，我们修改了收据上默认的QWeb模板。实际收据的模板名为 `OrderReceipt`，因此我们使用了它作为 `t-inherit` 属性的值。在第1步中我们已经发送了修改收据所需的信息。在QWeb模板中，我们在 `receipt.saved_amount` 键中获取到了节省的金额，因此我们在页脚之前又添加了一个 `<div>` 元素。这会在收据上打印出所节省的金额。如果想要学习更多有关重载的知识，请参见*修改POS界面UI*一节。
:::
