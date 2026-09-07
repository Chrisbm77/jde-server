# JD Edwards EnterpriseOne Tools 9.2 — Development Tools Overview Reference

> **Source:** Development Tools Overview Guide | Part Number: E53551-03 | Oracle, 2020

---

## 1. Overview: How Development Works in JDE

JD Edwards EnterpriseOne is built on an **object-based architecture** — discrete, reusable software objects are the building blocks of every application. Applications are not monolithic programs; they are collections of objects that developers assemble, configure, and extend using the EnterpriseOne development tools.

The development environment enables you to:

- Design and define application objects
- Enable applications to serve different locations and languages while sharing the same data
- Define end-to-end processes in a user-friendly, graphical design environment

All development begins in the **Object Management Workbench (OMW)**, which manages every object through its lifecycle — creation, checkout, modification, check-in, and deployment.

---

## 2. The Object Model

In EnterpriseOne, an **object** is a reusable entity based on software specifications (metadata) created by the development tools. Each object has its own specification stored on both the server and the workstation. Specifications describe the object's type — for example, data structure specifications, processing option structures, or media object structures.

### Core Object Types

| Object Type | Abbreviation | Purpose |
|---|---|---|
| **Data Dictionary Item** | DD | Central repository of data item definitions and attributes |
| **Table** | TBLE | Relational database table storing application data |
| **Business View** | BSVW | Subset of data items from one or more tables for application use |
| **Data Structure** | DS / DSTR | Parameter list for passing data between objects |
| **Interactive Application** | — | User-facing forms for data entry, search, and display |
| **Batch Application** | UBE | Server-side reports and batch processes |
| **Business Function** | BSFN | Encapsulated business rules and logic (C code or NER) |
| **Event Rule** | ER | Logic statements attached to events on forms, reports, or tables |
| **Named Event Rule** | NER | Reusable business function event rules (compiled, stored as objects) |
| **Media Object** | — | Attachments (text, images, OLE, shortcuts, URLs) linked to records |
| **Processing Option** | PO | Runtime configuration parameters for applications/reports |
| **User Defined Code** | UDC | Validation code lists (non-Object Librarian) |
| **Workflow Object** | WF | Automated process flow definitions |

### Object Storage

Objects are stored in two locations:

1. **Central-storage server** — Central objects reside here for deployment. Specifications go into a relational database; DLLs and source code go on a file server.
2. **Workstation/server replicas** — A copy (replicated set) of the central objects must reside on each development workstation and server that runs EnterpriseOne. The **path code** indicates the directory where these objects are located.

Objects move between server and workstation via **check-in / check-out** in OMW. When you create an object, it initially resides only on your workstation. After check-in, it becomes available to others.

### Object Librarian vs. Non-Object Librarian Objects

**Object Librarian objects** (path code-based, support tokens):
- Batch applications and versions
- Business functions
- Business views
- Data structures
- Interactive applications
- Media objects
- Tables

**Non-Object Librarian objects** (data source-based):
- Data dictionary items
- User defined code items
- Workflow objects

---

## 3. The Development Cycle

The development cycle follows a specific sequence. Not every step is required for every project — you can skip steps if existing objects already meet your needs.

```
┌─────────────────────────────┐
│  Object Management Workbench │
│  (OMW)                       │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Table Design               │
│  + Table Event Rules        │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Business View Design       │
└──────────┬──────────────────┘
           │
     ┌─────┴──────┐
     ▼            ▼
┌──────────┐ ┌──────────────┐
│Form Design│ │Report Design │
│+ Event    │ │+ Event       │
│  Rules    │ │  Rules       │
└────┬─────┘ └──────┬───────┘
     │               │
     └───────┬───────┘
             ▼
     ┌───────────────┐
     │ Menu Revisions │
     └───────────────┘
```

### Step-by-Step Walkthrough

1. **Start in OMW** — Create or select a project, add objects to it
2. **Data Dictionary** — Define or verify data items (if new fields are needed)
3. **Table Design** — Create tables if existing ones don't cover the requirement; select data items, assign key fields/indexes. Optionally attach **Table Event Rules** for referential integrity
4. **Business View Design** — Select data items from one or more tables that the application needs. This generates the SQL. Both interactive and batch applications require a business view
5. **Form Design (FDA)** — For interactive applications: create forms, associate each form with a business view, add controls (grids, fields, buttons). Attach **Event Rules** for business logic
6. **Report Design (RDA)** — For batch applications: create report templates with sections, associate with business views. Attach **Event Rules** for processing logic
7. **Business Functions** — Create reusable logic (C or NER) that can be called from forms, reports, or other business functions
8. **Menu Revisions** — Add the completed application to the EnterpriseOne menu system

---

## 4. Object Types In Depth — Purpose and Relationships

### 4.1 Data Dictionary (DD)

**What it is:** A central repository containing every data item definition used across the entire system.

**What it controls:**
- How a data item appears on reports and forms (column headings, row descriptions)
- Data entry validation within applications
- Field help text
- How data is stored in tables

**Key behavior:** The data dictionary is **dynamic** — any change to a data item is effective immediately for all applications that use it. This means modifying a data item's type or attributes can affect data storage and cause discrepancies.

**Relationships:**
- Data items must exist in the DD **before** they can be added to a table
- DD items define the columns in tables
- DD items define the fields in business views
- DD items define the members in data structures
- DD items provide edit rules, visual attributes, and help text to forms and reports at runtime

### 4.2 Tables (TBLE)

**What it is:** A relational database table storing application data in columns (data items) and rows (records).

**What it does:**
- Stores all persistent application data
- Uses key fields as indexes for retrieval and update
- Must be formally defined via Table Design so EnterpriseOne recognizes it

**Relationships:**
- Tables are composed of **Data Dictionary items** (columns)
- Tables are accessed through **Business Views** (never directly by forms/reports)
- Tables can have **Table Event Rules (TER)** attached — database triggers that fire for any application hitting that table
- Tables are the ultimate data source for both interactive and batch applications

### 4.3 Business Views (BSVW)

**What it is:** A selection of data items from one or more tables, defining exactly what data an application needs.

**What it does:**
- Links applications to tables
- Generates the appropriate SQL for the target database platform
- Reduces network traffic by selecting only needed columns
- Supports joins and unions across multiple tables

**Key rule:** Every form and every report section **must** have a business view attached.

**Relationships:**
- Business views pull **data items from tables**
- Business views are **required by forms** (FDA) and **report sections** (RDA)
- Business views generate the **Form Data Structure** automatically when attached to a form
- Business views determine which data items are available to event rules on that form/report

### 4.4 Data Structures (DS / DSTR)

**What it is:** A list of parameters (data items) used to pass data between objects.

**Types of data structures:**

| Type | Generated By | Purpose |
|---|---|---|
| **Form DS** | System (auto) | Passes parameters between forms during Form Interconnects |
| **Report DS** | System (auto) | Passes parameters to/from batch applications |
| **Media Object DS** | User (manual) | Passes arguments to the media object table |
| **Processing Option DS** | User (manual) | Defines runtime configuration parameters |
| **Business Function DS** | User (manual) | Defines input/output parameters for BSFNs |

**Relationships:**
- Data structures are composed of **Data Dictionary items**
- **Form DS** connects to **Form Interconnects** (form-to-form navigation)
- **Report DS** connects to batch application parameters
- **BSFN DS** is the required interface for every **Business Function** call
- **Processing Option DS** attaches to both interactive and batch applications
- Data structures are the **communication contract** between any two objects that exchange data

### 4.5 Forms / Interactive Applications (FDA)

**What it is:** The graphical user interface through which users interact with the system. An application is a collection of one or more forms.

**Form types:**
- **Find/Browse** — Search and list records (usually the first form)
- **Fix/Inspect** — View/edit a single record's detail
- **Power Forms** — Combine search and detail in one form

**What it does:**
- Presents data logically to users
- Contains controls: grids, edit fields, push buttons, radio buttons
- Receives and sends parameters through Form Interconnects

**Relationships:**
- Each form is associated with a **Business View** (which connects it to tables)
- Forms contain **Event Rules** (embedded ER) for business logic
- Forms call **Business Functions** through event rules
- Forms use **System Functions** for built-in operations
- Forms receive runtime configuration through **Processing Options**
- Forms connect to other forms via **Form Interconnects** (passing data through Form DS)
- Forms can have **Media Objects** attached to records/rows
- Interactive Application Design includes both FDA and Event Rules Design

### 4.6 Reports / Batch Applications (RDA)

**What it is:** Server-side batch processes that present data from the database, created through Report Design Aid.

**Key concepts:**
- A report is a **template** (set of specifications) from which multiple **Batch Versions** can be created
- Batch versions define processing options, data selection, and data sequencing
- Once submitted, batch versions run without user interaction
- Reports are composed of **sections** (building blocks)

**Relationships:**
- Report sections are associated with **Business Views**
- Reports contain **Event Rules** for processing logic
- Reports call **Business Functions** for complex operations
- Reports receive configuration through **Processing Options**
- Reports generate output reviewed via **BrowsER**, cover pages, and logs
- Batch versions are managed through the **Batch Versions** tool

### 4.7 Event Rules (ER)

**What it is:** Logic statements created and attached to events. Events are activities on forms (entering a field, clicking a button), reports (processing a section), or tables (database operations).

**Types of event rules:**

| Type | Scope | Where Attached | Reusable? |
|---|---|---|---|
| **Embedded ER** | Specific to one application or table | Forms (FDA), Reports (RDA), Tables (TDA) | No |
| **Business Function ER (NER)** | Standalone, compiled object | Stored as objects in Object Librarian | Yes |
| **Application Event Rules** | Specific to one application | Interactive apps (FDA) or Batch apps (RDA) | No |
| **Table Event Rules (TER)** | Specific to one table | Table Design Aid (TDA) | Shared by all apps using that table |

**What ER can do:**
- Conditional logic (If/Else/While)
- Assignments and calculations
- Call business functions
- Form/report interconnections
- Call system functions
- Table I/O operations (validate, retrieve, update, delete, add records)

**Where ER can be attached:**
- **Controls** — push buttons, edit fields, grids (each control has event points)
- **Events** — user-initiated (tab, click) or system-initiated (Last Grid Record Read)
- **Form Processing** — default business logic per form type

**Relationships:**
- ER operates on data exposed by the **Business View** attached to the form/report
- ER calls **Business Functions** (both C and NER) through data structures
- ER calls **System Functions** for tool-provided operations
- ER uses **Table I/O** to access tables directly (without coding C)
- ER passes data between forms via **Form Interconnects** and **Data Structures**
- **Table Event Rules** fire for ALL applications that perform database operations on that table — providing centralized referential integrity

### 4.8 Business Functions (BSFN)

**What it is:** An encapsulated set of business rules and logic that accomplishes a specific task, reusable across multiple applications.

**Two creation methods:**
1. **Named Event Rules (NER)** — Created using the event rules scripting language; preferred when possible. NERs get generated into C or Java.
2. **C Business Functions** — Written directly in C code. Used for: batch error-level messaging, large/complex functions, performance-critical operations, complex SQL statements.

**Categories:**
- **Master Business Functions** — Access master files (Address Book, Item Master). Provide full transaction functionality: validation, security, data integrity. Third-party apps should use these for complete EnterpriseOne integration.
- **Transaction Master Business Functions** — Access transaction files (Sales Orders, Purchase Orders). Simpler than master file BSFNs. Contain all default values and editing logic for transaction integrity.

**Relationships:**
- Business functions require a **Business Function Data Structure** (BSFN DS) as their interface
- Business functions are called from **Event Rules** (on forms, reports, or tables)
- Business functions access **Tables** through database APIs (hUser, hRequest)
- Business functions can call other business functions (via jdeCallObject or CALLIBF/CALLIBFRET)
- Business functions provide the **reusable business logic layer** between the UI (forms/reports) and the database (tables)

### 4.9 System Functions

**What it is:** Predefined procedures shipped with EnterpriseOne that perform specialized operations without custom code.

**Where used:** Within Event Rules in FDA, RDA, and Workflow. Each tool has its own specific set of available system functions.

**Examples:** Hide/show fields, execute sections in batch, navigate between forms.

**Relationship:** System functions are called from **Event Rules** — they are the built-in counterpart to user-written **Business Functions**.

### 4.10 Processing Options (PO)

**What it is:** Runtime configuration parameters that control how an application or report processes data and appears to users.

**What they do:**
- Control navigation paths
- Set default values
- Configure behavior for different companies/users
- Control form/report formatting
- Manage page breaks and totaling
- Specify default versions of related applications

**Key concept:** Processing options let you create different **versions** of the same application without building a new application. Each version can have unique processing option values.

**Relationships:**
- Processing options are defined through a **Processing Option Data Structure**
- Processing options attach to **Interactive Applications** and **Batch Applications**
- Processing options are set at the **Batch Version** level for reports
- Processing options are read by **Event Rules** to drive conditional logic

### 4.11 Media Objects

**What it is:** Attachments that enrich records with additional information — text, images, OLE objects, shortcuts (links to other EnterpriseOne applications), and URLs.

**Attachment types:**
- **Text** — Word-processor style text attachments
- **Image** — Bitmaps, GIFs, JPEGs, scanned documents
- **OLE** — Links to external programs (Excel, Word, etc.)
- **Shortcuts** — Links to other EnterpriseOne applications
- **URLs/Files** — Links to web pages or file system resources

**Relationships:**
- Media objects attach to **applications, forms, rows**, and **Object Librarian objects**
- Media objects require a **Media Object Data Structure** to pass arguments
- System administrators can set up **templates** with predefined attachments

### 4.12 Workflow (WF)

**What it is:** Automation of high-volume, formerly paper-based processes into email-based process flows across a network.

**What it does:** Documents, information, and tasks pass between participants based on procedural rules, resulting in automated processes with minimal user involvement.

**Relationships:**
- Workflow uses **Event Rules** for process logic
- Workflow connects to **Business Functions** for data operations
- Workflow objects are **non-Object Librarian** objects (data source-based)

---

## 5. Object Relationship Map

The following shows how all object types connect to each other:

```
                        ┌──────────────┐
                        │ DATA         │
                        │ DICTIONARY   │
                        │ (DD)         │
                        └──┬───┬───┬──┘
              ┌────────────┤   │   ├────────────────┐
              ▼            ▼   │   ▼                ▼
        ┌──────────┐ ┌────────┐│┌───────────┐ ┌──────────────┐
        │ TABLES   │ │BUSINESS││ │  DATA     │ │ PROCESSING   │
        │ (TBLE)   │ │ VIEWS  │││STRUCTURES │ │ OPTIONS DS   │
        │          │ │(BSVW)  │││  (DS)     │ │              │
        └─┬──┬─────┘ └──┬──┬─┘│└──┬──┬─────┘ └──────┬───────┘
          │  │           │  │  │   │  │               │
          │  │    ┌──────┘  │  │   │  │               │
          │  │    │    ┌────┘  │   │  └────────┐      │
          │  │    │    │       │   │            │      │
          │  │    ▼    ▼       │   ▼            ▼      ▼
          │  │ ┌─────────┐    │ ┌──────────┐ ┌──────────────┐
          │  │ │  FORMS   │   │ │ BUSINESS │ │ INTERACTIVE  │
          │  │ │  (FDA)   │◄──┼─│FUNCTIONS │ │ & BATCH      │
          │  │ │          │   │ │ (BSFN)   │ │ APPLICATIONS │
          │  │ └────┬─────┘   │ └─────┬────┘ └──────────────┘
          │  │      │         │       │
          │  │      ▼         │       │
          │  │ ┌─────────┐   │       │
          │  │ │  EVENT   │◄──┘      │
          │  └►│  RULES   │◄─────────┘
          │    │  (ER)    │
          │    └────┬─────┘
          │         │
          │         ▼
          │    ┌─────────┐
          │    │ TABLE    │
          └────│ EVENT    │
               │ RULES   │
               │ (TER)   │
               └─────────┘
```

### Key Dependency Chains

**Data flow (bottom-up):**
```
DD Items → Tables → Business Views → Forms/Reports → Event Rules → Business Functions
```

**Development sequence (top-down):**
```
OMW → DD (if needed) → Table Design → Business View → FDA/RDA → Event Rules → Menu
```

**Runtime call chain:**
```
User → Form → Event Rule → Business Function → Table (via DB APIs)
                         → System Function
                         → Table I/O (direct)
                         → Form Interconnect → Another Form
```

---

## 6. Object Management Workbench (OMW)

OMW is the **central hub** for all development activity. Everything begins and ends here.

### Projects
- All development must occur within a **project**
- Projects contain objects and owners
- Users must be added to a project in a role with permission to add objects
- A user can belong to multiple projects with different roles

### Allowed Actions
- Rules that define what actions a user role can perform
- Configured per: user role, object type, and project status
- Set up through the OMW Configuration program

### Tokens
- Prevent one user from overwriting another user's changes
- Provide a single-checkout environment (no merging/versioning of specs)
- Only **Object Librarian objects** have tokens

### The OMW Interface
Three panels (left to right):
1. **Project window** — displays projects, related objects, and users
2. **Center column** — action buttons for the selected object (context-sensitive)
3. **Information window** — displays web site, project status, release info, object info, or search results

---

## 7. Additional Development Topics

### 7.1 Caching (JDECACHE)

A process that stores local copies of frequently accessed remote data for performance improvement. Two modes:
- **Automatic** — System caches certain tables (e.g., constants) at startup
- **Application-level** — JDECACHE APIs let developers use server/workstation memory as temporary storage

JDECACHE can hold any indexed data type, is platform-independent, supports both fixed-length and variable-length records, and requires only a simple API set.

### 7.2 Messaging

Four message types for communicating with users:
1. **Interactive error message** — Real-time during record entry
2. **Informational message** — Sent to Workflow Center for follow-up
3. **Alert message** — Urgent, requires immediate attention
4. **Batch error message** — Generated during report/batch processing

Batch error messages appear in the **Employee Work Center** after a batch job completes, using a tree structure (parent/child) to organize related messages. Messages support text substitution and can be made "active" (clickable to open an associated form).

### 7.3 Transaction Processing

A logical unit of work (one or more SQL statements) performed atomically on the database. Either all updates succeed or none do, maintaining data consistency and integrity. Developers enable transaction processing and define which database operations comprise a transaction through the development tools.

### 7.4 Currency

For international enterprises, EnterpriseOne handles:
- Local currency conversion
- Multi-currency consolidation for reporting
- Regulatory compliance across countries
- Exchange rate fluctuation/revaluation

Currency implementation is developer-controlled through: database triggers and Table Event Rules (TER), business function event rules, and system APIs for cached table access.

### 7.5 Debugging

Two debugger tools:
1. **EnterpriseOne Event Rules Debugger** — For debugging ER in interactive applications, reports, and table conversions
2. **Microsoft Visual C++ Debugger** — For debugging C business functions or NERs generated into C

### 7.6 Cross Reference Facility (XREF)

Determines where objects are used and shows relationships between objects and their components:
- Identify every instance where a business function is used
- View all forms within an application
- Display all fields within a business view
- Cross-reference all applications using a specific field

Cross-reference files must be **rebuilt periodically** (they are not auto-updated when objects change).

---

## 8. Acronym Quick Reference

| Acronym | Meaning |
|---|---|
| BDA | Business View Design Aid |
| BSFN | Business Function |
| BSVW | Business View |
| CSV | Comma Separated Values |
| DD | Data Dictionary |
| DS / DSTR | Data Structure |
| ER | Event Rules |
| FDA | Form Design Aid |
| H4A | HTML for Applications |
| NER | Named Event Rule |
| OCM | Object Configuration Manager |
| OL | Object Librarian |
| OMC | Object Management Configuration |
| OMW | Object Management Workbench |
| OSA | Output Stream Access |
| PO | Processing Option |
| QBE | Query by Example |
| RDA | Report Design Aid |
| TAM | Table Access Management |
| TBLE | Table |
| TC | Table Conversions |
| TDA | Table Design Aid |
| TER | Table Event Rule |
| UBE | Universal Batch Engine |
| UDC | User Defined Code |
| UTB | Universal Table Browser |
| WF | Workflow |
| XREF | Cross Reference Facility |

---

## 9. Summary: What Each Object Does and When to Use It

| When You Need To... | Use This Object | Created With |
|---|---|---|
| Define a new field/column | Data Dictionary Item | Data Dictionary |
| Store data persistently | Table | Table Design Aid (TDA) |
| Enforce referential integrity at the DB level | Table Event Rule | Table Design Event Rules |
| Select specific columns for an app | Business View | Business View Design (BDA) |
| Build a user interface | Interactive Application (Forms) | Form Design Aid (FDA) |
| Add logic to a form | Embedded Event Rule | Event Rules Design (in FDA) |
| Build a report or batch process | Batch Application | Report Design Aid (RDA) |
| Create a reusable batch version | Batch Version | Batch Versions tool |
| Write reusable business logic | Business Function (NER or C) | Event Rules Design / C IDE |
| Pass data between objects | Data Structure | Data Structure Design |
| Configure app behavior at runtime | Processing Option | Processing Option DS |
| Validate field values against a list | User Defined Code | UDC tool |
| Attach files/text to records | Media Object | Media Object tools |
| Automate multi-step processes | Workflow | Workflow tools |
| Find where an object is used | Cross Reference | XREF Facility |

---

*Reference generated from JD Edwards EnterpriseOne Tools 9.2 Development Tools Overview Guide (E53551-03)*
