## 处理流程及其技术

1, 数据获取，使用“同花顺”可以查询到一个公司的大部分信息，一个公司的高管对应一个 html。Tushare 可以直接给出股票的概念和行业信息，但是现在要注册才给用。

这个部分，同花顺的网页直接下载 html 格式。

2, parse html。

parse 部分主要使用的技术是 lxml 中的 etree。

这个部分主要涉及使用 XPath 选取内容，具体可参考：

https://www.ruanyifeng.com/blog/2009/07/xpath_path_expressions.html

在 Chrome 中右键“检查”一个元素，可以找到 html 的路径，右键可以选择 copy，下面有个 Copy XPath。

```
//*[@id="ml_001"]/table/tbody/tr[1]/td[2]

//*[@id="ml_001"]/table/tbody/tr[1]/td[1]/div/table/thead/tr[1]/td[1]/h3/a
```

3, 设计知识图谱

对于关系型数据库而言，任务是设计表，设计表项

对于图数据库而言，任务是设计图结构，设计实体和实体间关系

其实我觉得知识图谱的设计取决于业务的需求，就像关系型数据库的表设计一样，都是根据需求来的。什么样的需求决定了什么样的知识图谱。

4, 使用 neo4j

方法一：使用 `IMPORT CSV`，直接导入

方法二：使用 `neo4j-admin import` 导入，需要处理成 neo4j 可以认识的格式。这个命令在数据库所在的 bin 文件夹中。

方法一详解：

这种方法的缺陷是会出现多个重复的实体。

(1) 导入董事

```
LOAD CSV WITH HEADERS FROM 'file:///executive.csv' AS row
CREATE (p:Person {name: row.name, gender: row.gender, age: row.age, person_id: row.person_id})
RETURN p
```

(2) 导入概念

```
LOAD CSV WITH HEADERS FROM 'file:///concept.csv' AS row
CREATE (c:Concept {ID: row.concept_id, name: row.name})
RETURN c
```

(3) 导入行业

```
LOAD CSV WITH HEADERS FROM 'file:///industry.csv' AS row
CREATE (c:Industry {ID: row.industry_id, name: row.name})
RETURN c
```

(4) 导入股票

```
LOAD CSV WITH HEADERS FROM 'file:///stock.csv' AS row
CREATE (c:Stock {ID: row.stock_id, name: row.name, code: row.code})
RETURN c
```

(5) 导入股票-董事关系

执行速度特别慢，> 30 min

```
LOAD CSV WITH HEADERS FROM 'file:///executive_stock.csv' AS row
MATCH (a:Executive {person_id: row.start}), (b:Stock {code: row.end})
MERGE (a)-[r:employ_of]->(b) SET r.jobs = [row.jobs]
RETURN a,r,b
```

(6) 导入股票-行业关系

```
LOAD CSV WITH HEADERS FROM 'file:///stock_industry.csv' AS row
MATCH (a:Stock {ID: row.start}), (b:Industry {ID: row.end})
MERGE (a)-[r:industry_of]->(b)
RETURN a,r,b
```

(7) 导入股票-概念关系

```
LOAD CSV WITH HEADERS FROM 'file:///stock_concept.csv' AS row
MATCH (a:Stock {ID: row.start}), (b:Concept {ID: row.end})
MERGE (a)-[r:concept_of]->(b)
RETURN a,r,b
```

方法二详解：

原作者有个 `import.sh` 文件，但是在 Windows 10 上的 neo4j Desktop 执行的时候，发现有两个参数不行。

```
.\bin\neo4j-admin.bat import --skip-duplicate-nodes --id-type=STRING --nodes executive.csv --nodes stock.csv --nodes concept.csv --nodes industry.csv --relationships executive_stock.csv --relationships stock_industry.csv --relationshi ps stock_concept.csv
```
