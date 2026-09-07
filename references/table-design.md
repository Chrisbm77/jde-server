# JD Edwards EnterpriseOne — Table Design Reference (TBLE Objects)

*Source: JD Edwards EnterpriseOne Tools — Table Design Guide, Release 9.2 (Part Number E53616-03)*

---

## 1. Overview

Tables are the foundational data-storage objects in JD Edwards EnterpriseOne. The system uses a relational database where tables are related through common key fields. Each column in a table is a **data item** (drawn from the Data Dictionary), and each row is a **record**. Custom tables can be created for use in JDE applications.

**Object Type Code:** `TBLE`  
**Object Use:** `2` (or any value from the 200 series)  
**Design Tool:** Table Design Aid (Form `W9860AL`)  
**Management Tool:** Object Management Workbench (OMW, Form `W98220A`)

---

## 2. Naming Conventions

Table names follow the format **Fxxxxyyy** (max 8 characters):

| Position | Meaning | Examples |
|---|---|---|
| **F** | Prefix — indicates a data table | Always `F` |
| **xx** (digits 2–3) | System code | `00` = Foundation, `01` = Address Book, `03` = AR, `03B` = AR, `04` = AP, `09` = GL, `11` = Multicurrency |
| **xx** (digits 4–5) | Group type | `01` = Master, `02` = Balance, `1X` = Transaction |
| **yyy** (digits 6–8) | Object version / variant | Programs performing similar functions but differing in specific processing |

**Suffixes:**
- `LA` through `LZ` = Logical file
- `JA` through `JZ` = Table join

**Column Prefix:** Every column in a table must have a unique **two-character prefix**. The first character must be alphabetic; the second can be alphanumeric. No special characters (`$`, `#`, `@`). The prefix typically reflects the data domain (e.g., columns in the Address Book Master `F0101` begin with `AB`).

**Table Description:** Max 60 characters. Should describe the table's topic. If the description comes from IBM i, it should match the file name (e.g., `F0101` = "Address Book Master", `F4101` = "Item Master").

**Custom Tables:** Use product codes **55–59** (reserved for clients). Example: `F550101A`.

---

## 3. Creating Tables — Step by Step

### 3.1 Create a Table Object in OMW

1. Open **Object Management Workbench** (W98220A).
2. Click the **Objects** node of a project and click **Add** → opens **Add EnterpriseOne Object to the Project** (W98220C).
3. Select **Table** and click **OK** → opens **Add Object** form (W9861AF).
4. Fill in:
   - **Object Name** — unique name following `Fxxxxyyy` convention
   - **Description** — meaningful, ≤60 chars
   - **Product Code** — UDC 98/SY; use 55–59 for custom
   - **Product System Code** — UDC 98/SY representing the JDE module
   - **Object Use** — `2` (Files) or any 200-series value
   - **Column Prefix** — two-character prefix for all columns
5. Object Type is auto-populated as `TBLE`.

### 3.2 Design the Table (Table Design Aid)

Click **OK** on Add Object (or select a table in a project and click **Design**) to open the **Table Design Aid** (W9860AL). This is a single window with four sub-forms:

| Sub-Form | Purpose |
|---|---|
| **Columns** | Shows the data items selected for the table |
| **Data Dictionary Browser** | Search/locate data items via QBE |
| **Indices** | Define keys for sorting and unique identification |
| **Object Properties** | Attributes of a selected data item |

**Selecting Data Items:**
1. Use the QBE line in the Data Dictionary Browser to find data items.
2. Double-click or drag items to the Columns form.
3. Tables can contain data items from multiple system codes.
4. To remove: select the column → Edit → Delete.

**Important:** Data items must exist in the Data Dictionary before they can be added. Modifying/deleting items requires table regeneration and can affect dependent business views and forms.

### 3.3 Include Audit Trail Columns

Every new table should include these standard audit columns:

| Column | Alias | Purpose |
|---|---|---|
| User ID | `USER` | Who last modified the record |
| Program ID | `PID` | Which program made the change |
| Machine Key | `MKEY` | Which machine was used |
| Date - Updated | `UPMJ` | Date of last modification |
| Time - Last Updated | `UPMT` | Time of last modification |

### 3.4 Define Indices

Indices locate specific records and sort data faster.

**Rules:**
- Every table **must** have exactly one **Primary Index** (marked with key icon + letter "P").
- The primary index is the unique identifier for each record — the system won't save without it.
- Primary index is used to build business views.
- A **unique index** is marked with a single key (right-click → toggle Unique).
- Index name max length: **19 characters**. Exceeding this causes compiler warnings and incorrect fetches in business functions.
- Max fields per index: **10**.
- Index naming: one field → use field name; two fields → list consecutively; more fields sharing first two fields with another index → append an alpha character. Commas and spaces between fields and the alpha suffix.
- Right-click a data item in an index → toggle **Ascending/Descending** sort order.

### 3.5 Generate the Table

Generating creates the physical table in the database. **Generating an existing table clears all data from it.**

1. From Table Design form → **Table Operations** tab → **Generate Table** → opens Generate Table form (W9866E).
2. Fill in:
   - **Table Name** — auto-populated
   - **Data Source** — where the database resides (e.g., "Business Data - TEST")
   - **Object Owner ID** — database owner (e.g., "TESTDTA")
   - **Password** — password for the owner ID
3. Click **OK**.

Table generation also creates a `.h` (header) file used in business functions and table event rules.

**To preserve data on modification:** Export data → Regenerate table → Import data back.

**Object Configuration Manager** (P986110) is used to configure which data source a table maps to. If none is specified, the default data source mapping is used. Changing the path code causes a drop + recreate.

### 3.6 Generate Indices Only

Use when modifying existing indices or creating additional indices **without** regenerating the entire table. This preserves existing data. Also modifies the `.h` file.

- Table Design form → **Table Operations** tab → **Generate Indexes** (W9866J).

### 3.7 Generate Header Files Only

Header files (`.h`) are used in business functions and table event rules. Located in the Include folder of the path code (e.g., `E812\DV812\Include`).

- Table Design Aid → **Design Tools** tab → **Generate Header File**.

---

## 4. Additional Table Operations

### 4.1 Copying Tables

- Use the **Copy Table** feature (W9866M) to copy data from one data source to another.
- This copies data only — **not** the table specifications.
- You can also use **Table Conversion** to copy between data sources.
- Fields: Table Name, Source Data Source, Destination Data Source, Object Owner ID, Password.

### 4.2 Removing Tables

- Deleting a table via Table Design Aid removes only **specifications**, not the physical table.
- To completely remove: **Table Operations** tab → **Remove Table From Database** (W9866D).
- Fields: Table Name, Data Source, Object Owner ID, Password.

### 4.3 Viewing Data

Two tools:
- **JD Edwards Data Browser** (web client) — secured via Security Workbench (P00950)
- **Universal Table Browser (UTB)** (Windows client) — secured via form security on W98TAMC

Both verify data existence and table structure across all supported database types.

**UTB Format Data options:**
- **Formatted** — displays according to Data Dictionary specs (e.g., `56.2185` for a PROC value stored as `562185`)
- **Unformatted** — displays raw database values (e.g., `562185.000000000000000`)

### 4.4 Modifying Table Objects

1. Click **OK** on Add Object or select a table → click **Design**.
2. On the **Summary** tab, revise: Description, Product Code, Product System Code, Object Use.
3. On the **Attachments** tab, enter documentation text.

---

## 5. Table I/O (Input/Output)

Table I/O is used within **Event Rules Design** to create instructions for database read/write operations. It enables table access through event rules.

### 5.1 Available Operations

| Operation | Description |
|---|---|
| **FetchSingle** | Combines Select + Fetch. Uses indexed columns for Select, non-indexed for Fetch. Opens the table but does not close it (auto-closes when form closes). |
| **Insert** | Inserts a new row |
| **Update** | Updates an existing row. Only mapped columns are updated. Partial key updates may affect multiple records. |
| **Delete** | Deletes one or more rows |
| **Open** | Opens a table or business view |
| **Close** | Closes a table or business view |
| **Select** | Selects rows for a subsequent FetchNext |
| **SelectAll** | Selects all rows for FetchNext |
| **FetchNext** | Fetches rows from a Select; can loop or chain multiple FetchNext calls |

### 5.2 Mapping Operators by Operation

| Operation | Valid Operators |
|---|---|
| FetchSingle | Index fields: `=, <, <=, >, >=, !=, Like`; Non-index: Copy Target |
| Insert | All fields: Copy Source |
| Update | Index fields: `=`; Non-index: Copy Source |
| Delete | All fields: `=` |
| Open / Close | N/A |
| Select | All fields: `=, <, <=, >, >=, !=, Like` |
| SelectAll | N/A |

**Return code:** Stored in system variable `SV File_IO_Status`. On Insert/Flush failure, may contain `CO ERROR_DETAILS_AVAILABLE` — use **Get Error Data** special operation to retrieve details.

### 5.3 Creating Table I/O Event Rules

1. Open a batch application in RDA → access Event Rules Design.
2. Click **Table I/O** button.
3. On the Insert TableIO Operation form → select operation (Basic, Advanced, or Special) → click **Next**.
4. Select a table, business view, or handle as the data source → click **Next**.
5. On the Mapping form → map Available Objects to table columns.
6. Set operators for each mapping.
7. Click **Finish**.

---

## 6. Buffered Inserts

Buffered inserts improve performance when inserting hundreds or thousands of records. They are **not** available with interactive applications — only with:
- Table conversions
- Table I/O
- Batch processes
- Business functions

**Supported databases only:** Oracle (V8+), DB2/400, SQL Server. Not available with Access or multiple-table views.

**How they work:** Records are inserted individually; the buffer auto-flushes when full. The middleware delivers one buffer load at a time. The buffer can also be explicitly flushed (on commit, table/view close, or via the business function/Table I/O feature).

**Error handling:** Buffered inserts provide no immediate feedback on failure — errors go to a log file. For detailed error messages, use the Table Conversion application's tracing feature or explicitly request them. Clear the output tables to avoid duplicate error logging.

### 6.1 Special Operations for Buffered Inserts

| Operation | Purpose |
|---|---|
| **Flush Insert Buffer** | Flushes pending inserts to the database. Must be done before any non-insert operation on the same table. Must flush before closing the table. |
| **Get Error Data** | Retrieves error information for failed inserts. Retrieve **before** the next insert begins, as new inserts overwrite error data. Returns the values used in the failed insert for all requested columns. |

### 6.2 Using Buffered Inserts (in RDA Event Rules)

1. Click **Table I/O** button.
2. Select **Open** under Advanced Operations → click **Next**.
3. Select the table → click **Advanced Options**.
4. Select **Buffer Inserts** → click **OK**.

---

## 7. Handles

A **handle** is a file pointer connecting the application or Universal Batch Engine (UBE) to the JDE database middleware. Handles point to a database table and are references to addresses within the middleware.

**Handles enable:**
- Concurrently opening multiple instances of a single table or business view.
- Opening a table/business view in an environment different from the login environment.
- Passing into forms, named event rules, or business functions to avoid reopening tables.

**Handles cannot** be used in transaction processing.

### 7.1 Creating a Handle Data Dictionary Item

Navigate: EnterpriseOne Life Cycle Tools → Application Development → Data Dictionary Design → Work With Data Dictionary Items.

**Key fields:**
- **Data Item:** 32-char alphabetical, no spaces/special chars (e.g., `HandleF0116`)
- **Alias:** unique identifier (e.g., `HF550116`)
- **Glossary Group:** `D` (Primary Data Elements)
- **Data Type:** `7` (Identifier) — handle is an identifier type
- **Class:** `HANDLE`
- **Control Type:** `4`
- **Product Code:** 55–59 for clients
- **Size:** `11`

### 7.2 Using Handles with Table I/O

1. Create an event rule variable using the handle data dictionary item.
2. Click **Table I/O** → select **Open** under Advanced Operations → click **Next**.
3. On the Data Source form → select **Handles** tab → select handle → click **Next**.
4. Select a variable for the environment name → click **Finish** (use `SL LoginEnvironment` for the login environment).
5. Perform table I/O operations.
6. To close: Table I/O → **Close** → **Handles** tab → select handle → **Finish**.

---

## 8. Table Event Rules (Database Triggers)

Table event rules attach database triggers that automatically run when an action (event) occurs against the table. They provide embedded logic at the table level — **neither the calling application nor the user is notified** of changes or events.

### 8.1 Available Events

- After Record is Deleted
- After Record is Fetched
- After Record is Inserted
- After Record is Updated
- Before Record is Deleted
- Before Record is Inserted
- Before Record is Updated
- Currency Conversion is On

### 8.2 Available Functions in Table Event Rules

| Function | Description |
|---|---|
| Assignment/Expression | Create assignments and complex expressions |
| If/While | Conditional statements |
| Business Function | Call existing business functions |
| System Function | Attach JDE system functions |
| Variables | Create event rule variables |
| Else | Insert ELSE clause (within IF/ENDIF) |
| Table I/O | Database access event rules |

**No data structures required** — the table itself serves as the data structure passed to the function.

### 8.3 Building Table Event Rules

The build process:
1. Converts the event rule to C source code → creates `OBNM.c` and `OBNM.hxx` (one function per event).
2. Creates a make file to compile the code.
3. Runs the make file → compiles and adds functions into `JDBTRIG.DLL` (consolidated table event rule DLL).

### 8.4 Creating Table Event Rules — Procedure

1. Open **OMW** → check out the table → click **Design**.
2. On Table Design form → **Design Tools** tab → click **Start Table Trigger Design Aid**.
3. Select an event from the Events list.
4. In Event Rules Design → click event rule buttons → complete the rules.
5. Click **Save** → click **Close**.
6. **If creating a new table:** Table Operations tab → Generate Table (enter Data Source + Password + click OK). **Never do this on an existing table — it clears all data.**
7. On Table Design form → **Design Tools** tab → click **Build Table Triggers**.
8. To review the build log: Generate Header File → open the created file.

The resulting table event rule is called by the JDE database middleware whenever the corresponding event occurs.

---

## 9. Forms Reference

| Form Name | Form ID | Navigation | Purpose |
|---|---|---|---|
| Object Management Workbench | W98220A | EnterpriseOne Life Cycle Tools → Application Development (GH902) → OMW | Select/view objects, access design tools |
| Add EnterpriseOne Object to the Project | W98220C | Click Objects node → Add in OMW | Add new objects to a project |
| Add Object | W9861AF | Select Table → OK on Add Object form | Enter table name, description, product code, column prefix |
| Table Design Aid | W9860AL | Complete Add Object → OK | Main design surface: columns, indices, DD browser, properties |
| Generate Table | W9866E | Table Operations → Generate Table | Generate physical table in database |
| Generate Indexes | W9866J | Table Operations → Generate Indexes | Regenerate indices only (preserves data) |
| Copy Table | W9866M | Table Operations → Copy Table | Copy table data between data sources |
| Remove Table | W9866D | Table Operations → Remove Table from Database | Physically remove table from database |
| Universal Table Browser | N/A | Development Tools (GH902) → Object Management | View table data |

---

## 10. XML Par File Considerations for Table Objects

When packaging JDE table objects (TBLE) for deployment via XML par files, the following attributes are relevant:

**Object Identification:**
- **Object Name:** The `Fxxxxyyy` table name
- **Object Type:** `TBLE`
- **Product Code:** The system code (UDC 98/SY)
- **Product System Code:** The JDE module code
- **Object Use:** `2` (Files)

**Dependencies to include in the package:**
- The table specification itself (columns, indices, primary key)
- Associated **Data Dictionary items** used as columns (if custom)
- Any **Table Event Rules** (compiled into `JDBTRIG.DLL`)
- The generated **header file** (`.h`) — required by business functions
- Related **Business Views** (BSVW) that reference this table
- Any **Data Structures** used by table event rules

**Generation artifacts:**
- Physical table in the target data source
- Header file in the path code's Include folder
- `JDBTRIG.DLL` (if table event rules exist)

**Key considerations:**
- Generating a table on the target environment **clears all existing data** — plan data migration separately.
- Index changes require at minimum an index regeneration.
- Column prefix must match across environments.
- Product codes 55–59 are reserved for custom objects — use these for client-created tables.
- The Object Configuration Manager (P986110) maps tables to data sources — ensure OCM entries exist in the target environment.

---

## 11. Quick Reference Card

| What | How |
|---|---|
| Create a new table | OMW → Add → Table → fill name/desc/product code/prefix → OK → Design in Table Design Aid → add columns from DD → define indices → Generate Table |
| Add a column | Table Design Aid → DD Browser → drag item to Columns → Regenerate Table |
| Add an index | Table Design Aid → Indices form → Add New → drag columns → name index → Generate Indexes |
| Copy table data | Table Design Aid → Table Operations → Copy Table → specify source/destination data sources |
| Remove physical table | Table Design Aid → Table Operations → Remove Table From Database |
| Create table event rule | Table Design Aid → Design Tools → Start Table Trigger Design Aid → select event → write rules → Save → Build Table Triggers |
| Use Table I/O in event rules | Event Rules Design → Table I/O button → select operation → map fields → set operators → Finish |
| Enable buffered inserts | Table I/O → Open (Advanced) → select table → Advanced Options → Buffer Inserts |
| Create a handle | Data Dictionary → new item with Data Type=7 (Identifier), Class=HANDLE → use in Table I/O with Handles tab |
