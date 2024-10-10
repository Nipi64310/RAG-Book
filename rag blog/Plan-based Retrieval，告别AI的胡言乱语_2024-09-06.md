论文笔记分享，标题：Analysis of Plan-based Retrieval for Grounded Text Generation

如何通过 Plan-based Retrieval 来改善基于文本的生成任务中的“幻觉”问题。

跟一些Agent写作有点像，比如longwriter。 

s1: 生成每个段落的计划，要写些什么； s2：确定每个段落的搜索query； s3: 搜索文档； s4: 生成最终的文档。

![](https://files.mdnice.com/user/50285/a569464a-6d57-4a35-b656-03f038d50383.png)

**观察**：

![](https://files.mdnice.com/user/50285/9436c335-8811-4766-8eea-d194d73191c8.png)

- 当仅依赖语言模型的参数知识进行文本生成时，生成的文本很难完全追溯到源文档，容易出现幻觉 （用AIS归属性来衡量）
- 与仅使用参数知识相比，通过检索补充的证据可以显著提高文本的归属性
- 使用Plan-based Retrieval 可以做到比One-Retrieval更好的归属性得分。也就是说可以提高生成文本的准确性。
- 在Plan-based Retrieval中，通过为每个段落独立生成的问题进行第二轮搜索，可以进一步收集信息，从而提高归属性。
- 在检索过程中，如果某些问题无法找到答案，将这些问题标记为unanswerable，而不是从上下文中删除，可以提高生成文本的归属性。
- 比较了两种不同的最终生成提示格式（Var.A 和 Var.B），发现包含问题和检索计划的提示（Var.B）可以生成更长的文本，同时保持较高的归属性。
- 在生成问题之前先创建一个概述可以提高检索信息的有用性，从而提高归属性。


one-retrieval出现幻觉的示例
![](https://files.mdnice.com/user/50285/9dc659f3-4393-418f-b5b6-cbc413e0ed45.png)
