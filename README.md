Truth-O-Meter: MAKING ChatGPT TRUTHFUL

Despite its capabilities, GPT-4 has similar limitations to earlier GPT models: it is not fully reliable (e.g. can suffer from “hallucinations”) : OpenAI (2023) https://cdn.openai.com/papers/gpt-4.pdf

This project addresses this exact issue. It takes a text generated by GPT and verifies it against the web knowledge. Suspicious phrases and values are highlighted in sample HTML correction files in /html folder 
White paper: https://www.preprints.org/manuscript/202307.1723/v1

It is inspired by the patent 
CORRECTING CONTENT GENERATED BY DEEP LEARNING
https://patents.justia.com/patent/20220284174

Publication number: 20220284174

Abstract: Methods for correcting raw text generated by deep learning techniques is disclosed. The methods may be performed by systems/computing devices described herein. Raw text previously generated by the deep learning techniques may be obtained. A search query can be generated from a raw text sentence of the raw text. The search query is executed against a knowledge base or a corpus of text to obtain a set of search results, the set of search results comprising a plurality of candidate true sentences that can potentially be utilized to correct one or more entities or phrases of the raw text sentence. A candidate true sentence is selected from the plurality and used to correct the raw text sentence. For example, at least one entity or phrase of the candidate true sentence can be used to replace a corresponding entity or phrase of the raw text sentence.

Type: Application

Filed: February 2, 2022

Publication date: September 8, 2022

Applicant: Oracle International Corporation

Inventor: Boris Galitsky

HOW TO RUN

python src/correction_in_web_browser_opener.py

You need to create an account with azure.microsoft.com to get the key to specify in api_keys/api_keys.csv

SAMPLE FACT-CHECKING REPORTS
