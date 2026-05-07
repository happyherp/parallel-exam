# AI-Assisted Exam Variant Generation (education-15-01029)

*Source: education-15-01029.xml (MDPI Education Sciences journal)*

---

# AI-Assisted Exam Variant Generation: A Human-in-the-Loop Framework for Automatic Item Creation

**Authors:** Charles MacDonald Burke

**Authors:** Rachel Vannatta; Audrey Conway Roberts

## Abstract

Educational assessment relies on well-constructed test items to measure student learning accurately, yet traditional item development is time-consuming and demands specialized psychometric expertise. Automatic item generation (AIG) offers template-based scalability, and recent large language model (LLM) advances promise to democratize item creation. However, fully automated approaches risk introducing factual errors, bias, and uneven difficulty. To address these challenges, we propose and evaluate a hybrid human-in-the-loop (HITL) framework for AIG that combines psychometric rigor with the linguistic flexibility of LLMs. In a Spring 2025 case study at Franklin University Switzerland, the instructor collaborated with ChatGPT (o4-mini-high) to generate parallel exam variants for two undergraduate business courses: Quantitative Reasoning and Data Mining. The instructor began by defining “radical” and “incidental” parameters to guide the model. Through iterative cycles of prompt, review, and refinement, the instructor validated content accuracy, calibrated difficulty, and mitigated bias. All interactions (including prompt templates, AI outputs, and human edits) were systematically documented, creating a transparent audit trail. Our findings demonstrate that a HITL approach to AIG can produce diverse, psychometrically equivalent exam forms with reduced development time, while preserving item validity and fairness, and potentially reducing cheating. This offers a replicable pathway for harnessing LLMs in educational measurement without sacrificing quality, equity, or accountability.

**Keywords:** artificial intelligence, large language models, human-in-the-loop, automatic item generation, AI assisted assessment, cheating, prompt engineering, educational measurement, psychometric validation, bias mitigation

## 1. Introduction

Educational assessment remains a cornerstone of teaching and learning, shaping how educators gauge student understanding, track progress, and inform pedagogical strategies (Drasgow et al., 2006; Reeves, 2003). Historically, assessment design involved manually crafting test items that evaluate student knowledge in fair, consistent, and reliable ways (Bormuth, 1969). However, this manual approach presents significant practical challenges, especially in contexts involving large classes, frequent testing, take-home exams, or standardized exam formats (Song et al., 2025). Instructors must create numerous questions and parallel exam forms, each calibrated for difficulty and aligned with specified learning objectives (Song et al., 2025; Gierl & Haladyna, 2012). This process demands considerable time, subject matter expertise, and psychometric knowledge, resources that are often limited in educational settings balancing rigorous assessment standards with heavy teaching and administrative loads (Drasgow et al., 2006).

Automatic item generation (AIG) emerged in response to these challenges, utilizing algorithmic templates to efficiently produce large sets of test question variants (Gierl & Haladyna, 2012). These templates systematically vary certain components (e.g., numerical values, scenarios, contexts) to create multiple unique yet psychometrically equivalent items (Gierl & Haladyna, 2012). For instance, a mathematics problem template may generate variants by altering specific numbers or contextual details, ensuring each student encounters a different but comparable problem (Gierl & Haladyna, 2012). AIG offers scalability and consistency, which is particularly valuable in standardized testing environments requiring extensive item pools and form equivalence (Gierl & Haladyna, 2012). Despite its benefits, traditional AIG requires substantial initial investment in psychometric expertise and technical skill (Song et al., 2025). Educators must define explicit item models, the variables (parameters) that determine item difficulty, and implement algorithms to systematically vary these parameters (Drasgow et al., 2006; Gierl & Haladyna, 2012). This complexity poses a barrier to broad adoption, especially for educators without programming backgrounds or specialized psychometric training (Song et al., 2025). Consequently, while AIG holds promise for large-scale and standardized assessments, its steep learning curve has limited its use in classrooms outside of specialized testing organizations (Gierl & Haladyna, 2012).

In parallel, recent advances in artificial intelligence (particularly the rise of large language models (LLMs) like ChatGPT, Gemini, Claude, etc.) have opened new pathways for generating educational content dynamically and interactively (Kasneci et al., 2023). These conversational AI systems can interpret and generate natural language, allowing educators to describe assessment needs in plain language and receive generated items in return (Fernández et al., 2024). For example, an instructor can conversationally specify an assessment scenario, item format, and difficulty criteria, and the LLM will rapidly produce tailored questions (Fernández et al., 2024). This approach dramatically lowers the barrier to item creation for those lacking coding skills, effectively democratizing the more technical aspects of AIG (Khademi, 2023). Early explorations have found that LLM-based methods can indeed produce plausible test questions, complete with distractors and solutions, in a fraction of the time of manual writing (Circi et al., 2025). However, using AI in assessment design also introduces new concerns (Bulut et al., 2024). Without careful oversight, AI-generated items may contain factual inaccuracies, ambiguous wording, unrealistic scenarios, or embedded biases, thereby undermining test fairness and validity (Belzak et al., 2023). Moreover, LLMs generate content based on patterns in their training data; as a result, they can reproduce societal biases or hallucinate information with fluency (Belzak et al., 2023). Educators who rely on automated item generation without safeguards and validation checks risk presenting students with confusing or erroneous questions (Belzak et al., 2023). Indeed, recent systematic reviews highlight issues such as unintended difficulty shifts and stereotype perpetuation in AI-created items, emphasizing the ethical stakes of unvetted AI usage in testing (Yaneva & von Davier, 2023).

Against this background, one where traditional AIG offers rigorous parallel forms but demands technical expertise, and AI-driven methods offer convenience but pose validity risks, there is a clear need for an integrated hybrid framework (Tan et al., 2024). Such an approach would harness the strengths of both: the meticulous psychometric control of human-developed item templates and the flexibility and speed of LLM-based generation (Tan et al., 2024). Crucially, a hybrid framework explicitly positions the educator as a central “human-in-the-loop” (HITL) (Diyab et al., 2025). Rather than fully automating test creation, the AI is used to accelerate content generation while the human expert retains critical decision-making authority over item selection, difficulty calibration, bias review, and quality assurance (Diyab et al., 2025). In short, human oversight at key points (item modeling, reviewing AI outputs, and editing or discarding problematic items) is essential and cannot be eliminated (Falcão et al., 2022).

This article presents a case study of such a hybrid AIG approach, implemented in the Spring semester of 2025 at Franklin University Switzerland. In this study, the instructor interactively collaborated with an LLM (ChatGPT’s o4-mini-high model) to generate multiple exam variants for two undergraduate business courses (Quantitative Reasoning and Data Mining). The process began with explicit parameterization: instructors predefined the variables influencing item difficulty (referred to as “radicals”) and those representing superficial variations (“incidentals”) to guide AI generation. Throughout, the instructor performed vital validation checks, refining or correcting the AI’s outputs whenever necessary. Notably, the instructor intervened to address the practical issues that arose, such as clarifying ambiguous timeframes (where the AI had suggested broad intervals instead of precise dates) and adjusting unrealistic numerical criteria (where the AI proposed thresholds that yielded no usable data) during item generation.

These swift interventions by human expertise prevented potential student confusion, ensured realistic and fair item conditions, and safeguarded the validity of the assessments. The hybrid workflow also included meticulous documentation by the educator, including the prompt parameters, chat transcripts, and item revisions, all of which form an auditable trail that promotes transparency and reproducibility in the test design process. Beyond resolving immediate technical and ethical issues, the approach fundamentally reshapes educators’ roles in assessment design: rather than acting solely as an item writers or programmers, educators in this HITL framework become “parameter stewards” and “validity auditors,” focusing on higher-order pedagogy, assessment oversight, and ethical considerations. This paradigm leverages AI for efficiency and scale while reaffirming educators’ central authority in maintaining test quality and equity.

In the following sections, this article reviews relevant literature on AIG and AI in assessment, describes the conceptual foundations of the human-in-the-loop approach, details the case study implementation and its outcomes, and discusses implications for educators and possible future implications for standardized testing. By bridging psychometric rigor with AI innovation, the aim is to demonstrate a balanced, pragmatic path forward for standardized test development—one that empowers educators to harness AI capabilities effectively while upholding fairness, validity, and inclusivity.

## 2. Literature Review

### 2.1. Automatic Item Generation (AIG) and Challenges

AIG is an approach to educational assessment that systematically produces multiple test items to create multiple exam variants from algorithmic templates (Gierl & Haladyna, 2012). Grounded in cognitive and psychometric theories, traditional AIG methods seek to generate large banks of items that are psychometrically equivalent yet diverse in surface features, enhancing test security and reducing item exposure (Bormuth, 1969). The core of AIG is the construction of item models—structured templates containing both fixed components and variable parameters (Gierl & Haladyna, 2012). By altering these parameters, many unique items can be generated while targeting the same skills and difficulty level (Gierl & Haladyna, 2012). A key concept in AIG is distinguishing between “radical” and “incidental” parameters. Radicals are the elements of a question that directly affect its cognitive demand or difficulty (e.g., the numerical values or problem type), whereas incidentals are superficial context details that can vary without affecting difficulty (like the name of a city or day of the week) (Gierl & Haladyna, 2012). Rigorous identification and manipulation of radicals ensure that all generated items remain equivalent in difficulty, while varying incidentals provides uniqueness and reduces the chance of cheating (Gierl & Haladyna, 2012).

Despite clear advantages in efficiency and consistency, traditional AIG has faced significant barriers to wide adoption. Developing high-quality item models requires extensive psychometric expertise and domain-specific knowledge (Circi et al., 2025). Crafting the algorithms or code to automate production of these models often demands advanced programming skills, limiting AIG’s accessibility for many educators (Song et al., 2025). In a typical classroom and even some standardized testing contexts, few teachers have the training or time to design such complex systems from scratch. As a result, the use of classical AIG has largely been confined to specialized assessment teams or researchers, rather than everyday classroom teachers (Gierl & Haladyna, 2012).

### 2.2. Large Language Models (LLMs) in Assessment

Recent developments in AI have introduced new possibilities for item generation. LLMs produce coherent, contextually relevant, and sophisticated text by leveraging knowledge from vast training datasets (Kasneci et al., 2023). In educational settings, LLMs have demonstrated the ability to draft plausible test questions, generate realistic distractors, rephrase prompts at different reading levels, and even explain concepts in simple terms (Fernández et al., 2024; Khademi, 2023). Crucially, these models can be guided through natural-language prompts rather than code, allowing educators without programming skills to engage in automatic item generation by “talking” to an AI (Fernández et al., 2024). This conversational interface dramatically lowers the barrier to entry, effectively democratizing AIG for a broader range of users (Kasneci et al., 2023).

Empirical studies are beginning to explore the potential of LLM-driven item generation. For instance, Bulut et al. (2024) illustrate that items produced by LLMs often exhibit high linguistic clarity and adaptability to different contexts, substantially reducing the manual workload of item writing. Likewise, Andersson and Picazo-Sanchez (2023) achieved success in using AI to automatically generate distractor options for language tests, highlighting the broad applicability of LLM-generated content across various subject areas. Furthermore, Kiyak et al. (2023) demonstrated the effectiveness of LLMs in creating viable clinical scenario questions for medical education, with the AI-generated items (after expert review) showing psychometric properties comparable to traditionally authored items. These examples across domains (measurement, language testing, medical education) underscore the wide-ranging potential of LLMs to support assessment development.

### 2.3. Limitations of AI-Only Item Generation

Notwithstanding their promise, LLMs used in isolation have notable limitations (Belzak et al., 2023). Common issues include shifts in difficulty level (an AI might simplify or complicate word problems unpredictably), factual inaccuracies or hallucinations (confidently presenting incorrect answers as correct), and subtle biases reflecting the data the model was trained on (providing examples not broadly understood across demographics, for example) (Belzak et al., 2023). Recent evaluations of automatically generated exam items have indeed identified concerns with item quality and usability that necessitate human quality assurance (Tan et al., 2024). For example, Fernández et al. (2024) found that while AI could generate and even score chemistry exam questions, the items still required expert vetting to ensure correctness and appropriate difficulty. These risks raise serious ethical and practical concerns if AI-generated content were to be used unchanged in high-stakes tests (Belzak et al., 2023). Presently, purely AI-generated assessments, without human modification, often fall short of the reliability and fairness standards expected in standardized testing (Belzak et al., 2023). As Bulut et al. emphasize, rigorous human oversight and validation are necessary to implement AI-generated items responsibly (Bulut et al., 2024).

### 2.4. Emergence of Hybrid AIG–AI Frameworks

To capitalize on AI’s benefits while mitigating its drawbacks, hybrid frameworks have been proposed that combine traditional AIG principles with LLM-based generation (Song et al., 2025). In these approaches, educators first establish clear item-model parameters and define radicals explicitly, as in classical AIG, to set the boundaries for item difficulty and content (Drasgow et al., 2006; Bormuth, 1969). Within those boundaries, LLMs are employed to generate variations and wording, providing speed and linguistic creativity (Chan et al., 2025). This hybrid strategy maintains essential psychometric controls (through human-defined parameters) while dramatically reducing the technical overhead for educators, since interaction with the AI is via natural language rather than code, and the output of several dozen parallel forms (or more) can be automated by the AI (Song et al., 2025; Tan et al., 2024). Conceptually, such frameworks promise the “best of both worlds”, making advanced item generation techniques accessible to non-programmer educators without sacrificing measurement principles (Chan et al., 2025).

However, despite their theoretical appeal, these hybrid methods are only beginning to be documented in the literature. Early discussions outline the potential advantages of combining human expertise with AI generation, but concrete empirical guidance on workflows and best practices remains limited (Song et al., 2025). In other words, the idea of human-in-the-loop item generation is recognized as promising, yet detailed implementations in case studies are sparse. Tan et al., for example, note that more research is needed to provide educators with structured frameworks for effectively leveraging LLMs in assessment while maintaining rigorous oversight (Tan et al., 2024). Preliminary reports that do exist consistently underscore one critical element: explicit human oversight must be at the core of any AI-integrated assessment design. Educators often need to intervene to correct AI outputs by adjusting unrealistic scenarios, fixing errors, or refining content to better match learning objectives. Without such intervention, AI-generated items can drift off target or introduce issues that undermine their utility (Belzak et al., 2023).

In sum, the literature suggests that while AI can greatly assist item generation, it is not a substitute for the educator’s role. Instead, a thoughtfully designed human-in-the-loop (HITL) process is essential to ensure that the resulting assessments uphold psychometric quality, relevance, and equity. This article contributes to that evolving body of knowledge by providing a detailed case study of implementing a HITL approach to AIG, illustrating how theory can translate into practice. It offers practical guidance and potential pitfalls for non-technical teachers hoping to leverage LLMs to create parallel classroom assessments, or to the standardize testing organizations that need to create and refresh exam variants to ensure fairness and reduce cheating.

## 3. Materials and Methods

### 3.1. Human-in-the-Loop Automatic Item Generation

The human-in-the-loop (HITL) framework originated in the field of machine learning, where human intervention in the machine learning process was integrated by design (Munro, 2021). In general, the HITL approach explicitly acknowledges the complementary strengths and limitations of human experts and machines, and the development process is structured so that humans actively guide, oversee, and/or correct the machine’s contributions (Tan et al., 2024; Malik & Terzidis, 2025). In other words, rather than viewing machine learning as autonomous, HITL frameworks treat a machine as a tool operating under human supervision (Munro, 2021; Malik & Terzidis, 2025). The goal of HITL approaches is to ensure that the efficiency gains of machine learning do not come at the expense of quality, fairness, or theoretical soundness (Belzak et al., 2023). Applying the HITL framework to automatic item generation (AIG) is especially promising, representing the opportunity for significant advancement in assessment design, particularly in the context of generating multiple standardized test variants augmented by AI (Song et al., 2025; Tan et al., 2024).

Motivated by AI efficiency yet recognizing the need for human oversight in standardized testing, this article hopes to articulate a more structured framework to human-in-the-loop automatic item generation than those found in previous studies. A detailed conceptual framework, a case study employing HITL, and a discussion of the potential implications of adopting a HITL approach to AIG comprise the following sections.

### 3.2. Defining Item Parameters

Central to the HITL framework is educators starting with clear learning assessment goals and active management of item-model parameters, the key variables that control item difficulty and content (Bormuth, 1969; Gierl & Haladyna, 2012). Drawing on classical psychometric theory, these parameters include both “radicals” (features that directly influence item difficulty or cognitive demand) and “incidentals” (features that can vary without affecting difficulty) (Gierl & Haladyna, 2012). At the outset of item development, educators using HITL must explicitly define these parameters for the LLM based on the learning objectives and desired difficulty range (Tan et al., 2024). For example, if the goal is to generate parallel math word problems, the instructor may prompt radicals as a specific range of numerical values or the type of mathematical operation required, whereas incidentals might be the names of people or places in the problem context (Gierl & Haladyna, 2012). By providing the AI with this structured blueprint of what can change and what must remain consistent, the human expert sets boundaries for output generation.

This step is fundamental: it encodes human judgment about what makes items equivalent or different in difficulty, thereby guarding against the AI inadvertently altering the challenge level or focus of the items (Diyab et al., 2025). In our case study, this meant the instructors pre-specified things like exact data ranges for analysis problems and threshold values for dataset filtering (the radicals) before any AI generation began.

### 3.3. Iterative Educator–AI Interactions

Once parameters are set, the HITL framework envisions an iterative cycle of exam generation and review (Diyab et al., 2025). As specified above, educators first use conversational prompts to instruct the LLM on what kind of item to produce, including any required context or constraints (Fernández et al., 2024). The AI then generates a draft item (or several), adhering to the given parameters (Fernández et al., 2024). Next, the educator critically reviews the AI-generated output for alignment with the intended learning outcome, clarity, difficulty, and fairness (Belzak et al., 2023). If the item is acceptable, it can move forward; if not, the educator provides feedback or adjustments to the AI and regenerates the affected items (Chan et al., 2025). This iterative loop continues until the item meets the quality standards of the instructor (Tan et al., 2024).

The necessity of continual human oversight in this process loop cannot be overstated. Unlike a fully automated system that might generate output en masse without human intervention, the HITL approach expects deviations and imperfections in AI output to be caught and corrected by the human expert in real-time (Bulut et al., 2024). These deviations can take many forms: an AI-generated question might use an unrealistic scenario, contain an ambiguity in phrasing, or assume knowledge outside the scope of the course (Bulut et al., 2024). For instance, if an AI suggests a data analysis question with an implausible parameter (like requiring analysis of a variable in a dataset that does not exist), the educator will spot this and adjust the prompt or parameters accordingly.

Prior studies have documented exactly such scenarios, reinforcing the importance of the human’s role (Fernández et al., 2024; Khademi, 2023; Belzak et al., 2023). For example, educators have had to intervene and modify AI-suggested numerical thresholds or context details to ensure the resulting items were realistic and pedagogically meaningful (Fernández et al., 2024). Likewise, maintaining the quality of multiple-choice distractors often requires human refinement; an AI might generate distractor options that are too obviously wrong or not conceptually aligned, prompting the educator to tweak or replace them (Tan et al., 2024). These iterative adjustments, guided by an educator’s domain knowledge and pedagogical intent, are at the heart of the HITL framework (Malik & Terzidis, 2025).

### 3.4. Bias and Fairness Oversight

Another crucial dimension of the HITL framework is proactive bias detection and the promotion of equity in generated items. AI systems like LLMs carry the risk of perpetuating biases present in their training data (Malik & Terzidis, 2025; Wing, 2021). Such biases can manifest in subtle ways—for instance, in the language or examples an AI uses (perhaps consistently favoring certain cultural contexts or gender roles) or in which content it emphasizes (Wing, 2021). Therefore, effective HITL implementation requires educators to be vigilant in identifying these biases and to enforce fairness standards throughout item development (Burstein & LaFlair, 2024). This can involve conducting systematic bias reviews of AI-generated content, seeking diverse perspectives to catch insensitive or non-inclusive material, and employing more sophisticated techniques like differential item functioning (DIF) analysis to statistically check that items do not favor one group of students over another (Belzak et al., 2023).

In practice, this means if the AI generates an item scenario that might be culturally specific or unfamiliar to some student groups, the educator will recognize this and modify the context to be more neutral or inclusive (Burstein & LaFlair, 2024). For example, suppose an AI-created a word problem that references an activity predominantly known in one culture; the educator might change it to a more universal context or offer a variety of contexts across items.

For instance, an AI initially could produce a data analysis question referencing a local baseball team’s statistics—a context that could disadvantage students unfamiliar with the sport. Recognizing the cultural specificity, the educator can intervene with a revised prompt:

*“Generate a similar data analysis problem using a globally familiar context (such as weather data or soccer data) instead of baseball, to ensure the scenario is accessible to all students regardless of cultural background.”*

Such an adjustment can help maintain inclusivity, removing a potential source of bias from the item.

Beyond context, the educator also checks that language is free of stereotypes or assumptions (e.g., using gender-neutral names and pronouns across items, or avoiding examples that might reinforce stereotypes). Every AI-generated item in the HITL process should be scrutinized not only for content accuracy, but also for cultural sensitivity and equal difficulty, aligning with principles of fairness and inclusive design (Burstein & LaFlair, 2024).

While human oversight inherently carries the risk of instructor biases, the transparency provided by detailed, iterative documentation greatly facilitates the identification and correction of such biases. We explicitly recommend the integration of collaborative reviews or peer-validation mechanisms as best practices to further mitigate the potential impact of individual instructor bias during the AI-assisted item generation process.

### 3.5. Preventing and Correcting AI “Hallucinations”

A related ethical concern is the AI’s tendency to sometimes generate factually incorrect or nonsensical information, known as hallucinations (Ji et al., 2023). In a testing context, an AI might fabricate a statistic, invent an author or study as part of a reading comprehension question, or suggest an implausible scenario. Following the HITL framework, educators must verify that any factual content introduced by the AI is accurate and relevant. If the AI references external information (e.g., a historical event or a dataset characteristic), the educator checks it against reliable sources or replaces it with a factually correct premise. This is especially important in subjects like medicine, where hallucinated exam scenarios and erroneous facts can have real world consequences (Falcão et al., 2022).

For example, when constructing a finance exam an LLM may confidently generate a scenario stating the following:

*“In 2024, Tesla stock experienced a single-day drop of 30% after a major product recall.”*

Suspecting this event was fabricated, the instructor investigates and finds no record of such an occurrence. Realizing the AI has introduced unsupported context, the educator then would correctly prompt the LLM to use a verified historical event:

*“Replace the scenario with a real event—for example, use the February 20, 2025, Cybertruck product recall incident where Tesla’s stock dropped about 3%—ensuring all details are factual and can be verified.”*

By revising the item to be based on a real event with accurate figures, the educator eliminates the AI’s hallucination and maintains the integrity of the assessment content. Each time the AI automatically generates a test item, the educator should treat it as a draft subject to verification, rather than a fully automated process (Burstein & LaFlair, 2024). Ideally, misleading or erroneous content should either be fixed or removed before any student ever sees the item. Therefore, in practice, the number of items and exam variants should be kept to small batches, as human fact-checking is labor-intensive but essential. This ensures that students are not presented with false information at all, and that each instruction or scenario in the assessment is credible and educationally appropriate. Over time, an experienced educator can also learn to prompt the AI in ways that reduce hallucinations. For instance, Anthropic instructs users to prompt its Claude LLM to limit itself to certain data sources, explain its reasoning, and admit its lack of knowledge to limit hallucinations (Anthropic, 2025). Nonetheless, final responsibility for accuracy lies with the human-in-the-loop.

### 3.6. Documentation and Transparency

Lastly, the HITL framework concludes with comprehensive documentation of the item generation process, serving multiple purposes. Every interaction between educator and AI (initial prompts, AI responses, educator feedback, item edits, and exam variants) should all be recorded and archived (Yaneva & von Davier, 2023). This could be as simple as saving chat transcripts or as structured as maintaining a log of item versions with notes on what changes were made and why. Such meticulous documentation creates an audit trail that fosters transparency and accountability. If a question’s validity is ever challenged, the development record can show exactly how the item was created and reviewed, demonstrating the due diligence applied. If an item lacks validity, generates confusion, or is in some way biased, keeping a record of how it was generated can intercept problematic future iterations.

This practice aligns with accreditation standards and institutional policies that call for transparency in assessment design processes (International Test Commission & Association of Test Publishers, 2022). Stakeholders like accreditation agencies, educational authorities, or even students have an interest in knowing that AI was used responsibly (Yaneva & von Davier, 2023). Clear records allow external reviewers to evaluate the quality control measures in place (International Test Commission & Association of Test Publishers, 2022). Moreover, documentation enables reproducibility and knowledge sharing: other educators can follow the recorded steps to replicate or adapt the item generation process for their own context. In our case study, the instructor preserved prompt templates, AI outputs, and the subsequent modifications made to create the final versions of each exam variant. These artifacts not only help track the rationale behind each item but can also serve as exemplars for training colleagues in HITL methods. In environments increasingly concerned with algorithmic accountability, the HITL approach provides reassurance that AI-generated content is not a “black box” output but the result of a controlled, reviewable process (International Test Commission & Association of Test Publishers, 2022)

### 3.7. The Human-in-the-Loop Automatic Item Generation Framework

In summary, the human-in-the-loop conceptual framework for AIG is characterized by a continuous collaboration between human expertise and AI capabilities (Gierl & Haladyna, 2012; Munro, 2021). It leverages the speed and versatility of AI while embedding rigorous human oversight to enforce theoretical soundness, fairness, and accuracy (Belzak et al., 2023). This framework redefines the role of the educator from being a sole author of test items to being a supervisor of AI augmentation, a curator who ensures that each item meets the high standards of educational assessment (Munro, 2021). Notably, the HITL approach treats key quality metrics like validity and reliability as dynamic, actively maintained properties rather than one-time achievements (Drasgow et al., 2006). Every iterative check and correction, once recorded, by the human contributes to a chain of validity evidence for the assessment (Embretson & Reise, 2000).

In the following section the framework illustrated in Figure 1 was utilized to generate exam variants that were administered to real students as part of their formal course assessment, with exams publicly available in the data repository linked below.

## 4. Results

### 4.1. Case Study and Ethical Considerations for HITL AIG

The following case study details a practical implementation of a human-in-the-loop AIG approach using a conversational LLM, highlighting concrete examples of educator interventions and ethical safeguards during the development of multiple parallel exam forms. Conducted in Spring 2025 at Franklin University Switzerland, this study was embedded in take-home exams for two undergraduate business courses (Quantitative Reasoning and Data Mining). The take-home nature of the exam context amplifies classic integrity risks: answer-sharing by screenshot, crowdsourced solutions on Q&A boards, or covert group-programming. A single paper exam variant would therefore be untenable (as even in-class exams with computer access may be), but parallel-form assessment offers a time-tested antidote to these problems. The aim was to create roughly two dozen versions of an exam with equivalent difficulty and content coverage, using AI (GPT o4 mini-high) to expedite the process while maintaining human oversight for quality control. This context provided a rich opportunity to examine both the strengths and limitations of integrating AI with human expertise in a real educational setting.

The HITL workflow utilized in this case study consisted of several key steps approximating the HITL conceptual framework detailed above. Each step illustrates the collaboration between the human instructor and the AI LLM in practical terms.

### 4.2. Initial Item-Model Parameterization

The process began with the instructor clearly defining the curricular objectives and intended learning outcomes to be assessed. Moreover, the limitations of students’ understanding and skill constraints were conveyed to the LLM in the initial prompt. From here, the instructor mapped out item-model parameters by identifying radicals and incidentals for each desired question type. For example, in the quantitative reasoning course, a target learning outcome was the ability to calculate and interpret stock price volatility over a specified period. The instructor decided that the radicals for items assessing this outcome would include the exact timeframe of data (start and end dates) and the method of volatility calculation, while incidentals were different companies’ stock tickers and the historical narrative framing the task. By explicitly delineating these parameters, the instructor set firm boundaries for the AI.

The LLM was then prompted to generate initial item variants with a detailed prompt, providing context for the AI to begin item generation for the Quantitative Reasoning course:

*“Generate a series of 26 quantitative reasoning exam variants analyzing monthly stock volatility, using real historical market crash dates from different world markets (Black Monday, Black Wednesday, etc.). Each problem must clearly specify exact start and end dates to ensure precise volatility calculation and maintain identical cognitive load across variants. Event dates and markets (NASDAQ, London Stock Exchange, NIKKEI, etc.) act as incidentals, while different methods of volatility analysis (daily standard deviation, drawdown, beta) act as radicals.*

*Students must demonstrate procedural fluency in Python 3.12.6 pandas library for accessing and analyzing stock prices, and to visualize stock volatility over time. Second, they are expected to exercise emergent statistical thinking by interpreting distributional change and articulate uncertainty in plain language rather than in formulaic jargon. Third, they must cultivate explanatory literacy, weaving narrative justifications for why they believe certain results manifested.*

*NOTE: To complete these tasks students have limited access and understanding of Python packages, accessing and using only pandas and matplotlib to manipulate, analyze, and visualize data.”*

Similarly, this is the initial prompt for the Data Mining course:

*“Draft a set of exam variants that asks students to analyze Airbnb listing data in different cities. Let the differing specified cities act as incidentals. Focus on properties listed by hosts owning multiple apartments as radicals. Provide clear instructions for identifying such properties and outline the exact quantitative metrics (*e.g.,* average price, occupancy rate) students should compute for these hosts.*

*Students should be able to apply data ingestion, cleaning, and feature-engineering techniques to extract and prepare datasets. Second, they should analyze database characteristics by implementing unions/joins and grouping to identify and compare host patterns across multiple tables. Third, students evaluate and interpret analytical results to generate actionable, data-driven recommendations for improving outcomes for Airbnb hosts and users.*

*NOTE: Students have not yet been taught to use windows functions in SQL to complete this task”*

These carefully crafted initial prompts convey specific instructions and learning goals to the LLM, ensuring that, from the outset, the AI’s output would be constrained to relevant learning objectives and student abilities. The prompts include key examples (like exact dates or variables), crucial for fairness and clarity. The initial clarity in parameter definition is foundational to establishing the rules of engagement for subsequent AI-generated content.

### 4.3. AI Generation and HITL AIG Iteration: Addressing Ambiguities

With the parameters in place, the LLM generated draft items. While many were on-target, the instructor had to remain vigilant for any ambiguities or deviations. LLMs tend to “drift” when performing multiple tasks (Embretson & Reise, 2000). When generating several dozen or more exam variants, each with its own unique set of items, some output drift is to be expected, and the human-in-the-loop must remain vigilant. One significant issue that arose in an early variant was temporal ambiguity.

In response to the above prompt about stock volatility, the AI produced an item stem in one exam variant that read:

*“Calculate and compare Tesla’s volatility between 2020–2021.”*

This phrasing was problematic, students could interpret “between 2020–2021” analysis in various ways (yearly? quarterly? monthly?), and it lacked a clear focus on a key event date, something stipulated in the initial prompt. Such ambiguity could lead to inconsistent interpretations and threaten the fairness of the item. As this variant was generated, in the chat, in real-time, recognizing the vagueness (no specific dates or timeframe), the instructor paused generation and supplied a refined prompt:

*“Moving forward, specify a precise 30-day period for the volatility calculation. For example: Using daily closing prices, calculate Tesla’s stock volatility from 8 September 2020, through 8 October 2020. Clearly indicate 8 September 2020, as the starting event date and use exactly a 30-day period of analysis. Specify the method of analyzing volatility (*e.g.,* daily standard deviation) in the variant’s instructions.”*

With this adjustment, the AI regenerated the item stem to the following:

*“Using daily closing prices between 8 September 2020 and 8 October 2020, calculate the volatility of Tesla’s stock (defined as the standard deviation of daily returns), speculate, and discuss the result.”*

The revision removed any ambiguity about the timeframe and calculation method, resulting in a clear and uniform task for all students. This example underscores how human oversight catches subtle issues (like an imprecise date range) that an AI, focused on linguistic patterns, might not recognize as critical.

Such interventions proved indispensable. Although the AI’s linguistic fluency and speed were tremendous assets, only the human expert could ensure that items made practical sense in context and adhered to a specific event date across all exam variants. By clarifying the temporal parameter, the instructor safeguarded the item’s validity. Students would now all analyze a defined date, over a defined period, using a defined method of analysis. This ensured comparability of responses and alignment with the learning objective of interpreting volatility over a specific event window.

### 4.4. AI Generation and HITL Vigilance: Ensuring Feasible Data Parameters

Another notable issue emerged when the AI suggested criteria that were technically within the prompt parameters but practically infeasible. For instance, one draft item for the data mining course asked students to analyze Airbnb data with the following instruction:

*“Identify properties listed by hosts owning more than eight apartments in Austin and analyze their rental trends.”*

At first glance, this fits the earlier parameter of varying host ownership levels. However, the instructor suspected that very few (if any) hosts manage more than eight properties, meaning the criterion could yield an empty or negligible dataset for students to analyze. To verify, the instructor performed a quick statistical check on the dataset and confirmed that virtually no hosts met that extreme criterion. If left uncorrected, this item would have been frustrating or impossible for students, thus invalidating the assessment attempt.

The instructor promptly revised the prompt:

*“Adjust the threshold to hosts owning at least three apartments in Austin and ensure that this yields a substantial number of properties (for example, at least 100 listings) so students have sufficient data to analyze. For each new variant adjust the threshold for this radical within a range of owning more than one to no more than four apartments, data permitting.”*

This modification led the AI to regenerate the item as follows:

*“In the Austin Airbnb dataset, identify properties listed by hosts who own three or more apartments. Analyze how these multi-property hosts’ listings differ in average price and occupancy rate compared to single-property hosts.”*

The corrected threshold was grounded in reality and guaranteed that students would have a meaningful sample to work with, thereby preserving the item’s feasibility and fairness.

By swiftly catching the AI’s unrealistic parameter, the educator again highlighted the importance of domain knowledge and contextual awareness—qualities an AI without real world context often lacks. Not only did this intervention prevent a potential dead-end for students, but it also ensured consistency across parallel exam forms (all forms now used a viable threshold, so no group of students would inadvertently get an unsolvable or trivial task).

### 4.5. Ethical Oversight: Bias and Hallucination Checks

Throughout the item generation and refinement process, the instructor also undertook systematic ethical reviews of the AI outputs. Maintaining fairness and inclusivity was a priority. Even with well-defined parameters, AI-generated content can sometimes include subtle biases or context choices that could advantage or disadvantage certain groups of students. For example, the AI might consistently use examples featuring a particular gender or cultural context in word problems. In this case, the AI used a context that was very US-centric in a course with many international students, and it was adjusted to something more globally familiar in a revised test version.

For instance, one AI-generated question in the business context read as follows:

*“Analyze the change in retail stock prices in the 30-day holiday period following Black Friday.”*

The instructor noted that this context might not be equally familiar to all students (especially those from different countries where the term for the start of the holiday shopping period “Black Friday” is not commonly known).

To avoid any unintended cultural bias, the instructor rephrased the item prompt to a more universal scenario:

*“Analyze the monthly stock return data of NYSE retail stocks over the month of December 2021.”*

This change kept the assessment of data analysis skills intact while removing culturally specific elements that were unnecessary for the skill being tested.

In addition to bias checks, the instructor was vigilant about AI hallucinations. Every factual statement or dataset detail in an AI-generated item was cross-verified. In our case study context, the AI at one point introduced a fictitious statistic about Tesla’s stock reaching a historic high on a certain date; any such erroneous detail should either be verifiably true or removed. The instructor edited the item to omit any unnecessary factual claims. By doing so, the risk of using misleading information in the assessment was eliminated.

It is worth noting that as the instructor engaged in these reviews, prompting strategies to preempt such issues emerged, such as instructing the AI up-front:

*“Do not invent any company names, historical dates, or statistics; use only companies that can be verifiably identified as listed on the NYSE, NASDAQ, London, Hong Kong, or NIKKEI stock exchanges”*

This reduced the frequency of hallucinations in later iterations of item generation.

### 4.6. Consolidation and Optimization of Prompts

After iteratively correcting issues like ambiguous timeframes, unrealistic parameters, and any biased or incorrect content, the instructor incorporated all these lessons into optimized finalized prompts for the AI in a new chat window. The goal here was twofold: to streamline the generation of any remaining items and to document best practices for future use. Two example prompts from the optimized phase are the following:

*“Generate exam variants that clearly instructs students to calculate stock volatility for verifiably listed stocks from the NYSE, NASDAQ, London, Hong Kong, or NIKKEI stock exchanges over a specific 30-day period (provide exact start and end dates, e.g., 8 September 2020–8 October 2020, and a historical narrative). Include guidance that volatility should be computed as either the standard deviation of daily returns, beta, or VIX and ensure no ambiguity in what data or date range is required. Exams should test the following learning objectives: procedural fluency, emergent statistical thinking, and explanatory literacy; related to their analysis of the dataset provided. Avoid culturally specific references to key dates (e.g., Black Friday)”*

And:

*“Generate a series of exam questions that asks students to analyze Airbnb data across two cities (for example, Austin and Amsterdam, or Cape Town and Istanbul). Focus on comparing hosts owning between 2 and 5 properties and single owners. Before finalizing the question, use the data provided to double-check that using a threshold in this range on a particular city returns at least 100 properties in each city’s dataset to allow meaningful analysis. The question should explicitly instruct students how to identify those multi-host properties and what metrics to compute. Students should be able to join, clean, analyze and interpret results using SQL.”*

These refined prompts encapsulate the interventions made earlier: they explicitly enforce precise date ranges, realistic thresholds validated by data, multiple contexts for inclusivity, and clarity in instructions. By feeding the AI such detailed instructions, the instructor found that the subsequent outputs required minimal tweaking, as the common pitfalls had been anticipated and avoided. In effect, the paper-trail of human interventions fed back into the process, improving the AI’s performance by way of better prompting. This reflects a key insight of HITL: over time, human oversight does not just correct AI outputs; better inputs can improve the AI’s outputs by evolving the prompts and parameters based on what the human has learned about the AI’s tendencies. The result was a collection of parallel exam items that were generated much faster than if written manually, yet still met the stringent criteria for clarity, fairness, and alignment with learning outcomes.

### 4.7. Outcomes and Reflections

The HITL approach in this case study yielded several notable outcomes. First, there were substantial efficiency gains. The initial pool of item drafts was generated by the AI in a matter of minutes, something that would have taken many hours of work for an instructor writing each item from scratch. This efficiency allowed the instructor to focus more time on higher-order tasks like reviewing and refining items, rather than on the blank-page creation of each question. In practice, the instructor’s role shifted from being a “writer” to being an “editor” and quality controller of exam content. This shift was empowering. Instead of spending energy on routine question drafting, the instructor could apply their expertise more strategically—ensuring each item’s accuracy, fairness, and pedagogical alignment. This shift was a positive experience, one that aligns with the professional strengths of educators (subject knowledge and pedagogical judgment), rather than their weaknesses (writing code or endlessly rewording new exam questions).

The case study also highlighted the irreplaceable value of human judgment in the loop. Each category of issue encountered (ambiguous timeframes, infeasible data parameters, biased context, and hallucinated facts) was caught through the educator’s intervention, not by the AI (even though the LLM selected, GPT o4 mini-high, was a “reasoning model”). Without human-in-the-loop oversight, any one of these issues could have made it into a final exam, with potentially negative consequences (confused students, unfair situations, or compromised assessment validity). With the HITL approach, however, none of these flaws persisted. All exam versions delivered to students were free of ambiguity, based on real or explicitly hypothetical data (clearly indicated as such), culturally neutral, and matched in difficulty and scope. This is a strong testament to the HITL framework’s central claim: AI can accelerate assessment development, but human expertise is essential to ensure quality and ethics.

Another outcome was a deeper understanding of the scalability and resource considerations for HITL. While AI dramatically cut down initial writing time, the iterative checking and refining did require significant instructor effort. For perhaps every 15–20 min the AI spent generating exam text, the instructor spent twice as long reviewing and tweaking content. This ratio improved as the prompts were optimized (later cycles needed fewer corrections), but it underscores that HITL is not hands-off. In a standardized testing scenario requiring multiple parallel forms and very large item banks (hundreds of items), a single instructor might become a bottleneck in validation if not given adequate time or support. Our study managed with one instructor by producing only a small batch of exam variants to review, effectively limiting the oversight load. If many more exam variants or items are needed, users of the HITL approach to AIG may wish to utilize such small batches regardless of class size and the total number of variants needed. The upper limit of the number of exams that can be efficiently and effectively generated in each batch and the ratio of human oversight to LLM output needed were not tested in this study.

However, simple checklists were developed (based on recurring issues) to guide the review of each item.

These include the following:Have all numerical values and thresholds been checked for realism?Does the item statement include any implicit assumptions or ambiguities?Could any student group find the context unfamiliar or biased?

This checklist approach, along with the small batch size, made the oversight process more efficient and could be a model for larger-scale implementation. These checklists were developed based upon our specific context and would likely require customization when adapted for use in other disciplines and courses.

Ethically, the approach proved robust. Fairness and equity across items were actively maintained. Each exam variant was examined to ensure a comparable cognitive load and absence of insensitive content. In doing so, we addressed a common critique of AI in assessment: that it might inadvertently introduce bias or uneven difficulty. By design, the HITL model caught and corrected such issues, arguably leading to more equitable assessments than one might achieve under time pressure without AI (where, regardless, an instructor might not have time to thoroughly vet every item’s inclusivity for large exams).

Specifically regarding evaluating exam difficulty, a simple t-test comparison of grades from the last two Quantitative Methods (Figure 2) and Data Mining (Figure 3) class cohorts tested mean difference. Spring 2024 assessments were generated solely by the instructor, while Spring 2025 exams represent the case study, created using the HITL approach to item creation. The result was minor changes in student performance from Spring 2024 to Spring 2025, but no statistical mean difference was found across either class cohorts. (Quantitative Methods: t = 0.61, *p* = 0.55; Data Mining: t = −0.18, *p* = 0.86).

We also prioritized transparency and accountability throughout the project. All interactions with the AI were saved and compiled as a brief methodology file outlining how the exams were generated and reviewed. Students were informed in general terms that an AI was used to help generate their own unique exam variant with extensive instructor oversight to ensure quality. This transparency did not raise any concerns, and likely helped students avoid the temptation of code sharing, recognizing that each of their take-home exams were unique. By openly communicating the process, educators can build trust and normalize the idea that AI can be a part of educational practice when used carefully and ethically.

Ultimately, this case study illustrates both the practical necessity and the ethical imperative of keeping humans in the loop when deploying AI in standardized test design. The AI contribution accelerated content creation and introduced creative variations that the instructor might not have thought of (for example, the AI suggested a paired analysis of Airbnb cities across different continents, which the instructor then adopted). Yet, every step of the way, it was the human expertise that guided the AI, corrected its missteps, and ensured the final product met the rigorous standards of a fair assessment. In doing so, the hybrid approach to AIG allowed the educator to produce many variations of high-quality tests at scale (something highly relevant to standardized testing scenarios) without relinquishing control over the assessment’s integrity.

## 5. Discussion

### 5.1. Implications for Educators and Future Assessment Design

Adopting a human-in-the-loop approach to AIG, especially when using advanced AI like LLMs, carries numerous practical, pedagogical, and ethical implications for educators. As the field of educational assessment moves toward integrating AI (in line with broader trends in standardized testing innovation), understanding these implications is crucial for successful implementation. Below, we outline key takeaways and considerations for educators and institutions.

### 5.2. Transforming the Educator’s Role

Perhaps the most significant shift is in the role of the educator within the test development process. Traditionally, teachers and test designers have been the sole authors of assessment items, laboring over each question’s phrasing and content. In a HITL framework, educators transition into roles that emphasize oversight, curation, and strategy (Kasneci et al., 2023; Belzak et al., 2023). They become orchestrators of item generation rather than only item writers. This means that professional expertise is applied in deciding what to generate (via parameters and prompts) and in vetting how it was generated, rather than writing every word. Educators will need to be comfortable with delegating the first draft of creative work to an AI, then rigorously editing it.

This shift aligns the assessment design process more closely with the educator’s strengths (such as subject matter knowledge, understanding of student needs, and ethical judgment) while outsourcing some of the rote work (like devising multiple incidental variants of the same question) to AI. However, it also implies that educators must trust their judgment enough to override or discard AI suggestions whenever necessary. They become the final arbiters of quality. This role transformation can be empowering (teachers focus on high-level decisions and leave some tedious aspects to AI), but it requires a mindset change and confidence in one’s oversight capabilities.

### 5.3. New Skill Sets and Professional Development

With the evolving role comes the need for new skills. Educators will require training in how to effectively interact with AI tools for assessment purposes (Kasneci et al., 2023). Crafting good prompts, for instance, is both an art and a science; our case study showed that small changes in prompt wording (like specifying exact dates or dataset thresholds) can dramatically improve the usefulness of AI outputs. Teachers may need guidance on prompt engineering techniques specific to item generation. Additionally, skills in identifying AI biases or errors are essential (Embretson & Reise, 2000). This overlaps with traditional assessment literacy (knowing what makes a good test item) but adds layers specific to AI (recognizing a subtle bias that an AI might introduce or spotting a hallucinatory detail an AI included).

Professional development programs should therefore expand to cover AI literacy (understanding what LLMs can and cannot do), strategic AI interaction (learning how to get the best results from AI, including how to “think aloud” through a prompt), bias and fairness auditing for AI content, and data verification techniques (Belzak et al., 2023). Institutions aiming to adopt HITL methods should invest in workshops or collaborative learning sessions where educators practice these skills, perhaps using examples from case studies like this one. In doing so, educators will feel more confident and competent in leveraging AI, seeing it as a partner rather than a threat.

It is important to note that instructors who are new to teaching or assessment design, or even experienced educators teaching a new course, should begin by developing a good foundational approach to assessment without the aid of AI. This includes developing item concepts and validation practices before fully adopting a HITL approach. In short, structured professional development programs and mentorship are necessary prerequisites or supplements to AI-driven assessment methods, but they are not a substitute for the deeper understanding of what comprises a quality assessment, which is often gained through classroom experience.

### 5.4. Dynamic Validation and Continuous Quality Control

HITL approaches blur the line between test development and validation (Drasgow et al., 2006). Instead of validation being a one-time step after an item bank is assembled, validation becomes an ongoing, iterative part of the generation process. Educators continuously validate items in real-time by reviewing AI outputs, which turns validity into a dynamic property (Burstein & LaFlair, 2024). This has implications for how assessments are quality-checked. Traditional protocols (like having an independent review committee or a pilot test after item writing) might evolve to incorporate tech-assisted checks (for example, using software to quickly flag certain types of bias or running statistical simulations on item difficulty).

However, the human element remains central: teachers are effectively performing mini-validity studies on the fly with each AI suggestion. To support this, institutions might curate valid assessment achieves as training data or develop validation tools that integrate with AI platforms as a first-pass alert for the human reviewer. Developing such tools could significantly streamline the dynamic validation process.

### 5.5. Documentation and Accountability Systems

The need for thorough documentation noted earlier implies that educators (and their institutions) should treat the HITL generation process with the same seriousness as they would treat data in a research study. This means setting up systems to log the development of items (Burstein & LaFlair, 2024). On a small scale, this could be as simple as using a shared document or spreadsheet where each item has an entry detailing its origin and edits. On a larger scale, assessment software could incorporate a “history” feature that records each AI prompt, the AI’s response, and the changes made by the human. From an accountability perspective, such documentation is invaluable. If an AI-generated item is ever challenged (e.g., a student questions its clarity or fairness), the instructor can produce a record showing the care that went into crafting it, including any expert adjustments. If the item truly lacks rigor, it can be scrapped from future exams.

This transparency can help build trust in AI-assisted assessments among stakeholders. It also aligns with ethical guidelines for AI in education which call for explainability—the ability to explain how an AI-influenced decision (in this case, an item’s final form) came about (Wing, 2021). Educators and testing programs should be prepared to answer questions like, “How do we know these AI-generated test questions are fair and valid?”. Documentation provides the evidence for those answers.

### 5.6. Bias Mitigation and Equity Assurance

The case study demonstrates that HITL can effectively mitigate biases, but only if educators apply systematic checks. Therefore, one implication is that bias review protocols should be integrated into assessment design workflows whenever AI is used (Burstein & LaFlair, 2024). For instance, when high-stakes assessments are involved, an institution might establish that any AI-generated item goes through a bias review by multiple human examiners (possibly of diverse backgrounds themselves) before it is finalized. Tools such as sensitivity review checklists or even AI-based bias detection (paradoxically using AI to check AI by scanning for flagged language) can supplement human judgment. Additionally, educators should consider conducting small-scale pilot testing of AI-generated items with a diverse sample of students before operational use. Gathering student feedback can reveal if any content is confusing or insensitive from the test-taker’s perspective. This iterative improvement loop—pilot, get feedback, refine—combined with the speed of AI generation, means tests can be rapidly updated to fix any issues discovered much faster than traditional item revision cycles.

Equity in cognitive load is another concern. All variants of a test, or all items on a test, should impose similar mental effort so that no one or group of students is inadvertently disadvantaged. The HITL approach can help manage this by using the AI to produce many variants and then selecting those that best match each other in difficulty (with human judgment). As illustrated, one can also instruct the AI to generate multiple contexts or versions and pick the most appropriate. The implication for educators is that they might use AI to over-generate and then curate. Instead of writing one item, an educator might have the AI produce five and then choose the top two that meet the criteria and refine those. This gives a buffer to ensure that only the best, most equitable items make the cut.

### 5.7. Efficiency vs. Workload: Managing the Trade-Off

While AI can save time in item creation, the oversight process does add to the workload (Bulut et al., 2024). Educators and administrators need to plan for this. It may be reasonable, for example, to give teachers dedicated time to produce exam variants up-front, or to reduced initial teaching loads while they develop item banks using HITL methods, recognizing that while AI does the first draft, the teacher’s role is still labor-intensive in a different way. In large-scale standardized testing organizations, this might involve restructuring item development teams to include AI facilitators (who specialize in generating content in conjunction with AI) and human validators (who focus on reviewing and polishing the AI output). In school settings, it might involve collaborative teams of teachers sharing the load. Perhaps a scenario where a teaching assistant generates the item model and the lead instructor reviews outputs and complies the final exam.

Our case study experience, where only one educator provided oversight, suggests that collaboration would significantly enhance both the quality and the efficiency of HITL item development. Peers can catch issues one person might miss and can share effective prompting techniques with each other.

### 5.8. Institutional Policies and Ethical Guidelines

The introduction of AI into assessment practices should be accompanied by clear institutional policies (Wing, 2021; Burstein & LaFlair, 2024). These would cover questions such as the following:Under what circumstances do we allow AI to be used in creating assessments?What disclosure needs to be made to students about AI involvement?How are data privacy and security handled (e.g., feeding students’ answers back into the AI)?What accountability measures are in place if an AI-generated item were to slip through with an error?

Institutions might, for instance, institute a policy that no AI-generated item can be used in a high-stakes exam without documented human review. They may also provide guidelines on maintaining academic integrity; for example, ensuring that using AI does not inadvertently recycle copyrighted material or existing test content. Many of these considerations dovetail with broader discussions on AI in education currently taking place (Belzak et al., 2023). By proactively creating guidelines, institutions can encourage positive uses of AI (like the HITL for AIG process advocated herein) while guarding against misuse or overreliance.

### 5.9. Student Perceptions and Transparency

Educators should not overlook the student side of the equation. How students perceive AI-generated content can influence their acceptance of the assessment’s legitimacy. In our case, being transparent that AI was involved, but under strict human oversight, helped maintain student trust. It is advisable for educators to communicate to students something like “Some questions on your exam were developed with the assistance of AI tools, but each has been carefully reviewed and edited by your instructor to ensure it is accurate and fair.” Such statements demystify the process and reassure students that they are not being evaluated by a soulless algorithm, but rather by the teacher who knows the course objectives and cares about their learning. Furthermore, involving students in discussions about AI (perhaps in class, separate from the exam) can turn this into a learning opportunity and show students that the institution is thoughtfully integrating technology (Roe et al., 2024).

### 5.10. Continuous Improvement and Evaluation

Finally, the move to HITL AI frameworks in general should be seen as iterative and evolving. After deploying AI-assisted assessments, educators should collect data on their effectiveness (Yan et al., 2024). This can include analyzing item statistics (difficulty indices, discrimination indices), or if it is a large class or standardized context, comparing them to historical data of human-only items. These checks help answer important questions like the following:Do AI-assisted items perform similarly in terms of difficulty?Are there any patterns of student responses that indicate confusion or bias that slipped through?

Another strategy could be to integrate both human and AI generated items into the same exam, gathering student feedback post-exam about the clarity and fairness of different questions (without specifically singling out which were AI-generated, to avoid biasing their feedback). Using this information, educators and institutions can refine their processes: perhaps updating prompt guidelines, adding an extra layer of review for certain types of content, or providing additional training where needed. The technology will also continue to improve; newer generations of AI might overcome some current limitations but instead will likely introduce new considerations. A culture of continuous improvement will help ensure that HITL methods remain effective and ethical over time (Falcão et al., 2022).

Lastly, while the current study demonstrates the methodological rigor and practical utility of our human-in-the-loop framework, empirical validation of student outcomes remains essential to fully establish the effectiveness of AI-generated assessments. Future research should specifically compare student performance on AI-assisted exams with traditional human-generated assessments, providing quantitative evidence to reinforce the validity and reliability of this innovative approach.

## 6. Conclusions

In conclusion, the integration of AI into parallel forms of standardized test development through a human-in-the-loop approach holds great promise. It offers a pathway to more efficiently create robust assessments and potentially innovate item formats and content in ways that engage students. However, it also demands that educators’ step into new roles, learn new skills, and maintain a vigilant eye on quality and equity. With thoughtful implementation supported by training, collaboration, and clear guidelines, HITL can enhance assessment practices. It empowers teachers to harness AI’s capabilities while firmly steering the process with their professional expertise and values. In doing so, educators can ensure that the future of generating assessment is one where technology serves pedagogy (and not the other way around), ultimately enriching both the educator and student learning experiences in the process.

# Institutional Review Board Statement

Ethical review and approval were waived for this study. It was exempt conducted to improve and enhance teaching and learning at Franklin University Switzerland.

# Informed Consent Statement

This case study was conducted with complete transparency. Students were informed that the instructor developed exam variants with the assistance of a large language model (LLM). Students consented to undertake their examination with that foreknowledge provided.

# Data Availability Statement

Full chat logs are long, fragmented, detailed, and require proper context to interpret. They can be shared upon request via an email to the corresponding author. Many of the most relevant prompts and outputs can be found quoted throughout the article and these can be used to replicate outputs. Some examples of final exam variants can be found at Burke, Charles (2025), “Exam Variants: Human-in-the-Loop AIG Quantitative Methods & Data Mining Spring 25”, Mendeley Data, V1, https://data.mendeley.com/datasets/748w3m9p5n/1 (accessed on 8 August 2025). They are available for use under the terms of the Creative Commons Attribution 4.0 International license (CC_BY 4.0).

# Conflicts of Interest

The author declares no conflicts of interest.

# Abbreviations

The following abbreviations are used in this manuscript: LLMLarge language modelAIGAutomatic item generationDIFDifferential item functioningHITLHuman-in-the-loop

## References

- Andersson T. Picazo-Sanchez P. Closing the gap: Automated distractor generation in Japanese language testing Education Sciences 2023 13 12 1203 10.3390/educsci13121203

- Anthropic Reducing hallucinations 2025 Available online: https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations (accessed on 23 June 2025)

- Belzak W. C. M. Naismith B. Burstein J. Ensuring fairness of human- and AI-generated test items Artificial intelligence in education: Posters and late breaking results, workshops and tutorials, industry and innovation tracks, practitioners, doctoral consortium and blue sky. AIED 2023 Wang N. Rebolledo-Mendez G. Dimitrova V. Matsuda N. Santos O. C. Communications in Computer and Information Science Springer 2023 Vol. 1831 10.1007/978-3-031-36336-8_108

- Bormuth J. On a theory of achievement test items University of Chicago Press 1969

- Bulut O. Beiting-Parrish M. Casabianca J. M. Slater S. C. Jiao H. Kuo B.-C. The rise of artificial intelligence in educational measurement: Opportunities and ethical challenges Chinese/English Journal of Educational Measurement and Evaluation 2024 5 3 3 10.59863/MIQL7785

- Burstein J. LaFlair G. T. Where assessment validation and responsible AI meet arXiv 2024 2411.02577 10.48550/arXiv.2411.02577

- Chan K. W. Ali F. Park J. Sham K. S. B. Tan E. Y. T. Chong F. W. C. Qian K. Sze G. K. Automatic item generation in various STEM subjects using large language model prompting Computers and Education: Artificial Intelligence 2025 8 100344 10.1016/j.caeai.2024.100344

- Circi R. Hicks J. Sikali E. Automatic item generation: Foundations and machine learning-based approaches for assessments Frontiers in Education 2025 8 858273 10.3389/feduc.2023.858273

- Diyab A. Frost R. M. Fedoruk B. D. Engineered prompts in ChatGPT for educational assessment in software engineering and computer science Education Sciences 2025 15 2 156 10.3390/educsci15020156

- Drasgow F. Luecht R. M. Bennett R. E. Brennan R. L. Technology and testing Educational measurement 4th ed. Praeger 2006 471 515 10.1007/978-0-387-85461-8_15

- Embretson S. E. Reise S. P. Item response theory for psychologists Lawrence Erlbaum Associates 2000

- Falcão F. Costa P. Pêgo J. M. Feasibility assurance: A review of automatic item generation in medical assessment Advances in Health Sciences Education 2022 27 2 405 425 10.1007/s10459-022-10092-z 35230589

- Fernández A. A. López-Torres M. Fernández J. J. Vázquez-García D. ChatGPT as an instructor’s assistant for generating and scoring exams Journal of Chemical Education 2024 101 9 3780 3788 10.1021/acs.jchemed.4c00231

- Gierl M. J. Haladyna T. M. Automatic item generation: Theory and practice Routledge 2012

- International Test Commission Association of Test Publishers Guidelines for technology-based assessment 2022 Available online: https://www.testpublishers.org/assets/TBA%20Guidelines%20final%202-23-2023%20v4.pdf (accessed on 22 June 2025)

- Ji Z. Lee N. Frieske R. Yu T. Su D. Xu Y. Ishii E. Bang Y. J. Madotto A. Fung P. Survey of hallucination in natural language generation ACM Computing Surveys 2023 55 12 248 10.1145/3571730

- KasneciE.SeßlerK.KüchemannS.BannertM.DementievaD.FischerF.GasserU.GrohG.GünnemannS.HüllermeierE.KruscheS.KutyniokG.MichaeliT.NerdelC.PfefferJ.PoquetO.SailerM.SchmidtA.SeidelT.…KasneciG. ChatGPT for good? On opportunities and challenges of large language models for education Learning and Individual Differences 2023 103 102274 10.1016/j.lindif.2023.102274

- Khademi A. Can ChatGPT and Bard generate aligned assessment items? A reliability analysis against human performance Journal of Applied Learning & Teaching 2023 6 1 75 80 10.37074/jalt.2023.6.1.28

- Kiyak Y. S. Budakoğlu İ. İ. Coşkun Ö. Koyun E. The first automatic item generation in Turkish for assessment of clinical reasoning in medical education Tıp Eğitimi Dünyası (Medical Education World) 2023 22 68 72 90 10.25282/ted.1225814

- Malik F. S. Terzidis O. A hybrid framework for creating artificial intelligence-augmented systematic literature reviews Management Review Quarterly 2025 10.1007/s11301-025-00522-8

- Munro R. Human-in-the-loop machine learning: Active learning and annotation for human-centered AI Manning 2021

- Reeves T. C. Storm clouds on the digital education horizon Journal of Computing in Higher Education 2003 15 1 3 26 10.1007/BF02940850

- Roe A. Richardson S. Schneider J. Cummings A. Forsberg N. Klein J. Semantic drift mitigation in large language model knowledge retention using the residual knowledge stability concept TechRxiv 2024 10.36227/techrxiv.173091142.28945162/v1 36284789

- Song Y. Du J. Zheng Q. Automatic item generation for educational assessments: A systematic literature review Interactive Learning Environments 2025 1 20 10.1080/10494820.2025.2482588

- Tan B. Armoush N. Mazzullo E. Bulut O. Gierl M. J. A review of automatic item generation techniques leveraging large language models EdArXiv 2024 10.35542/osf.io/6d8tj

- Wing J. M. Trustworthy AI Communications of the ACM 2021 64 10 64 71 10.1145/3448248

- Yan L. Sha L. Zhao L. Li Y. Martinez-Maldonado R. Chen G. Gašević D. Practical and ethical challenges of large language models in education: A systematic scoping review British Journal of Educational Technology 2024 55 1 90 112 10.1111/bjet.13370

- Yaneva V. von Davier M. Advancing natural language processing in educational assessment 1st ed. Routledge 2023 10.4324/9781003278658

## Figures

[Figure 1: Flowchart illustrating the human-in-the-loop conceptual framework for AIG.]

[Figure 2: Mean differences in cohort exam scores, Quantitative Methods.]

[Figure 3: Mean differences in cohort exam scores, Data Mining.]