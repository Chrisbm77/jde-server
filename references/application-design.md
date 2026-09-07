# JD Edwards EnterpriseOne 9.2 — Application Design Guidelines Reference

**Source:** Development Guidelines for Application Design Guide (Part Number: E53575-04)
**Platform:** JD Edwards EnterpriseOne Tools 9.2

---

## Table of Contents

1. [Overview](#1-overview)
2. [Application Development Guidelines](#2-application-development-guidelines)
3. [Naming Conventions](#3-naming-conventions)
4. [Task Design](#4-task-design)
5. [Table I/O Guidelines](#5-table-io-guidelines)
6. [Performance Considerations](#6-performance-considerations)
7. [Standard Event Rules Guidelines](#7-standard-event-rules-guidelines)
8. [BI Publisher Report Guidelines](#8-bi-publisher-report-guidelines)
9. [Using Currency](#9-using-currency)
10. [Translation Issues](#10-translation-issues)
11. [Acronyms and Abbreviations](#11-acronyms-and-abbreviations)
12. [Field Sizes](#12-field-sizes)
13. [Glossary](#13-glossary)

---

## 1. Overview

This guide provides the standards and conventions for interactive and batch application development in JD Edwards EnterpriseOne 9.2. It covers naming conventions for all object types, guidelines for application design, BI Publisher reporting standards, currency handling, translation readiness, and approved acronyms/abbreviations.

---

## 2. Application Development Guidelines

### 2.1 Object Management Workbench (OMW)

The Object Management Workbench (OMW) is the central tool for managing all JD Edwards EnterpriseOne objects. All development work begins and ends in OMW.

### 2.2 Object Types and Prefixes

| Prefix | Object Type |
|--------|-------------|
| B | Business Function |
| C | Customer Menu |
| D | Data Structure |
| F | Table |
| G | Menu |
| K | Workflow Process |
| N | Named Event Rule (NER) |
| P | Interactive Application |
| R | Batch Application (UBE) |
| S | Section Name |
| T | Processing Options Template/Data Structure |
| V | Business View |
| W | Form |
| GT | Media Object |
| WF | Workflow Data Structure |
| TV | Text Variable |
| TP | BI Publisher Template |
| RD | Report Definition |

### 2.3 System Codes

| System Code | Description |
|-------------|-------------|
| 00 | Foundation |
| 01 | Address Book |
| 02 | Electronic Mail |
| 03 | Accounts Receivable |
| 04 | Accounts Payable |
| 09 | General Accounting |
| 55 | Reserved for Clients |
| 60–69 | Custom Development |
| L00 | Partner Reserved |

### 2.4 Group Types

| Group Type | Description |
|------------|-------------|
| 01 | Master |
| 02 | Balance |
| 1X | Transaction |

### 2.5 Interactive Application Guidelines

#### Static Text Field Sizing
- Size static text fields to accommodate the maximum width of text they will contain
- Allow 30% expansion room for translation

#### Tab Sequence
- Set logical tab sequence through form controls
- Tab order should follow natural reading flow (left to right, top to bottom)

#### Form Type Descriptions

| Form Type | Description Convention |
|-----------|----------------------|
| Find/Browse | "Work With..." |
| Fix/Inspect | Topic title |
| Header Detail (HD) | Topic title |
| Headerless Detail (HLD) | Topic title |
| Lower-Level | Topic with calling form title appended |

#### Fiscal Year Display
- Display fiscal year consistently across applications

#### Subledger Defaults
- Follow standard subledger default behavior

### 2.6 Industry-Specific Guidelines

#### Financials Forms
- Use ALKY (Long Address Number, 20 chars) instead of AN8
- Use B0100016 (Scrub Address Number) business function
- Use X1202-F1201 (Validate Asset Number) for asset validation

#### Workforce Management
- Rename AN8 to "Employee Number"
- Retrieve job type/step from F08001

#### Manufacturing/Distribution
- Place Branch/Plant identifier in upper-right area
- Use MCU or MMCU for static text labels

#### Currency Controls Display Sequence
1. Currency Code (CRDC)
2. Exchange Rate (CRR)
3. Rate Base Currency Code (CRCD)
4. Foreign Option

### 2.7 Batch Application Auto-Standards

| Element | Standard |
|---------|----------|
| Font | 7pt Arial Regular |
| Report Name | Upper-left |
| Date/Time | Right side |
| Page Number | Upper-right |
| Report Titles | Centered |
| Company Name | First line |

---

## 3. Naming Conventions

### 3.1 Data Dictionary Items

#### Alias Rules
- Minimum 5 alpha characters
- No TIP or TERM prefix
- No special characters
- Maximum 8 characters for external data items

#### Name Rules
- Maximum 32 characters
- Allow 30% expansion room for translation

#### Description Conventions by Data Item Type
- Follow the standard description format for each data item category

#### External Data Items
- First character: Y or Z
- Alias format: `Ysssdddd` (max 8 chars)
  - `Y` = external prefix
  - `sss` = system code
  - `dddd` = data item identifier
- Name format: `Ysssddd...d` (max 32 chars)

#### Processing Option Data Items
- Help item alias format: `Syyyyyzz`
- Glossary group: H
- Follow standard glossary description guidelines

#### Table I/O Handle Data Item
- Format: `HFxxxxxx` (H + table name)

### 3.2 Tables

- Format: `Fxxxxyyyy`
- Maximum: 8 characters
- `xxxx` = system code
- `yyyy` = sequential number

### 3.3 Business Views

- Format: `VzzzzzzA`
- Maximum: 8 characters
- `A` = alphabetic suffix (incremented for multiple views on same table)

### 3.4 Processing Options Data Structures

- Format: `Txxxxxyyyy`
- Maximum: 10 characters

### 3.5 Versions

| Version | Description |
|---------|-------------|
| XJDE | Standard/demo version |
| ZJDE | Production version |

### 3.6 Interactive Applications

- Format: `Pxxxxyyyy`
- Maximum: 8 characters

### 3.7 Forms

- Format: `WzzzzzzzzA` (auto-assigned)
- System automatically assigns form names

### 3.8 Batch Applications (UBEs)

- Format: `Rxxxyyyyy`
- Maximum: 8 characters
- Function Use codes:
  - 130–139: Batch processes
  - 160–169: Reports

### 3.9 BI Publisher Objects

#### Templates
- Format: `TPwwwxxxxyyzz`
- Maximum: 100 characters
- Template type codes:

| Code | File Type |
|------|-----------|
| TE | .rtf (template) |
| TL | .xls (Excel) |
| TP | .pdf |
| TR | .rtf |
| TS | .xsl (stylesheet) |
| XL | .xml/.xlf |
| XF | .xsl |

#### Report Definitions
- Format: `RDwwwxxxxyy`
- Maximum: 10 characters

### 3.10 Section Names

- Format: `SzzzzzzzzA`
- Maximum: 10 characters

### 3.11 Purge Table Programs

- Format: `Pxxxxxxxp`
- Maximum: 8 characters

### 3.12 Event Rule Variables

- Format: `xxx_yyzzzzzz_AAAA`
- Prefix types: `frm_` (form), `evt_` (event)
- Hungarian notation type indicators:

| Prefix | Data Type |
|--------|-----------|
| c | Character |
| h | Handle |
| mn | Math Numeric |
| sz | String |
| jd | Julian Date |
| id | ID |

### 3.13 Business Functions

- C functions: `Bxxxxyyyy`
- Named Event Rules: `Nxxxxyyyy`

### 3.14 Business Function Data Structures

- Format: `DxxxyyyyA`

### 3.15 Workflow Objects

- Workflow Processes: `Kxxxxyyyy` (max 10 chars)
- Workflow Data Structures: `WFxxxxyyyA` or `WFxxxxyyyB`

### 3.16 Media Objects

- Format: `GTxxxxyyA`
- Maximum: 8 characters

### 3.17 Menus

- Format: `Gxxxxyyyy`
- Maximum: 9 characters
- Skill levels: 1–4

### 3.18 Table Conversions

- Format: `R89xxxxyyyy`
- Maximum: 10 characters

---

## 4. Task Design

### 4.1 Task Hierarchy

| Task Pattern | Description |
|-------------|-------------|
| GXX | System task |
| GXXYY | Module description |
| GXX10 | Daily tasks |
| GXX20 | Periodic tasks |
| GXX31 | Advanced/Technical tasks |
| GXX41 | System Setup tasks |

### 4.2 Task Processing Options

Uses UDC 98/CD with Option Codes:

| Code | Behavior |
|------|----------|
| Blank | Uses ZJDE0000 version |
| 1 | Uses XJDE0000 version |
| 2 | Uses undefined version |
| 3 | Prompts for version |

---

## 5. Table I/O Guidelines

### 5.1 Update Standards
- Always update date, time, user, and program name fields when modifying records
- Create one business function per table for encapsulating I/O operations
- Avoid cross-vertical table updates (e.g., Financials updating Manufacturing tables directly)

### 5.2 Best Practices
- Use business functions to encapsulate table operations
- Maintain audit trail fields on all table updates
- Follow the one-table-one-business-function pattern

---

## 6. Performance Considerations

### 6.1 Form Design Performance
- Limit the number of grid columns displayed
- Limit business view columns to only those needed
- Minimize form controls
- Use work fields instead of hidden controls when possible
- Disable unnecessary data dictionary functions (edit rules, visual assists) where not needed

### 6.2 Grid Performance
- Grid sort sequence must match the database index being used
- Use "Stop Processing" to prevent unnecessary record retrieval
- Only fetch records that are needed

### 6.3 General Performance
- Minimize database round-trips
- Use efficient queries with proper index alignment
- Avoid unnecessary processing in event rules

---

## 7. Standard Event Rules Guidelines

### 7.1 Coding Standards
- Use numeric values (1/0) instead of T/F for boolean logic
- Include blank lines between logical sections
- Add comments for complex logic
- Use text variables instead of hard-coded text strings
- Use PID (Program ID) for database update audit fields
- Use directional arrows (→) to indicate data flow
- Use # for unused parameters in business function calls

### 7.2 Documentation
- Maintain a revisions log in event rules
- Document the purpose and logic of each major section
- Comment business function calls with their purpose

---

## 8. BI Publisher Report Guidelines

### 8.1 Report Integration Types

| Type | Description |
|------|-------------|
| Embedded (Pixel Perfect) | Tightly integrated reports with precise layout control |
| One View Reporting | Ad-hoc reporting using One View framework |
| Ad Hoc Reporting | User-driven report creation |

### 8.2 UBE/Report Definition Guidelines

- Avoid report constants; use representative variable names instead
- Use representative section names that describe the data
- Level breaks in the UBE must match BI Publisher groups
- Perform sorting in the UBE, not in the template
- Avoid page-related data elements (Headers, Footers, Brought Forward, Carried Forward)
- Use conditional sections for dynamic content
- Perform data formatting in the UBE rather than the template

### 8.3 Report Definition Settings
- Select all output types
- Set PDF as the default output
- Use User Preference Language setting

### 8.4 BI Publisher Layout Editor Standards

#### Page Attributes
- Page size: 8¾ × 11 inches
- Default orientation: Landscape
- Maximum margins: 0.5 inches (minimum 0.03 inches)
- Use `<?start:body?>` / `<?end body?>` tags instead of Word built-in headers/footers

#### Page Header Elements

| Element | Format |
|---------|--------|
| Report Title | Arial 14pt Bold, Centered |
| Subtitle | Arial 12pt Bold, Centered (optional) |
| Company Logo | Upper-left |
| Date/Time | Upper-right, Arial 7pt |
| Page Number | Upper-right, "Page x of x", Arial 7pt |

#### Page Footer Elements

| Element | Format |
|---------|--------|
| Report ID / Version ID / Template Name | Lower-left, Arial 7pt |
| Confidential Notice | Centered, Arial 7pt Bold (max 9pt) |

### 8.5 Report Data Formatting

#### Standard Font
- Font: Arial
- Size: 7pt (maximum 9pt)
- Color: Black

#### Single Data Fields
- Left-aligned
- Bold labels
- 15% border on label cells

#### Multiple Row Tables
- Shaded header: RGB 207/224/241
- Alternate row shading: 15% grey
- Column headers: Centered, Bold

#### Table Formatting
- Position: Centered on page
- Cell margins: Top/Bottom 0.02", Left/Right 0.06"
- Borders: Solid ½pt, 25% grey

#### Totals Shading Levels

| Level | RGB Values | Description |
|-------|------------|-------------|
| Level 1 | 207, 224, 241 | Lightest |
| Level 2 | 180, 206, 228 | |
| Level 3 | 154, 188, 216 | |
| Level 4 | 131, 173, 207 | |
| Level 5 | 114, 161, 200 | Darkest |

#### Data Alignment
- Single data: Left-aligned with corresponding multiple-row table
- Totals: Right-aligned
- Report total data: Right-aligned, in own cell, Arial 7pt Bold

### 8.6 End of Report Indication

- Display "End of Report" centered on last page if total page count is not in header
- Format: Arial 7pt, Black, Bold
- Place in single-celled table after template content

### 8.7 No Data Indication

- Display "No Data Selected" when no data is found
- Format: Arial 7pt, Black, Bold, centered after template content
- Use If condition: `<?if:ErrorMessage_ID0='No Data Selected'?> No data Selected <?end if?>`

### 8.8 Page Break

- Do not use native Microsoft Word page breaks
- Use `<?split-by-page-break:?>` syntax immediately before `<?end for-each?>` instead

### 8.9 Multiple Tables
- For reports with multiple tables, center margins on the widest table
- Exception: Tables with related graphs — center each table with its graph
- Use page breaks to separate unrelated tables and graphs

### 8.10 Paragraph Settings
- Alignment: Left
- Indentation: Left 0", Right 0"
- Spacing: Before 0pt, After 0pt, Single line spacing
- Do not use tab characters (use borderless tables instead)

### 8.11 Translation Guidelines for Reports
- Allow 30% text expansion for translation
- Do not format with character-based lines (use tables with bold text)
- Do not use consecutive symbols in translatable strings
- Do not connect words with underscores (ACCOUNTING_SEQUENCE_NAME will not translate)
- Do not concatenate variable strings with static strings
- Use spell checker for correct spelling

### 8.12 XPath Usage
- BI Publisher uses XPath to access data elements
- For large data sets, use full relative paths for performance:
  - Instead of `<?for-each:DEPT?>` use `<?for-each:/DEPT_SALS/DEPT?>`
  - Instead of `<?DEPARTMENT_NAME?>` use `<?./DEPARTMENT_NAME?>`
- Full relative paths avoid full tree searches that affect performance with large documents

---

## 9. Using Currency

### 9.1 Currency Implementation Features
- **Currency retrieval:** Accomplished through database triggers and table event rules
- **Currency retrieval logic:** Handled using business functions
- **System APIs:** Assist in accessing cached tables

### 9.2 Advantages of Developer-Controlled Currency
- Adding currency tables does not require system module changes — only new business functions
- Business logic is captured in business functions, not system modules
- Table event rules attach currency retrieval at the table object level
- Table event rules are triggered by table events, not application events
- Same logic applies to all applications using the table
- No hard-coded logic in the runtime engine

### 9.3 Working with Currency

When identified amounts are written to or retrieved from a database, or used in calculations, proper decimal placement is critical. Currency implementation adjusts decimal placement on Math_Numeric currency fields according to a specified currency.

#### Implementing Currency Involves:
1. Performing currency setup
2. Creating currency business functions (currency triggers)
3. Attaching currency trigger to the Currency Conversion event in Table Event Rules (TER)
4. Designing TER functions through Event Rules Design
5. Compiling event rules into consolidated DLL through OMW
6. Modifying applications as necessary

#### Build Triggers Process
1. Converts event rules to C source code (creates OBNM.c and OBNM.hxx files)
2. Compiles new functions and adds them to JDBTRIG.DLL

### 9.4 Currency Conversion Process Flow

**On FETCH:**
1. Application requests data
2. Is currency on?
3. If yes, run currency trigger
4. Currency Trigger calls TER which executes business function, performs logic, scrubs data
5. Return data to database, then to application

**On ADD/UPDATE:**
1. Application sends data
2. Is currency on?
3. If yes, run currency trigger
4. Currency Trigger calls TER which executes business function, performs logic, scrubs data
5. Update database

### 9.5 Multi-Currency Conversion Codes

| Code | Description |
|------|-------------|
| N | No multi-currency accounting. Single currency for all companies. |
| Y | Activate multi-currency with multipliers. System multiplies foreign amount by exchange rate. |
| Z | Activate multi-currency with divisors. System divides foreign amount by exchange rate. |

### 9.6 Currency Forms and Navigation

| Form Name | Form ID | Navigation | Usage |
|-----------|---------|------------|-------|
| System Setup | W0000A | JDE Menus → Multi-Currency Setup (G1141) → Set Multi Currency Option | Set up currency conversion |
| General Accounting Constants | W0000B | System Setup → General Accounting Constants | Set up currency conversion |
| Form Design Aid | NA | OMW → select interactive app → Design button | Show currency-sensitive controls |
| Object Management Workbench | W98220A | Type OMW in Fast Path of Solution Explorer | Create a currency conversion trigger |

### 9.7 Showing Currency-Sensitive Controls
1. Double-click the control on the form
2. Select the Control Options tab
3. Verify the "No Display if Currency is Off" option is deselected to show currency fields

### 9.8 Creating a Currency Conversion Trigger
1. Move table into OMW project
2. Check out the table
3. Highlight table → click Design button
4. On Table Design, select Design Tools tab → Start Table Trigger Design Aid
5. On Event Rules Design, select Currency Conversion event → attach business function
6. Click Business Functions → search using Category **CUR** or System Code **11**
7. Select business function → click Select
8. Attach table columns to business function data structure → click OK
9. Save Event Rules Design
10. On Table Design, select Table Operations tab → Generate Table
11. Select data source → click OK
12. On Table Design, select Design Tools tab → Build Table Triggers

---

## 10. Translation Issues

### 10.1 Translatable Components
- Data dictionary items (Alpha, Row, and Column descriptions)
- Data dictionary glossaries (F1 help)
- Menus
- Tasks
- User Defined Codes (UDCs) — Column 1 description only
- Reports
- Forms
- Text variables in forms and reports
- Processing options
- Processing option glossaries (F1 help)
- Resource files

### 10.2 Writing for Translation

#### General Principles
- Use short, complete sentences
- Use active voice (e.g., "Use this program to enter vouchers" not "This program is used to enter vouchers")
- Keep sentences simple and clear

#### Consistent Terminology
- Follow the "one term, one concept" rule
- Avoid using one term for multiple concepts
- Commonly confused synonym groups:
  - Match / Reconcile
  - Spread / Distribute / Allocate
  - Move / Transfer
  - Change / Revise / Alter / Modify
- Use words in only one way (noun or verb, not both)

#### Avoid Telegraphic English
- Do not omit articles, pronouns, or linking verbs
- Evaluate error messages for ambiguity caused by omitted words
- Example: "Empty File" — is "Empty" a verb or adjective?

#### Placeholders
- Precede placeholders (&n) with a noun that identifies what they represent
- Example: "The &1 of test &2, branch &3, effective &4 through &5, has been approved."

#### Technical Jargon and Americanisms
- Avoid jargon, slang, and Americanisms
- Examples to avoid: "on the fly", "beef up the functionality"

#### Abbreviations and Acronyms
- Use only standard, common abbreviations
- Do not overuse JDE-created abbreviations
- Do not invent abbreviations
- Each abbreviation should mean only one thing

#### Including "That" in Relative Clauses
- Always include "that" in relative clauses for translation clarity
- Example: "Verify **that** the draft is at the appropriate status"

#### Avoiding False Subjects
- Avoid "It is", "There is", "There are" constructions
- Example: Change "There are currently no logs on this server" to "No logs are currently on this server"

#### Parallel Structure in Lists
- All items in a list should have the same structure
- All begin with imperative verb, all begin with noun, all are complete sentences, or all are phrases

#### Capitalization Rules
- Capitalize: first word of sentence, acronyms, headings, names of things
- In headings: capitalize first/last words and all words except articles, conjunctions, prepositions
- Capitalize names of systems, programs, forms, tables, fields with "the" before them
- Terms NOT capitalized when used generically: address book, automatic accounting instructions, category codes, chart of accounts, company constant, detail area, processing options, user defined codes, multicurrency, general ledger

### 10.3 Translation Coding Guidelines

- Limit text items to no more than 70% of allotted space (30% expansion room)
- Verify push buttons can change size dynamically for translation
- Use only approved acronyms and abbreviations
- Use text variables instead of hard-coded text
- Do not use contractions
- Avoid long or ambiguous noun strings
- Leave controls visible in Properties — use hide/show functionality in ER instead
- Hidden controls (Visible checkbox cleared) are NOT extracted for translation
- For UDC descriptions, retrieve from F0005 (English) or F0005D (other languages) based on logon language

### 10.4 Translation Expansion Requirements

| Source Length | Expansion Allowance |
|-------------|-------------------|
| 1 character | 400% |
| 2–10 characters | 101–200% |
| 11–20 characters | 81–100% |
| 21–30 characters | 61–80% |
| 31–70 characters | 31–40% |
| 70+ characters | 30% |

### 10.5 Translation Readiness Checklist

| Item | Question |
|------|----------|
| Abbreviations and Acronyms | Did I use only approved abbreviations and acronyms? |
| Concatenated Text | Was concatenation of text removed? |
| Controls | Are the controls listed in ER selected as visible? |
| Cultural References | Were puns and cultural references removed? |
| Data Dictionary | Were data dictionary glossaries written and formatted according to standards? |
| Font Overrides | Was the font override removed? |
| Hard-coded text | Was hard-coded text removed and replaced with text variables? |
| Icons and other Images | Was text removed from icons and other images? Are icons generic enough for all target markets? |
| Sizing of Text Areas and Buttons | Were text areas stretched to maximum width for text expansion? Were buttons sized wide enough? |
| Source Text | Is the source text grammatically correct and easy to understand? |
| Terminology | Did I use terminology consistently? |
| Text Variables | Were the text variables assigned to an identifier? |
| UDCs | Do UDCs retrieve the description in user language preference? |

### 10.6 Actions that Trigger Translation/Retranslation
- Adding text
- Deleting text
- Changing text (including correcting typos and punctuation)
- Changing text formatting, alignment, or indentation
- Adding or deleting spaces between text
- Changing field size
- Adding or deleting line breaks
- Changing menu sequence (even without text change)
- Changing processing option sequence on a tab
- Adding or changing menu toolbar exits

**Does NOT trigger retranslation:** Changing layout, tab sequence, or control location alone.

### 10.7 Working with Noun Strings

Avoid long noun strings (3+ nouns in succession). They are difficult to translate because relationships between words are unclear.

**Strategies to fix noun strings:**
- Insert helpful words: of, for, to
- Add -ing or -ed endings
- Reverse word order and add prepositions

**Example transformations of "Install System Code":**
- Installed System Code
- Install the System Code
- Code for Install System
- Install Code for System
- Code the Install System

### 10.8 Approved Noun Strings

| Text String | Usage |
|-------------|-------|
| Data Structure | Noun string — "data structure" means the structure of the data. Preceding text refers to the type. Examples: Business function data structure, Form data structure, Processing option data structure |
| [noun] Design | The JDE tool for creating a specific object type. Examples: Application Design, Business View Design, Table Design |
| [noun or verb] Event | Text preceding "event" is an adjective describing the event purpose. Examples: Button Clicked event, Row is Exited event |
| High-level Default Trigger | "High-level" is an adjective for "default trigger" — criteria automatically evaluated for data in a field |
| Install [noun] | "Install" is an adjective, not a verb. Examples: Install system, Install data |
| Line Number | The number of the line |
| Menu Revisions | Noun string — the tool that maintains interactive and batch application menus |
| Object Librarian | Noun string — the tool that maintains objects or building blocks |
| Object Type | Object type means the type of object |
| Process Function | A function of a process |
| Process Usage | A usage of a process |
| Set Up | Two words = verb |
| Setup [noun] | One word = noun or adjective. Examples: Setup function, Setup menu |

### 10.9 System Codes for Global Product Solutions
- Global solutions use system codes translated into all supported languages (e.g., Address Book = system code 01)
- Country-specific solutions use system codes specifying the country/region (e.g., HR & PR Foundation Canada = system code 05C)

---

## 11. Acronyms and Abbreviations

Oracle maintains an official list of approved acronyms and abbreviations for use in JD Edwards EnterpriseOne applications. You must refer to this list before using any acronym or abbreviation. If a specific one is not listed, request your application development manager to add it.

**Important:** When defining a form control or menu that includes an ampersand (&) symbol, enter two ampersands (&&) — otherwise the runtime engine interprets & as an underscore (_).

### 11.1 Common JDE-Specific Abbreviations

| Abbreviation | Description |
|-------------|-------------|
| A/B or AB | Address Book |
| A/P | Accounts Payable |
| A/R | Accounts Receivable |
| AAI | Automatic Accounting Instruction |
| AN | Address Number |
| AP | Accounts Payable |
| API | Application Program Interface |
| APPL | Application |
| AR | Accounts Receivable |
| BDA | Business View Design Aid |
| BSFN | Business Function |
| BSVW | Business View |
| BU | Business Unit |
| CASE | Computer-Aided Software Engineering |
| CNC | Computer Numeric Control |
| DD | Data Dictionary |
| DLL | Dynamic Link Library |
| ER | Event Rules |
| FDA | Form Design Aid |
| G/L | General Ledger |
| MBF | Master Business Function |
| MRP | Material Requirements Planning |
| NER | Named Event Rule |
| OMW | Object Management Workbench |
| PO | Purchase Order |
| QBE | Query by Example |
| RDA | Report Design Aid |
| SQL | Structured Query Language |
| TAM | Table Access Manager |
| TBLE | Table |
| TC | Table Conversion |
| TDA | Table Design Aid |
| TER | Table Event Rule |
| TT | Translation Tools |
| UBE | Universal Batch Engine |
| UDC | User Defined Code |
| UOM | Unit of Measure |
| WF | Workflow |
| WO | Work Order |
| XML | Extensible Markup Language |
| XMLP | XML Publisher (now BI Publisher) |

> **Note:** The full acronym list in the source document spans pages 77–119 with hundreds of entries covering general business, industry, and technical abbreviations (A through Z). The subset above highlights the most commonly used JDE-specific abbreviations. Consult the full guide for the complete reference.

---

## 12. Field Sizes

The JD Edwards EnterpriseOne system maintains standard field sizes for commonly used data types. **B's** represent the number of characters for alphabetical fields. **8's** represent the number of digits for numeric fields.

### 12.1 Standard Field Size Reference

| Category | Alias | Description | Application Field Location | B's | 8's |
|----------|-------|-------------|---------------------------|-----|-----|
| Branch/Plant | *MCU* | Any branch/plant field | Top-right corner | 12 | — |
| Address Number | AN8 | Any Address Number (internal and external) | 88 | 8 | — |
| Date | DATE | Any date field | — | — | 88/88/8888 |
| Time | TIME | Any time field | — | — | 88:88:88 |
| UDC | UDC | 1-Character | — | 1 | — |
| UDC | UDC | 2-Character | — | 2 | — |
| UDC | UDC | 3-Character | — | 3 | — |
| UDC | UDC | 4-Character | — | 4 | — |
| UDC | UDC | 8-Character | — | 8 | — |
| UDC | UDC | 10-Character | — | 10 | — |
| Amount | AEXP | Extended Cost | After Unit Cost | — | 15 |
| Company | CO | Company | — | 5 | — |
| Amount | CRR | Currency Exchange Rate | — | — | 15 |
| Document | DOC* | Document Number | — | 8 | — |
| Document | DCT* | Document Type | After Doc Number/No desc. | 2 | — |
| Document | KCO* | Key Company | After Doc Type/No desc. | 5 | — |
| Location | LOCN | Location | — | 20 | — |
| Location | LOTN | Lot Number | After LOCN | 30 | — |
| Location | TKID | Bulk - Tank ID | — | 8 | — |
| Quantity | TRQT | Quantity | — | — | 15 |
| Item Number | UITM | Item Number - Unknown | Left with desc. after | 26 | — |
| Amount | UNCS | Unit Cost | Before Extended Amount | — | 15 |
| Density | DEND | Density | After TEMP | — | 8 |
| Density Type | DNTP | Density Type | After DEND/No desc. | 1 | — |
| Pressure | VAPP | Vapor Pressure | After DETP | — | 15 |
| Unit of Measure | PREU | Pressure UOM | After VAPP/No desc. | 2 | — |
| Temperature | DETP | Density Temperature | After DEND | — | 8 |
| Temperature | TEMP | Temperature | — | — | 8 |
| Temperature | LPGV | LPG Vapor Temperature | After VAPP | — | 8 |
| Temperature Type | DTPU | Density Temperature Type | After DETP/No desc. | 1 | — |
| Temperature Type | TPU1 | Temperature Type | After LPGV/No desc. | 1 | — |
| Temperature Type | STPU | Temperature Type | After TEMP/No desc. | 1 | — |
| Volume | LIQV | Liquid Volume | — | — | 15 |
| Unit of Measure | BUMx | UOM | After Vol/No desc. | 2 | — |
| Correction Factor | VCF | Volume Correction Factor | — | — | 7 |
| Weight | LIQW | Liquid Weight | — | — | 15 |
| Volume | AMBR | Ambient Volume | — | — | 15 |
| Volume | VAPV | Vapor Volume | — | — | 15 |
| Volume | OVOL | Other Volume | — | — | 15 |
| Quantity | STUM | Stock Total | Not normally on a form | — | 15 |
| Quantity | STOK | Stock Volume | After AMBR | — | 15 |
| Weight | WGTR | Weight Result | After STOK | — | 15 |
| Line Number | JELN | Journal Entry Line Number | — | — | 7 |
| Batch Number | ICU | Batch Number | — | — | 8 |
| User ID | USER | User ID | — | 10 | — |
| Program ID | PID | Program ID | — | 10 | — |

---

## 13. Glossary

| Term | Definition |
|------|-----------|
| Activity Rule | The criteria by which an object progresses from one given point to the next in a flow. |
| Add Mode | A condition of a form that enables users to input data. |
| BIP | Business Intelligence Publisher, formerly known as XMLP. |
| Jargon | An alternative data dictionary item description that JD Edwards EnterpriseOne appears based on the product code of the current object. |
| Media Storage Object | Files that use one of the following naming conventions that are not organized into table format: Gxxx, xxxGT, or GTxxx. |
| RTF | Rich Text Format, a Microsoft Word file format. |
| Specification | A complete description of a JD Edwards EnterpriseOne object. Each object has its own specification (name), which is used to build applications. |
| Trigger | One of several events specific to data dictionary items. You can attach logic to a data dictionary item that the system processes automatically when the event occurs. |
| Vocabulary Override | An alternate description for a data dictionary item that appears on a specific JD Edwards EnterpriseOne form or report. |
| XML | Extensible Markup Language — a general-purpose specification for creating custom markup languages, used to facilitate sharing of structured data across information systems. |
| XMLP | XML Publisher, also called Business Intelligence Publisher (BIP). Oracle XML Publisher is a template-based publishing solution for report design and publishing using familiar desktop word processing tools. |
| XPath | The XML Path Language — a query language for selecting nodes from an XML document. |

---

## Quick Reference Cards

### Object Naming Quick Reference

| Object | Format | Max Length | Example |
|--------|--------|-----------|---------|
| Table | Fxxxxyyyy | 8 | F0101 |
| Business View | VzzzzzzA | 8 | V0101A |
| Interactive App | Pxxxxyyyy | 8 | P01012 |
| Batch App | Rxxxyyyyy | 8 | R04110 |
| Business Function (C) | Bxxxxyyyy | 8 | B0100016 |
| Named Event Rule | Nxxxxyyyy | 8 | N0100042 |
| Data Structure | DxxxyyyyA | — | D0100016A |
| Processing Options DS | Txxxxxyyyy | 10 | T01012 |
| Form | WzzzzzzzzA | Auto | W01012A |
| Section | SzzzzzzzzA | 10 | — |
| Menu | Gxxxxyyyy | 9 | G0111 |
| Workflow Process | Kxxxxyyyy | 10 | — |
| Workflow DS | WFxxxxyyyA | — | — |
| Media Object | GTxxxxyyA | 8 | — |
| Table Conversion | R89xxxxyyyy | 10 | — |
| BI Publisher Template | TPwwwxxxxyyzz | 100 | — |
| Report Definition | RDwwwxxxxyy | 10 | — |
| External Data Item | Ysssdddd | 8 | Y55CUSTO |
| Purge Table Program | Pxxxxxxxp | 8 | — |

### BI Publisher Formatting Quick Reference

| Element | Font | Size | Style | Position |
|---------|------|------|-------|----------|
| Report Title | Arial | 14pt | Bold | Centered, page header |
| Subtitle | Arial | 12pt | Bold | Centered, below title |
| Date/Time | Arial | 7pt | Regular | Upper-right |
| Page Number | Arial | 7pt | Regular | Upper-right, "Page x of x" |
| Report/Version/Template ID | Arial | 7pt | Regular | Lower-left footer |
| Confidential | Arial | 7pt | Bold | Centered footer (max 9pt) |
| Report Data | Arial | 7pt | Regular | — (max 9pt) |
| Column Headers | Arial | 7pt | Bold | Centered in cell |
| Single Data Labels | Arial | 7pt | Bold | Right-aligned in cell |
| Single Data Values | Arial | 7pt | Regular | Left-aligned in cell |
| End of Report | Arial | 7pt | Bold | Centered, last page |
| No Data Selected | Arial | 7pt | Bold | Centered, after template |

---

*Reference compiled from JD Edwards EnterpriseOne Tools 9.2 — Development Guidelines for Application Design Guide (E53575-04)*
