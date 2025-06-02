# Flowbit-AI-Internship-Project

A multi-format autonomous AI system with contextual decisioning & chained actions that processes various document types, extracts intent, and executes appropriate follow-up actions.


https://github.com/user-attachments/assets/b921c3ed-1021-46b5-986a-15aa7bc04492


## Project Overview

This project implements a multi-agent system that intelligently processes documents in various formats (Email, JSON, PDF), classifies both the format and business intent, routes to specialized agents, and triggers appropriate follow-up actions based on extracted data.

## Architecture

![Input (1)](https://github.com/user-attachments/assets/149212bf-8223-4d47-bfce-560f07d32d80)



## Key Features

- **Multi-Format Processing**: Seamlessly handles emails, JSON webhooks, and PDF documents
- **Intent Classification**: Identifies business intent (RFQ, Complaint, Invoice, etc.)
- **Format Detection**: Automatically determines input format
- **Contextual Decision Making**: Applies different processing rules based on content
- **Chained Actions**: Triggers appropriate follow-up actions based on extracted information
- **Shared Memory**: Maintains context across agent interactions for audit and traceability
- **API Integration**: Simulates external system notifications (CRM, alerts, etc.)
- **Live Action Logging UI**: Real-time monitoring of agent actions through SSE

## Components

### Classifier Agent
- Detects input format (JSON, Email, PDF)
- Determines business intent (RFQ, Complaint, Invoice)
- Routes to appropriate specialized agent
- Uses few-shot examples and schema matching

### Email Agent
- Extracts structured fields: sender, urgency, issue/request
- Identifies tone (escalation, polite, threatening)
- Triggers actions based on tone and urgency
- Handles escalation for high-priority issues

### JSON Agent
- Parses webhook data
- Validates against required schema fields
- Flags issues for follow-up

### PDF Agent
- Extracts text and structure from documents
- Parses line-item invoice data or policy documents
- Flags high-value transactions (>$10,000)

### Shared Memory Store
- Maintains context across agent interactions
- Stores input metadata and processing results
- Records triggered actions and decision traces
- Enables auditing of the complete workflow

### Action Router
- Determines appropriate follow-up actions based on agent outputs
- Triggers simulated external system notifications
- Handles escalations, ticket creation, and risk flagging
- Completes the processing workflow

### Real-time UI with SSE
- Implements Server-Sent Events (SSE) in FastAPI for real-time data streaming
- Displays agent logs, processing steps, and triggered actions in real-time

## Implementation Details

### Structured Data Handling
- Uses Pydantic models for type safety and validation
- Ensures consistent data structures throughout the system

### Modular Architecture
- Implements LangChain's Runnable Lambda pattern
- Enables independent testing of components
- Supports dynamic routing based on document classification

### Server-Sent Events Integration
- Establishes persistent connections for real-time event streaming
- Pushes agent action logs to the UI as they occur


## Technologies Used

- **Backend Framework**: FastAPI
- **LLM Integration**: LangChain with Google Gemini
- **Data Modeling**: Pydantic for structured data
- **PDF Processing**: PyPDF2
- **Memory Store**: Redis
- **Real-time Updates**: Server-Sent Events (SSE)
- **Development**: Python 3.10
