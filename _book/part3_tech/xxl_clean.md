# xxl-job数据定时插入

**简介**：资讯，数据，报告定时更新到数据库

**HOST**:192.168.0.11:8066

**联系人**:

**Version**:1.0

**接口路径**：/v2/api-docs

## 数据导入xxl-job数据库

## 把行业数据插入xxl的数据库

**接口描述**:把行业数据插入xxl的数据库

**接口地址**:`/quota/data/insert`

**请求方式**：`POST`


**consumes**:`["application/json"]`


**produces**:`["*/*"]`


**请求示例**：
```json
[
	{
		"country": "",
		"data_day": 0,
		"data_month": 0,
		"data_source": "",
		"data_value": 0,
		"data_year": 0,
		"frequency": 0,
		"indic_name": "",
		"path": [],
		"region": "",
		"sign": "",
		"status": 0,
		"unit": ""
	}
]
```


**请求参数**：

| 参数名称         | 参数说明     |     in |  是否必须      |  数据类型  |  schema  |
| ------------ | -------------------------------- |-----------|--------|----|--- |
|mons| mons  | body | true |array  | QuotaMongoDTO   |

**schema属性说明**



**QuotaMongoDTO**

| 参数名称         | 参数说明     |     in |  是否必须      |  数据类型  |  schema  |
| ------------ | -------------------------------- |-----------|--------|----|--- |
|country|   | body | false |string  |    |
|data_day|   | body | false |integer(int32)  |    |
|data_month|   | body | false |integer(int32)  |    |
|data_source|   | body | false |string  |    |
|data_value| 数据内容  | body | true |number(double)  |    |
|data_year|   | body | false |integer(int32)  |    |
|frequency| 数据频率  | body | true |integer(int32)  |    |
|indic_name| 数据名字  | body | true |string  |    |
|path| 数据的菜单列表，从行业大类开始至最后一级菜单为止  | body | true |array  |    |
|region|   | body | false |string  |    |
|sign|   | body | false |string  |    |
|status|   | body | false |integer(int32)  |    |
|unit| 单位  | body | false |string  |    |

**响应示例**:

```json
{
	"code": 0,
	"data": {},
	"msg": "",
	"success": true
}
```

**响应参数**:


| 参数名称         | 参数说明                             |    类型 |  schema |
| ------------ | -------------------|-------|----------- |
|code|   |integer(int32)  | integer(int32)   |
|data|   |object  |    |
|msg|   |string  |    |
|success|   |boolean  |    |





**响应状态**:


| 状态码         | 说明                            |    schema                         |
| ------------ | -------------------------------- |---------------------- |
| 200 | OK  |ResponseDTO|
| 201 | Created  ||
| 401 | Unauthorized  ||
| 403 | Forbidden  ||
| 404 | Not Found  ||
## 把行业报告插入xxl的数据库

**接口描述**:把行业报告插入xxl的数据库

**接口地址**:`/report/data/insert`


**请求方式**：`POST`


**consumes**:`["application/json"]`


**produces**:`["*/*"]`


**请求示例**：
```json
[
	{
		"author": "",
		"day": 0,
		"image_url": "",
		"month": 0,
		"paper": "",
		"paper_abstract": "",
		"paper_from": "",
		"paper_url": "",
		"path": [],
		"title": "",
		"year": 0
	}
]
```


**请求参数**：

| 参数名称         | 参数说明     |     in |  是否必须      |  数据类型  |  schema  |
| ------------ | -------------------------------- |-----------|--------|----|--- |
|reports| reports  | body | true |array  | ReportMongoDTO   |

**schema属性说明**



**ReportMongoDTO**

| 参数名称         | 参数说明     |     in |  是否必须      |  数据类型  |  schema  |
| ------------ | -------------------------------- |-----------|--------|----|--- |
|author| 报告pdf作者  | body | false |string  |    |
|day| 日  | body | false |integer(int32)  |    |
|image_url| 标题图片的url路径  | body | false |string  |    |
|month| 月  | body | false |integer(int32)  |    |
|paper| 报告pdf文件的存放路径  | body | true |string  |    |
|paper_abstract| 报告pdf内容简介  | body | false |string  |    |
|paper_from| 报告pdf来源  | body | false |string  |    |
|paper_url| 报告pdf文件的网站来源url  | body | false |string  |    |
|path| 报告pdf文件的菜单，从行业大类开始  | body | true |array  |    |
|title| 报告标题  | body | true |string  |    |
|year| 年  | body | false |integer(int32)  |    |

**响应示例**:

```json
{
	"code": 0,
	"data": {},
	"msg": "",
	"success": true
}
```

**响应参数**:


| 参数名称         | 参数说明                             |    类型 |  schema |
| ------------ | -------------------|-------|----------- |
|code|   |integer(int32)  | integer(int32)   |
|data|   |object  |    |
|msg|   |string  |    |
|success|   |boolean  |    |





**响应状态**:


| 状态码         | 说明                            |    schema                         |
| ------------ | -------------------------------- |---------------------- |
| 200 | OK  |ResponseDTO|
| 201 | Created  ||
| 401 | Unauthorized  ||
| 403 | Forbidden  ||
| 404 | Not Found  ||
# 资讯导入xxl-job数据库


## 向mongo中导入资讯

**接口描述**:向mongo中导入资讯

**接口地址**:`/policy/insertToMongo`


**请求方式**：`POST`


**consumes**:`["application/json"]`


**produces**:`["*/*"]`


**请求示例**：
```json
[
	{
		"content": "",
		"content_url": "",
		"day": 0,
		"information_source": "",
		"month": 0,
		"path": [],
		"tags": "",
		"title": "",
		"title_image": "",
		"year": 0
	}
]
```


**请求参数**：

| 参数名称         | 参数说明     |     in |  是否必须      |  数据类型  |  schema  |
| ------------ | -------------------------------- |-----------|--------|----|--- |
|policy| policy  | body | true |array  | PolicyRecMongoDTO   |

**schema属性说明**



**PolicyRecMongoDTO**

| 参数名称         | 参数说明     |     in |  是否必须      |  数据类型  |  schema  |
| ------------ | -------------------------------- |-----------|--------|----|--- |
|content| 资讯内容  | body | true |string  |    |
|content_url| 文章的链接  | body | false |string  |    |
|day|   | body | false |integer(int32)  |    |
|information_source| 文章的来源网站的名称  | body | false |string  |    |
|month|   | body | false |integer(int32)  |    |
|path| 报告pdf文件的菜单，从行业大类开始  | body | true |array  |    |
|tags| 文章的分类标签  | body | false |string  |    |
|title| 文章的标题  | body | true |string  |    |
|title_image| 文章的标题图片  | body | false |string  |    |
|year|   | body | false |integer(int32)  |    |

**响应示例**:

```json
{
	"code": 0,
	"data": {},
	"msg": "",
	"success": true
}
```

**响应参数**:


| 参数名称         | 参数说明                             |    类型 |  schema |
| ------------ | -------------------|-------|----------- |
|code|   |integer(int32)  | integer(int32)   |
|data|   |object  |    |
|msg|   |string  |    |
|success|   |boolean  |    |





**响应状态**:


| 状态码         | 说明                            |    schema                         |
| ------------ | -------------------------------- |---------------------- |
| 200 | OK  |ResponseDTO|
| 201 | Created  ||
| 401 | Unauthorized  ||
| 403 | Forbidden  ||
| 404 | Not Found  ||
