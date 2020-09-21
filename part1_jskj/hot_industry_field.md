# 热门行业字典目录

- [资讯字段](#热门行业资讯字段)

- [数据字段](#热门行业数据字段)

- [报告字段](#热门行业报告字段)

## 热门行业资讯字段

| 序号 | 字段                   | 类型             | 名称           | 备注                         |
| ---- | ---------------------- | ---------------- | -------------- | ---------------------------- |
| 1    | news_id                | string           | id             | url哈希值                    |
| 2    | category               | string           | 行业           | 中文                         |
| 3    | sub_category           | string           | 行业子类       | 中文                         |
| 4    | information_categories | string           | 资讯类别       |                              |
| 5    | content_url            | string           | 链接地址       |                              |
| 6    | title                  | string           | 标题           |                              |
| 7    | issue_time             | string           | 发布时间       |                              |
| 8    | title_image            | string           | 标题图片       |                              |
| 9    | information_source     | string           | 网站名         |                              |
| 10   | source                 | **string非list** | 来源           |                              |
| 11   | author                 | **string非list** | 作者           |                              |
| 12   | content                | **string非list** | 内容           |                              |
| 13   | images                 | **string非list** | 图片           |                              |
| 14   | attachments            | **string非list** | 附件           |                              |
| 15   | area                   | string           | 地区           |                              |
| 16   | address                | string           | 地址           |                              |
| 17   | tags                   | **string非list** | 标签           |                              |
| 18   | sign                   | string           | sign           | 02                           |
| 19   | update_time            | string           | 时间戳         | `str(int(time.time()*1000))` |
| 20   | cleaning_status        | int              | 清洗位 默认为0 |                              |

## 热门行业数据字段

| 字段            | 类型       | 解释                                           | 示例          |
| --------------- | ---------- | ---------------------------------------------- | ------------- |
| parent_id       | **string** | 数据目录                                       | 1 001 001 001 |
| indic_name      | string     | 名称                                           |               |
| data_year       | int        | 年：1992                                       |               |
| data_month      | int        | 月：1-12                                       | 没有为0       |
| data_day        | int        | 日：1-31                                       | 没有为0       |
| frequency       | int        | 频率(0：季度， 1234： 季度 ，5678：年月周日  ) | 1             |
| unit            | string     | 单位                                           |               |
| data_source     | string     | 数据来源(网站名)                               | 国家统计局    |
| region          | string     | 全国、省份、市等地区                           |               |
| country         | string     | 国家                                           |               |
| create_time     | date       | 数据产生时间                                   | xxxx-xx-xx    |
| update_time     | datetime   | 数据插入时间（爬取时间）                       |               |
| data_value      | double     | 数值                                           |               |
| sign            | string     | 个人编号                                       | 01-20         |
| status          | int        | 0:无效  1: 有效                                |               |
| cleaning_status | int        | 0 : 未清洗  1 ： 清洗过                        |               |

## 热门行业报告字段

| 序号 | 字段            | 类型   | 名称        | 备注           |
| ---- | --------------- | ------ | ----------- | -------------- |
| 1    | menu            | string | 行业名称    | 中文           |
| 2    | abstract        | string | 报告摘要    |                |
| 3    | title           | string | 标题        |                |
| 4    | paper_url       | string | 文件下载url |                |
| 5    | date            | string | 时间        |                |
| 6    | paper_from      | string | 文件来源    |                |
| 7    | paper           | string | 文件路径    |                |
| 8    | author          | string | 文件作者    | 多个以逗号隔开 |
| 9    | update_time     | string | 更新时间    | 时间戳形式     |
| 10   | parent_id       | string | 父级id      |                |
| 11   | sign            | string | 签名        |                |
| 12   | cleaning_status | int    | 清洗位      | 默认为0        |

