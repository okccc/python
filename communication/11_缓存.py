"""
CPU要读取一个数据时,首先从Cache中查找,如果找到就立即读取并送给CPU处理；如果没有找到,就用相对慢的速度从内存中读取并送给CPU处理,同时把这个数据所在的数据块调入Cache中,可以使得以后对整块数据的读取都从Cache中进行,不必再调用内存。
正是这样的读取机制使CPU读取Cache的命中率非常高（大多数CPU可达90%左右）,也就是说CPU下一次要读取的数据90%都在Cache中,只有大约10%需要从内存读取。这大大节省了CPU直接读取内存的时间,也使CPU读取数据时基本无需等待。总的来说,CPU读取数据的顺序是先Cache后内存。

缓存是为了解决CPU速率和内存速率的速率差异问题,缓存的速率比内存快很多,内存中被CPU访问最频繁的数据和指令被复制入CPU中的缓存
"""