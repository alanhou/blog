---
series: "odoo14-cookbook"
seriesOrder: 18
title:
  en: "Chapter 18: Automated Test Cases"
  zh: "第18章 自动化测试用例"
description:
  en: "Write and run automated tests for Odoo 14 modules including Python tests, JavaScript QUnit tests, tour tests, and data population."
  zh: "编写和运行Odoo 14模块的自动化测试，包括Python测试、JavaScript QUnit测试、引导测试和数据填充。"
date: 2021-06-08
tags: ["odoo", "odoo14", "testing", "automated-tests", "unit-tests", "qunit"]
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080"
---

:::zh
在开发大型应用程序时，使用自动化测试用例是提高模块可靠性的良好实践。这使得模块更加健壮。每年，Odoo都会发布其软件的新版本，而自动化测试用例在检测应用程序中的回归方面非常有用，这些回归可能是由版本升级引起的。幸运的是，Odoo框架附带了不同的自动化测试工具。Odoo包含以下三种主要的测试类型：

- **Python测试用例**：用于测试Python业务逻辑
- **JavaScript QUnit测试**：用于测试Odoo中的JavaScript实现
- **导览测试**：集成测试，用于检查Python和JavaScript是否能正确地协同工作

本章中，我们将讲解如下小节：

- 添加Python测试用例
- 运行打标签的Python测试用例
- 为客户端测试用例设置Headless Chrome
- 添加客户端QUnit测试用例
- 添加导览测试用例
- 通过UI运行客户端测试用例
- 调试客户端测试用例
- 为失败的测试用例生成视频/截图
- 填充随机测试数据

## 技术准备

在本章中，我们将详细介绍所有测试用例。为了在单个模块中涵盖所有测试用例，我们创建了一个小模块。其Python定义如下：

```python
class LibraryBook(models.Model):
    _name = 'library.book'

    name = fields.Char('Title', required=True)
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner', string='Authors')
    state = fields.Selection(
        [('draft', 'Not Available'),
         ('available', 'Available'),
         ('lost', 'Lost')],
        'State', default="draft")
    color = fields.Integer()

    def make_available(self):
        self.write({'state': 'available'})

    def make_lost(self):
        self.write({'state': 'lost'})
```

上面给出的Python代码将帮助我们编写针对Python业务场景的测试用例。对于JavaScript测试用例，我们添加了[第十五章 网页客户端开发](/blog/odoo-14-web-client-development)中*创建自定义微件*一节中的 `int_color` 微件。

你可以从本书的GitHub仓库下载此初始模块：<https://github.com/PacktPublishing/Odoo-14-Development-Cookbook-Fourth-Edition/tree/master/Chapter18/00_initial_module>。

## 添加Python测试用例

Python测试用例用于检查业务逻辑的正确性。在[第五章 基本服务端开发](/blog/odoo-14-basic-server-side-development)中，你已经看到了如何修改我们现有应用的业务逻辑。这使得测试更加重要，因为自定义可能会破坏应用的功能。在本节中，我们将编写一个测试用例来验证更改图书状态的业务逻辑。

### 准备工作

我们将使用GitHub仓库中 `Chapter18/r0_initial_module` 目录下的 `my_library` 模块。

### 如何实现...

按照以下步骤为 `my_library` 模块添加Python测试用例：

1. 添加一个新文件 `tests/__init__.py`，内容如下：

   ```python
   from . import test_book_state
   ```

2. 添加 `tests/test_book_state.py` 文件，并添加测试用例，如下所示：

   ```python
   from odoo.tests.common import TransactionCase

   class TestBookState(TransactionCase):

       def setUp(self, *args, **kwargs):
           super(TestBookState, self).setUp(*args, **kwargs)
           self.test_book = self.env['library.book'].create({'name': 'Book 1'})

       def test_button_available(self):
           """Make available button"""
           self.test_book.make_available()
           self.assertEqual(self.test_book.state, 'available',
               'Book state should be changed to available')

       def test_button_lost(self):
           """Make lost button"""
           self.test_book.make_lost()
           self.assertEqual(self.test_book.state, 'lost',
               'Book state should be changed to lost')
   ```

3. 要运行测试用例，使用以下选项启动Odoo服务器：

   ```bash
   ./odoo-bin -c server.conf -i my_library --test-enable
   ```

现在，检查服务器日志。如果测试用例成功运行，你将看到以下日志：

```
... INFO test odoo.addons.my_library.tests.test_book_state: Starting TestBookState.test_button_available ...
... INFO test odoo.addons.my_library.tests.test_book_state: Starting TestBookState.test_button_lost ...
... INFO test odoo.modules.loading: Module my_library loaded in 0.79s (incl. 0.12s test), 179 queries (+10 test)
```

如果测试用例失败或出现错误，你将看到 `ERROR` 日志而不是 `INFO`。

### 运行原理...

在Odoo中，Python测试用例添加到模块的 `tests/` 目录中。Odoo会自动识别该目录并运行其中的测试。

> 📝**注：**你还需要在 `tests/__init__.py` 中列出你的测试用例文件。如果不这样做，该测试用例将不会被执行。

Odoo使用Python的 `unittest` 来处理Python测试用例。要了解更多关于Python `unittest` 的信息，请参阅 <https://docs.python.org/3.5/library/unittest.html>。Odoo提供了一些封装在 `unittest` 之上的辅助类。这些类简化了开发测试用例的过程。在我们的例子中，我们使用了TransactionCase。TransactionCase在不同的事务中运行每个测试用例方法。一旦测试用例方法成功运行，事务就会自动回滚。这意味着下一个测试用例不会包含前一个测试用例所做的任何修改。

以 `test_` 开头的类方法被视为测试用例。在我们的例子中，我们添加了两个测试用例。它们检查更改图书状态的方法。`self.assertEqual` 方法用于检查测试用例是否成功运行。我们在对图书记录执行操作后检查了图书状态。因此，如果开发者犯了错误且方法没有按预期更改状态，测试用例将失败。

> 📝**重要信息**：请注意，`setUp()` 方法会在每个测试用例运行时自动调用，因此在本节中，我们添加了两个测试用例，`setUp()` 将被调用两次。根据本节的代码，在测试期间将只有一条图书记录存在，因为使用TransactionCase时，每个测试用例结束后事务都会被回滚。

方法上的 `docstrings` 将打印在日志中。这对于检查特定测试用例的状态非常有帮助。

### 扩展知识...

测试套件提供了以下额外的测试工具类：

- **SingleTransactionCase**：通过此类生成的测试用例将在单个事务中运行所有用例，因此一个测试用例所做的更改将在第二个测试用例中可用。这样，事务随第一个测试方法开始，仅在最后一个测试用例结束时回滚。
- **SavepointCase**：这与SingleTransactionCase相同，但在这种情况下，测试方法在一个回滚的保存点内运行，而不是将所有测试方法放在单个事务中。这用于创建大型测试用例，通过只生成一次测试数据使其更快。在这里，我们使用 `setUpClass()` 方法来生成初始测试数据。

## 运行打标签的Python测试用例

当你使用 `--test-enabled` 选项运行Odoo服务器时，测试用例会在模块安装后立即运行。如果你想在所有模块安装完成后运行测试用例，或者只想运行某一个模块的测试用例，`tagged()` 装饰器就是答案。在本节中，我们将说明如何使用此装饰器来控制测试用例。

### 准备工作

对于本节，我们将使用上一节中的 `my_library` 模块。我们将修改测试用例的运行顺序。

### 如何实现...

按照以下步骤为Python测试用例添加标签：

1. 向测试类添加 `tagged()` 装饰器（如下所示），以便在所有模块安装完成后运行：

   ```python
   from odoo.tests.common import TransactionCase, tagged

   @tagged('-at_install', 'post_install')
   class TestBookState(TransactionCase):
       ...
   ```

2. 之后，像以前一样运行测试用例：

   ```bash
   ./odoo-bin -c server.conf -i my_library --test-enable
   ```

3. 现在检查服务器日志。这次你将看到我们的测试用例日志出现在以下日志之后，这意味着我们的测试用例是在所有模块安装完成后运行的：

   ```
   ... INFO book odoo.modules.loading: 9 modules loaded in 1.87s, 177 queries (+0 extra)
   ... INFO book odoo.modules.loading: Modules loaded.
   ... INFO book odoo.service.server: Starting post tests
   ... INFO book odoo.addons.my_library.tests.test_book_state: Starting TestBookState.test_button_available ...
   ... INFO book odoo.addons.my_library.tests.test_book_state: Starting TestBookState.test_button_lost ...
   ... INFO book odoo.service.server: 2 post-tests in 0.14s, 10 queries
   ```

在这些日志中，第一行显示九个模块已加载。第二行显示所有请求的模块及其依赖已成功安装，第三行显示它将开始运行标记为post_install的测试用例。

### 运行原理...

默认情况下，所有测试用例都被标记为 `standard`、`at_install` 和当前模块的技术名称（在我们的例子中，技术名称是 `my_library`）。因此，如果你不使用 `tagged()` 装饰器，你的测试用例将拥有这三个标签。

在我们的例子中，我们希望在所有模块安装完成后运行测试用例。为此，我们向TestBookState类添加了 `tagged()` 装饰器。默认情况下，测试用例具有at_install标签。由于此标签，你的测试用例将在模块安装后立即运行；它不会等待其他模块安装完成。我们不希望这样，因此要移除at_install标签，我们在tagged函数中添加了 `-at_install`。以 `-` 为前缀的标签将移除该标签。

通过在 `tagged()` 函数中添加 `-at_install`，我们阻止了模块安装后的测试用例执行。由于我们没有指定其他标签，测试用例将不会运行。

因此，我们添加了post_install标签。此标签指定测试用例需要在所有模块安装完成后运行。

如你所见，所有测试用例默认都标记有 `standard` 标签。Odoo将运行所有标记有 `standard` 标签的测试用例。如果你不想始终运行特定的测试用例，而只想在需要时运行，你需要通过在 `tagged()` 装饰器中添加 `-standard` 来移除 `standard` 标签，并添加一个自定义标签，如下所示：

```python
@tagged('-standard', 'my_custom_tag')
class TestClass(TransactionCase):
    ...
```

所有非标准的测试用例将不会在 `--test-enable` 选项下运行。要运行上述测试用例，你需要使用 `--test-tags` 选项，如下所示（注意这里不需要显式传递 `--test-enable` 选项）：

```bash
./odoo-bin -c server.conf -i my_library --test-tags=my_custom_tag
```

### 扩展知识...

在开发测试用例的过程中，仅运行单个模块的测试用例很重要。默认情况下，模块的技术名称作为标签添加，因此你可以将模块的技术名称与 `--test-tags` 选项一起使用。例如，如果你想运行 `my_library` 模块的测试用例，可以这样运行服务器：

```bash
./odoo-bin -c server.conf -i my_library --test-tags=my_library
```

上面给出的命令将运行 `my_library` 模块中的测试用例，但仍会根据at_install和post_install选项来决定运行顺序。

## 为客户端测试用例设置Headless Chrome

Odoo使用Headless Chrome来执行JavaScript测试用例和导览测试用例。Headless Chrome是一种无需完整UI即可运行Chrome的方式。这样我们可以在与终端用户相同的环境中运行JavaScript测试用例。在本节中，我们将安装Headless Chrome和其他包以运行JavaScript测试用例。

### 如何实现...

你需要安装Chrome才能启用JavaScript测试用例。在模块开发中，我们主要使用桌面操作系统。因此，如果你的系统上已安装Chrome浏览器，则无需单独安装。你可以使用桌面Chrome运行客户端测试用例。确保你的Chrome版本高于Chrome 59。Odoo还支持Chromium浏览器。

> 📝**注：**Headless Chrome客户端测试用例在macOS和Linux上运行良好，但Odoo不支持在Windows上运行Headless Chrome测试用例。

当你想在生产服务器或服务器操作系统上运行测试用例时，情况会略有不同。服务器操作系统没有GUI，因此你需要以不同的方式安装Chrome。如果你使用的是基于Debian的操作系统，可以使用以下命令安装Chromium：

```bash
apt-get install chromium-browser
```

> 📝**重要信息**：Ubuntu 18.04服务器版默认未启用 `universe` 仓库。因此，安装 `chromium-browser` 可能会显示安装候选项错误。要修复此错误，请使用以下命令启用 `universe` 仓库：`sudo add-apt-repository universe`。

Odoo还使用WebSockets进行JavaScript测试用例。为此，Odoo使用了 `websocket-client` Python库。要安装它，请使用以下命令：

```bash
pip3 install websocket-client
```

现在你的系统已准备好运行客户端测试用例。

### 运行原理...

Odoo使用Headless Chrome进行JavaScript测试用例。原因是它在后台运行测试用例，因此也可以在服务器操作系统上运行。Headless Chrome倾向于在后台运行Chrome浏览器，而不打开GUI浏览器。Odoo在后台打开一个Chrome标签页并开始在其中运行测试用例。它还使用jQuery的QUnit进行JavaScript测试用例。在接下来的几节中，我们将为自定义JavaScript微件创建QUnit测试用例。

对于测试用例，Odoo在单独的进程中打开Headless Chrome，因此为了了解在该进程中运行的测试用例的状态，Odoo服务器使用WebSockets。`websocket-client` Python库用于管理WebSockets以从Odoo服务器与Chrome进行通信。

## 添加客户端QUnit测试用例

在Odoo中构建新字段或视图非常简单。只需几行XML，就可以定义一个新视图。然而，在底层，它使用了大量的JavaScript。在客户端修改/添加新功能很复杂，可能会破坏一些东西。大多数客户端问题不容易被注意到，因为大多数错误仅在控制台中显示。因此，QUnit测试用例在Odoo中用于检查不同JavaScript组件的正确性。

### 准备工作

对于本节，我们将继续使用前一节中的 `my_library` 模块。我们将为 `int_color` 微件添加QUnit测试用例。

### 如何实现...

按照以下步骤为 `int_color` 微件添加JavaScript测试用例：

1. 添加 `/static/tests/colorpicker_tests.js` 文件，包含以下代码：

   ```javascript
   odoo.define('colorpicker_tests', function (require) {
       "use strict";

       var FormView = require('web.FormView');
       var testUtils = require('web.test_utils');

       QUnit.module('Color Picker Tests', {
           beforeEach: function () {
               this.data = {
                   book: {
                       fields: {
                           name: { string: "Name", type: "char" },
                           color: { string: "color", type: "integer"},
                       },
                       records: [
                           {id: 1, name: "Book 1", color: 1},
                           {id: 2, name: "Book 2", color: 3}
                       ]
                   }
               };
           }
       }, function () {
           // 在此处放置第2步内容
       });
   });
   ```

2. 添加颜色拾取器字段的QUnit测试用例，如下所示：

   ```javascript
   QUnit.only('int_color field test cases', async function (assert) {
       assert.expect(2);
       var form = await testUtils.createView({
           View: FormView,
           model: 'book',
           data: this.data,
           arch: '<form string="Books">' +
               '<group>' +
               '<field name="name"/>' +
               '<field name="color" widget="int_color"/>' +
               '</group>' +
               '</form>',
           res_id: 1,
       });
       await testUtils.form.clickEdit(form);
       assert.strictEqual(
           form.$('.o_int_colorpicker .o_color_pill').length,
           10,
           "colorpicker should have 10 pills"
       );
       await testUtils.dom.click(
           form.$('.o_int_colorpicker .o_color_pill:eq(5)')
       );
       assert.strictEqual(
           form.$('.o_int_colorpicker .o_color_5').hasClass('active'),
           true,
           "click on pill should make pill active"
       );
       form.destroy();
   });
   ```

3. 在 `/views/template.xml` 中添加以下代码以将其注册到测试套件中：

   ```xml
   ...
   <template id="qunit_suite" name="colorpicker test"
       inherit_id="web.qunit_suite">
       <xpath expr="." position="inside">
           <script type="text/javascript"
               src="/my_library/static/tests/colorpicker_tests.js" />
       </xpath>
   </template>
   ...
   ```

要运行此测试用例，在终端中使用以下命令启动服务器：

```bash
./odoo-bin -c server.conf -i my_library,web --test-enable
```

要检查测试是否成功运行，搜索以下日志：

```
... INFO test odoo.addons.web.tests.test_js.WebSuite: console log: "Color Picker Tests" passed 2 tests.
```

### 运行原理...

在Odoo中，JavaScript测试用例添加到 `/static/tests/` 目录中。在*第1步*中，我们添加了 `colorpicker_tests.js` 文件用于测试用例。在该文件中，我们导入了 `formView` 和 `test_utils` 引用。导入 `web.FormView` 是因为我们为表单视图创建了 `int_color` 微件，所以要测试该微件，我们需要表单视图。

`web.test_utils` 将提供我们构建JavaScript测试用例所需的测试工具。如果你不了解JavaScript导入的工作方式，请参阅[第十四章 CMS网站开发](/blog/odoo-14-cms-website-development)中*为网站扩展CSS和JavaScript*一节。

Odoo客户端测试用例基于QUnit框架构建，QUnit是jQuery的JavaScript单元测试框架。请参考 <https://qunitjs.com/> 了解更多信息。`beforeEach` 函数在运行测试用例之前调用，这有助于初始化测试数据。`beforeEach` 函数的引用由QUnit框架本身提供。

我们在 `beforeEach` 函数中初始化了一些数据。让我们看看这些数据是如何在测试用例中使用的。客户端测试用例运行在一个隔离（模拟）的环境中，不与数据库建立连接，因此对于这些测试用例，我们需要创建测试数据。在内部，Odoo创建模拟服务器来模仿**远程过程调用**（**RPC**）调用，并使用 `this.data` 属性作为数据库。因此，在 `beforeEach` 中，我们在 `this.data` 属性中初始化了测试数据。`this.data` 属性中的键被视为表，值包含有关字段和表行的信息。`fields` 键用于定义表字段，`records` 键用于表行。在我们的例子中，我们添加了一个 `book` 表，包含两个字段：`name(char)` 和 `color(integer)`。请注意，这里你可以使用任何Odoo字段，甚至关系字段；例如，`{string: "M2o Field", type: "many2one", relation: 'partner'}`。我们还使用 `records` 键添加了两条图书记录。

接下来，我们使用 `QUnit.test` 函数添加了测试用例。函数中的第一个参数是描述测试用例的字符串。第二个参数是你需要添加测试用例代码的函数。该函数由QUnit框架调用，并将assert工具作为参数传递。在我们的例子中，我们在 `assert.expect` 函数中传入了期望的测试用例数量。我们添加了两个测试用例，所以传入了 `2`。

我们想要在可编辑的表单视图中测试 `int_color` 微件，因此我们使用 `testUtils.createView` 创建了可编辑的表单视图。`createView` 函数接受不同的参数，如下所示：

- `View` 是你要创建的视图的引用。你可以为测试用例创建任何类型的视图；只需在此传递视图引用即可。
- `model` 是给定视图创建的模型名称。所有模型都列在 `this.data` 属性中。我们想为book模型创建视图，所以在我们的例子中，使用book作为模型。
- `data` 是我们将在视图中使用的记录。
- `arch` 是你要创建的视图的定义。因为我们想测试 `int_color` 微件，所以我们传递了带有该微件的视图定义。请注意，你只能使用在模型中定义的字段。
- `res_id` 是正在显示的记录的ID。此选项仅用于表单视图。在我们的例子中，表单视图将显示book 1记录的数据，因为我们将 `1` 作为 `res_id` 添加。

创建带有 `int_color` 微件的表单视图后，我们添加了两个测试用例。第一个用于检查UI上颜色块的数量，第二个测试用例用于检查点击后颜色块是否正确激活。我们使用了QUnit框架assert工具中的 `strictEqual` 函数。如果前两个参数匹配，`strictEqual` 函数将通过测试用例。如果不匹配，测试用例将失败。

### 扩展知识...

QUnit测试用例还有一些其他可用的assert函数，如 `assert.deepEqual`、`assert.ok` 和 `assert.notOk`。要了解更多关于QUnit的信息，请参阅其文档：<https://qunitjs.com/>。

## 添加导览测试用例

你现在已经了解了Python和JavaScript测试用例。这两者都在隔离的环境中工作，它们不会相互交互。要测试JavaScript和Python代码之间的集成，需要使用导览测试用例。

### 准备工作

对于本节，我们将继续使用前一节中的 `my_library` 模块。我们将添加一个导览测试用例来检查图书模型的流程。此外，请确保你已安装 `web_tour` 模块或已在清单文件中添加了 `web_tour` 模块依赖。

### 如何实现...

按照以下步骤为图书添加导览测试用例：

1. 添加 `/static/src/js/my_library_tour.js` 文件，然后添加导览，如下所示：

   ```javascript
   odoo.define('my_library.tour', function (require) {
       "use strict";

       var core = require('web.core');
       var tour = require('web_tour.tour');
       var _t = core._t;

       tour.register('library_tour', {
           url: "/web",
           test: true,
           rainbowManMessage: _t("Congrats, you have listed a book."),
           sequence: 5,
       }, [tour.stepUtils.showAppsMenuItem(),
           // 在此处放置第2步内容
       ]);
   });
   ```

2. 为测试导览添加步骤：

   ```javascript
   {
       trigger: '.o_app[data-menu-xmlid="my_library.library_base_menu"]',
       content: _t('Manage books and authors in <b>Library app</b>.'),
       position: 'right'
   }, {
       trigger: '.o_list_button_add',
       content: _t("Let's create new book."),
       position: 'bottom',
   }, {
       trigger: 'input[name="name"]',
       extra_trigger: '.o_form_editable',
       content: _t('Set the book title'),
       position: 'right',
       run: function (actions) {
           actions.text('Test Book');
       },
   }, {
       trigger: '.o_form_button_save',
       content: _t('Save this book record'),
       position: 'bottom',
   }
   ```

3. 在测试资源中添加 `my_library_tour.js` 文件：

   ```xml
   <template id="assets_tests" name="Library Assets Tests"
       inherit_id="web.assets_tests">
       <xpath expr="." position="inside">
           <script type="text/javascript"
               src="/my_library/static/tests/my_library_tour.js" />
       </xpath>
   </template>
   ```

4. 添加 `/tests/test_tour.py` 文件，通过HttpCase运行导览，如下所示：

   ```python
   from odoo.tests.common import HttpCase, tagged

   class TestBookUI(HttpCase):

       @tagged('post_install', '-at_install')
       def test_01_book_tour(self):
           """Books UI tour test case"""
           self.browser_js("/web",
               "odoo.__DEBUG__.services['web_tour.tour'].run('library_tour')",
               "odoo.__DEBUG__.services['web_tour.tour'].tours.library_tour.ready",
               login="admin")
   ```

要运行测试用例，使用以下选项启动Odoo服务器：

```bash
./odoo-bin -c server.conf -i my_library --test-enable
```

现在检查服务器日志。如果测试用例成功运行，你将看到以下日志：

```
... INFO test odoo.addons.my_library.tests.test_tour.TestBookUI: console log: Tour library_tour succeeded
```

### 运行原理...

要创建导览测试用例，你需要首先创建UI导览。如果你想了解更多关于UI导览的信息，请参阅[第十五章 网页客户端开发](/blog/odoo-14-web-client-development)中*通过引导提升用户上手体验*一节。

在*第1步*中，我们注册了一个名为 `library_tour` 的新导览。这个导览与我们在[第十五章 网页客户端开发](/blog/odoo-14-web-client-development)*通过引导提升用户上手体验*一节中创建的导览完全相同。在*第2步*中，我们添加了导览的步骤。

与入门导览相比，这里有两个主要变化。首先，我们在导览定义中添加了 `test=true` 参数；其次，我们添加了一个额外的属性 `run`。在 `run` 函数中，你需要编写执行通常由用户完成的操作的逻辑。例如，在导览的第四步中，我们要求用户输入图书标题。

为了自动化这一步骤，我们添加了一个 `run` 函数来设置标题字段的值。`run` 函数将action工具作为参数传递。这提供了一些执行基本操作的快捷方式。最重要的有：

- `actions.click(element)` 用于点击给定元素。
- `actions.dblclick(element)` 用于双击给定元素。
- `actions.tripleclick(element)` 用于三击给定元素。
- `actions.text(string)` 用于设置输入值。
- `actions.drag_and_drop(to, element)` 用于拖放元素。
- `actions.keydown(keyCodes, element)` 用于在元素上触发特定的键盘事件。
- `actions.auto()` 是默认操作。当你不在导览步骤中传递 `run` 函数时，将执行 `actions.auto()`。这通常会点击导览步骤的触发器元素。唯一的例外是input元素。如果触发器元素是 `input`，导览将在输入框中设置默认值 `Test`。这就是为什么我们不需要在所有步骤中都添加 `run` 函数。

或者，如果默认操作不够用，你可以手动执行整个操作。在下一个导览步骤中，我们想为颜色拾取器设置一个值。请注意，我们使用了手动操作，因为默认值在这里不起作用。因此，我们添加了带有基本jQuery代码的 `run` 方法来点击颜色拾取器的第三个色块。在这里，你可以通过 `this.$anchor` 属性找到触发器元素。

默认情况下，注册的导览会显示给终端用户以改善入门体验。要将它们作为测试用例运行，你需要在Headless Chrome中运行它们。为此，你需要使用HttpCase Python测试用例。它提供了 `browser_js` 方法，该方法打开URL并执行作为第二个参数传递的命令。你可以像这样手动运行导览：

```javascript
odoo.__DEBUG__.services['web_tour.tour'].run('library_tour')
```

在我们的例子中，我们在 `browser_js` 方法中传递了导览的名称作为参数。下一个参数用于在执行第一个命令之前等待给定对象就绪。`browser_js()` 方法中的最后一个参数是用户名。这个用户名将用于创建新的测试环境，所有测试操作将代表该用户执行。

## 通过UI运行客户端测试用例

Odoo提供了一种从UI运行客户端测试用例的方式。通过从UI运行测试用例，你将能够看到测试用例的每个步骤的执行过程。这样，你可以验证UI测试用例是否完全按照我们的期望工作。

### 如何实现...

你可以从UI运行QUnit测试用例和导览测试用例。由于Python测试用例在服务端运行，无法从UI运行。要查看从UI运行测试用例的选项，你需要启用开发者模式。

#### 从UI运行QUnit测试用例

点击小虫图标打开下拉菜单。点击 **Run JS Tests** 选项：

图18.1 – 运行测试用例的选项

这将打开QUnit套件并开始逐一运行测试用例。默认情况下，它只显示失败的测试用例。要显示所有通过的测试用例，取消勾选 **Hide passed tests** 复选框：

图18.2 – QUnit测试用例的结果

#### 从UI运行导览

点击小虫图标打开下拉菜单，然后点击 **Start Tour**：

图18.3 – 运行导览测试用例的选项

这将打开一个包含已注册导览列表的对话框。点击侧边的播放按钮来运行导览：

图18.4 – 导览测试用例列表

测试导览只有在你启用了测试资源模式时才会显示在列表中。如果你在列表中找不到 `library_tour` 导览，请确保你已激活测试资源模式。

### 运行原理...

QUnit的UI由QUnit框架本身提供。在这里，你可以按模块筛选测试用例。你甚至可以只运行某一个模块的测试用例。通过UI，你可以看到每个测试用例的进度，并可以深入查看测试用例的每个步骤。在内部，Odoo只是在Headless Chrome中打开相同的URL。

点击 **Run tours** 选项将显示可用导览的列表。通过点击列表中的播放按钮，你可以运行导览。请注意，当导览通过命令行选项运行时，它在回滚的事务中运行，因此通过导览所做的更改在导览成功后会被回滚。然而，当导览从UI运行时，它的工作方式就像用户在操作一样，这意味着从导览所做的更改不会被回滚并会保留，所以请谨慎使用此选项。

## 调试客户端测试用例

开发复杂的客户端测试用例可能令人头疼。在本节中，你将学习如何在Odoo中调试客户端测试用例。我们不会运行所有的测试用例，而是只运行一个。此外，我们将显示测试用例的UI。

### 准备工作

对于本节，我们将继续使用前一节中的 `my_library` 模块。

### 如何实现...

按照以下步骤以调试模式运行测试用例：

1. 打开 `/static/tests/colorpicker_tests.js` 文件，将 `QUnit.test` 替换为 `QUnit.only`，如下所示：

   ```javascript
   ...
   QUnit.only('int_color field test cases', function (assert) {
   ...
   ```

2. 在 `createView` 函数中添加 `debug` 参数，如下所示：

   ```javascript
   var form = testUtils.createView({
       View: FormView,
       model: 'book',
       data: this.data,
       arch: '<form string="Books">' +
           '<group>' +
           '<field name="name"/>' +
           '<field name="color" widget="int_color"/>' +
           '</group>' +
           '</form>',
       res_id: 1,
       debug: true
   });
   ```

打开开发者模式并点击顶部菜单栏上的小虫图标打开下拉菜单，然后点击 **Run JS Tests**。这将打开QUnit套件：

图18.5 – 运行测试用例的选项

这将只运行一个测试用例，即我们的颜色拾取器测试用例。

### 运行原理...

在*第1步*中，我们将 `QUnit.test` 替换为 `QUnit.only`。这将只运行此测试用例。在开发测试用例期间，这可以节省时间。请注意，使用 `QUnit.only` 将阻止测试用例通过命令行选项运行。这只能用于调试或测试，并且只有在从UI打开测试用例时才能工作，因此在开发完成后不要忘记将其替换回 `QUnit.test`。

在我们的QUnit测试用例示例中，我们创建了表单视图来测试 `int_color` 微件。如果你从UI运行QUnit测试用例，你会发现你无法在UI中看到创建的表单视图。从QUnit套件的UI中，你只能看到日志。这使得开发QUnit测试用例非常困难。为了解决这个问题，在 `createView` 函数中使用了 `debug` 参数。在*第2步*中，我们在 `createView` 函数中添加了 `debug: true`。这将在浏览器中显示测试表单视图。在这里，你将能够通过浏览器调试器定位**文档对象模型**（**DOM**）元素。

> ⚠️**警告**：在测试用例的末尾，我们通过 `destroy()` 方法销毁了视图。如果你销毁了视图，那么你将无法在UI中看到表单视图，所以为了在浏览器中看到它，请在开发期间移除那一行。这将帮助你调试测试用例。

以调试模式运行QUnit测试用例可以帮助你非常轻松和快速地开发测试用例。

## 为失败的测试用例生成视频/截图

Odoo使用Headless Chrome。这开辟了新的可能性。从Odoo 12开始，你可以录制失败测试用例的视频，或者也可以为失败的测试用例截图。

### 如何实现...

为测试用例录制视频需要 `ffmpeg` 包。

1. 要安装它，你需要在终端中执行以下命令（注意此命令仅在基于Debian的操作系统上有效）：

   ```bash
   apt-get install ffmpeg
   ```

2. 要生成视频或截图，你需要提供一个目录位置来存储视频或截图。

3. 如果你想生成测试用例的录屏（视频），使用 `--screencasts` 命令，如下所示：

   ```bash
   ./odoo-bin -c server.conf -i my_library --test-enable --screencasts=/home/pga/odoo_test/
   ```

4. 如果你想生成测试用例的截图，使用 `--screenshots` 命令，如下所示：

   ```bash
   ./odoo-bin -c server.conf -i my_library --test-enable --screenshots=/home/pga/odoo_test/
   ```

### 运行原理...

为了生成失败测试用例的截图/录屏，你需要在运行服务器时提供保存视频或图片文件的路径。当你运行测试用例时，如果测试用例失败，Odoo将在给定目录中保存失败测试用例的截图/视频。

要生成测试用例的视频，Odoo使用 `ffmpeg` 包。如果你没有在服务器上安装此包，则只会保存失败测试用例的截图。安装该包后，你将能够看到任何失败测试用例的mp4文件。

> 📝**注：**为测试用例生成视频可能会消耗更多的磁盘空间，因此请谨慎使用此选项，仅在确实必要时使用。

请记住，截图和视频仅针对失败的测试用例生成，因此如果你想测试它们，你需要编写一个会失败的测试用例。

## 填充随机测试数据

到目前为止，我们已经看到了用于检测业务逻辑中错误或bug的测试用例。然而，有时我们需要用大量数据来测试我们的开发。生成大量数据可能是一项繁琐的工作。Odoo提供了一组工具来帮助你为模型生成大量随机数据。在本节中，我们将使用 `populate` 命令为 `library.book` 模型生成测试数据。

### 准备工作

对于本节，我们将继续使用前一节中的 `my_library` 模块。我们将添加 `_populate_factories` 方法，用于生成测试数据。

### 如何实现...

按照以下步骤为 `library.book` 模型生成数据：

1. 在 `my_library` 模块中添加一个 `populate` 文件夹。同时添加一个 `__init__.py` 文件，内容如下：

   ```python
   from . import library_data
   ```

2. 添加 `my_library/populate/library_data.py` 文件并添加以下代码来生成图书数据：

   ```python
   from odoo import models
   from odoo.tools import populate

   class BookData(models.Model):
       _inherit = 'library.book'
       _populate_sizes = {'small': 10, 'medium': 100, 'large': 500}

       def _populate_factories(self):
           return [
               ('name', populate.constant('Book no {counter}')),
           ]
   ```

3. 运行以下命令来生成图书数据：

   ```bash
   ./odoo-bin populate --models=library.book --size=medium -c server.conf -i my_library
   ```

这将为图书生成100条数据。生成数据后，进程将终止。要查看图书数据，不带 `populate` 参数运行命令即可。

### 运行原理...

在*第1步*中，我们在 `my_library` 模块中添加了populate文件夹。该文件夹包含用于填充测试数据的代码。

在*第2步*中，我们添加了填充图书数据的代码。要生成随机数据，使用了 `_populate_factories` 方法。`_populate_factories` 方法返回模型字段的工厂，用于生成随机数据。`library.book` 模型有必填的 `name` 字段，所以在我们的例子中，我们返回了 `name` 字段的生成器。此生成器将用于在数据生成过程中生成随机的图书记录数据。我们为name字段使用了 `populate.constant` 生成器；当我们在数据生成期间迭代时，它将生成不同的名称。

就像 `populate.constant` 一样，Odoo提供了其他几种用于填充数据的生成器；以下是这些生成器的列表：

- `populate.randomize(list)` 将从给定列表中返回一个随机元素。
- `populate.cartesian(list)` 与 `randomize()` 类似，但它会尝试包含列表中的所有值。
- `populate.iterate(list)` 将遍历给定列表，一旦所有元素都被遍历完，它将基于 `randomize` 返回随机元素。
- `populate.constant(str)` 用于生成格式化字符串。你还可以传递 `formatter` 参数来格式化值。默认情况下，格式化器是字符串格式化函数。
- `populate.compute(function)` 用于当你想根据自定义函数计算值时使用。
- `populate.randint(a, b)` 用于生成 `a` 和 `b` 参数之间的随机数。

这些生成器可用于生成你所选择的测试数据。

另一个重要的属性是 `_populate_sizes`。它用于根据 `--size` 参数定义你想要生成的记录数量。它的值始终取决于业务对象。

在*第3步*中，我们为图书模型生成了数据。要填充测试数据，你需要使用 `--size` 和 `--model` 参数。在内部，Odoo使用 `_populate` 方法来生成随机记录。`_populate` 方法本身使用 `_populate_factories` 方法来获取记录的随机数据。`_populate` 方法将为 `--model` 参数中给定的模型生成数据，测试数据的数量将基于模型的 `_populate_sizes` 属性。根据我们的例子，如果我们使用 `--size=medium`，将生成100条图书数据。

> 📝**注：**如果你多次运行 `populate` 命令，数据也会被多次生成。谨慎使用这一点很重要：如果你在生产数据库中运行该命令，它将在生产数据库中生成测试数据。这是你应该避免的。

### 扩展知识...

有时，你还想生成关联数据。例如，在生成图书的同时，你可能还想创建作者或借阅记录。要管理此类记录，你可以使用 `_populate_dependencies` 属性：

```python
class BookData(models.Model):
    _inherit = 'library.book'
    _populate_sizes = {'small': 10, 'medium': 100, 'large': 500}
    _populate_dependencies = ['res.users', 'res.company']
    ...
```

这将在填充当前模型之前先填充依赖项的数据。完成后，你可以通过 `populated_models` 注册表访问已填充的数据：

```python
company_ids = self.env.registry.populated_models['res.company']
```

上面给出的代码将为你提供在为当前模型生成测试数据之前已填充的公司列表。
:::
