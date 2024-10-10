论文笔记分享，标题：Superposition Prompting: Improving and Accelerating Retrieval-Augmented Generation， ICML2024，代码开源

LMMs 在处理长文本时，一方面成本会跟着长度呈二次方增长，另一方面，更长的文本，LLMs还表现出“distraction phenomenon”，即prompt中的不相关上下文会降低输出质量。

一个新的方案，无需finetuning。在处理RAG任务时允许LLMs通过并行prompt路径处理输入文档，并在认为它们不相关时丢弃这些路径。

假如下图每一个颜色块是一个token，naive rag的token就是顺序的，后文的token会持续注意到上文信息。叠加提示词方法就是一个并行方案。
![](https://files.mdnice.com/user/50285/017d4b91-8309-4fde-b609-70d1f8cdb257.png)


看注意力依赖更直观
![](https://files.mdnice.com/user/50285/4ba0deac-ac33-44c8-860e-2bba0cc2708a.png)


使用MPT-7B模型时，在NaturalQuestions-Open数据集上，相比于传统的RAG方法，计算时间减少了93倍，准确率提高了43%。
![](https://files.mdnice.com/user/50285/01057369-57e1-49ae-b858-4ef0107eea5f.png)


后续为不详细的算法原理，代码开源地址：https://github.com/apple/ml-superposition-prompting/tree/main

使用ForkJoin的图来表示整个prompt。在这个结构中，每个query复制与documents配对，形成多个路径。（这样允许模型并行处理每个document和query的组合，然后通过剪枝丢弃不相关的路径，从而提高效率。）

然后这里有个细节，由于存在多个可能长度不一的路径，直接为每个token分配连续的整数位置可能会导致较短文档的token在模型中不公平。所以提出了一种平衡位置分配策略，通过调和平均来平衡不同长度路径的贡献，避免这个问题。
![](https://files.mdnice.com/user/50285/c7809553-b7a8-4b26-be5f-01d8931a0452.png)
对于每个路径 d，首先确定其在平衡状态下的起始位置 s_i ，然后使用这个起始位置和路径长度来分配该路径上所有token的位置。


使用bayes来计算每个文档相对于查询的后验概率，作为其相关性得分。选topk。用于路径剪枝。
![](https://files.mdnice.com/user/50285/9e32ba58-2eee-45ca-ae0a-6ef8e2b31030.png)


其次还有path caching， path parallelization 等加速策略。


