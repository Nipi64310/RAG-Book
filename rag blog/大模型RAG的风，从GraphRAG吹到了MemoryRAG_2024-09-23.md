最近相关的标题应该是很多了，RAG的热浪从GraphRAG吹到了MemoryRAG，节奏很快。论文标题MemoRAG: Moving towards Next-Gen RAG Via Memory-Inspired Knowledge Discovery。智源BAAI开源，代码https://github.com/qhjqhj00/MemoRAG

![](https://files.mdnice.com/user/50285/3f47036a-db9b-40c8-8401-81c2ce9ddc79.png)

如上图，对比标准的RAG，多了一个记忆模型生成线索，草稿答案插到召回之前。（别说跟hyde碰瓷？）


记忆模型的主要目的是逐步将原始输入token压缩为明显更小的一组记忆token，同时保留基本的语义信息。想实现这个过程，作者使用一组记忆token$X_{m}$插在模型的每一步的上下文窗口之后。看下图，先看x，每个窗口之后添加k个记忆token，算attention的时候，k,v会用到历史的cache 记忆token，q取当前窗口的token。
![](https://files.mdnice.com/user/50285/cb1786b9-7509-4abf-ba3c-999dfb5c4b37.png)

这种记忆模型仍然是通过预训练+sft训练完成，训练目标如下，给定最近的token和历史记忆，最大化下一个token的概率：

![](https://files.mdnice.com/user/50285/fe71bfd1-d32e-47cc-93e5-1cd410f1089e.png)

开源了2个模型：
- https://huggingface.co/TommyChien/memorag-qwen2-7b-inst
- https://huggingface.co/TommyChien/memorag-mistral-7b-inst

线索示例：

整体取得了不错的结果：
![](https://files.mdnice.com/user/50285/d6ace446-b16a-4e26-82d1-22df189d90de.png)




