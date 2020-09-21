# 行业字段

| 序号 | 字段                   | 类型             | 名称                               | 备注 |
| ---- | ---------------------- | ---------------- | ---------------------------------- | ---- |
| 1    | id                     | string           | id                                 |      |
| 2    | industry_categories    | string           | 行业门类                           | B    |
| 3    | industry_Lcategories   | **string**       | 行业大类                           | 07   |
| 4    | industry_Mcategories   | string  or None  | 行业中类                           | 071  |
| 5    | industry_Scategories   | string  or None  | 行业小类                           | 0711 |
| 6    | information_categories | string           | 资讯类别                           |      |
| 7    | content_url            | string           | 链接地址                           |      |
| 8    | title                  | string           | 标题                               |      |
| 9    | issue_time             | string           | 发布时间                           |      |
| 10   | information_source     | string           | 网站名                             |      |
| 11   | source                 | **string非list** | 来源                               |      |
| 12   | author                 | **string非list** | 作者                               |      |
| 13   | content                | **string非list** | 内容                               |      |
| 14   | images                 | **string非list** | 图片                               |      |
| 15   | attachments            | **string非list** | 附件                               |      |
| 16   | area                   | string           | 地区                               |      |
| 17   | address                | string           | 地址                               |      |
| 18   | tags                   | **string非list** | 标签                               |      |
| 19   | sign                   | **string非list** | sign                               | 02   |
| 20   | update_time            | string           | 时间戳，str(int(time.time()*1000)) |      |
| 21   | title_image            | string           | 标题图片                           | 新增 |