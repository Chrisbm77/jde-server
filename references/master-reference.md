# JD Edwards EnterpriseOne 9.2 — Unified Development Master Reference

> **Purpose:** A single, authoritative guide for developing or modifying any JDE EnterpriseOne 9.2 object. Covers every object type, its naming convention, constraints, relationships to other objects, and the correct development workflow. Synthesized from 10 official Oracle guides.

---

## PART 1: ARCHITECTURE AND OBJECT MODEL

### 1.1 Core Principle

JDE EnterpriseOne uses an **object-based architecture**. Applications are not monolithic programs — they are assemblies of discrete, reusable objects managed through the Object Management Workbench (OMW). Every object has a specification (metadata) stored in a relational database and/or file server.

### 1.2 Complete Object Type Registry

| Prefix | Object Type | Abbrev | OL Object? | Design Tool |
|--------|------------|--------|------------|-------------|
| `F` | Table | TBLE | Yes | Table Design Aid (TDA) |
| `V` | Business View | BSVW | Yes | Business View Design (BDA) |
| `D` | Data Structure (BSFN) | DSTR | Yes | Data Structure Design |
| `T` | Processing Option DS | DSTR | Yes | Processing Option Design |
| `P` | Interactive Application | APPL | Yes | Form Design Aid (FDA) |
| `W` | Form (auto-assigned) | — | — | FDA (part of APPL) |
| `R` | Batch Application (Report) | UBE | Yes | Report Design Aid (RDA) |
| `B` | C Business Function | BSFN | Yes | C IDE + BF Builder |
| `N` | Named Event Rule | NER | Yes | Event Rules Design |
| `G` | Menu | — | — | Menu Design |
| `GT` | Media Object | — | Yes | Media Object tools |
| `K` | Workflow Process | — | No | Workflow tools |
| `WF` | Workflow Data Structure | — | No | Workflow tools |
| — | Data Dictionary Item | DD | No | P92001 / P92002 |
| — | User Defined Code | UDC | No | UDC tool |
| `S` | Section Name (Report) | — | — | RDA (part of UBE) |
| `TP` | BI Publisher Template | — | — | BI Publisher |
| `RD` | Report Definition | — | — | BI Publisher |
| `TV` | Text Variable | — | — | Text Variable tool |

**Object Librarian (OL) objects** are path code-based, support tokens (single checkout), and move via check-in/check-out. **Non-OL objects** (DD items, UDCs, Workflow) are data source-based.

### 1.3 System Codes

| Code | System | Code | System |
|------|--------|------|--------|
| 00 | Foundation | 09 | General Accounting |
| 01 | Address Book | 11 | Multicurrency |
| 02 | Electronic Mail | 31 | Equipment/Plant Mgmt |
| 03 | Accounts Receivable | 42 | Sales Order Processing |
| 03B | AR (extended) | 43 | Procurement |
| 04 | Accounts Payable | 48 | Inventory |
| 05 | HCM/Payroll | **55–59** | **Reserved for Clients** |
| 06 | Job Cost | 60–69 | Custom Development |
| 07 | Payroll (US) | L00–L99 | Partner Reserved |
| 08 | Human Resources | M00–M99 | Partner Reserved |

### 1.4 Group Types (for table naming)

| Group | Meaning |
|-------|---------|
| 01 | Master file |
| 02 | Balance file |
| 1X | Transaction file |

---

## PART 2: NAMING CONVENTIONS — COMPLETE REFERENCE

### 2.1 Data Dictionary Items

| Element | Rule |
|---------|------|
| **Alias** | 5–8 alpha characters, no TIP/TERM prefix, no special characters |
| **Name** | Max 32 characters, allow 30% expansion for translation |
| **External DD Item Alias** | `Ysssdddd` — Y prefix + system code + identifier (max 8 chars) |
| **External DD Item Name** | `Ysssddd...d` (max 32 chars) |
| **PO Help Item Alias** | `Syyyyyzz` — S prefix + sequence |
| **Glossary Groups** | C, D, K, S = can be table columns; E, H, X, Y = glossary-only messages |

### 2.2 Tables

| Element | Rule |
|---------|------|
| **Format** | `Fxxxxyyyy` (max 8 chars) |
| **F** | Always prefix F |
| **xxxx** | System code |
| **yyyy** | Sequential number |
| **Suffixes** | `LA–LZ` = logical file, `JA–JZ` = table join |
| **Column Prefix** | 2-char prefix per table; 1st char alphabetic, 2nd alphanumeric; no $, #, @ |
| **Custom Tables** | Use system codes 55–59 |
| **Description** | Max 60 characters |

### 2.3 Business Views

| Element | Rule |
|---------|------|
| **Format** | `VzzzzzzA` (max 8 chars) |
| **V** | Always prefix V |
| **zzzzzz** | Matches primary table name (without F prefix) |
| **A** | Alphabetic sequence suffix (A=first, B=second, etc.) |
| **External Views** | `Vssss9999` — system code + unique number |
| **Joined BV Description** | Primary table first, separated by `/` (e.g., "Item Master and Branch F4101/F4102") |
| **Description** | Max 60 chars, reflect application + form type |

### 2.4 Data Structures

| Type | Format | Max Length |
|------|--------|-----------|
| **BSFN Data Structure** | `DxxxyyyyA` | 10 chars |
| **Processing Option DS** | `Txxxxxyyyy` | 10 chars |
| **Media Object DS** | `GTxxxxyyA` | 8 chars |
| **Workflow DS** | `WFxxxxyyyA` or `WFxxxxyyyB` | — |

**BSFN DS naming:** D = prefix, xx = system code, yyyy = next number, A = alphabetic suffix (always include A even for single DS).

### 2.5 Interactive Applications & Forms

| Element | Rule |
|---------|------|
| **Application** | `Pxxxxyyyy` (max 8 chars) |
| **Form** | `Wnnnnnnx` — auto-assigned (W + app number + sequence letter A–Z) |
| **Subform** | `Snnnnnnx` (S + app number + sequence letter) |
| **Custom** | Use system codes 55–59 for client |

### 2.6 Batch Applications (UBE / Reports)

| Element | Rule |
|---------|------|
| **Format** | `Rxxxyyyyy` (max 8 chars) |
| **Function Use Codes** | 130–139 = batch processes, 160–169 = reports |
| **Section Names** | `SzzzzzzzzA` (max 10 chars) |
| **Standard Versions** | `XJDE` = demo (do not modify), `ZJDE` = production (copy to customize) |

### 2.7 Business Functions

| Element | Rule |
|---------|------|
| **C Source/Header** | `bxxyyyy.c` / `bxxyyyy.h` (max 8 chars); b = BSFN, xx = sys code, yyyy = seq number |
| **C BSFN object** | `Bxxxxyyyy` |
| **Named Event Rule** | `Nxxxxyyyy` |
| **External function signature** | `JDEBFRTN (ID) JDEBFWINAPI FunctionName(LPBHVRCOM lpBhvrCom, LPVOID lpVoid, LPDSDXXXXXXX lpDS)` |
| **Internal function** | `Ixxxxxx_a` — I + source filename + _ + description (max 42 chars total, description max 32 chars, PascalCase, no spaces) |

### 2.8 Other Objects

| Object | Format |
|--------|--------|
| **Menu** | `Gxxxxyyyy` (max 9 chars) |
| **Workflow Process** | `Kxxxxyyyy` (max 10 chars) |
| **Table Conversion** | `R89xxxxyyyy` (max 10 chars) |
| **Purge Program** | `Pxxxxxxxp` (max 8 chars) |
| **BI Publisher Template** | `TPwwwxxxxyyzz` (max 100 chars) |
| **Report Definition** | `RDwwwxxxxyy` (max 10 chars) |

### 2.9 Event Rule Variables

Format: `xxx_yyzzzzzz_AAAA`
- Prefix types: `frm_` (form scope), `evt_` (event scope)
- Hungarian notation: `c` = char, `h` = handle, `mn` = math numeric, `sz` = string, `jd` = date, `id` = ID

---

## PART 3: OBJECT RELATIONSHIPS AND DEPENDENCIES

### 3.1 Dependency Chain (What Requires What)

```
Data Dictionary Items
  └─► Tables (columns ARE DD items)
       └─► Business Views (select columns FROM tables)
            ├─► Forms / FDA (each form REQUIRES a business view)
            │    ├─► Event Rules (operate on BV columns)
            │    ├─► Form Data Structures (auto-generated from BV)
            │    └─► Form Interconnects (use Form DS to pass data)
            └─► Report Sections / RDA (each section REQUIRES a business view)
                 ├─► Event Rules (operate on BV columns)
                 └─► Report Data Structures (for report interconnects)

Data Structures (BSFN DS)
  └─► Business Functions (every BSFN REQUIRES a DS)
       └─► Called FROM Event Rules (on forms, reports, or tables)

Processing Option DS
  └─► Attached to Interactive or Batch Applications
       └─► Read by Event Rules to drive conditional behavior

Table Event Rules
  └─► Attached to Tables (fire for ALL applications accessing that table)

Media Object DS
  └─► Attached to applications for media object functionality
```

### 3.2 Object Relationship Rules

| Rule | Explanation |
|------|-------------|
| DD items must exist BEFORE table columns | You cannot add a column to a table unless the data item is already defined in the Data Dictionary |
| Tables must exist BEFORE business views | A BV selects columns from one or more existing tables |
| Business views must exist BEFORE forms/reports | Every form and every report section must have a BV attached |
| BSFN DS must exist BEFORE business function | Every business function (C or NER) requires a defined data structure |
| Processing option DS is attached BEFORE versions | PO template must be created and attached to the app before creating versions with PO values |
| One BV per form | Each form gets exactly one business view (except header-detail forms which get two — header BV + detail BV) |
| BV generates Form DS automatically | When you attach a BV to a form, the system auto-generates the form data structure |
| Table Event Rules fire for ALL apps | Logic attached to a table via TER runs for every application that performs DB operations on that table |

### 3.3 How Objects Communicate

| From → To | Mechanism |
|-----------|-----------|
| Form → Form | Form Interconnect (passes data via Form DS) |
| Form → Business Function | ER calls BSFN, passing data via BSFN DS |
| Form → Table | Via Business View (read), or via Table I/O in ER (read/write) |
| Form → Report | Report Interconnect (passes data via Report DS) |
| Report → Table | Via Business View attached to report section |
| Report → Business Function | ER calls BSFN from within report processing |
| BSFN → Table | Via JDB APIs (JDB_InitBhvr → JDB_OpenTable → Fetch/Insert/Update/Delete → JDB_CloseTable → JDB_FreeBhvr) |
| BSFN → BSFN (external) | jdeCallObject (across DLLs) |
| BSFN → BSFN (internal, same DLL) | CALLIBF (no return) / CALLIBFRET (with return) |
| App → Processing Options | PO DS read at app launch, accessible via PO available objects in ER |

---

## PART 4: DEVELOPMENT WORKFLOW

### 4.1 Standard Development Sequence

Always start in OMW. Not every step is required for every project.

```
1. OMW ──► Create/select project, add objects
2. Data Dictionary ──► Create new DD items if needed (P92001)
3. Table Design (TDA) ──► Create table, select DD items as columns,
                          define primary + secondary indices,
                          add audit trail columns (USER, PID, MKEY, UPMJ, UPMT),
                          generate table
4. Table Event Rules ──► (Optional) Attach referential integrity logic to table
5. Business View Design ──► Select columns from table(s),
                            define joins if multi-table,
                            create the BV
6a. Form Design Aid (FDA) ──► Create interactive application:
    - Add forms (Find/Browse, Fix/Inspect, Header Detail, etc.)
    - Attach BV to each form
    - Place controls, bind to BV columns
    - Define form interconnections
    - Write event rules
6b. Report Design Aid (RDA) ──► Create batch application:
    - Add sections (columnar, group, tabular)
    - Attach BV to each section
    - Place fields, define level breaks
    - Write event rules
    - Create batch versions
7. Business Functions ──► (If needed) Create NER or C BSFNs:
    - Create BSFN DS first
    - Write function logic
    - Test and compile
8. Processing Options ──► (If needed) Create PO template:
    - Create PO DS
    - Attach to application/report
    - Define tab pages and data items
9. Menu Revisions ──► Add application to JDE menu system
10. Check In ──► Check all objects into the server
```

### 4.2 When to Create Each Object Type

| Scenario | Objects Needed |
|----------|---------------|
| **New interactive application** | DD items (if new) → Table (if new) → BV → Application (APPL) with Forms → ER → PO (optional) → Menu |
| **New batch report** | DD items (if new) → Table (if new) → BV → Report (UBE) with Sections → ER → Batch Version → PO (optional) → Menu |
| **New reusable business logic** | BSFN DS → Business Function (NER preferred, C if needed) |
| **Modify existing form** | Check out APPL → modify form/ER in FDA → check in |
| **Add field to existing form** | Verify DD item exists → modify BV to include column (if from table) → add control to form → update ER if needed |
| **New table** | DD items → Table (TDA) with indices + audit columns → Generate → Configure in OCM |
| **Cross-table integrity** | Table Event Rules on the parent table |
| **Runtime configuration** | PO DS → attach to application → read PO values in ER |

---

## PART 5: OBJECT-SPECIFIC CONSTRAINTS AND RULES

### 5.1 Data Dictionary Constraints

- Display decimals and file decimals CANNOT be overridden in FDA/RDA
- Alpha description, data type, and size CANNOT be overridden in FDA/RDA
- Allow blank entry, upper case only, triggers, and headings CAN be overridden
- Deleting a DD item does NOT check if it's in use — the dependent app will fail
- Changes to DD items are effective IMMEDIATELY for all applications
- Glossary group C, D, K, S items CAN be table columns; E, H, X, Y CANNOT
- Text substitution uses `&1`, `&2` placeholders in glossary text

### 5.2 Table Constraints

- Every table MUST have exactly one Primary Index
- Primary index = unique identifier for records; system won't save without it
- Index name max: 19 characters (exceeding causes compiler warnings and incorrect fetches)
- Max fields per index: 10
- **Generating an existing table CLEARS ALL DATA** — export first if modifying
- Every table should include audit columns: USER, PID, MKEY, UPMJ, UPMT
- Custom tables must use system codes 55–59
- Column prefix: exactly 2 characters, first alphabetic, no special characters

### 5.3 Business View Constraints

- Adding a new BV does NOT affect performance
- Using an existing BV with many unused columns DOES hurt performance
- Only ONE BV per form type (except header-detail which gets two)
- At least one BV per table should include ALL columns
- BV generates SQL for the target database — never write raw SQL
- For joined BVs, primary table name goes first in the description
- Do NOT enable Text Search unless the BV is specifically for full-text search

### 5.4 Data Structure Constraints

- Modifying an existing DS can have significant system-wide impact — use XREF first
- Form DS is auto-generated and modified through FDA
- Report DS is auto-generated with empty default — add fields through RDA File menu
- Every BSFN (C or NER) MUST have a data structure
- PO DS changes don't take effect until a new package is built; PO text changes are immediate

### 5.5 Form / Interactive Application Constraints

- Form type determines predefined layout and runtime behavior
- Find/Browse description convention: "Work With..."
- Entry Point property designates the first form shown
- Static text fields: allow 30% expansion room for translation
- Tab sequence follows natural reading flow (left to right, top to bottom)
- Limit grid columns displayed for performance
- Use work fields instead of hidden controls when possible
- Grid sort sequence MUST match the database index being used

**Form types and their purposes:**

| Form Type | Use When |
|-----------|----------|
| Find/Browse | Users need to search and list records |
| Fix/Inspect | Users need to view/edit a single record |
| Header Detail | Line items with a header context (e.g., Sales Order Entry) |
| Headerless Detail | Editable grid without header context |
| Search & Select | User must select and return a value to a calling form |
| Message | Confirmation dialog or simple message |
| Parent/Child | Hierarchical data (tree + grid) |
| Power Browse | Multiple simultaneous data views (read-only) |
| Power Edit | Multiple simultaneous data views (editable) |
| Wizard | Multi-step guided workflow |

### 5.6 Report / Batch Application Constraints

- A report is a template — runtime instances are batch versions
- You CANNOT process a report without a batch version
- Standard versions: XJDE = demo (do NOT modify), ZJDE = production (copy to customize)
- Font standard: 7pt Arial Regular
- Report name upper-left, date/time right side, page number upper-right, titles centered
- Tabular sections do NOT support: conditional sections, subsection joins, database output, section-level totals via standard mechanism, Do Section event
- Level breaks in UBE must match BI Publisher groups
- Perform sorting in the UBE, not in the BI Publisher template
- Avoid page-related data elements for BI Publisher (headers, footers, brought forward, carried forward)

### 5.7 Event Rules Constraints

- ER operates on data exposed by the attached BV
- Use numeric values (1/0) instead of T/F for boolean logic
- Use text variables instead of hard-coded text strings
- Use PID for database update audit fields
- Use `#` for unused parameters in BSFN calls
- Use directional arrows (→) to indicate data flow in assignments
- Table Event Rules apply ONLY to JDE applications, not external DB access
- Named Event Rules (NER) are reusable and compiled; embedded ER is not reusable
- BC and FC share the same internal structure (changing one changes both) — except for filter fields

**Available Objects in ER:**

| Code | What It Is | Usage |
|------|-----------|-------|
| BC | Business View column | Data from/to database |
| GC | Grid column | Current grid row value |
| GB | Grid buffer | Staging row for insert/update |
| FC | Form control | Screen field value |
| FI | Form interconnect value | Data passed between forms |
| PO | Processing option value | Runtime configuration |
| QC | QBE cell value | Query-by-example filter |
| VA | ER variable | Developer-defined variable |
| SV | System variable | Environment values |
| SL | System literal | Constants |
| HC | Hypercontrol item | Menu/toolbar items |

### 5.8 Business Function Constraints (C Code)

**Coding standards:**
- Comments: `/* */` only (NOT `//`) — max 80 chars wide
- Indentation: 3 spaces (no tabs)
- Compound statements: always use braces, one statement per line, braces on separate lines
- Single exit point preferred — use `idReturn` (ER_SUCCESS/ER_ERROR) to control flow
- All variables declared at beginning of function block, one per line
- Pointers initialized to NULL with type cast
- Data structures zeroed via memset
- MATH_NUMERIC and JDEDATE initialized to `{0}`

**Variable naming — Hungarian notation prefixes:**

| Prefix | Type | Prefix | Type |
|--------|------|--------|------|
| `c` | JCHAR | `mn` | MATH_NUMERIC |
| `sz` | NULL-terminated JCHAR string | `jd` | JDEDATE |
| `z` | ZCHAR | `lp` | Long pointer |
| `zz` | NULL-terminated ZCHAR string | `i` | Integer |
| `n` | Short | `by` | Byte |
| `l` | Long | `ul` | Unsigned long |
| `b` | Boolean | `us` | Unsigned short |
| `ds` | Data structure | `h` | Handle |
| `e` | Enumerated | `id` | Long integer (JDE return) |
| `ut` | JDEUTIME | — | — |

**Critical API patterns:**

| Operation | API |
|-----------|-----|
| Call external BSFN | `jdeCallObject` |
| Call internal BSFN (no return) | `CALLIBF` |
| Call internal BSFN (with return) | `CALLIBFRET` |
| Database init | `JDB_InitBhvr` → returns `hUser` |
| Open table | `JDB_OpenTable` → returns `hRequest` |
| Close table | `JDB_CloseTable` |
| Free DB handle | `JDB_FreeBhvr` |
| Copy string (same length) | `jdeStrcpy` |
| Copy string (different lengths) | `jdeStrncpy` (count excludes NULL terminator) |
| Character count | `DIM()` macro |
| Byte count | `sizeof()` |
| Store pointer for ER | `jdeStoreDataPtr` |
| Retrieve pointer from ER | `jdeRetrieveDataPtr` |
| Remove pointer from ER | `jdeRemoveDataPtr` |
| Allocate memory | `jdeAlloc` |
| Free memory | `jdeFree` |
| Set error | `jdeErrorSet` |

**MATH_NUMERIC rules:**
- NEVER use flat assignment (`=`) for MATH_NUMERIC — use `MathCopy` or `ZeroMathNumeric`
- Structure members: String, Sign, EditCode, nDecimalPosition, nLength, wFlags, szCurrency, nCurrencyDecimals, nPrecision

**JDEDATE rules:**
- NEVER use flat assignment — use `memcpy` or `JDEDATECopy` macro
- Structure members: nYear, nMonth, nDay

**Unicode compliance:**
- `JCHAR` (2 bytes) for Unicode, `ZCHAR` (1 byte) for non-Unicode
- Use `jdeSxxxxxxx` functions for Unicode strings
- Use `jdeZSxxxxx` functions for non-Unicode strings
- Pointer arithmetic uses character count, not byte count
- Use `jdeFromUnicode` / `jdeToUnicode` for third-party API conversion

**Portability rules:**
- ANSI-compatible code only
- No `//` comments (use `/* */`)
- No data alignment dependencies
- Lowercase `#include` filenames
- Newline at end of every file
- `'\0'` for null character (not `'/0'`)
- No unreferenced variables

---

## PART 6: TABLE I/O GUIDELINES

### 6.1 Standards

- Always update audit fields (date, time, user, program name) when modifying records
- Create one business function per table to encapsulate I/O operations
- Avoid cross-vertical table updates (e.g., don't have Financials code directly updating Manufacturing tables)
- Use business functions to encapsulate table operations — do not scatter raw table I/O across multiple forms

### 6.2 Table I/O in Event Rules

Use the Table I/O button in Event Rules Design to perform database operations without writing C code:
- Validate data
- Retrieve records
- Update or delete records across files
- Add records

View SQL via Log Viewer in `jdedebug.log` (debugging must be set to File in `jde.ini`).

### 6.3 Table I/O in C Business Functions

```
hUser = JDB_InitBhvr(lpBhvrCom, ...);
hRequest = JDB_OpenTable(hUser, tableId, ...);
/* Fetch/Insert/Update/Delete operations */
JDB_CloseTable(hRequest);
JDB_FreeBhvr(hUser);
```

Always pair: `JDB_InitBhvr` ↔ `JDB_FreeBhvr`, `JDB_OpenTable` ↔ `JDB_CloseTable`.

---

## PART 7: PERFORMANCE GUIDELINES

### 7.1 Form Performance

- Limit grid columns displayed to only what users need
- Limit BV columns to only those the form requires
- Minimize form controls
- Use work fields instead of hidden controls where possible
- Disable unnecessary DD functions (edit rules, visual assists) when not needed
- Grid sort sequence MUST match the database index being used
- Use "Stop Processing" to prevent unnecessary record retrieval

### 7.2 Business View Performance

- Adding a new BV has zero performance impact
- Using a BV with excess unused columns hurts performance
- Size BVs appropriately for the form type:
  - Search & Select: minimum fields
  - Find/Browse: moderate fields
  - Input-Capable: larger, all fields needed for add/update

### 7.3 General Performance

- Minimize database round-trips
- Use efficient queries with proper index alignment
- Avoid unnecessary processing in event rules
- Only fetch records that are needed

---

## PART 8: ERROR HANDLING AND MESSAGING

### 8.1 Error Message Types

| Type | Code Range | Usage |
|------|-----------|-------|
| JDB Errors | 078D–078K, 078S | Database operation errors |
| Cache Errors | 078L–078R | Cache operation errors |
| Interactive Errors | Glossary Group E | Real-time validation during data entry |
| Batch Errors | Glossary Group Y | Batch job completion messages |
| Log Messages | Glossary Group X | System operation logs |

### 8.2 Implementing Errors in BSFNs

- Use `cSuppressErrorMessage` in the DS to control error display
- Use `szErrorMessageID` in the DS to return error identifiers
- Use `jdeErrorSet` to set errors with text substitution
- DD trigger data structure: 3 predefined members (`idBhvrErrorId`/BHVRERRID, `szBehaviorEditString`/BHVREDTST, `szDescription001`/DL01) + 1 variable member per trigger

### 8.3 Implementing Errors in Event Rules

- Use system functions to set errors on controls
- Use text variables for error message text (never hard-code)
- Check return values from business function calls

---

## PART 9: CURRENCY AND INTERNATIONALIZATION

### 9.1 Currency

- Currency implementation is developer-controlled
- Use database triggers and Table Event Rules (TER) for currency retrieval
- Use business function event rules for currency calculations
- Use system APIs for accessing cached currency tables
- Standard display sequence: Currency Code (CRDC) → Exchange Rate (CRR) → Rate Base Currency Code (CRCD) → Foreign Option

### 9.2 Translation

- Allow 30% expansion room for all static text and field labels
- Use text variables instead of hard-coded text strings
- Use data dictionary jargon and alternate language support
- Test with longest language translations

---

## PART 10: INDUSTRY-SPECIFIC STANDARDS

### 10.1 Financials

- Use ALKY (Long Address Number, 20 chars) instead of AN8
- Use B0100016 (Scrub Address Number) business function
- Use X1202-F1201 (Validate Asset Number) for asset validation

### 10.2 Workforce Management

- Rename AN8 to "Employee Number"
- Retrieve job type/step from F08001

### 10.3 Manufacturing/Distribution

- Place Branch/Plant identifier in upper-right area
- Use MCU or MMCU for static text labels

---

## PART 11: CROSS REFERENCE AND DEBUGGING

### 11.1 Cross Reference Facility (XREF)

Use before modifying any shared object:
- Identify every application using a business function
- View all forms within an application
- Display all fields within a business view
- Cross-reference all applications using a specific field
- **Cross-reference files must be rebuilt periodically** — they are NOT auto-updated

### 11.2 Debugging

| Debugger | Use For |
|----------|---------|
| EnterpriseOne Event Rules Debugger | ER in interactive apps, reports, table conversions |
| Microsoft Visual C++ Debugger | C business functions, NERs generated into C |

---

## PART 12: DEVELOPMENT CHECKLISTS

### 12.1 New Interactive Application Checklist

- [ ] Create project in OMW
- [ ] Identify/create DD items for all fields
- [ ] Identify/create table(s) with proper naming, indices, and audit columns
- [ ] Create business view(s) — one per form, sized appropriately for form type
- [ ] Create application object (P-prefix) in OMW
- [ ] Design forms in FDA:
  - [ ] Entry-point form (usually Find/Browse, titled "Work With...")
  - [ ] Detail forms (Fix/Inspect or Header Detail as needed)
  - [ ] Search & Select forms (if selection patterns are needed)
- [ ] Attach BV to each form
- [ ] Place controls and bind to BV columns
- [ ] Configure tab sequence (left to right, top to bottom)
- [ ] Define form interconnections with proper DS mappings
- [ ] Write event rules for business logic
- [ ] Create/attach processing options if needed
- [ ] Create business functions (NER preferred) for reusable logic
- [ ] Test thoroughly
- [ ] Add to menu system
- [ ] Check in all objects

### 12.2 New Batch Report Checklist

- [ ] Create project in OMW
- [ ] Identify/create DD items for all fields
- [ ] Identify/create table(s) if needed
- [ ] Create business view(s) for each report section
- [ ] Create report object (R-prefix) in OMW
- [ ] Design in RDA:
  - [ ] Add sections (columnar, group, or tabular)
  - [ ] Attach BV to each section
  - [ ] Place fields and configure layout
  - [ ] Define level breaks and totals
  - [ ] Configure data selection and data sequencing
- [ ] Write event rules for processing logic
- [ ] Create processing options if needed
- [ ] Create batch version(s) — never modify XJDE/ZJDE, copy them
- [ ] Format: 7pt Arial, report name upper-left, page number upper-right
- [ ] Test batch version submission
- [ ] Check in all objects

### 12.3 New Business Function Checklist

- [ ] Determine: NER (preferred) or C business function
- [ ] Create BSFN data structure (D-prefix) in Data Structure Design
- [ ] Add all input/output parameters as DD items
- [ ] For NER: Create NER object (N-prefix) and write logic in Event Rules Design
- [ ] For C BSFN:
  - [ ] Create BSFN object (B-prefix) in OMW
  - [ ] Name source/header files (`bxxyyyy.c` / `.h`, max 8 chars)
  - [ ] Write external function with standard signature
  - [ ] Follow Hungarian notation for all variables
  - [ ] Use `/* */` comments only, max 80 chars wide
  - [ ] 3-space indentation, braces on separate lines
  - [ ] Initialize all variables at block beginning
  - [ ] Implement single exit point pattern
  - [ ] Handle errors via `jdeErrorSet` / DS error fields
  - [ ] Pair all JDB_Init/Free and Open/Close calls
  - [ ] Use `MathCopy` for MATH_NUMERIC (never `=`)
  - [ ] Use `memcpy`/`JDEDATECopy` for JDEDATE (never `=`)
  - [ ] Ensure ANSI portability (no `//`, no alignment deps)
  - [ ] Newline at end of file
  - [ ] Compile and test
- [ ] Check in all objects

### 12.4 Modifying an Existing Object Checklist

- [ ] Run Cross Reference Facility to understand impact
- [ ] Check out the object in OMW
- [ ] For DD items: changes are immediate system-wide — verify impact
- [ ] For tables: regeneration clears data — export first
- [ ] For BVs: deleting columns requires verifying no form/report uses them
- [ ] For DS: modifying affects all callers — use XREF
- [ ] Make changes
- [ ] Test all dependent objects
- [ ] Add change log entry (SAR number, Date, Initials, Comment)
- [ ] Check in

---

## PART 13: QUICK DECISION GUIDE

### "I need to..." → Use this approach:

| Need | Object(s) | Key Rules |
|------|-----------|-----------|
| Store new data | DD Item → Table → BV | Use sys codes 55–59; include audit columns; define primary index |
| Show data to users | BV → Form (FDA) | One BV per form; size BV to form type; set entry point |
| Generate a report | BV → Report (RDA) → Batch Version | Never modify XJDE/ZJDE; use sections appropriately |
| Reusable business logic | BSFN DS → NER or C BSFN | Prefer NER; use C only for performance/complexity; always create DS first |
| Pass data between forms | Form Interconnect + Form DS | Map DS members correctly; use FI objects in ER |
| Pass data to/from BSFNs | BSFN DS | Define all I/O params as DD items; use `#` for unused params |
| Configure app behavior at runtime | PO DS → Attach to app | Read PO values in ER; create versions with different PO values |
| Validate field values | UDC + DD trigger | Attach visual assist trigger to DD item |
| Enforce referential integrity | Table Event Rules | Attach to parent table; fires for ALL apps |
| Attach files to records | Media Object + MO DS | DS contains primary key fields of the record |
| Automate multi-step processes | Workflow | Use workflow tools; WF objects are non-OL |
| Find where an object is used | Cross Reference Facility | Rebuild XREF files periodically |

---

*Master reference synthesized from 10 Oracle JD Edwards EnterpriseOne Tools 9.2 guides: Development Tools Overview, Table Design, Business View Design, Data Dictionary, Data Structure Design, Event Rules, Form Design Aid, Report Design Aid, Application Design Guidelines, and Business Function Programming Standards.*
