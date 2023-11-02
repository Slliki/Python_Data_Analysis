# SQL 刷题总结
# 1.topN问题
一般来说，topN问题可以分为两类：
- 一类是求某一字段的分组排名在前N名的记录，比如公司不同部门薪水的前三名；
- 另一类是求某一字段的排名在前N名的记录，比如全国人口排名前三的省份。

## 1.使用窗口函数
一般使用`dense_rank()`或者`rank()`来创建一个新列（排名列），然后选出该列前N行\
基本思路：使用子查询得到一个虚拟表，该表应该是按某字段进行rank排序得到rk列的表，
然后从该表选取目标字段和rk列，再按rk列进行排序，最后选取前N行即可。

`select t.col1,t.col2
from (select col1,col2,
dense_rank() over(partition by col1 order by col3 desc) as rk
from ... ) as t
where t.rk<=N`\
\
重点是先得到虚拟子表(t表),在该表中使用rank()等窗口函数得到新一列作为判断条件，
再从子表中选取目标字段(where t.rk<=N)

**注意**：关于窗口函数用over的情况下，`partition by`相当于`group by`，即分组

## 2.使用limit
`select col1,col2
from ...
order by col3 desc
limit N`\
重点是先排序，再选取前N行，该方法仅适用于不用分组的情况

# 2.连续\重复问题
## 1.连续
可以使用暴力解法，多表自连接：\
`table as t1, table as t2, table as t3`\
`where t1.id=t2.id-1 and t2.id=t3.id-1 and t1.num=t2.num and t2.num=t3.num`
即保证id连续，num相同则说明连续出现。
## 2.重复
同样使用多表自连：\
`where t1.id!=t2.id and t1.num=t2.num`\
当id不同，num相同则说明重复出现。

**注意**：进行自连接时，最后select语句中的字段从自连接表1中取出，否则会出现表二进行比较时无法取出表一的字段的情况。

# 3.中位数问题

# 4.累计区间计算问题

# 5.条件求和问题

# 6.行转列问题

# 7.笛卡儿积问题

# 8.递归问题

