论文笔记分享，标题是 Golden-Retriever: High-Fidelity Agentic Retrieval Augmented Generation for Industrial Knowledge Base

Golden-Retriever系统主要是想通过一些流程优化，来克服传统LLM、RAG框架在特定领域术语和上下文解释方面的一些挑战。

看下对比图，一目了然。首先离线流程上区别不大，不过这个工作中会生成文档的摘要。在线流程，常规的corretive-rag、self-rag。最大的问题是，如果用户的问题不明确，缺乏上下文。系统就无法检索到相关文档，限制了结果的准确性。 本文的方法主要是前处理部分，会识别出术语，根据术语以及上下文对问题进行增强。
![](https://files.mdnice.com/user/50285/465b3b6c-e030-4e1a-93dd-516c2f23c114.png)

对应下来，离线部分就是基本操作+生成摘要

![](https://files.mdnice.com/user/50285/97a28ef7-5708-4faf-ac52-1761bf1fca07.png)

在线部分，传统的RAG流程，就只有红色的一条路径。然后多了一些模块，包括识别术语、确定上下文、查询术语字典、增强问题，最后就是检索文档，生成答案，提示词都在下边。
![](https://files.mdnice.com/user/50285/20c22c7f-d7c0-4034-bdcc-182ce3c78cdb.png)

与LLM和普通的RAG方法相比，Golden-Retriever在多个LLM基座上平均提高了57.3%和35.0%的分数。而且，Golden-Retriever还能够有效地识别问题中的缩写，即使这些缩写是未知的。
![](https://files.mdnice.com/user/50285/dc4b4410-78a6-42af-85a3-983856135ed3.png)



