# JD Edwards EnterpriseOne 9.2 — Event Rules Reference

> **Source:** *JD Edwards EnterpriseOne Tools — Event Rules Guide, Release 9.2 (Part Number: E53554-03)*
> **Object Type:** Event Rules (ER) / Named Event Rules (NER)

---

## 1. Overview

Event rules (ER) are logic statements that you create and attach to runtime events in JD Edwards EnterpriseOne applications. When an event occurs at runtime — such as initializing a form, clicking a button, or exiting a field — the system evaluates the attached ER and executes the logic you have defined. ER is the primary mechanism for implementing custom business logic without writing C code.

Oracle's JD Edwards EnterpriseOne Tools for event rules are used to create or modify ER in interactive applications (via Form Design Aid), batch applications (via Report Design Aid), and at the table level (via Table Design Event Rules). The two main tools for working with ER are **Event Rules Design** (for authoring) and **BrowsER** (for viewing and searching).

### What Event Rules Can Do

ER statements support a wide variety of logic, including conditional statements (If/Else/End If), While loops, assignments, calls to business functions, calls to system functions, form or report interconnections, and table I/O operations. You can attach multiple event rules to a single event.

### Two Kinds of Event Rules

JD Edwards EnterpriseOne supports two kinds of event rules:

- **Named Event Rules (NER):** A reusable series of ER statements (assignments, business function calls, system function calls, etc.) encapsulated into one callable component. You call a NER the same way you call a business function. Business functions implement customized logic using C language; NERs implement customized logic using event rule statements. NERs are also referred to as "business function event rules."

- **Embedded Event Rules:** ER that is specific to a particular table, interactive application, or batch application. Embedded ER for a table is called *table event rules* or *table triggers*. Embedded ER for an interactive application or batch application is called *application event rules*.

### Application Event Rules

You can add business logic specific to a particular application. Interactive applications connect ER using Form Design Aid (FDA), while batch event rules use Report Design Aid (RDA).

### Table Event Rules

Table-specific event rules attach to a table using Table Design Event Rules. This logic runs whenever any JD Edwards EnterpriseOne application accesses that table and uses that ER. For example, to maintain referential integrity, you might attach ER to a master table that deletes all children when a parent is deleted. Any application deleting from that table benefits from the logic automatically.

> **Note:** Table event rules apply only to JD Edwards EnterpriseOne applications. Other applications that access the same database table cannot and do not use these ERs.

---

## 2. Understanding Events

**Events** are activities that occur on a form, such as entering a form, exiting a field by using Tab, or clicking a button. Events can be initiated by the user or by the application. A single control might initiate multiple events. The system also initiates some events automatically, such as Last Grid Record Has Been Read, when certain actions occur.

Each form type has different properties and event flow. The system provides events for the forms so that you can insert custom logic. These events occur regardless of whether you add event rule logic for that event.

---

## 3. Runtime Processing of Event Rules

**Runtime processing** refers to how, at runtime, the system evaluates various events (such as initializing a form, clicking a button, and using Tab to move between fields) and their attached ER. ER is attached to events, which in turn are attached to controls or forms.

FDA provides several different form types, each of which includes predefined fields and features specific to the form type. For example, a find/browse form automatically includes a Find menu option or toolbar button with appropriate functions attached. To avoid generating unnecessary ER, you should understand the different field types and associated capabilities that characterize each form type.

### Runtime Data Structures

**Runtime data structures** are structures or blocks of memory that hold data when a user is working with an application. You should know what is happening to each form at runtime and what is in a runtime structure at a given event point.

The runtime system dynamically creates runtime data structures. For example, if a form contains hidden controls, the system allocates memory for those controls even though they are not visible on the form. When you pass processing option (PO) values in a form, the system allocates memory to store the PO value.

### Available Objects and Runtime Data Structures

A runtime data structure is made of a variety of objects on a form. An available object is represented by a two-character alphabetical code that characterizes the source of data and determines how the object data is used in an interactive application at runtime.

| Object Code | Description |
|---|---|
| **BC** | A column in the business view (BV). BCs for both the form view and the grid view appear in this list. The system fills these columns with values from the database when it performs a fetch. The system writes these values to the database during an add or update. |
| **GC** | A column in the grid. The row that the value references depends on which event is accessing the GC. During the fetch cycle, it is usually the selected row. In some circumstances, GC objects also denote a particular physical column in the grid instead of a value. An example is the Set Grid Font system function. |
| **GB** | The grid buffer. This buffer is one row of data that is independent of the lines that the system reads from the database and writes to the grid. The GB enables you to manipulate column data for a line that you want to insert or update without affecting the present state of the grid. You access the GB through an available GB object, which appears after the GC objects in the list of available objects in Event Rules Design. Each grid contains only one instance of each GB column. |
| **FC** | A control on the form. If the control is a database item, this field corresponds to a BC object. Furthermore, if the control is not a filter, the FC object represents the same value as the BC object, and changing one of these results in changing both. |
| **FI** | A value passed through a form interconnection. You access this object either to read values that are passed into the form or to set values to be passed back. These objects correspond to the elements of the form data structure. |
| **PO** | A value passed from a processing option. These values are passed into the application when a user launches it. Any form in that application can access them. POs can either be entered by the user, or they can be set up in a particular version of an application. |
| **QC** | A cell from the QBE line in the grid. These objects represent the values in any QBE cell on the grid. They include wild cards, but do not include any comparison operators. Likewise, assignments to these objects can include wild cards, but not comparison operators. To set comparisons, you must use a system function. |
| **HC** | A hypercontrol item. A hypercontrol item is a menu item or a toolbar item. |
| **VA** | ER variables. These objects represent any variables that you set up in ER. |
| **SV** | System variables. These objects represent some environment variables that are accessible to ER. |
| **SL** | System literals. These objects represent some constant system values that are accessible to ER. |
| **TP** | Tab page object. |
| **TK** | A column in the table that contains the table ER. |
| **CO** | A constant, such as the return code for an error. |
| **TV** | Text variables. |
| **RC** | Report constants for a batch application. |
| **RV** | Report variables (batch application). |
| **IC** | An input column (table conversion). |
| **OC** | An output column (table conversion). |

### Processing Available Objects

BC and FC share the same internal structure if an FC is associated with a database item; filter fields are an exception. This means:

- FC data and BC data are always identical.
- Whenever FC data is changed, BC items are changed to the same value.
- Whenever BC values are changed, the FC runtime values also change to the same values. This change may not immediately be reflected to the screen.
- On Control is Exited processing, the value entered into the form control is captured in both the BC and FC item for that control.

### Control is Exited Processing

Control is Exited processing includes these actions:

1. The value in the control is saved to internal runtime structures.
2. The Control is Exited event is processed.

If the value has changed since the previous time the control was exited, these additional steps occur:

1. The system processes the Control Exited/Changed–Inline event.
2. The system processes the Control Exited/Changed–Async event.
3. The system validates the value using edit rules defined for the DD item.
4. The form control data is formatted using format rules defined for the DD item and displayed on the screen.

The **Trigger Parallel Event** system function is available for the **Control Exited/Changed–Inline** and **Control Exited/Changed–Async** events. This system function enables a parallel event to run on a separate thread and will not interfere with existing Event Rules.

---

## 4. Form Flow — Find/Browse Form Example

Each form type has different properties and event flow. The following sections describe the typical events for a find/browse form and the order in which they are processed when the form is called directly from a menu.

### Pre-Dialog Is Initialized

These steps occur before the Dialog is Initialized event is processed and the form appears:

1. Initialize runtime structures (clear memory): BC = null, FC = null, GC = null, FI = Values passed from a calling form (if any), PO = Values passed from processing options.
2. Initialize form controls.
3. Initialize error handling.
4. Initialize static text.
5. Initialize helps.
6. Create tool bar.
7. Load form interconnect data into corresponding BC columns and filter fields (if any exist).
8. Initialize thread handling.

### Dialog Is Initialized

The system processes all event rule logic attached to the Dialog Is Initialized event. When this event starts, the runtime structures contain: BC = Any FI values passed, FC = Any FI values passed, GC = null, FI = Values passed from a calling form (if any), PO = Values passed from POs.

### Post Dialog Is Initialized

Before the system fires the Post Dialog Is Initialized event, the runtime structures contain: BC = null (or values already passed in), FC = null (or values already passed in), GC = null (or values already passed in), FI = Values passed from a calling form (if any), PO = Values passed from POs.

The Post Dialog Is Initialized event is commonly used to:

- Load filter fields that will be used for the WHERE clause in the SQL SELECT statement.
- Load PO values into filter fields.
- Perform any one-time logic for the form, such as fetching a system date.

### Building SQL SELECT

After the user clicks Find, the system builds a SELECT statement with a WHERE clause. The SQL SELECT statement includes all columns in the BV. The WHERE clause includes any values in the QBE or filter fields. It can also contain values passed through Set Selection and Set Lower Limit system functions.

### Fetching Records

Records are fetched one page at a time (unless page-at-a-time is disabled). The system processes each record fetched one by one and displays it in the grid row.

**Page-at-a-Time Processing:** The system fetches only a single page worth of records to display. To see the next page, the user clicks the Next button. You can customize the page size for each grid in FDA. A system administrator can also set a global page size for all grids. JD Edwards EnterpriseOne standards state that you should not disable page-at-a-time processing unless you have a valid business reason.

### BC Assigned Database Values

After the system fetches each record from the database, it copies the database values to the BC items. Values from each marked column in the table appear in the BC runtime structure elements.

### Grid Record Is Fetched

At this point: BC = Values from the database (for the first record read), FC = Values from the database (if the fields are database fields), GC = null, FI = Values passed from a calling form (if any), PO = Values passed from POs.

Commonly used to:

- Calculate a value for a work field in the grid.
- Suppress a row from being written to the grid.

After Grid Rec Is Fetched fires, the BC values are copied into the GC runtime structure.

### Write Grid Line–Before

At this point: BC = Values from the database (from the record just read), FC = Values from the database (if the fields are database fields), GC = Values from the database (from the previous read), FI = Values passed from a calling form (if any), PO = Values passed from POs.

Commonly used to:

- Suppress a grid row from being written.
- Add logic before the user sees a row on the form.
- Change formatting of a grid column.
- Convert any grid value, such as unit of measure.
- Retrieve additional information for the grid row, such as a description, from tables that are not in the BV.

After Write Grid Line–Before, the GC elements (which now include the database values for the first record) are copied to the grid cells on the form.

### Write Grid Line–After

At this point: BC = Values from the database (from the first record read), FC = Values from database (if the field is a database field), GC = Values from the database (from the first record read), FI = Values passed from a calling form (if any), PO = Values passed from POs.

Commonly used to add logic after the user sees a row on the form.

The system continues to read records from the database and performs the same processing steps (Assign BC → Grid Rec Is Fetched ER → Assign BC to GC → Write Grid Line–Before ER → Display values → Write Grid Line–After ER) until there are no more records fetched.

### Last Grid Record Has Been Read

When there are no more records fetched from the database, the engine fires this event. At this point: BC = Values from the last record read, FC = Values from database (if the field is a database field), GC = Values from the last record read, FI = Values passed from a calling form (if any), PO = Values passed from POs.

Commonly used to write total lines to the grid and to display totals that are based on grid values.

### Select Button Processing

When a user selects a grid row and clicks the Select button, the BC structure stays the same, however the GC structure reflects values on the row that is being selected. Note that the BC and GC structures may not contain the same values if the selected row is not the last fetched row.

**Button Clicked (Select):** BC = Values from the last record read, FC = Values from the database, GC = Values from the selected grid row, FI = Values passed from a calling form, PO = Values passed from processing options.

Commonly used to connect to another form. Use **Repeat Business Rules for Grid** to repeat ER when multiple rows are selected.

### Add Button Processing

Normally, the user does not select a row before an add action, but if a row is highlighted, the system updates the GC values to reflect the selected row values (the database is not updated). You typically use the Button Clicked event for the Add button to interconnect to another form, such as a fix/inspect or headerless detail form on which the system actually performs the add action.

### Delete Button Processing

When the user selects a grid row and clicks the Delete button, the system does not update the database immediately. The delete sequence follows this order:

1. **Button Clicked (Delete):** Engine fires Button Clicked event. BC = last record read, GC = selected row.
2. **Delete Grid Rec Verify–Before:** Fires before the verification popup.
3. **Delete confirmation popup** displayed to the user.
4. **Delete Grid Rec Verify–After:** Fires after the user clicks OK. Use this event for custom validation logic (e.g., checking for dependent records).
5. **Delete Grid Rec From DB–Before:** FC is blank. The system has not yet deleted the record. You can use the **Suppress Delete** system function here to prevent the system from deleting the record.
6. The system builds a SQL DELETE statement and deletes the current record. When the user selects multiple records, all selected records are deleted.
7. **Delete Grid Rec From DB–After:** After records are deleted. Use this event to call a business function to delete information from related tables not in the current BV.
8. **All Grid Recs Deleted From DB:** Fires after all selected records are deleted. FC is blank.

### Parallel Event

A parallel processing event runs in a new thread and will not interfere with existing Event Rules.

---

## 5. Using Event Rules Design

You use JD Edwards EnterpriseOne Event Rules Design to create event rule (ER) logic for forms and controls on a form. Before creating an ER, consider which control (form, button, field, grid, etc.) you want to add logic to and what event you want to add the logic for. Ask yourself:

- Is the user initializing the form?
- Is the user clicking a button?
- Is the user exiting from a field?
- Is the user changing or exiting from a row?

After you place controls on a form, you can add ERs to any of the events that the control supports. A form is also a control, and you can create logic that the system automatically processes whenever a form event is fired.

### Event Rules Design Toolbar Buttons

| Button | Purpose |
|---|---|
| **Event Information** | Displays information about event relevance. |
| **Assignment** | Creates an assignment or a complex expression. |
| **Business Function** | Attaches an existing business function. |
| **System Function** | Attaches an existing JD Edwards EnterpriseOne system function. |
| **If/While** | Creates an If/While conditional statement. |
| **Report Interconnect** | Establishes a connection to a batch application or report. |
| **Form Interconnect** | Establishes a form interconnection. |
| **Else** | Inserts an Else clause (valid only within the bounds of If and End If). |
| **Variable** | Creates a programmer-defined field. |
| **Table I/O** | Enables ER support for database access. Performs table I/O, data validations, and record retrieval. |

> **Note:** All event rule keywords are colored blue within Event Rules Design for easy identification.

### Event Rule Capabilities

ER statements can perform a wide variety of tasks:

- Perform a mathematical calculation.
- Pass data from a field on a form to a field on another form.
- Count grid rows that are populated with data.
- Interconnect two forms.
- Hide or display a control using a system function.
- Evaluate If/While and Else conditions.
- Assign a value or an expression to a field.
- Create variables or programmer-defined fields at runtime.
- Perform a batch process upon completion of an interactive application.
- Process table input and output, validate data, and retrieve records.

### Cut, Copy, and Paste

You can cut or copy an ER and paste it in the same event, form, or application or in a different event, form, or application. You can also paste ERs into other applications, such as word processing documents (useful for documentation).

When you paste an ER, the system resolves objects from the source. If an object is partially resolved, the system pastes the closest matching object and inserts a comment line above the partially-resolved line. For criteria statements, the paste operation adds whatever is necessary to maintain a clean logical structure (e.g., a missing EndIf is automatically added for a pasted If statement).

### Event Rule Validation

When you save an application, the system automatically validates all ERs. If errors occur, details on the ER event, control, and line number are displayed in a popup window. You can also start validation manually in FDA by selecting File → Validate Event Rules.

The error log is stored in a file such as `b9\prod\log\p1234.log` (where `prod` is the environment). If no errors exist, the system does not generate a log.

### ER Consistency

Events can be either relevant or not relevant. A **relevant event** is one that is valid and can be executed by the associated control. A **not relevant event** is one that is not executed by the associated control because the properties of that control do not create the conditions that cause the events to execute. A not relevant event is displayed in dimmed italic text in the Event combo box. You can change a not relevant event to a relevant event by updating the properties of the control.

---

## 6. Working with Assignments

Use an assignment to assign a field with a fixed value or a mathematical expression. For example, you can create an assignment that inserts a default value when the user leaves a field, or use an assignment to calculate a value.

When you create an expression, calculate only data items of the exact same numerical scale or data type. Do not calculate different currencies or decimal figures that represent different decimal values because the result might compromise data integrity.

> **Note:** You can use the filter capability to search for variables to use in common Event Rule functions like assignments, system functions, report interconnects, form interconnects, and business function mappings.

### Assigning a Value — Step by Step

1. On Event Rules Design, select an event.
2. Click the Assignment/Expression button.
3. On Assignment, select the **To Object** that you want to receive the assigned value.
4. Determine the **From/Object Literal** value using one of these methods:
   - Select a **From Object** in the right-hand column to create a simple statement: `[left-hand column] = [right-hand column]`.
   - Type a **literal expression** (number, text, etc.) in the text entry box: `[left-hand column] = [literal]`.
   - Press the **ƒ(X)** button to create a complex expression or advanced mathematical function using Expression Manager.

---

## 7. If and While Statements

If and While statements are conditional instructions for an ER. They evaluate conditions and dictate the flow of logic when the ER is activated.

When you create an If statement, the system inserts an Else clause automatically. You can delete the Else clause using the Delete button and reinsert it using the Insert Else button. When you delete an If or While statement, the system also deletes the associated Else and EndIf or EndWhile clauses, but not the lines inside those statements.

You can drag and drop statements line-by-line to change their sequence. Resequencing ER can result in improper syntax — when you click Save or OK, the system verifies the syntax.

### Creating an If or While Statement — Step by Step

1. On Event Rules Design, select an event and click the If/While button.
2. Select either the **If** or **While** operator.
3. Select a **left operand** from the list of available data items. Right-click to sort by name or object type.
4. Select a **logical operator** comparison (is equal to, is less than, etc.).
5. Select a **right operand** from the object list, or select `<Literal>` to assign a literal.
6. To create complex If statements, select the **And** or **Or** option and continue the logic.

> **Tip:** To expand or collapse all statement blocks within Event Rules Design, select Expand/Collapse All Statements in the View menu.

---

## 8. ER Variables

An ER variable is a variable that you can use within event rules. You must assign a Data Dictionary (DD) item to an ER variable; the DD item defines the type and default behavior of the variable.

**Use ER variables instead of hidden fields.** ER variables use fewer system resources at runtime.

After you add an ER variable, you cannot modify it — you must delete it and create another one.

### Variable Scope

Each ER variable is available within a scope. The scope determines how you can use the variable. Different scope options are available for interactive and batch applications.

The system automatically assigns one of these prefixes based on scope:

| Prefix | Scope |
|---|---|
| `frm_` | Form — variable is available across all events on the form |
| `evt_` | Event — variable is available only within the event in which it was created |
| `grd_` | Grid — variable is available within grid events |
| `rpt_` | Report — variable is available anywhere in the report |
| `sec_` | Section — variable is available within a report section |

After you create an ER variable, it appears in the available objects list in Event Rules Designer where you added it. If you create an event-level variable and do not use it in ERs, FDA automatically deletes it.

### Creating an ER Variable — Step by Step

1. On Event Rules Design, click the **Variables** button. The Variables form displays different scope options depending on whether you are working with an interactive application, batch application, or NER.
2. Complete the variable naming field located under the Add button.
3. Click one of the **Scope** options (Form or Event) depending on the purpose.
4. If you selected Form Scope and want a grid variable, click the **Grid** option.
5. Click the **DD visual assist** to browse for DD items.
6. Select the DD item to which the variable is associated and click the **Add** button. The system automatically assigns a prefix based on scope.

### Example: Automatic Line Numbering

You can use event rules to create automatic line numbering in form grids:

**Step 1 — Create a variable:** Use the data dictionary item LNID.
```
VA frm_LineNumber_LNID
```

**Step 2 — Initialize on Post Dialog Is Initialized:**
```
VA frm_LineNumber_LNID = 0
```

**Step 3 — On Grid Record Is Fetched, track the highest line number:**
```
If BC LineNumber > VA frm_LineNumber_LNID
    VA frm_LineNumber_LNID = BC LineNumber
End If
```

**Step 4 — On Add Last Entry Row to Grid, increment and assign:**
```
VA frm_LineNumber_LNID = VA frm_LineNumber_LNID + 1
GC LineNumber = VA frm_LineNumber_LNID
```

---

## 9. Attaching Functions to Events

### Attaching a System Function

System functions are predefined functions provided by JD Edwards EnterpriseOne. For example, you can attach system functions to an event that hide or display a control, or display media objects.

**Step by Step:**

1. On Event Rules Design, select an event.
2. Click the **ƒ(S)** button.
3. Select a category in the System Functions box.
4. Select the system function that you want to attach.
5. In the Available Objects list, select objects to pass to the system function.

### Attaching a Business Function

Business functions include C code (source language C) or Named Event Rules / NERs (source language Event Rules). You typically use business functions for referential integrity (e.g., deleting secondary records when a master record is deleted), editing routines, and large/complex calculations that might otherwise overload the runtime engine.

**Step by Step:**

1. On Event Rules Design, select an event.
2. Click the **ƒ(B)** button. You can view a description (if one exists) by choosing Attachments from the Row menu.
3. Select a business function and click the **Select** button.
4. In the Available Objects list, select objects to pass to the business function.
5. To assign a literal to a parameter, select `<Literal>` in the Available Objects list. Enter a single value and click OK. Range and List are not valid literals for business function parameters.
6. Indicate the **direction of data flow** between Value and Data Items. Click the direction arrow to toggle through:
   - **Right-pointing arrow:** Data flows from the source to the target.
   - **Left-pointing arrow:** Data flows from the target to the source.
   - **Bi-directional arrow:** Data flows both directions.
   - **Slashed circle:** No data flow.
7. If direction is hard-coded in the data structure (input, output, or bidirectional), that predetermined direction appears. Required items appear in red.
8. Select the **Do Filtering** checkbox under Transfer Filtering to transfer end-user dynamic filter criteria to the business function along with the parameter criteria.
9. Select the **Include in Transaction** option to include the business function for transaction processing (transaction forms only).
10. Select the **Asynchronously** option to enable asynchronous processing.
11. Click **Business Function Notes**, **Structure Notes**, or **Parameter Notes** to add notes.

> **Tip:** To view mapped parameters for a business function in Event Rules Design, right-click the business function and select **Expand BSFN**. To view mapped parameters for all business functions on a specific event, select **Expand All BSFNs** from the View menu.

---

## 10. Using BrowsER

JD Edwards EnterpriseOne **BrowsER** is a read-only viewer for event rules in interactive and batch applications. BrowsER displays the structure of forms within an interactive application (or sections within a batch application) in a hierarchical structure, with events and ER for each event. You can search, filter, and disable or enable ER using BrowsER, but you cannot modify or print ER from it.

### BrowsER View Options

- **Expand Tree / Expand Node** — Control the hierarchical view.
- **Show Object IDs** — Display object identifiers.
- **Hide Objects with no ER** — Reduce clutter by hiding controls that have no event rule logic.
- **Filter ER Records** — Show or hide specific ER statement types: Assignments, Business Functions, Criterion, Comments, Form Interconnections, Options, System Functions.
- **Search ER Records** — Search for specific ER statements or text within those statements.

### Working with BrowsER — Step by Step

1. On OMW, select an object with ER and click the **Design** button.
2. On Interactive Design, click the **Design Tools** tab, then click the **Browse Event Rules** button. Alternatively, access BrowsER directly from within FDA or RDA by choosing **BrowsER** from the View menu.
3. On Browsing, click the **+** and **–** buttons to expand or collapse the hierarchical view of events.
4. To disable an ER line, select the line and click **Disable** button.
5. To enable a disabled line, select the line and click **Enable** button.
6. To hide objects with no ER, right-click anywhere on the BrowsER window and select **Hide objects with no ER**.
7. To start a search or filter, right-click anywhere on the Browsing form and select **Search** or **Filter ER Records**.

---

## 11. Debugging Event Rules

Debugging is the method you use to determine the state of your program at any point of execution. Use debugging to solve problems and to test and confirm program execution. The JD Edwards EnterpriseOne Event Rules Debugger is used to debug interactive applications, reports (batch applications), and table conversions. You can debug both NERs and table ER.

### Debugger Features

| Feature | Description |
|---|---|
| **Go** | Resumes program execution after a breakpoint is reached. |
| **Breakpoint** | Tells the debugger to stop when a particular line is reached. Set breakpoints on lines of code where you want to start debugging. |
| **Delete Breakpoint** | Removes all breakpoints currently set. |
| **Step / Step Over** | Executes the current line of code. Lets you run the program one line at a time to determine the results of every line. |
| **Step Into** | When the current line contains a function call, the debugger steps into the function for line-by-line debugging. Can be used to debug a second application called from within an application. |
| **Disconnect** | Disconnects the debugger from the current application. The application continues to run as if the debugger had not been started. |

### Debugger Setup Steps

1. Launch the ER Debugger.
2. Load into the Debugger the applications to debug (this step takes a few minutes — the Debugger reads all specs and translates them into a Debugging Information Archive, or DIA).
3. Set any desired breakpoints.
4. Launch the application, report, or table conversion. (Step 4 may be done at any point before, during, or after steps 1–3.)

Once you load an application, the ER Debugger provides a **Deactivate** feature to prevent debugging on that application without having to rebuild the DIA later.

### Debugger Interface Components

- **Object Browse window** — Locates applications to load into the debugger. Provides three tabs: interactive applications, UBEs, and TCs.
- **Object Tree** — Lists applications with debug information built. Navigate through a tree structure to a specific event and open an Event Rules window. For power forms with subforms, subforms are listed under the power form. Form IDs appear next to the form name.
- **Event Rules window** — Displays the ER for one event. Shows the current line of execution when the runtime engine is stopped on a line break. Use this window to set and remove breakpoints.
- **Breakpoint Manager** — Tracks set breakpoints and their locations (application name, form name, event name, ER line number, conditions).
- **Variable Tree and Watch window** — Two panes: the Variable Tree (lists variable types and their variables in scope of the current event) and the Watch pane (displays selected variables and their most recently known values).

### Setting Breakpoints

You can set breakpoints using any of these methods:

- Double-click the line in ER.
- Right-click a line and select Insert Breakpoint or New Breakpoint.
- Select a line and press **F9**.
- Single-click in the margin to the left of the ER text.

> **Note:** You cannot set a breakpoint on a comment line (the breakpoint automatically goes to the first code line after the comment). You cannot set a breakpoint on a data structure member (the breakpoint goes to the function call above it that "owns" the data structure).

### Breakpoint State Indicators

- **Red circle** — Normal breakpoint.
- **Question mark inside red circle** — Breakpoint with condition.
- **Hollow circle** — Disabled breakpoint.

### Breakpoint Conditions

Breakpoints have **Condition** and **Hit Count** properties which can be set in the Breakpoint Properties dialog.

**Condition:** A logical expression (e.g., `PO cSelfServiceMode='1'`). Use the Validate Condition button to validate. Check the Condition checkbox to enable it; if unchecked, the condition is saved but not effective.

**Hit Count:** Specifies a certain number of times the breakpoint must be reached before the debugger stops on it.

When both a Condition and a Hit Count are set on a single breakpoint, the debugger stops if either condition is met.

### Inspecting and Modifying Variables

When halted at a breakpoint, you can examine runtime structures and evaluate ER variables. You can add a variable to the Watch pane by double-clicking it in the Variable Tree, or by right-clicking and selecting "Watch Variable."

You can change the value of variables during debugging by double-clicking the variable in the Watch pane and entering a new value. If the ER engine accepts the new value, it appears in the Watch pane. If you enter an inappropriate value (e.g., alpha for a numeric field), the value is not changed.

Special values displayed for variables:

- **blank** — The variable contains only blanks (string and character types only).
- **null** — The variable has no value, or a null/empty value.
- **unknown** — The value could not be obtained from the runtime engine (initial state, application not running, or variable out of scope).

> **Note:** Variable inspection and modification is not available for debugging NERs and table ER.

### ER Variable Tooltip

The ER window can show values of ER variables during a debugging session. Move the mouse cursor over the variable and its value will appear in a ToolTip window when the ER Engine is paused (stopped on a breakpoint or stepping through code).

### Search Combo Box

Use the Search combo box on the toolbar to search for ER text. Enter text and press Enter or F3. The search supports regular expression searches:

| Character | Description |
|---|---|
| `^` | Beginning of a line. Example: `^If` matches "If" only at the beginning of a line. |
| `^` (inside `[ ]`) | Excludes characters. Example: `[^0-9]` matches any non-digit character. |
| `$` | End of a line. Example: `abc$` matches "abc" only at the end of a line. |
| `\|` | Alternation. Example: `a\|b` matches "a" or "b". |
| `.` | Matches any character. |
| `*` | Zero or more occurrences of the preceding character. |
| `+` | One or more occurrences of the preceding character. |
| `?` | Zero or one occurrence of the preceding character. |
| `()` | Grouping and tagged expressions. |
| `[ ]` | Character set — any enclosed character can match. |

---

## 12. Debugging Strategies

### Is the Program Ending Unexpectedly?

The cause is likely an unhandled exception. Set breakpoints at strategic points throughout the code and run the program until you find the problem. If other objects are missing, termination is more abrupt. Remember to transfer all Media Object (Generic Text) objects correctly. If an application has a Row exit to an application that does not exist, an unhandled exception occurs immediately. A missing object is the most likely problem if you cannot enter the program at all.

### Is the Output Incorrect?

Incorrect output typically indicates a flaw within the logic. To find the error:

1. Set a breakpoint prior to the point where bad output is produced.
2. Step through the ER line by line, monitoring relevant ER variables.
3. If the erroneous value occurs before your breakpoint, set another breakpoint earlier and restart.
4. Continue until you find the statement causing the wrong value assignment.

### General Advice

If you don't know which ER event is causing an error, try to isolate it by temporarily disabling ER one event at a time. You can repeat the processing of a single event by performing unnatural actions in the GUI, like toggling up and down between grid rows to force the execution of the Row Is Exited event. Be creative and persistent.

### Debug Logs

You can output a log of SQL statements and events by changing your `jde.ini` file:

```ini
[DEBUG]
TAMMULTIUSERON=0
Output=FILE
ServerLog=0
LEVEL=BSFN,EVENTS
DebugFile=c:\jdedebug.log
JobFile=c:\jde.log
Frequency=10000
RepTrace=0
```

> **Warning:** The `jdedebug.log` file can become very large. To narrow it down, set breakpoints in ER and make a separate copy of the log file each time the application stops at a breakpoint. Label each copy for easier correlation.

---

## 13. Implementation Steps

The following steps need to be performed before working with JD Edwards EnterpriseOne event rules:

1. **Configure OMW** — Configure Oracle's JD Edwards EnterpriseOne Tools Object Management Workbench. See *"Configuring JD Edwards EnterpriseOne OMW"* in the OMW Guide.
2. **Configure OMW user roles and allowed actions.** See *"Configuring User Roles and Allowed Actions"* in the OMW Guide.
3. **Configure OMW functions.** See *"Configuring JD Edwards EnterpriseOne OMW Functions"* in the OMW Guide.
4. **Configure OMW activity rules.** See *"Configuring Activity Rules"* in the OMW Guide.
5. **Configure OMW save locations.** See *"Configuring Object Save Locations"* in the OMW Guide.
6. **Set up default location and printers.** See *"Understanding Report Printing Administration Technologies"* in the Report Printing Administration Technologies Guide.

---

## 14. Glossary

| Term | Definition |
|---|---|
| **Business Function** | A named set of user-created, reusable business rules and logs that can be called through event rules. Business functions can run a transaction or a subset of a transaction. They contain the APIs that enable them to be called from a form, a database trigger, or a non-JDE application. Can be created through event rules or C language. Examples: Credit Check, Item Availability. |
| **Business Function Event Rule** | See Named Event Rule (NER). |
| **Business View** | A means for selecting specific columns from one or more JDE application tables whose data is used in an application or report. A BV does not select specific rows, nor does it contain actual data. |
| **Embedded Event Rule** | An event rule specific to a particular table or application. Examples: form-to-form calls, hiding a field based on a PO value, calling a business function. Contrast with NER. |
| **Event Rule** | A logic statement that instructs the system to perform one or more operations based on an activity that can occur in a specific application, such as entering a form or exiting a field. |
| **Fast Path** | A command prompt that enables the user to move quickly among menus and applications using specific commands. |
| **jde.ini** | A JDE configuration file that provides the runtime settings required for initialization. Must reside on every machine running JDE (workstations and servers). |
| **jde.log** | The main diagnostic log file of JDE. Located in the root directory on the primary drive; contains status and error messages from startup and operation. |
| **Named Event Rule (NER)** | Encapsulated, reusable business logic created using event rules rather than C programming. NERs can be reused in multiple places by multiple programs, providing modularity and code reuse. |
| **Subscriber Table** | Table F98DRSUB, stored on the publisher server with the F98DRPUB table; identifies all subscriber machines for each published table. |
| **Table Conversion** | An interoperability model enabling information exchange between JDE and third-party systems using non-JDE tables. |
| **Table Event Rules** | Logic attached to database triggers that runs whenever the action specified by the trigger occurs against the table. Provides embedded logic at the table level. |
| **Workbench** | A program that enables users to access a group of related programs from a single entry point to complete a large business process. Examples: Payroll Cycle Workbench (P07210), Service Management Workbench (P90CD020). |

---

## 15. Quick Reference Card

### Event Rules at a Glance

| Aspect | Detail |
|---|---|
| **Object Type** | Event Rules (ER) / Named Event Rules (NER) |
| **Purpose** | Attach custom business logic to runtime events |
| **Design Tool** | Event Rules Design (within FDA/RDA) |
| **Viewing Tool** | BrowsER |
| **Debugging Tool** | Event Rules Debugger (GH902 → Debug Application) |
| **Two Kinds** | Named Event Rules (NER) — reusable; Embedded ER — application/table-specific |
| **Validation** | Automatic on Save; manual via File → Validate Event Rules |
| **Error Log** | `b9\prod\log\p1234.log` |

### Available Object Codes Quick Reference

| Code | Object | Code | Object |
|---|---|---|---|
| BC | Business View Column | QC | QBE Cell |
| GC | Grid Column | HC | Hypercontrol Item |
| GB | Grid Buffer | VA | ER Variable |
| FC | Form Control | SV | System Variable |
| FI | Form Interconnect | SL | System Literal |
| PO | Processing Option | TP | Tab Page |
| TK | Table Column (Table ER) | CO | Constant |
| TV | Text Variable | RC | Report Constant |
| RV | Report Variable | IC | Input Column (TC) |
| OC | Output Column (TC) | | |

### ER Variable Scope Prefixes

| Prefix | Scope | Available In |
|---|---|---|
| `frm_` | Form | All events on the form |
| `evt_` | Event | Only the event where created |
| `grd_` | Grid | Grid events |
| `rpt_` | Report | Anywhere in the report |
| `sec_` | Section | Within a report section |

### Find/Browse Form Event Flow

```
Pre-Dialog Is Initialized
  └─ Dialog Is Initialized
       └─ Post Dialog Is Initialized
            └─ [User clicks Find]
                 └─ Build SQL SELECT
                      └─ Fetch Records (loop per record):
                           ├─ BC assigned from database
                           ├─ Grid Record Is Fetched
                           ├─ BC values copied to GC
                           ├─ Write Grid Line–Before
                           ├─ GC values displayed in grid
                           └─ Write Grid Line–After
                      └─ Last Grid Record Has Been Read
```

### Delete Processing Event Flow

```
Button Clicked (Delete)
  └─ Delete Grid Rec Verify–Before
       └─ [Confirm popup]
            └─ Delete Grid Rec Verify–After
                 └─ Delete Grid Rec From DB–Before
                      └─ [SQL DELETE]
                           └─ Delete Grid Rec From DB–After
                                └─ All Grid Recs Deleted From DB
```

### Event Rules Design Toolbar Quick Reference

| Button | Shortcut | Purpose |
|---|---|---|
| Assignment | — | Assign value or expression |
| ƒ(B) | — | Attach business function |
| ƒ(S) | — | Attach system function |
| If/While | — | Create conditional statement |
| Form Interconnect | — | Connect to another form |
| Report Interconnect | — | Connect to batch application |
| Else | — | Insert Else clause |
| Variable | — | Create ER variable |
| Table I/O | — | Database access operations |

### Debugger Breakpoint Methods

| Method | Action |
|---|---|
| Double-click ER line | Toggle breakpoint |
| Right-click → Insert Breakpoint | Set breakpoint |
| Select line + F9 | Toggle breakpoint |
| Click left margin | Set breakpoint |

### Troubleshooting Checklist

| Symptom | Likely Cause | Resolution |
|---|---|---|
| Program ends unexpectedly | Unhandled exception; missing object | Set breakpoints; verify all objects exist. Check media objects and Row exits. |
| Incorrect output | Logic flaw in ER | Set breakpoint before bad output; step through line-by-line monitoring variables. |
| Cannot enter program | Missing object (form, table, BV) | Verify all pieces of the application are present and correctly built. |
| ER not executing | Not relevant event | Check Event Information; update control properties to make event relevant. |
| Variable shows "unknown" | Out of scope or app not running | Verify variable scope; ensure application is running and stopped at a breakpoint. |
| ER validation errors on save | Syntax errors in ER | Review error log; fix syntax (mismatched If/EndIf, invalid objects, etc.). |
| Debug log too large | Output=FILE in jde.ini | Copy and label log at each breakpoint; set Output=NONE when done. |

### jde.ini Debug Configuration

```ini
[DEBUG]
TAMMULTIUSERON=0
Output=FILE          ; Set to NONE when not debugging
ServerLog=0
LEVEL=BSFN,EVENTS
DebugFile=c:\jdedebug.log
JobFile=c:\jde.log
Frequency=10000
RepTrace=0
```

### Key BC/FC/GC Relationships

- BC and FC share the same internal structure when FC is a database item (filter fields are the exception).
- Changing FC automatically changes BC to the same value.
- Changing BC automatically changes FC runtime values (screen may not immediately reflect this).
- On Control Is Exited, the entered value is captured in both BC and FC.
- After Grid Rec Is Fetched fires, BC values are copied into GC.
- After Write Grid Line–Before, GC values are copied to grid cells on the form.
- When selecting a grid row, GC reflects the selected row; BC retains the last-fetched record.
