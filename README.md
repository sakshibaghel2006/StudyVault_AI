# StudyVault AI

> **Your course material. One place. No hallucinations.**

StudyVault AI is an AI-powered course-material study assistant built for the **"The Night Before"** problem statement.

It allows students to ask questions about their course material and receive answers based only on the available study documents, with relevant source and page citations.

If the uploaded material does not contain enough evidence to answer a question, StudyVault AI responds with **NOT COVERED** instead of generating an unsupported answer.

## 🚀 Live Demo

**Live Website:**  
https://studyvault-ai.onrender.com/app/

## 📌 Problem Statement

Students often have to search through lecture notes, PDFs, presentations, text files, and handwritten notes before an exam.

StudyVault AI provides a single interface where students can ask questions and retrieve relevant information from their course material.

The system focuses on:

- Evidence-based answers
- Source and page citations
- Semantic search
- Handwritten-note support using OCR
- Refusal when information is not present
- Evaluation of answerable and unanswerable questions

## ✨ Features

### 1. Course Material Search

The system processes course material and divides it into searchable chunks.

### 2. Semantic Search

Questions are converted into embeddings and compared with stored document embeddings to find relevant passages based on meaning rather than only exact keywords.

### 3. Source Citations

Every generated answer is accompanied by relevant source information such as:

- Document name
- Page number
- Relevance score
- Source type

### 4. NOT COVERED Detection

If the available course material does not contain enough evidence, the system refuses to answer.

Example:

```text
Question: What is Python programming?

Result: NOT COVERED

The provided course material does not contain enough evidence to answer this question.
