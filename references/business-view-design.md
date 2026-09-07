# JD Edwards EnterpriseOne — Business View Design Reference (BSVW Objects)

*Source: JD Edwards EnterpriseOne Tools — Business View Design Guide, Release 9.2 (Part Number E53618-04)*

---

## 1. Overview

A business view is a selection of data items from one or more tables. After creating a table, you use Business View Design to create a business view that contains only the data items required for a specific application. JD Edwards EnterpriseOne uses the business view to generate the appropriate SQL statements to retrieve data from the database.

Business views can be attached to:
- **Forms** that update data in interactive applications
- **Reports** that display data

Business views improve performance by moving less data across the network — only the columns the application actually needs are included.

**Object Type Code:** `BSVW`  
**Object Use:** `300` (business views)  
**Design Tool (Classic):** Business View Design Aid (Form `W9860AL`)  
**Design Tool (Web OMW, Release 9.2.8+):** Business View Design (Form `W98720WA`)  
**Management Tool:** Object Management Workbench (OMW, Form `W98220A` / Web OMW `W98220WAC`)

**Key capabilities of business views:**
- Link a JDE application to one or more tables
- Contain all or a subset of data items from one or more tables
- Use table joins to combine multiple tables on common fields
- Serve as building blocks for text search indexes (with the Text Search option enabled and at least one GT data structure added)

**Important:** Do not enable Text Search unless the business view is intended for full-text searching — it negatively affects performance.

---

## 2. Naming Conventions

### Standard Business Views

Business view names follow the format **VzzzzzA** (max 8 characters):

| Position | Meaning | Examples |
|---|---|---|
| **V** | Prefix — indicates a business view | Always `V` |
| **zzzzz** | Characters representing the primary table | Matches the table name without the `F` prefix (e.g., `0101` for `F0101`) |
| **A** | Sequence letter — designates the order of business views created over the same table | `A` = first, `B` = second, `C` = third, etc. |

**Examples:**
- `V0101A` — first business view over table `F0101` (Address Book Master)
- `V0101B` — second business view over `F0101`
- `V0101C` — third business view over `F0101`

### External Developer Business Views

For custom applications created by consultants or external developers, the naming convention is:

**Vssss9999** where:

| Position | Meaning |
|---|---|
| **V** | Prefix — business view |
| **ssss** | System code for the enterprise |
| **9999** | Unique next number or character pattern within the enterprise |

This format prevents interference between JDE and non-JDE objects.

### Joined Business View Descriptions

When creating a business view that joins tables, the description should:
- Include the names of the tables being joined
- Place the primary table name first
- Separate table names with a forward slash (`/`)

**Example:** A business view joining `F4101` (Item Master) and `F4102` (Item Branch) with `F4101` as primary: *"Item Master and Branch F4101/F4102"*

### Description Guidelines

- Maximum **60 characters**
- Should reflect the application description followed by the form type
- Example: *"Item Master Browse"*, *"Item Master Revisions"*

### Custom Business Views

Use product codes **55–59** (reserved for clients) or `L00–L99`, `M00–M99`, `P00–P99` (for business partners).

---

## 3. Understanding Business View Design Aid

### Design Principles

Before designing a business view, determine:
1. The purpose of the application that needs the business view
2. The data items required
3. The tables where those data items reside

**Key design guidelines:**
- Adding a new business view does not affect performance
- Using an existing business view with many unused columns *does* negatively affect performance
- Business views usually contain a few more fields than are used on the form/grid/batch application — the extras should be related fields that might be needed if requirements change
- You can modify business views to reflect changing requirements — adding fields is easy, but deleting fields requires verifying they are not used in any interactive or batch application
- At least one business view for each table should include **all columns** from the table
- Only **one business view** is allowed per form type, except for header detail forms (which can use two — one for header, one for detail)

### Business View Sizing by Form Type

| Form Type | Sizing Guidance |
|---|---|
| **Search & Select** | Minimum fields — only what's needed for filtering and associated description outputs |
| **Find Browse** | More fields than Search & Select, but still limited to filtering and display fields |
| **Parent Child** | Similar to Find Browse |
| **Input-Capable** | Usually large — include all fields needed to add or update a record, including audit fields |

### Business View Design Aid Interface (Classic)

The Business View Design Aid window contains these forms:

| Form | Description |
|---|---|
| **Table Joins** | Displays selected tables and their columns. Key icon marks primary key fields. The primary table is where an application begins a search. |
| **Available Tables** | Enables locating tables and moving them to the Table Joins form |
| **Selected Columns** | Displays the data items selected from the table to include in the business view |
| **Object Properties** | Displays properties of a data item selected in the Selected Columns form |

### Business View Design (Web OMW — Release 9.2.8+)

Starting with Tools Release 9.2.8, business views can also be created in the Web Object Management Workbench. The web interface uses:

| Form | Form ID | Description |
|---|---|---|
| **Object Management Workbench - Web** | `W98220WAC` | Select/view objects in projects, access design tools |
| **Create EnterpriseOne Object** | `W98220WAB` | Add a new object to a project |
| **Add Object** | `W9861AWC` | Add business views |
| **Business View Design** | `W98720WA` | Access Business View Design and create a type definition |

### Deletion Impact

| What You Delete | Impact |
|---|---|
| **A data item** from a business view | Error message when running the application — must open the application and delete the data item from there too |
| **An entire table** from a business view | Cannot run any application using the business view — must open the application, delete all items from the deleted table, attach a different business view, and reconnect controls |
| **An entire business view** | All forms using it will fail — must select a new business view and reconnect all controls |

---

## 4. Tables for Business Views

When selecting tables for a business view:
- Choose tables that include the fields required for the business purpose
- Prefer table joins over one large business view with many columns — performance is negatively affected by large business views

### Table Limits for Performance

| Join Configuration | Maximum Tables |
|---|---|
| All simple (inner) joins | **5** tables (standard) / **15** tables (Web OMW 9.2.8+) |
| Any outer join or table union | **3** tables (standard) / **15** tables (Web OMW 9.2.8+) |

**Note:** The Web OMW (Release 9.2.8+) supports up to 15 tables for both simple joins and outer join/union scenarios.

### Data Items for Business Views

- If multiple tables are in the business view, designate which is the **primary table** first, then select data items
- All data items from all selected tables are available for inclusion
- Select data items required by the interactive or batch application
- Balance between keeping the view small (performance) and including enough fields for future needs
- If a data item exists in multiple tables, select it from the primary table
- Selecting the same item from multiple tables causes it to appear multiple times (each with its own table reference)
- In joined business views, **primary key fields are automatically selected** and cannot be removed
- Joins must be performed on fields of the **same data type**
- **Maximum 256 columns** in a business view for optimal performance

---

## 5. Table Joins

Table joins combine fields from different tables into a single business view, enabling an application to access data from multiple tables simultaneously.

### When to Use Joins

- **Recommended for:** Find browse forms, reports, and other non-input-capable forms
- **Use with caution for:** Input-capable forms — only when the relationship between the two tables is simple
- The relationship between records must be precise when updating the database

### Primary vs. Secondary Tables

- **Primary table:** The table where you initiate the join (usually the left table in Business View Design Aid). This is where an application begins its search. A crown icon appears in its upper-left corner.
- **Secondary table:** The table where you conclude the join (usually the right table)
- If only one table exists, it is the primary table by default
- The first table added is automatically designated primary; you can change this by double-clicking a different table's title bar (classic) or clicking the primary option (web)

### Join Types

| Join Type | Description | Visual |
|---|---|---|
| **Simple (Inner) Join** | Includes only rows that match in both primary and secondary tables | Intersection of two circles |
| **Right Outer Join** | Includes matching rows from both tables, plus unmatched rows from the **secondary** table | Full right circle + intersection |
| **Left Outer Join** | Includes matching rows from both tables, plus unmatched rows from the **primary** table | Full left circle + intersection |
| **SQL 92 Left Outer Join** | Includes matching rows from both tables, unmatched rows from the primary table, AND any rows with null values from the secondary table — regardless of any WHERE clause against the secondary table's fields | Extended left outer |

**Default join type:** Simple (inner join)

### Join Operators

| Operator | Symbol |
|---|---|
| Equal | `=` |
| Not Equal | `<>` |
| Less than | `<` |
| Greater than | `>` |
| Less than or equal | `<=` |
| Greater than or equal | `>=` |

**Default operator:** Equal (`=`)

### Join Requirements

- Both columns being joined must have the **same data type**
- Column names do not need to match
- Use the Object Properties form to verify data type and decimal compatibility
- You may need to add columns, build new indices, or create new tables to support required joins
- Join on as many fields as necessary to ensure data is fetched properly for each record

### Creating Table Joins (Classic — Business View Design Aid)

1. On the Table Joins form, click and draw a line from a column in the primary table to the associated column in the secondary table
2. Click the drawn line — both fields highlight
3. From the **Join** menu, select **Types** → choose the join type (default: Simple)
4. From the **Join** menu, select **Operators** → choose the operator (default: Equal)
5. To delete a join: click the line, then select **Delete** from the Join menu (or right-click → Delete)

### Creating Table Joins (Web OMW — Release 9.2.8+)

1. In Join Mode with more than one table selected, the Table Joins pane and Column Joins pane appear
2. Click **Add** in the Table Joins pane
3. Select a table from the **Left Table** dropdown and a table from the **Right Table** dropdown (if a join already exists for these two tables, an error is shown)
4. Select a join type from the **Join Type** dropdown (default: Simple)
5. Click **Add** in the Column Joins pane
6. Select a column from the Left Table tab (becomes Left Column of the join)
7. Select a column from the Right Table tab (becomes Right Column)
8. Select an operator from the **Join Operator** dropdown (default: Equal)
9. To delete: click **Delete** in Table Joins or Column Joins pane
10. If you add more data items from Selected Columns, click **Refresh** to save changes (warning: unsaved column joins will be removed)

---

## 6. Table Unions

Table unions combine rows from tables that have the **same structure** (all columns in one table must also exist in the other).

### Union Types

| Union Type | Behavior |
|---|---|
| **Union** | Retrieves rows from both tables but eliminates duplicates — only one copy of identical records is returned |
| **Union All** | Retrieves all rows from both tables, including duplicates |
| **Distinct Union All** | Retrieves the distinct rows from both the primary and secondary tables |

**Union vs. Union All performance:** Union All is faster because it does not scan for distinct records.

### Creating Table Unions (Classic)

1. From the **Table** menu, select either **Union Mode** or **Union All Mode** (or click the toolbar button)
2. Select the tables for the union
3. Union/Union All features are available only if all columns in one table also reside in the other table

### Creating Table Unions (Web OMW)

1. From **Table/Column Selection**, select **Union Mode** or **Union All Mode**
2. Click **Yes** in the confirmation window
3. Select the tables for the union
4. The first table added is automatically the primary table
5. Select data items from the primary table only (items from other tables cannot be chosen individually)

### Creating a Distinct Union All Business View

**Classic:** Table menu → Union All Mode → Table menu → Distinct Mode → Select tables  
**Web OMW:** Table/Column Selection → Union All Mode → Table/Column Selection → Distinct → Select tables

**Note (Web OMW):** If you select more than one table in Join Mode, you cannot switch to Union/Union All mode. However, if you select tables in Union or Union All mode, you can switch between them (but not back to Join mode).

---

## 7. Select Distinct

The Select Distinct feature eliminates duplicate rows from business view query results.

### When It's Needed

- When a business view includes the **primary key fields** of the primary table, every row is unique — Select Distinct is unnecessary
- When the business view does **NOT** include all primary key fields, duplicate rows can occur
- Use Select Distinct to return only unique rows

### Currency Columns That Affect Select Distinct

Business views with a primary table containing any of the following currency/security columns may cause the Select Distinct feature to display duplicate values:

| Column | Description |
|---|---|
| CO | Company |
| CRCD | Currency Code - From |
| CRDC | Currency Code - To |
| CRCX | Currency Code - Denominated In |
| CRCA | Currency Code - A/B Amounts |
| LT | Ledger Type |
| AID | Account ID |
| MCU | Business Unit |
| KCOO | Order Company (Company Code) |
| EMCU | Business Unit Header |
| MMCU | Branch |
| AN8 | Address Number |

### Example: Using Select Distinct

Using the `V98EVDTL` business view over `F98EVDTL` (Event Detail File):

1. **Without Select Distinct** (using Key by Formtyp, Evtyp, Obj index):
   ```sql
   SELECT EDOBJTYPE, EDEVTYPE, EDFORMTYPE FROM PVC.F98EVDTL
   ```
   Result: ~281 rows

2. **With Select Distinct** (same index):
   ```sql
   SELECT DISTINCT EDOBJTYPE, EDEVTYPE, EDFORMTYPE FROM PVC.F98EVDTL_Continue2
   ```
   Result: ~53 rows

### Steps to Enable Select Distinct (Classic)

1. In Business View Design Aid, select the primary table
2. Table menu → **Distinct Mode**
3. Table menu → **Change Index** (changes the primary table index to a non-unique index)
4. Select the desired index from Available Indices → OK
5. Save the business view

### Steps to Enable Select Distinct (Web OMW)

1. Select the primary table
2. From **Table/Column Selection**, select **Distinct**

### Changing the Primary Table Index

1. Select the primary table in Business View Design Aid
2. From the **Table** menu, select **Change Index**
3. A warning displays — click **Yes** to continue
4. Select the desired index from the Available Indices form
5. Save and quit

**Note:** The software stores the business view in cache memory. Even after changing a business view, the previous version runs until the cache is cleared. You may need to quit and sign back in.

---

## 8. Primary Key Fields

The fields included in the primary index of a table are displayed as **key fields** in Business View Design Aid, marked with a key icon next to the field name.

- Primary key fields are **always included** in the business view
- They carry information from the table to the application
- To include additional information beyond primary keys, select additional fields to include in the business view
- In a joined business view, primary key fields from all tables are automatically selected and **cannot be removed**

---

## 9. Creating Business Views — Step-by-Step

### Via Classic OMW (Object Management Workbench)

#### Forms Used

| Form Name | Form ID | Navigation | Usage |
|---|---|---|---|
| Object Management Workbench | `W98220A` | EnterpriseOne Life Cycle Tools → Application Development (GH902) → Object Management → Object Management Workbench | Select/view objects in projects; access design tools |
| Add EnterpriseOne Object to the Project | `W98220C` | Click Objects node of a project → click Add | Add a new object to a project |
| Add Object | `W9861AF` | Select Business View → click OK | Add business views |
| Business View Design Aid | `W9860AL` | Complete object information → click OK on Add Object form | Access Business View Design Aid; create type definition |

#### Step-by-Step Procedure

1. **Open OMW:** Navigate to EnterpriseOne Life Cycle Tools → Application Development (GH902) → Object Management → Object Management Workbench
2. **Add to project:** Click the Objects node of a project → click **Add**
3. **Select object type:** Select **Business View** → click **OK**
4. **Fill in object properties:**
   - **Object Name:** Following naming convention (`VzzzzzA` or `Vssss9999`)
   - **Description:** Meaningful description (max 60 chars)
   - **Product Code:** UDC 98/SY (55–59 for clients, L00-L99/M00-M99/P00-P99 for partners)
   - **Product System Code:** UDC 98/SY matching the JDE system (01=AB, 03B=AR, 04=AP, 09=GL, 11=Multicurrency)
   - **Object Use:** `300` (business views)
   - **Object Type:** `BSVW` (auto-populated)
   - **Text Search:** Only enable if the business view will be used for full-text searching
5. Click **OK** → Business View Design Aid opens
6. **Select tables:** On the Available Tables form, use QBE to search → drag tables to the Table Joins form
7. **Set primary table:** If multiple tables, double-click the title bar of the desired primary table
8. **Select data items:** Double-click columns on the Table Joins form to include them (check mark appears; item shows on Selected Columns form)
9. **Configure joins** (if multiple tables): Draw lines between common columns → set join type and operator
10. **Enable Select Distinct** (if needed): Table menu → Distinct Mode → Change Index
11. **Save** the business view

### Via Web OMW (Release 9.2.8+)

1. **Open Web OMW:** Navigate to Object Management Workbench - Web
2. **Add to project:** Click the Objects node → click **Add**
3. **Select object type:** Select **Business View** → click **OK**
4. **Fill in object properties** (same fields as Classic OMW)
5. Click **OK** → Business View Design form opens
6. **Set mode:** The form defaults to Join Mode; switch to Union/Union All via Table/Column Selection if needed
7. **Select tables:** Search in Available Tables pane → click the arrow in the Select column
8. **Set primary table:** Click the **primary** option for the desired table (green dot appears in Primary column)
9. **Select data items:** Check items in the Selected Columns pane (Select All available; primary keys are pre-selected and locked in Join mode)
10. **Configure joins** (if in Join Mode with multiple tables): Add table joins, add column joins, set types and operators
11. **Enable Distinct** (if needed): Table/Column Selection → Distinct
12. **Save** the business view

---

## 10. XML Par File Considerations

### Object Type Identification

When working with XML par files for business view deployment, the key identifiers are:

| Property | Value |
|---|---|
| **Object Type** | `BSVW` |
| **Object Use** | `300` |
| **UDC Table for Product Code** | `98/SY` |
| **UDC Table for Object Use** | `98/FU` |

### Dependencies and Related Objects

Business views have dependencies on:
- **Tables (TBLE):** The underlying table(s) must exist before the business view can be created or deployed
- **Data Dictionary items:** All columns referenced in the business view must exist in the Data Dictionary
- **Indices:** If Select Distinct is used with a non-primary index, that index must exist on the table

When packaging business views in par files, ensure:
1. All referenced tables are included or already exist in the target environment
2. The Data Dictionary items for all included columns are present
3. Any custom indices used by the business view are included
4. If the business view references joined tables, all tables in the join must be available

### Product Code Ranges

| Range | Reserved For |
|---|---|
| **55–59** | Client customizations |
| **L00–L99** | Business partners |
| **M00–M99** | Business partners |
| **P00–P99** | Business partners |

### System Code Reference

| Code | System |
|---|---|
| 00 | Foundation |
| 01 | Address Book |
| 03B | Accounts Receivable |
| 04 | Accounts Payable |
| 09 | General Accounting |
| 11 | Multicurrency |

---

## 11. Quick Reference Card

### Business View At a Glance

| Property | Value |
|---|---|
| Object Type Code | `BSVW` |
| Object Use | `300` |
| Naming Convention | `VzzzzzA` (standard) / `Vssss9999` (external) |
| Max Name Length | 8 characters |
| Max Description Length | 60 characters |
| Max Columns | 256 |
| Max Tables (Simple Joins, Classic) | 5 |
| Max Tables (Outer Join/Union, Classic) | 3 |
| Max Tables (Web OMW 9.2.8+) | 15 |
| Design Tool (Classic) | Business View Design Aid (`W9860AL`) |
| Design Tool (Web) | Business View Design (`W98720WA`) |
| Default Join Type | Simple (Inner Join) |
| Default Join Operator | Equal (`=`) |

### Join Types Summary

| Type | Primary Table Rows | Secondary Table Rows | Unmatched Primary | Unmatched Secondary |
|---|---|---|---|---|
| Simple (Inner) | Matching only | Matching only | Excluded | Excluded |
| Left Outer | All | Matching only | Included | Excluded |
| Right Outer | Matching only | All | Excluded | Included |
| SQL 92 Left Outer | All | Matching + nulls | Included (ignores WHERE on secondary) | Included as nulls |

### Union Types Summary

| Type | Duplicates | Performance |
|---|---|---|
| Union | Eliminated | Slower (scans for duplicates) |
| Union All | Included | Faster |
| Distinct Union All | Eliminated across both tables | Moderate |

### Key Forms Reference

| Form | Form ID | Purpose |
|---|---|---|
| Object Management Workbench | `W98220A` | Manage objects/projects |
| OMW - Web | `W98220WAC` | Web-based object management |
| Add Object (Classic) | `W9861AF` | Add business view objects |
| Add Object (Web) | `W9861AWC` | Add business view objects (web) |
| Business View Design Aid | `W9860AL` | Design business views (classic) |
| Business View Design | `W98720WA` | Design business views (web) |

### Checklist: Before Creating a Business View

1. Identify the application purpose and required data items
2. Identify the table(s) containing those data items
3. Determine if joins are needed and what type
4. Verify column data types match for any planned joins
5. Plan which index to use (primary or alternate for Select Distinct)
6. Follow naming conventions (`VzzzzzA` for standard, `Vssss9999` for external)
7. Use product codes 55–59 for custom business views
8. Keep column count under 256 for performance
9. Ensure at least one business view per table includes all columns
10. Only enable Text Search if full-text searching is needed

### Common Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| Business view changes not reflected at runtime | Cache not cleared | Quit the software and sign back in |
| Cannot remove a primary key field | Primary keys are locked in business views | This is by design — primary keys must remain |
| Application error after deleting a data item from business view | Data item still referenced in the application | Open the application and remove the data item reference |
| Cannot switch from Join Mode to Union Mode (Web OMW) | Multiple tables already selected in Join Mode | Remove extra tables first, then switch modes |
| Duplicate rows appearing with Select Distinct | Currency/security columns in primary table | Review the currency columns list (CO, CRCD, CRDC, CRCX, CRCA, LT, AID, MCU, KCOO, EMCU, MMCU, AN8) |
| Cannot create a table union | Tables do not have the same structure | All columns in one table must also exist in the other |
| Join between two columns fails | Data type or decimal mismatch | Verify both columns have identical data type and decimal attributes via Object Properties |
