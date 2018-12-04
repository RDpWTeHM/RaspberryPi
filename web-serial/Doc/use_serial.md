# Use Serial

  --

## *Overview*

[TOC]

## Contents

  ```
README
    Overview
    Contents
    TODO
    Note
    Change Log(2018)
        --
        
  ```



## TODO



## Note



## Change Log(2018)

### Dec/03

#### select Serial?/COM?

##### basic serialcom-UI

![basic_web_serialcom-UI](res/basic_web_serialcom-UI.png)

##### Template Serial/COM select

```html
[...]
<body>
	<h1>Serial/COM</h1>

	<form action="" method="POST">
		<div>
			<label>Serial/COM:</label>
			<select>
				<option>ttyS0</option>
				<option>ttyAMA0</option>
				<option>ttyUSB0</option>
			</select>

			<label>Baud:</label>
			[...]
```

​ ​ :point_up_2: 这是 hard-code for now.



修改 HTML 使用 django 模板系统

```html
[...]
<body>
	<h1>Serial/COM</h1>

	<form action="" method="POST">
		<div>
			<label>Serial/COM:</label>
			<select>
				<option>Select one Device</option>
			{% for device in serial.devices	%}
				<option>{{ device }}</option>
			{% endfor	%}
			</select>

			<label>Baud:</label>
[...]
```

需要传递一个 serial 实例，这个 实例的类中有 `.devices` attribute, 后面的 HTML 模板中还会使用这个实例的其它 attribute 对应 serial/COM 的 configuration.

在 views.py load HTML 处的传递该实例代码：

```python
[...]
from .serial.josser import SerialCOM

def index(request):
    serial = SerialCOM()
    serial.devices = ["ttyS0", "ttyAMA0", "ttyUSB0", ]
    return render(request, 'serialcom/index.html',
                  {'serial': serial}, )
```

`SerialCOM` 类在 `serial/josser.py` 中定义

```python
#### filename: josser.py
class SerialCOM():
    devices = []

    def __init__(self):
        pass

```

暂时不需要太多内容。

##### Serial/COM select by read device

使用 `@classmethod` 直接调用类方法来返回类本身；在类方法中，读取 device 信息。

使用：

```python
--- a/web-serial/source/serialcom/views.py
+++ b/web-serial/source/serialcom/views.py
@@ -6,7 +6,6 @@ from .serial.josser import SerialCOM
 
 
 def index(request):
-    serial = SerialCOM()
-    serial.devices = ["ttyS0", "ttyAMA0", "ttyUSB0", ]
+    serial = SerialCOM.init()
     return render(request, 'serialcom/index.html',
                   {'serial': serial}, )

```

使用 `@classmethod` 实现的 init 函数：

```python
class SerialCOM():
    devices = []
    [...]

    @classmethod
    def init(cls):
        # cls.devices = ["ttyS0", "ttyAMA0", "ttyUSB0", ]
        portList = list(serial.tools.list_ports.comports())
        serial_name_set = set()
        for i in range(len(portList)):
            portList_coder = list(portList[i])
            serial_name_set.add(portList_coder[0])

        cls.devices = [_serialname for _serialname in serial_name_set]

        return cls()
```

这样刷新浏览器获 select 中得到的是真实的设备信息。



### Dec/04

#### handler POST

为了使浏览器载入 HTML 后 POST 带有数据，需要在 form 中指定要 POST 的字段的 id/name:

```html
[...]
	<h1>Serial/COM</h1>

	<form action="" method="POST">
		<div>
			<label>Serial/COM:</label>
			<select name="device_select" id="device_select">
				<option>Select one Device</option>
			{% for device in serial.devices	%}
				<option>{{ device }}</option>
			{% endfor	%}
			</select>

			<label>Baud:</label>
			<input type="text" name="baud" id="baud"
			       value="9600"/>
			<br/>

			<input type="checkbox" name="advance"
			       value="advance">Advance
			<input type="submit" name="connect"
			       id="connect" value="Connect"/>
		</div>
		{% csrf_token %}
	</form>
```

django server 接收处理 POST：

```python 
def index(request):
    if request.method == 'POST':
        if __debug__:
            print(request.POST['baud'], file=sys.stderr)
            print(request.POST['device_select'], file=sys.stderr)
        return HttpResponse("POST OK")
    elif request.method == 'GET':
        serial = SerialCOM.init()
        return render(request, 'serialcom/index.html',
                      {'serial': serial}, )
    else:
        pass  # not support.
```

可以点击浏览器的 ”Connect“ 按钮，看 server 的 terminal 上是否有 POST 过来的 debug 数据输出。

预期浏览器会变为”POST OK“页面。

