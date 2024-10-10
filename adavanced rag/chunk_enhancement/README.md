关于文档块增强的策略，常见的有以下几种

1. 使用overlap： 这里不是指的滑动窗口切块的过程中有一定窗口重叠，而是召回的时候会去检索前后的文档块，llamaindex中有比较方便的实现。

overlap.ipynb

2. 使用语义对chunk进行切分

semantic.ipynb

3. 上下文压缩

context_compression


4. 文档块的辅助信息

