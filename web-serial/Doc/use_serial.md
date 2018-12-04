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

##### Serial/COM select

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

