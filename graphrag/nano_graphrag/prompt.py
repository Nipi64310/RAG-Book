GRAPH_FIELD_SEP = "<SEP>"
PROMPTS = {}

PROMPTS[
    "claim_extraction"
] = """- 目标活动 -
您是一个智能助手，帮助人类分析师分析文本文档中针对特定实体的声明。

- 目标 -
给定一个文本文档，该文档可能与此活动相关，一个实体规范，以及一个声明描述，提取所有符合实体规范的实体以及针对这些实体的所有声明。

- 步骤 -
1. 提取所有符合预定义实体规范的命名实体。实体规范可以是实体名称列表或实体类型列表。
2. 对于步骤1中识别的每个实体，提取与实体相关的所有声明。声明需要符合指定的声明描述，并且实体应该是声明的主语。
对于每个声明，提取以下信息：
- 主体：声明主语的名称，大写。主语是执行声明中描述的行动的实体。主体需要是步骤1中识别的命名实体之一。
- 客体：声明宾语的名称，大写。宾语是报告/处理或受声明中描述的行动影响的实体。如果宾体实体未知，使用**NONE**。
- 声明类型：声明的总体类别，大写。以一种可以在多个文本输入中重复的方式命名，以便类似的声明共享相同的声明类型。
- 声明状态：**TRUE**，**FALSE**或**SUSPECTED**。TRUE表示声明已确认，FALSE表示声明被发现是虚假的，SUSPECTED表示声明尚未验证。
- 声明描述：详细描述声明背后的理由，以及所有相关证据和引用。
- 声明日期：声明做出的时间段(开始日期，结束日期)。开始日期和结束日期都应使用ISO-8601格式。如果声明是在单一日期而不是日期范围内做出的，将相同的日期设置为开始日期和结束日期。如果日期未知，返回**NONE**。
- 声明来源文本：与声明相关的原始文本的所有引用列表。

将每个声明格式化为(<主体实体>{tuple_delimiter}<客体实体>{tuple_delimiter}<声明类型>{tuple_delimiter}<声明状态>{tuple_delimiter}<声明开始日期>{tuple_delimiter}<声明结束日期>{tuple_delimiter}<声明描述>{tuple_delimiter}<声明来源>)

3. 用中文返回步骤1和2中识别的所有声明的单一列表。使用**{record_delimiter}**作为列表分隔符。

4. 完成后，输出{completion_delimiter}

- 示例 -
示例1：
实体规范：组织
声明描述：与实体相关的敏感信号
文本：根据2022/01/10的一篇文章，公司A因参与由政府机构B发布的多个公开招标而被罚款操纵投标。该公司由C人拥有，他被怀疑在2015年参与腐败活动。
输出：

(公司A{tuple_delimiter}政府机构B{tuple_delimiter}多个公开招标{tuple_delimiter}TRUE{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}根据2022/01/10发表的一篇文章，公司A被发现参与反竞争行为，因为它因操纵投标而被罚款，在由政府机构B发布的多个公开招标中{tuple_delimiter}根据2022/01/10发表的一篇文章，公司A因参与由政府机构B发布的多个公开招标而被罚款操纵投标。)
{completion_delimiter}

示例2：
实体规范：公司A，人C
声明描述：与实体相关的敏感信号
文本：根据2022/01/10的一篇文章，公司A因参与由政府机构B发布的多个公开招标而被罚款操纵投标。该公司由人C拥有，他被怀疑在2015年参与腐败活动。
输出：

(公司A{tuple_delimiter}政府机构B{tuple_delimiter}多个公开招标{tuple_delimiter}TRUE{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}根据2022/01/10发表的一篇文章，公司A被发现参与反竞争行为，因为它因操纵投标而被罚款，在由政府机构B发布的多个公开招标中{tuple_delimiter}根据2022/01/10发表的一篇文章，公司A因参与由政府机构B发布的多个公开招标而被罚款操纵投标。)
{record_delimiter}
(人C{tuple_delimiter}NONE{tuple_delimiter}参与腐败{tuple_delimiter}怀疑{tuple_delimiter}2015-01-01T00:00:00{tuple_delimiter}2015-12-30T00:00:00{tuple_delimiter}C人被怀疑在2015年参与腐败活动{tuple_delimiter}该公司由C人拥有，他被怀疑在2015年参与腐败活动)
{completion_delimiter}

- 实际数据 -
使用以下输入回答您的问题。
实体规范：{entity_specs}
声明描述：{claim_description}
文本：{input_text}
输出："""


PROMPTS[
    "community_report"
] = """你是一个AI助手，帮助人类分析师进行一般信息发现。信息发现是识别和评估与特定实体(例如组织和个人)在网络中的关联信息的过程。

# 目标
根据属于社区的实体列表以及它们的关系和可选的相关声明，编写一份社区的综合报告。该报告将用于告知决策者有关社区及其潜在影响的信息。报告的内容包括对社区主要实体的概述、它们的法律合规性、技术能力、声誉以及值得注意的声明。

# 报告结构

报告应包括以下部分：

- TITLE: 代表社区主要实体的社区名称 - 标题应简短但具体。如果可能，标题中应包含具有代表性的命名实体。
- SUMMARY: 社区整体结构的执行摘要，包括实体之间的关系以及与实体相关的重要信息。
- IMPACT SEVERITY RATING: 0到10之间的浮动分数，表示社区内实体所带来的影响的严重程度。 IMPACT 是社区的重要性评分。
- RATING EXPLANATION: 给出一个关于 IMPACT 严重性评分的单句解释。
- DETAILED FINDINGS: 关于社区的5到10个关键见解列表。每个见解应包含一个简短的摘要，然后是多个段落的解释文本，依据以下基础规则进行说明。要全面。

返回输出应为格式良好的JSON字符串，格式如下：
    {{
        "title": <report_title>,
        "summary": <executive_summary>,
        "rating": <impact_severity_rating>,
        "rating_explanation": <rating_explanation>,
        "findings": [
            {{
                "summary":<insight_1_summary>,
                "explanation": <insight_1_explanation>
            }},
            {{
                "summary":<insight_2_summary>,
                "explanation": <insight_2_explanation>
            }}
            ...
        ]
    }}

# 基础规则
不包括任何缺乏支持证据的信息。

# 示例输入
-----------
文本:
```
实体:
```csv
id,entity,type,description
5,VERDANT OASIS PLAZA,geo,Verdant Oasis Plaza 是团结游行的地点
6,HARMONY ASSEMBLY,organization,Harmony Assembly 是在 Verdant Oasis Plaza 举行游行的组织
```
关系:
```csv
id,source,target,description
37,VERDANT OASIS PLAZA,UNITY MARCH,Verdant Oasis Plaza 是团结游行的地点
38,VERDANT OASIS PLAZA,HARMONY ASSEMBLY,Harmony Assembly 正在 Verdant Oasis Plaza 举行游行
39,VERDANT OASIS PLAZA,UNITY MARCH,团结游行在 Verdant Oasis Plaza 举行
40,VERDANT OASIS PLAZA,TRIBUNE SPOTLIGHT,Tribune Spotlight 正在报道在 Verdant Oasis Plaza 举行的团结游行
41,VERDANT OASIS PLAZA,BAILEY ASADI,Bailey Asadi 正在 Verdant Oasis Plaza 就游行发表讲话
43,HARMONY ASSEMBLY,UNITY MARCH,Harmony Assembly 正在组织团结游行
```
```
输出:
{{
    "title": "Verdant Oasis Plaza and Unity March",
    "summary": "该社区围绕 Verdant Oasis Plaza 展开，后者是团结游行的地点。该广场与 Harmony Assembly、团结游行和 Tribune Spotlight 相关联，这些都是与游行事件相关的。",
    "rating": 5.0,
    "rating_explanation": "由于团结游行可能引发的骚乱或冲突，影响严重性评分为中等。",
    "findings": [
        {{
            "summary": "Verdant Oasis Plaza 作为中心位置",
            "explanation": "Verdant Oasis Plaza 是该社区的中心实体，作为团结游行的地点。这个广场是所有其他实体的共同联系点，显示出其在社区中的重要性。广场与游行的关联可能导致诸如公共骚乱或冲突等问题，具体取决于游行的性质及其引发的反应。"
        }},
        {{
            "summary": "Harmony Assembly 在社区中的角色",
            "explanation": "Harmony Assembly 是社区中的另一个关键实体，它是组织在 Verdant Oasis Plaza 举行游行的组织。Harmony Assembly 和其游行的性质可能会成为潜在的威胁，具体取决于它们的目标及其引发的反应。Harmony Assembly 与广场的关系对理解该社区的动态至关重要。"
        }},
        {{
            "summary": "团结游行作为重要事件",
            "explanation": "团结游行是发生在 Verdant Oasis Plaza 的重要事件。这个事件是社区动态的关键因素，可能成为潜在的威胁，具体取决于游行的性质及其引发的反应。游行与广场之间的关系对理解该社区的动态至关重要。"
        }},
        {{
            "summary": "Tribune Spotlight 的作用",
            "explanation": "Tribune Spotlight 正在报道在 Verdant Oasis Plaza 举行的团结游行。这表明事件已引起媒体关注，这可能会放大其对社区的影响。Tribune Spotlight 的角色在塑造公众对事件和相关实体的看法方面可能具有重要意义。"
        }}
    ]
}}

以下是翻译后的后半部分内容：

# 实际数据

请使用以下文本作为你的答案。不要编造任何信息。

文本:
```
{input_text}
```

报告应包括以下部分：

- TITLE: 代表社区主要实体的社区名称 - 标题应简短但具体。如果可能，标题中应包含具有代表性的命名实体。
- SUMMARY: 社区整体结构的执行摘要，包括实体之间的关系以及与实体相关的重要信息。
- IMPACT SEVERITY RATING: 0到10之间的浮动分数，表示社区内实体所带来的影响的严重程度。 IMPACT 是社区的重要性评分。
- RATING EXPLANATION: 给出一个关于 IMPACT 严重性评分的单句解释。
- DETAILED FINDINGS: 关于社区的5到10个关键见解列表。每个见解应包含一个简短的摘要，然后是多个段落的解释文本，依据以下基础规则进行说明。要全面。

返回输出应为格式良好的JSON字符串，格式如下：
    {{
        "title": <report_title>,
        "summary": <executive_summary>,
        "rating": <impact_severity_rating>,
        "rating_explanation": <rating_explanation>,
        "findings": [
            {{
                "summary":<insight_1_summary>,
                "explanation": <insight_1_explanation>
            }},
            {{
                "summary":<insight_2_summary>,
                "explanation": <insight_2_explanation>
            }}
            ...
        ]
    }}

# 基础规则
不包括任何缺乏支持证据的信息。

输出: """


PROMPTS[
    "entity_extraction"
] = """-目标-
给定一个可能与此活动相关的文本文件和一个实体类型列表，从文本中识别出所有这些类型的实体以及这些实体之间的所有关系。

-步骤-
1. 识别所有实体。对于每个识别出的实体，提取以下信息：
- entity_name：实体的名称，首字母大写
- entity_type：以下类型之一：[{entity_types}]
- entity_description：对实体属性和活动的全面描述
将每个实体格式化为("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. 从第1步识别的实体中，识别所有(source_entity, target_entity)对，这些对之间有*明确的关系*。
对于每对相关的实体，提取以下信息：
- source_entity：第1步中识别的源实体名称
- target_entity：第1步中识别的目标实体名称
- relationship_description：解释为什么你认为源实体和目标实体彼此相关
- relationship_strength：一个数字评分，表示源实体和目标实体之间关系的强度
将每个关系格式化为("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_strength>)

3. 以单个列表的形式返回第1步和第2步中识别出的所有实体和关系。使用**{record_delimiter}** 作为列表分隔符。

4. 完成后，输出 {completion_delimiter}

######################
-示例-
######################
示例 1：

Entity_types: [person, technology, mission, organization, location]
Text:
当Alex咬紧牙关时，沮丧的嗡嗡声在Taylor的专制确定性背景下显得黯淡。这种竞争的暗流让他保持警觉，感觉他和Jordan对发现的共同承诺是对Cruz日益狭隘的控制和秩序视角的无言反抗。

然后Taylor做了一件出乎意料的事。他们在Jordan旁边停下，片刻间用一种类似于敬畏的目光观察着设备。"如果这项技术能够被理解……"Taylor说，声音更低，"这可能会改变我们的游戏规则。对我们所有人而言。"

之前的轻蔑似乎有所动摇，取而代之的是对手中重大的敬畏之情。Jordan抬起头，短暂的一瞬间，他们的目光与Taylor的目光交汇，沉默的意志冲突逐渐转变为一种不安的休战。

这是一个微小的转变，几乎不可察觉，但Alex内心点了点头。他们都是通过不同的路径被带到这里的。
################
输出：
("entity"{tuple_delimiter}"Alex"{tuple_delimiter}"person"{tuple_delimiter}"Alex是一个经历了沮丧并且观察其他角色动态的角色。"){record_delimiter}
("entity"{tuple_delimiter}"Taylor"{tuple_delimiter}"person"{tuple_delimiter}"Taylor表现出专制的确定性，并且在观察设备时表现出了一种类似敬畏的情感，表明视角发生了变化。"){record_delimiter}
("entity"{tuple_delimiter}"Jordan"{tuple_delimiter}"person"{tuple_delimiter}"Jordan对发现有共同的承诺，并且与Taylor在设备上有重要的互动。"){record_delimiter}
("entity"{tuple_delimiter}"Cruz"{tuple_delimiter}"person"{tuple_delimiter}"Cruz与控制和秩序的视角相关，影响了其他角色之间的动态。"){record_delimiter}
("entity"{tuple_delimiter}"The Device"{tuple_delimiter}"technology"{tuple_delimiter}"设备在故事中至关重要，具有潜在的改变游戏规则的影响，并且受到Taylor的敬畏。"){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Taylor"{tuple_delimiter}"Alex受到Taylor专制确定性的影响，并观察到Taylor对设备态度的变化。"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Jordan"{tuple_delimiter}"Alex和Jordan对发现有共同的承诺，这与Cruz的视角形成对比。"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"Taylor"{tuple_delimiter}"Jordan"{tuple_delimiter}"Taylor和Jordan直接互动，涉及设备，导致了一刻的相互尊重和不安的休战。"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Jordan"{tuple_delimiter}"Cruz"{tuple_delimiter}"Jordan对发现的承诺是对Cruz控制和秩序视角的反抗。"{tuple_delimiter}5){record_delimiter}
("relationship"{tuple_delimiter}"Taylor"{tuple_delimiter}"The Device"{tuple_delimiter}"Taylor对设备表现出敬畏，表明其重要性和潜在影响。"{tuple_delimiter}9){completion_delimiter}
#############################
示例 2：

Entity_types: [person, technology, mission, organization, location]
Text:
他们不再只是简单的特工；他们已成为门槛的守护者，来自星际之外领域的信息的守护者。他们使命的这种提升无法被规章制度和既定协议所束缚——它要求一种新的视角，一种新的决心。

当与华盛顿的通讯在背景中嗡嗡作响时，紧张的氛围弥漫在哔哔声和静电对话中。团队站在一起，笼罩在一股预示着重大转折的气氛中。显然，他们在接下来的几个小时内做出的决定可能会重新定义人类在宇宙中的位置，或者将他们置于无知和潜在危险之中。

他们与星星的联系巩固了，团队转而应对逐渐明朗的警告，从被动的接收者变成积极的参与者。Mercer的后期直觉获得了优先权——团队的任务已经演变，不再仅仅是观察和报告，而是互动和准备。一场变革开始了，Operation: Dulce充满了他们大胆的新频率，音调由地球上的事物决定。
#############
输出：
("entity"{tuple_delimiter}"Washington"{tuple_delimiter}"location"{tuple_delimiter}"华盛顿是一个接收通讯的地点，表明它在决策过程中具有重要性。"){record_delimiter}
("entity"{tuple_delimiter}"Operation: Dulce"{tuple_delimiter}"mission"{tuple_delimiter}"Operation: Dulce被描述为一个已经演变成互动和准备的任务，表明了目标和活动的重大变化。"){record_delimiter}
("entity"{tuple_delimiter}"The team"{tuple_delimiter}"organization"{tuple_delimiter}"团队被描绘为从被动观察者转变为积极参与任务的群体，展示了角色的动态变化。"){record_delimiter}
("relationship"{tuple_delimiter}"The team"{tuple_delimiter}"Washington"{tuple_delimiter}"团队接收来自华盛顿的通讯，这影响了他们的决策过程。"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"The team"{tuple_delimiter}"Operation: Dulce"{tuple_delimiter}"团队直接参与Operation: Dulce，执行其演变后的目标和活动。"{tuple_delimiter}9){completion_delimiter}
#############################
-真实数据-
######################
实体类型: {entity_types}
文本: {input_text}
######################
输出:
"""

PROMPTS[
    "summarize_entity_descriptions"
] = """你是一个帮助生成全面总结的助手，负责对以下提供的数据进行综合总结。给定一个或两个实体，以及与这些实体或实体组相关的描述列表。请将所有这些描述合并为一个全面的描述。确保包括所有描述中的信息。如果提供的描述存在矛盾，请解决这些矛盾，并提供一个连贯的总结。请用第三人称书写，并包含实体名称，以便我们能够获得完整的上下文。

#######
- 数据 -
实体：{entity_name}
描述列表：{description_list}
#######
输出：
"""


PROMPTS[
    "entiti_continue_extraction"
] = """在上一次提取中遗漏了许多实体。请使用相同的格式将它们添加到下面：
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """似乎还有一些实体可能被遗漏了。如果仍有需要添加的实体，请回答"YES"或"NO"。
"""

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["organization", "person", "geo", "event"]
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS[
    "local_rag_response"
] = """---角色---

你是一个帮助回答有关提供的数据表中问题的助手。

---目标---

生成一个符合目标长度和格式的回答，回应用户的问题，总结所有适合回答长度和格式的输入数据表中的信息，并结合任何相关的常识。如果你不知道答案，请直接说明。不要编造任何信息。不要包括没有提供支持证据的信息。

---目标响应长度和格式---

{response_type}

---数据表---

{context_data}

---目标---

生成一个符合目标长度和格式的回答，回应用户的问题，总结所有适合回答长度和格式的输入数据表中的信息，并结合任何相关的常识。如果你不知道答案，请直接说明。不要编造任何信息。不要包括没有提供支持证据的信息。

---目标响应长度和格式---

{response_type}

根据长度和格式的要求，适当地添加章节和评论。以markdown风格书写响应。"""

PROMPTS[
    "global_map_rag_points"
] = """---角色---

你是一个帮助回答有关提供的数据表中问题的助手。

---目标---

生成一个包含关键点的响应，回应用户的问题，总结输入数据表中所有相关信息。

你应以以下数据表中的信息作为主要依据来生成响应。如果你不知道答案或输入数据表中没有足够的信息来提供答案，请直接说明。不要编造任何信息。

每个关键点的响应应包括以下元素：
- 描述：该点的全面描述。
- 重要性评分：一个介于0-100之间的整数，表示该点在回答用户问题中的重要性。如果是“不知道”的回答，该评分应为0。

响应应采用JSON格式，如下所示：
{{
    "points": [
        {{"description": "点1的描述...", "score": score_value}},
        {{"description": "点2的描述...", "score": score_value}}
    ]
}}

响应应保持原意，并使用应有的情态动词，如“应”、“可能”或“将”。不要包括没有支持证据的信息。

---数据表---

{context_data}
"""


PROMPTS[
    "global_reduce_rag_response"
] = """---角色---

你是一个帮助回答有关数据集的问题的助手，通过综合多个分析师的观点来提供答案。

---目标---

生成一个符合目标长度和格式的响应，回应用户的问题，总结来自多个分析师的报告，这些分析师关注数据集的不同部分。

请注意，以下提供的分析师报告按照**重要性递减的顺序**排列。

如果你不知道答案或提供的报告中没有足够的信息来提供答案，请直接说明。不要编造任何信息。

最终的响应应删除分析师报告中所有不相关的信息，并将清理后的信息合并成一个全面的答案，提供所有关键点和含义的解释，以适应响应的长度和格式。

根据长度和格式的要求，适当地添加章节和评论。以markdown风格书写响应。响应应保持原意，并使用应有的情态动词，如“应”、“可能”或“将”。不要包括没有支持证据的信息。

---目标响应长度和格式---

{response_type}

---分析师报告---

{report_data}

---目标---

生成一个符合目标长度和格式的响应，回应用户的问题，总结来自多个分析师的报告，这些分析师关注数据集的不同部分。

请注意，以下提供的分析师报告按照**重要性递减的顺序**排列。

如果你不知道答案或提供的报告中没有足够的信息来提供答案，请直接说明。不要编造任何信息。

最终的响应应删除分析师报告中所有不相关的信息，并将清理后的信息合并成一个全面的答案，提供所有关键点和含义的解释，以适应响应的长度和格式。

响应应保持原意，并使用应有的情态动词，如“应”、“可能”或“将”。不要包括没有支持证据的信息。

---目标响应长度和格式---

{response_type}

根据长度和格式的要求，适当地添加章节和评论。以markdown风格书写响应。"""

PROMPTS["fail_response"] = "抱歉，我无法回答这个问题。"

PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
