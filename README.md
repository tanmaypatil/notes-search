# resume search intelligence
Resume search using natural queries .  Demo application using openai RAG api and opensource VLM model to do resume analysis.

## Objective 
Objective of resume intelligence would be to support natural language query on a set of resumes .
It can be used to do comparative analysis of resumes .
Let us say , that we have 4 or 5 resumes of prospective software engineers
Some of the query , which it should allow you to fire are 
1. Does any of the candidates have team management experience ? 
2. Who has more experience in java and docker in set of resumes ?

## How to run 
  This example can be run on local windows machine/laptop. 
  It does not have special requirement in terms of GPU 
  You need to select 2 resumes from UI application , type in the query in prompt box.  
  and hit submit.
  User needs to key in openai key in .env file which is present in root of the folder. 

```
   OPENAI_KEY=<substitute your key>
``` 
```bash
   python ui_resume_compare.py
```
## Demo
![Demo](demo.gif)

## Approaches
Here i use RAG approaches 
1. RAG - with openai
   openai has assistant api , which has option of storing the vector representation of document and searching against the same .
   Refer here for documentation [File Search](https://platform.openai.com/docs/assistants/tools/file-search)
   On how to use file search api , i referred simon wilson's excellent [blog](https://simonwillison.net/2024/Aug/30/openai-file-search/) and gist he made [sample code](https://gist.github.com/simonw/97e29b86540fcc627da4984daf5b7f9f)

2. RAG - with opensource colpali
   This is approach of using VLM . I plan to use Byaldi which internally uses colpali
   Refer to notebook , which has sample code [chat with pdf using byaldi
   ](https://github.com/AnswerDotAI/byaldi/blob/main/examples/chat_with_your_pdf.ipynb)
   I am yet to implement this.

## Using openai file search 
This is a straightforward approach .I use openai apis to create a vector store and add all pdf documents to vector store . post that create a assistant and attach vector store to assistant 

### concatenation of files
openai file search , seems to be not working well , for queries which is touching multiple documents . One solution seems to be concatenating multiple documents into a single document.
This seems to be true at nov 2023 as per this blog [openai assistant for RAG](https://www.tonic.ai/blog/rag-evaluation-series-validating-openai-assistants-rag-performance) . This hack also is needed in 2024. 
