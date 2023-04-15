import time
import requests
from login import *


token = many_token()


def add_assert(token, num):
    add_tuopu_url = f"{host}/topology/personal/save"
    # add_tuopu_header = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}', "User-Agent": f'{ua.chrome}'}
    add_tuopu_header = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}', "User-Agent": ua1}
    add_tuopu_body = {
  "topoData": {
    "version": "2.0",
    "datas": [
      {
        "_className": "Q.Node",
        "json": {
          "name": "大屏",
          "parent": {
            "_ref": 201
          },
          "styles": {
            "label.color": "#FFF"
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -270,
              "y": -310,
              "rotate": 0
            }
          },
          "size": {
            "width": 68.95125294193048,
            "height": 39.50720438834936
          },
          "image": "/static/data/topo/模拟显示屏.png"
        },
        "_refId": "200"
      },
      {
        "_className": "Q.Group",
        "json": {
          "zIndex": -1,
          "name": "中央控制室",
          "styles": {
            "label.font.size": 26,
            "label.color": "#FFF"
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -579.0584124230315,
              "y": -299.0626147556238,
              "rotate": 0
            }
          },
          "image": "Q-group",
          "minSize": {
            "x": -38.66848295679142,
            "width": 402.96224694232296,
            "y": -54.08330405625014,
            "height": 331.24860253351056
          }
        },
        "_refId": "201"
      },
      {
        "_className": "Q.Group",
        "json": {
          "name": "运行图编辑室",
          "styles": {
            "label.font.size": 26,
            "label.color": "#FFF"
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -193.1293230038226,
              "y": -305.89888183667733,
              "rotate": 0
            }
          },
          "image": "Q-group",
          "minSize": {
            "x": 0,
            "width": 217.44332151098274,
            "y": -46.07994219017638,
            "height": 327.941652426838
          }
        },
        "_refId": "204"
      },
      {
        "_className": "Q.Group",
        "json": {
          "zIndex": -1,
          "name": "信号设备室-网管室",
          "styles": {
            "label.font.size": 26,
            "label.color": "#FFF"
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 86.531996289034,
              "y": -351.5817505853723,
              "rotate": 0
            }
          },
          "image": "Q-group",
          "minSize": {
            "x": 0,
            "y": 0,
            "width": 925.4122862332271,
            "height": 326.7664833973831
          }
        },
        "_refId": "206"
      },
      {
        "_className": "Q.Group",
        "json": {
          "zIndex": -1,
          "name": "安全管理中心",
          "parent": {
            "_ref": 206
          },
          "styles": {
            "label.font.size": 22,
            "label.color": "#FFF"
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 507.03999457402017,
              "y": -182.68444125158845,
              "rotate": 0
            }
          },
          "image": "Q-group",
          "minSize": {
            "x": 0,
            "width": 413.42755000658804,
            "y": -14.178443750823476,
            "height": 137.21841484591175
          }
        },
        "_refId": "208"
      },
      {
        "_className": "Q.Group",
        "json": {
          "zIndex": -1,
          "name": "设备集中站",
          "styles": {
            "label.font.size": 26,
            "label.color": "#FFF"
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -578.6608125955765,
              "y": 290.2539019054209,
              "rotate": 0
            }
          },
          "image": "Q-group",
          "minSize": {
            "x": -33.56706133543628,
            "width": 580.6394444894403,
            "y": -16.111867898663036,
            "height": 281.62469267583816
          }
        },
        "_refId": "210"
      },
      {
        "_className": "Q.Group",
        "json": {
          "zIndex": -1,
          "name": "车辆段-停车场",
          "styles": {
            "label.font.size": 26,
            "label.color": "#FFF"
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 8.109304468263531,
              "y": 272.43691770238604,
              "rotate": 0
            }
          },
          "image": "Q-group",
          "minSize": {
            "x": 0,
            "width": 1006.8550069812052,
            "y": 0,
            "height": 280.15997741232337
          }
        },
        "_refId": "212"
      },
      {
        "_className": "Q.Node",
        "json": {
          "name": "调度长\n工作站",
          "parent": {
            "_ref": 201
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "调度长\n工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -480,
              "y": -310,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "214"
      },
      {
        "_className": "Q.Node",
        "json": {
          "name": "大屏接口\n计算机",
          "parent": {
            "_ref": 201
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "大屏接口\n计算机",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -360,
              "y": -310,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "216"
      },
      {
        "_className": "Q.Node",
        "json": {
          "name": "行车调度员\n工作站",
          "parent": {
            "_ref": 201
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "行车调度员\n工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -540,
              "y": -140,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "218"
      },
      {
        "_className": "Q.Node",
        "json": {
          "name": "运行图显示\n工作站",
          "parent": {
            "_ref": 201
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "运行图显示\n工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -410,
              "y": -130,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "220"
      },
      {
        "_className": "Q.Node",
        "json": {
          "name": "A3彩色激光\n打印机",
          "parent": {
            "_ref": 201
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "A3彩色激光\n打印机",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -290,
              "y": -130,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "222"
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 200
          },
          "to": {
            "_ref": 216
          },
          "edgeType": "orthogonal.V.H"
        }
      },
      {
        "_className": "Q.Node",
        "json": {
          "name": "时刻表-运行图\n编辑工作站",
          "parent": {
            "_ref": 204
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "时刻表-运行图\n编辑工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -130,
              "y": -310,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "226"
      },
      {
        "_className": "Q.Node",
        "json": {
          "name": "绘图仪",
          "parent": {
            "_ref": 204
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "绘图仪",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -50,
              "y": -120,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "228"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "应用服务器",
          "parent": {
            "_ref": 206
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "应用服务器",
            "specifyDeviceType": 'true',
            "typeIds": [
              "301001",
              "301002",
              "301003",
              "301004",
              "301005",
              "301006",
              "301007",
              "301008",
              "301009",
              "301099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 130,
              "y": -300,
              "rotate": 0
            }
          },
          "size": {
            "width": 33,
            "height": 42
          },
          "image": "/static/data/basic/servernew1.svg"
        },
        "_refId": "230"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "数据库服务器",
          "parent": {
            "_ref": 206
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "数据库服务器",
            "specifyDeviceType": 'true',
            "typeIds": [
              "301001",
              "301002",
              "301003",
              "301004",
              "301005",
              "301006",
              "301007",
              "301008",
              "301009",
              "301099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 230,
              "y": -300,
              "rotate": 0
            }
          },
          "size": {
            "width": 33,
            "height": 42
          },
          "image": "/static/data/basic/servernew1.svg"
        },
        "_refId": "232"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "网管服务器",
          "parent": {
            "_ref": 206
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "网管服务器",
            "specifyDeviceType": 'true',
            "typeIds": [
              "301001",
              "301002",
              "301003",
              "301004",
              "301005",
              "301006",
              "301007",
              "301008",
              "301009",
              "301099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 360,
              "y": -300,
              "rotate": 0
            }
          },
          "size": {
            "width": 33,
            "height": 42
          },
          "image": "/static/data/basic/servernew1.svg"
        },
        "_refId": "234"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "NMS工作站",
          "parent": {
            "_ref": 206
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "NMS工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 480,
              "y": -300,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "236"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "ATS维护工作站",
          "parent": {
            "_ref": 206
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "ATS维护工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 600,
              "y": -300,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "238"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "MSS工作站",
          "parent": {
            "_ref": 206
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "MSS工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 740,
              "y": -300,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "240"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "轨旁通信服务器",
          "parent": {
            "_ref": 206
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "轨旁通信服务器",
            "specifyDeviceType": 'true',
            "typeIds": [
              "301001",
              "301002",
              "301003",
              "301004",
              "301005",
              "301006",
              "301007",
              "301008",
              "301009",
              "301099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 180,
              "y": -120,
              "rotate": 0
            }
          },
          "size": {
            "width": 33,
            "height": 42
          },
          "image": "/static/data/basic/servernew1.svg"
        },
        "_refId": "242"
      },
      {
        "_className": "Q.Node",
        "json": {
          "name": "通信前置机",
          "parent": {
            "_ref": 206
          },
          "styles": {
            "label.color": "#FFF"
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 290,
              "y": -110,
              "rotate": 0
            }
          },
          "size": {
            "width": 44.311961879516566,
            "height": 15.338756035217273
          },
          "image": "/static/data/topo/前置机.png"
        },
        "_refId": "244"
      },
      {
        "_className": "Q.Node",
        "json": {
          "name": "监测审计平台",
          "parent": {
            "_ref": 206
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "监测审计平台",
            "specifyDeviceType": 'true',
            "typeIds": [
              "202007"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 430,
              "y": -110,
              "rotate": 0
            }
          },
          "size": {
            "width": 50,
            "height": 36
          },
          "image": "/static/data/basic/sma1.svg"
        },
        "_refId": "246"
      },
      {
        "_className": "Q.Node",
        "json": {
          "name": "交换机",
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "交换机",
            "specifyDeviceType": 'true',
            "typeIds": [
              "201002"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 60,
              "y": -210,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 34
          },
          "image": "/static/data/basic/switch1.svg"
        },
        "_refId": "248"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "工业防火墙",
          "parent": {
            "_ref": 208
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "工业防火墙",
            "specifyDeviceType": 'true',
            "typeIds": [
              "202003",
              "202004"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 720,
              "y": -170,
              "rotate": 0
            }
          },
          "size": {
            "width": 51,
            "height": 36
          },
          "image": "/static/data/basic/firewall1.svg"
        },
        "_refId": "250"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "态势感知平台",
          "parent": {
            "_ref": 208
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "态势感知平台",
            "specifyDeviceType": 'true',
            "typeIds": [
              "202013"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 550,
              "y": -110,
              "rotate": 0
            }
          },
          "size": {
            "width": 50,
            "height": 36
          },
          "image": "/static/data/basic/soc1.svg"
        },
        "_refId": "252"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "统一安全管理平台",
          "parent": {
            "_ref": 208
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "统一安全管理平台",
            "specifyDeviceType": 'true',
            "typeIds": [
              "202011"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 670,
              "y": -110,
              "rotate": 0
            }
          },
          "size": {
            "width": 50,
            "height": 36
          },
          "image": "/static/data/basic/usm1.svg"
        },
        "_refId": "254"
      },
      {
        "_className": "Q.Node",
        "json": {
          "name": "安全运维管理系统",
          "parent": {
            "_ref": 208
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "安全运维管理系统",
            "specifyDeviceType": 'true',
            "typeIds": [
              "202008"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 800,
              "y": -110,
              "rotate": 0
            }
          },
          "size": {
            "width": 50,
            "height": 36
          },
          "image": "/static/data/basic/soms1.svg"
        },
        "_refId": "256"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "漏洞扫描",
          "parent": {
            "_ref": 208
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "漏洞扫描",
            "specifyDeviceType": 'true',
            "typeIds": [
              "202020"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 920,
              "y": -110,
              "rotate": 0
            }
          },
          "size": {
            "width": 50,
            "height": 36
          },
          "image": "/static/data/basic/vulnerability_scan1.svg"
        },
        "_refId": "258"
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 252
          },
          "to": {
            "_ref": 250
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 254
          },
          "to": {
            "_ref": 250
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 256
          },
          "to": {
            "_ref": 250
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 258
          },
          "to": {
            "_ref": 250
          }
        }
      },
      {
        "_className": "Q.ShapeNode",
        "json": {
          "busLayout": 'true',
          "name": "总线",
          "parent": {
            "_ref": 206
          },
          "styles": {
            "arrow.to": 'false',
            "shape.stroke": 10
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 310,
              "y": -210,
              "rotate": 0
            }
          },
          "path": {
            "_className": "Q.Path",
            "json": [
              {
                "type": "m",
                "points": [
                  485.41841522294754,
                  0
                ]
              },
              {
                "type": "l",
                "points": [
                  -200,
                  0
                ]
              }
            ]
          }
        },
        "_refId": "268"
      },
      {
        "_className": "Q.Node",
        "json": {
          "name": "工业防火墙",
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "工业防火墙",
            "specifyDeviceType": 'true',
            "typeIds": [
              "202003",
              "202004"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 60,
              "y": -80,
              "rotate": 0
            }
          },
          "size": {
            "width": 51,
            "height": 36
          },
          "image": "/static/data/basic/firewall1.svg"
        },
        "_refId": "272"
      },
      {
        "_className": "Q.ShapeNode",
        "json": {
          "zIndex": 1,
          "name": "环网",
          "styles": {
            "arrow.to": 'false',
            "shape.stroke": 2.5,
            "layout.by.path": 'false',
            "shape.fill.color": "",
            "shape.stroke.style": "#2898E0"
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 183.1814133582992,
              "y": 120,
              "rotate": 0
            }
          },
          "path": {
            "_className": "Q.Path",
            "json": [
              {
                "type": "m",
                "points": [
                  -446.4132111113606,
                  -114.55550127804605
                ]
              },
              {
                "type": "l",
                "points": [
                  446.4132111113606,
                  -114.55550127804605
                ]
              },
              {
                "type": "c",
                "points": [
                  892.8264222227212,
                  -114.55550127804605,
                  892.8264222227212,
                  114.55550127804605,
                  446.4132111113606,
                  114.55550127804605
                ]
              },
              {
                "type": "l",
                "points": [
                  -446.4132111113606,
                  114.55550127804605
                ]
              },
              {
                "type": "c",
                "points": [
                  -892.8264222227212,
                  114.55550127804605,
                  -892.8264222227212,
                  -114.55550127804605,
                  -446.4132111113606,
                  -114.55550127804605
                ]
              },
              {
                "type": "z",
                "points": [
                  -446.4132111113606,
                  -114.55550127804605
                ]
              }
            ]
          }
        },
        "_refId": "274"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": 1,
          "name": "交换机",
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "交换机",
            "specifyDeviceType": 'true',
            "typeIds": [
              "201002"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 60,
              "y": 0,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 34
          },
          "image": "/static/data/basic/switch1.svg"
        },
        "_refId": "282"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": 1,
          "name": "交换机",
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "交换机",
            "specifyDeviceType": 'true',
            "typeIds": [
              "201002"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -550,
              "y": 180,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 34
          },
          "image": "/static/data/basic/switch1.svg"
        },
        "_refId": "284"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": 1,
          "name": "交换机",
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "交换机",
            "specifyDeviceType": 'true',
            "typeIds": [
              "201002"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 910,
              "y": 180,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 34
          },
          "image": "/static/data/basic/switch1.svg"
        },
        "_refId": "286"
      },
      {
        "_className": "Q.Edge",
        "json": {
          "styles": {
            "edge.to.offset": {
              "x": -111.7722465208748,
              "y": -111.7722465208748
            }
          },
          "from": {
            "_ref": 282
          },
          "to": {
            "_ref": 274
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "styles": {
            "edge.to.offset": {
              "x": 779.8784611832046,
              "y": 37.79333351441487
            }
          },
          "from": {
            "_ref": 286
          },
          "to": {
            "_ref": 274
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "styles": {
            "edge.to.offset": {
              "x": -791.7200795228629,
              "y": 27.94306163021881
            }
          },
          "from": {
            "_ref": 284
          },
          "to": {
            "_ref": 274
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 272
          },
          "to": {
            "_ref": 282
          },
          "edgeType": "orthogonal.V.H"
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 248
          },
          "to": {
            "_ref": 272
          },
          "edgeType": "orthogonal.V.H"
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 248
          },
          "to": {
            "_ref": 268
          },
          "edgeType": "orthogonal.V.H"
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 268
          },
          "to": {
            "_ref": 230
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 268
          },
          "to": {
            "_ref": 232
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 268
          },
          "to": {
            "_ref": 234
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 268
          },
          "to": {
            "_ref": 236
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 268
          },
          "to": {
            "_ref": 238
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 268
          },
          "to": {
            "_ref": 240
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 268
          },
          "to": {
            "_ref": 242
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 268
          },
          "to": {
            "_ref": 244
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 268
          },
          "to": {
            "_ref": 246
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 268
          },
          "to": {
            "_ref": 250
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 226
          },
          "to": {
            "_ref": 248
          },
          "edgeType": "orthogonal.V.H"
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 228
          },
          "to": {
            "_ref": 248
          },
          "edgeType": "orthogonal.V.H"
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 222
          },
          "to": {
            "_ref": 248
          },
          "edgeType": "orthogonal.V.H"
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 220
          },
          "to": {
            "_ref": 248
          },
          "edgeType": "orthogonal.V.H"
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 218
          },
          "to": {
            "_ref": 248
          },
          "edgeType": "orthogonal.V.H"
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 216
          },
          "to": {
            "_ref": 248
          },
          "edgeType": "orthogonal.V.H"
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 214
          },
          "to": {
            "_ref": 248
          },
          "edgeType": "orthogonal.V.H"
        }
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "ATS监视\n工作站",
          "parent": {
            "_ref": 210
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "ATS监视\n工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -490,
              "y": 460,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "334"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "MSS维护\n工作站",
          "parent": {
            "_ref": 210
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "MSS维护\n工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -360,
              "y": 460,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "336"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "ATP维护\n工作站",
          "parent": {
            "_ref": 210
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "ATP维护\n工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -230,
              "y": 460,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "338"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "现地控制\n工作站",
          "parent": {
            "_ref": 210
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "现地控制\n工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -90,
              "y": 460,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "340"
      },
      {
        "_className": "Q.ShapeNode",
        "json": {
          "busLayout": 'true',
          "name": "总线",
          "parent": {
            "_ref": 210
          },
          "styles": {
            "arrow.to": 'false',
            "shape.stroke": 10
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -370,
              "y": 380,
              "rotate": 0
            }
          },
          "path": {
            "_className": "Q.Path",
            "json": [
              {
                "type": "m",
                "points": [
                  317.09473445044046,
                  -1.330621982391336
                ]
              },
              {
                "type": "l",
                "points": [
                  -200,
                  0
                ]
              }
            ]
          }
        },
        "_refId": "342"
      },
      {
        "_className": "Q.Node",
        "json": {
          "name": "监测审计平台",
          "parent": {
            "_ref": 210
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "监测审计平台",
            "specifyDeviceType": 'true',
            "typeIds": [
              "202007"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": -420,
              "y": 310,
              "rotate": 0
            }
          },
          "size": {
            "width": 50,
            "height": 36
          },
          "image": "/static/data/basic/sma1.svg"
        },
        "_refId": "346"
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 284
          },
          "to": {
            "_ref": 342
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 342
          },
          "to": {
            "_ref": 346
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 342
          },
          "to": {
            "_ref": 334
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 342
          },
          "to": {
            "_ref": 336
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 342
          },
          "to": {
            "_ref": 338
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 342
          },
          "to": {
            "_ref": 340
          }
        }
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "ATS\n工作站",
          "parent": {
            "_ref": 212
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "ATS\n工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 150,
              "y": 460,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "360"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "MSS维护\n工作站",
          "parent": {
            "_ref": 212
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "MSS维护\n工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 300,
              "y": 460,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "362"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "维修服务器",
          "parent": {
            "_ref": 212
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "维修服务器",
            "specifyDeviceType": 'true',
            "typeIds": [
              "301001",
              "301002",
              "301003",
              "301004",
              "301005",
              "301006",
              "301007",
              "301008",
              "301009",
              "301099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 440,
              "y": 460,
              "rotate": 0
            }
          },
          "size": {
            "width": 33,
            "height": 42
          },
          "image": "/static/data/basic/servernew1.svg"
        },
        "_refId": "364"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "派班工作站",
          "parent": {
            "_ref": 212
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "派班工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 600,
              "y": 460,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "366"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "联锁控制\n工作站",
          "parent": {
            "_ref": 212
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "联锁控制\n工作站",
            "specifyDeviceType": 'true',
            "typeIds": [
              "302001",
              "302002",
              "302003",
              "302004",
              "302032",
              "302099"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 780,
              "y": 460,
              "rotate": 0
            }
          },
          "size": {
            "width": 45,
            "height": 42
          },
          "image": "/static/data/basic/workstation1.svg"
        },
        "_refId": "368"
      },
      {
        "_className": "Q.Node",
        "json": {
          "zIndex": -1,
          "name": "监测审计平台",
          "parent": {
            "_ref": 212
          },
          "styles": {
            "label.color": "#FFF"
          },
          "properties": {
            "nodeName": "监测审计平台",
            "specifyDeviceType": 'true',
            "typeIds": [
              "202007"
            ]
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 730,
              "y": 310,
              "rotate": 0
            }
          },
          "size": {
            "width": 50,
            "height": 36
          },
          "image": "/static/data/basic/sma1.svg"
        },
        "_refId": "370"
      },
      {
        "_className": "Q.ShapeNode",
        "json": {
          "busLayout": 'true',
          "name": "总线",
          "parent": {
            "_ref": 212
          },
          "styles": {
            "arrow.to": 'false',
            "shape.stroke": 10
          },
          "location": {
            "_className": "Q.Point",
            "json": {
              "x": 250,
              "y": 380,
              "rotate": 0
            }
          },
          "path": {
            "_className": "Q.Path",
            "json": [
              {
                "type": "m",
                "points": [
                  710.4005350860497,
                  8.881784197001252e-16
                ]
              },
              {
                "type": "l",
                "points": [
                  -207.21141606419144,
                  0
                ]
              }
            ]
          }
        },
        "_refId": "372"
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 360
          },
          "to": {
            "_ref": 372
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 372
          },
          "to": {
            "_ref": 362
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 372
          },
          "to": {
            "_ref": 364
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 372
          },
          "to": {
            "_ref": 366
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 372
          },
          "to": {
            "_ref": 368
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 372
          },
          "to": {
            "_ref": 370
          }
        }
      },
      {
        "_className": "Q.Edge",
        "json": {
          "from": {
            "_ref": 372
          },
          "to": {
            "_ref": 286
          }
        }
      }
    ],
    "scale": 0.6209213230591552,
    "tx": 491.600063277502,
    "ty": 334.56230169592,
    "currentSubNetwork": 'null'
  },
  "name": f"test{num}",
  "action": "add"
}
    res = requests.post(url=add_tuopu_url, headers=add_tuopu_header, json=add_tuopu_body, verify=False)
    add_tuopu_result = res.json()
    print("操作结果：", add_tuopu_result)


if __name__ == '__main__':
    num = 1
    # add_assert(token[0], num)
    while num <= 22:
        add_assert(token[0], num)
        num += 1


