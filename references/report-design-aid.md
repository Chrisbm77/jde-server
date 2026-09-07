# JD Edwards EnterpriseOne — Report Design Aid Reference (UBE Objects)

*Source: JD Edwards EnterpriseOne Tools — Report Design Aid Guide, Release 9.2 (Part Number E53555-xx)*

---

## 1. Overview

Oracle's JD Edwards EnterpriseOne Report Design Aid (RDA) is the primary tool for creating and modifying batch applications (reports) within JD Edwards EnterpriseOne 9.2. Reports—also called batch applications—run in the background to extract, process, and format data from EnterpriseOne tables. They can produce printed output, PDF files, CSV files, and can also perform database maintenance operations (insert, update, delete).

The batch engine—called the Universal Batch Engine (UBE)—processes batch applications. Each batch application is stored as a report object with object type `UBE`. A report template defines the layout, business view connections, sections, event rules, and processing options. Batch versions are runtime instances of a report template that store specific data selection, data sequencing, and processing option values.

**Object Type Code:** `UBE` (Universal Batch Engine / Report)
**Design Tool:** Report Design Aid (RDA)
**Management Tool:** Object Management Workbench (OMW, Form `W98220A` / Web OMW `W98220WAC`)
**Runtime Engine:** Universal Batch Engine (UBE)
**Report Director:** Wizard-based template creation tool integrated into RDA
**Output Formats:** PDF, CSV, OSA (Output Stream Access), Line Printer

---

## 2. Report Concepts and Architecture

### 2.1 Report Formats

JD Edwards EnterpriseOne supports two primary report formats:

**Application Reports** — Created using the Report Director with predefined Report Director templates. Application reports include financial reporting, fixed assets, and job cost reports. They use smart fields and predefined business views and are guided by the Director wizard. The Application Report drop-down in the Director lists available Report Director templates.

**Standard Reports** — Created using the Report Director or manually within RDA. Standard reports use three detail section types: columnar, group, and tabular.

### 2.2 Report Components

A report template consists of these components:

| Component | Description |
|---|---|
| **Report Header** | Prints once at the beginning of the report. Contains title, company information, runtime fields |
| **Page Header** | Prints at the top of every page. Contains column headings, date, page number |
| **Detail Sections** | The body of the report—columnar, group, or tabular sections that fetch and display data |
| **Level Break Headers** | Print when the value of a level break field changes (before the new group) |
| **Level Break Footers** | Print when the value of a level break field changes (after the completed group); contain aggregates |
| **Page Footer** | Prints at the bottom of every page |
| **Report Footer** | Prints once at the end of the report |

### 2.3 Detail Section Types

**Columnar Sections** — Present data in a column-and-row format similar to a spreadsheet. Column headings appear once at the top, and one row of data prints for each database record fetched. Columnar sections support data selection, data sequencing, level breaks, totals, and conditional logic.

**Group Sections** — Present data in a label-and-field format where the field description (row description) appears to the left and the data value appears to the right. One group of label/value pairs prints per database record. Group sections are useful for forms, individual record displays, or reports where each record requires a multi-line layout.

**Tabular Sections** — Present data in a spreadsheet-like grid with columns (defined by business view fields or calculations) and rows (data rows, sum rows, constant rows, underline rows, calculation rows). Tabular sections support automatic totaling, level breaks (tabular breaks), cell overrides, decimal scaling, and the Drill Down feature. They are commonly used for financial reports. Tabular sections do NOT support: conditional sections, subsection joins, database output, section-level totals through the standard totals mechanism, or the Do Section event for record-by-record suppression (use Column Inclusion instead).

### 2.4 Master Specifications and Batch Versions

**Master Specifications** — The central definition of a report template. Master specifications are stored centrally and define the base layout, sections, event rules, and all design-time settings. All batch versions derive from the master specification.

**Batch Versions** — Runtime instances of a report template. Each version can override:
- Data selection (which records to process)
- Data sequencing (sort order)
- Processing option values
- Report-level overrides (location of objects, printer settings)

Standard versions shipped with JDE begin with `XJDE` (do not modify) or `ZJDE` (can be copied and modified). Custom versions should use names that do not begin with `XJDE` or `ZJDE`. To customize a shipped version, copy the `XJDE` or `ZJDE` version to a new name, then modify the copy.

### 2.5 Report Model

A typical report model includes:

1. **Report Object** — Created in OMW with object type UBE
2. **Business View** — Links the report section to database tables; defines which columns are available
3. **Report Template** — The design-time layout created in RDA
4. **Batch Versions** — One or more runtime configurations
5. **Processing Option Template** — Optional; provides user-configurable parameters at runtime
6. **Report Data Structure** — Optional; used for report interconnects and subsystem jobs

---

## 3. Creating Report Objects

### 3.1 Creating a Report Object in OMW

1. Open Object Management Workbench (OMW)
2. Select a project and click **Add**
3. Select **Batch Application** and click **OK**
4. Enter the object name following naming conventions (see Section 17)
5. Enter description, product code (55–59 for custom), and product system code
6. Click **OK** to create the object

### 3.2 Creating from an Existing Object

You can create a new report by copying an existing report object:
1. In OMW, select the existing object
2. Use **Copy** to create a new object with a new name
3. Modify the copied template as needed

### 3.3 Report Object Properties

| Property | Description |
|---|---|
| **Object Name** | Must follow naming conventions (R prefix + product code + sequence) |
| **Description** | Meaningful description of the report's purpose |
| **Product Code** | 55–59 reserved for custom development |
| **Product System Code** | System code relating to the report's functional area |
| **Object Use** | Typically left at default for reports |

### 3.4 Default Report Component Standards

When a new report is created, the system establishes default standards for:
- Font family and size
- Column spacing
- Page margins
- Header and footer content
- Grid alignment settings

---

## 4. Report Director

### 4.1 Understanding the Report Director

The Report Director is a wizard that guides the developer through the report template creation process. It presents a series of forms to define page headers, business view selection, section layout, data sequencing, data selection, and additional properties. The Director simplifies report creation by presenting relevant options based on the section type being created.

### 4.2 Creating Columnar Sections with the Director

1. Launch the Director from the Batch Application Design form
2. Select **Columnar** section type on the Welcome form
3. **Page Header Details** — Define page header fields (report title, company title, date, page number)
4. **Business View Selection** — Choose how to select the business view:
   - Search for a specific business view
   - Browse all business views
   - Use a predefined (favorite) business view
5. **Section Layout** — Select columns from the business view to include in the report
6. **Data Sequencing** — Define sort order; optionally define level break fields
7. **Define Sort Properties** — Set ascending/descending order for each sort field
8. **Data Selection** — Define record filtering criteria
9. Click **Finish** to generate the report template

### 4.3 Creating Group Sections with the Director

The process is similar to columnar sections. Group sections organize fields as label/value pairs rather than columns. Each field in the section layout displays its row description to the left and the data value to the right.

### 4.4 Creating Tabular Sections with the Director

1. Select **Tabular** section type on the Welcome form
2. **Page Header Details** — Same as columnar
3. **Business View Selection** — Same as columnar
4. **Select Columns** — Choose business view columns and smart fields for the tabular layout
5. For smart fields: define column headings, smart field parameters, and smart field data selection
6. **Data Sequencing Help** — Define sort order and level breaks (first two fields become level break fields by default)
7. **Help with Section Data Selection** — For financial reports, choose balance sheet or income statement
8. **Additional Properties** — Set financial-specific options (Use Financial Description, Display Level of Detail, Display AAI Subtotal, Display Adjust Sign, Display Suppress Zero Rows)
9. Click **Finish**

### 4.5 Application Reports with the Director

Application reports use predefined Report Director templates (see Section 14). The Director presents additional forms based on the template specifications, including smart field configuration and financial-specific criteria.

---

## 5. Configuring the RDA Workspace

### 5.1 User Options

User options allow developers to customize the RDA workspace:

| Option | Description |
|---|---|
| **Show Navigation Assistant** | Enables the navigation panel for quick access to report sections |
| **Show Tip Dialog** | Displays helpful tips at startup |
| **Show Alignment Grid** | Overlays a grid to assist with object alignment |
| **Set Grid Alignment** | Configures grid spacing for object positioning |
| **Show CSV Grid Alignment** | Displays alignment grid for CSV output |

### 5.2 Previewing Reports

Reports can be previewed before full execution:
- Use **File > Print Preview** or the preview toolbar button
- Preview renders the report using the local batch engine
- Preview output can be viewed in Adobe Reader (PDF format)

---

## 6. Working with Properties

### 6.1 Properties Hierarchy

Properties in RDA exist at multiple levels, and lower levels inherit from or override higher levels:

1. **Report Level** — Global properties for the entire report (File > Report Properties)
2. **Section Level** — Properties for individual sections
3. **Column/Row Level** — Properties for columns and rows (tabular sections)
4. **Object Level** — Properties for individual data fields, constants, and variables

### 6.2 Report Properties

| Property Tab | Key Settings |
|---|---|
| **Report Properties** | Report name, description, attached processing option template |
| **Advanced** | Transaction processing enable, subsystem enable, wait time, report data structure |

### 6.3 Section Properties

| Property | Description |
|---|---|
| **Section Description** | Descriptive name for the section |
| **Business View** | The attached business view for data retrieval |
| **Data Selection** | Record filtering criteria |
| **Data Sequencing** | Sort order |
| **Currency** | Currency formatting options |

### 6.4 Tabular Section Properties

Tabular sections have additional properties:

| Property | Description |
|---|---|
| **Number of Optimized Inclusion Rows** | Rows processed using optimized calculation logic |
| **Number of Non-Optimized Inclusion Rows** | Rows processed using standard calculation logic |
| **Row Description Column** | Enable/configure the row description column |

### 6.5 Column and Object Properties

| Property | Description |
|---|---|
| **Variable Name** | Name used in event rules to reference the object |
| **Description Tab** | Data item, alias, column heading text |
| **Display Tab** | Field length, display decimals, justification, edit code |
| **Font/Color Tab** | Font family, size, style, color |
| **Advanced Tab** | Global variable flag, override data item |
| **Position Tab** | X/Y coordinates, absolute positioning |

---

## 7. Working with Objects in Report Sections

### 7.1 Data Field Types

| Field Type | Description |
|---|---|
| **Alpha Variable** | Text/string field from a business view column or event rule variable |
| **Numeric Variable** | Numeric field from a business view column or event rule variable |
| **Date Variable** | Date field from a business view column or event rule variable |
| **Page Number** | System-generated page counter |
| **Report Date** | Date when the report was generated |
| **Report Time** | Time when the report was generated |
| **Company Title** | Company name from system configuration |
| **Report Title** | Title defined in report properties |
| **Page n of Total** | Page number with total page count |
| **Constant** | Static text that prints on every record/row |

### 7.2 Inserting Objects

Objects are inserted into sections via the **Insert** menu:
- Select the field type (alpha variable, numeric variable, date variable, constant, etc.)
- Position the field in the section
- Set properties (variable name, data item, display settings)

### 7.3 Totals

For columnar and group sections, totals can be set up at the section level:
- **In-section totaling** — Sums are calculated and printed at the end of the section
- Total operators include: Sum, Count, Average, Minimum, Maximum

---

## 8. Objects Unique to Tabular Sections

### 8.1 Columns, Rows, and Cells

Tabular sections are structured as a grid:

- **Columns** — Defined by business view fields, smart fields, or calculations
- **Rows** — Multiple row types exist (see below)
- **Cells** — The intersection of a column and a row; cells can have individual overrides

### 8.2 Row Types

| Row Type | Description |
|---|---|
| **Data Row** | Fetches and displays data from the business view. One data row prints for each database record |
| **Calculation Row** | Performs calculations using the Expression Manager. Does not fetch data |
| **Sum Row** | Automatically calculates the sum of the data rows above it |
| **Constant Row** | Displays static text or a fixed value |
| **Underline Row** | Prints a line (single or double) to visually separate data |

### 8.3 Row Description Column

The Row Description column is the leftmost column in a tabular section. It displays descriptive text for each row (e.g., account descriptions in financial reports). The row description can be:
- Automatically populated from the data dictionary
- Manually entered
- Populated via event rules

### 8.4 Calculation Columns

Calculation columns perform column-level calculations using the Expression Manager. Calculations can reference other columns (e.g., variance = budget − actual). Calculation types include column references, mathematical operators, and expressions.

### 8.5 Cell Overrides

Cell overrides modify the properties or data at a specific column-row intersection. You can override:
- The data displayed in a cell
- Font, color, and display properties
- Cell-specific event rules

### 8.6 Decimal Scaling

Decimal scaling simplifies large numbers in tabular sections by dividing values by a specified factor (e.g., divide by 1000 to show amounts in thousands). Decimal scaling is set at the column level and applies to all data rows in that column.

### 8.7 Row Optimization

Tabular sections can optimize row processing for performance. The UBE log file reports the number of optimized vs. non-optimized rows. Optimized rows use streamlined calculation logic for better performance with large datasets.

---

## 9. Modifying Appearance of Report Sections

### 9.1 Section Descriptions

Each section has a description that identifies it in the RDA workspace. Descriptions can be modified through section properties.

### 9.2 Hiding and Showing Sections

Sections can be hidden at design time (they exist but do not print) or shown/hidden dynamically at runtime using the **Hide Section** / **Show Section** system functions in event rules.

### 9.3 Aligning Objects

Objects can be aligned within a section or across sections:
- **Align Left/Right/Top/Bottom** — Aligns selected objects to a common edge
- **Center Horizontally/Vertically** — Centers objects within the section
- **Distribute** — Evenly spaces objects

The alignment grid provides visual guides for positioning. Grid settings are configurable through User Options.

### 9.4 Column Spacing

Column spacing controls the horizontal distance between columns in columnar sections. Spacing can be adjusted through the Section Spacing dialog (Format > Column Spacing).

### 9.5 Absolute Position

Objects can be placed at exact X/Y coordinates using the Position tab of Object Properties. Absolute positioning overrides the automatic layout engine.

### 9.6 Page Breaks

Manual page breaks can be inserted between sections. Page breaks force the next section to begin on a new page.

---

## 10. Modifying Appearance of Report Objects

### 10.1 Field Length and Column Width

- **Field Length** — The number of characters displayed for a field. Set on the Display tab of Object Properties
- **Column Width** — The physical width of a column in the report output. Adjustable by dragging column borders or through properties

### 10.2 Fonts

RDA supports multiple font types:

| Font Type | Description |
|---|---|
| **Proportional Fonts** | Variable-width characters (e.g., Arial, Times New Roman). Used for PDF output |
| **Nonproportional Fonts** | Fixed-width characters (e.g., Courier). Required for line printer output |
| **PCL Fonts** | Printer Command Language fonts for HP-compatible printers |
| **PostScript Fonts** | Fonts for PostScript-compatible printers |
| **TrueType Fonts** | Scalable fonts available on Windows platforms |
| **CJK Fonts** | Chinese, Japanese, Korean double-byte character fonts |
| **Bar Code Fonts** | Special fonts that render as bar codes when printed |

### 10.3 Dynamic Positioning

Dynamic positioning automatically repositions report objects when fonts change size due to language or platform differences. This ensures reports render correctly across different environments.

### 10.4 Font Substitution

**Font Substitution by Language** — Automatically replaces fonts based on the user's language setting. Useful for multinational deployments where different languages require different character sets.

**Line Printer Font Substitution** — Replaces proportional fonts with nonproportional equivalents when output is directed to a line printer.

### 10.5 Justification

Objects can be justified:
- **Left** — Text aligned to the left edge
- **Right** — Text/numbers aligned to the right edge (default for numeric fields)
- **Center** — Text centered within the field width

### 10.6 Edit Codes (Numeric Formatting)

Edit codes control how numeric values are displayed:

| Edit Code | Commas | Decimal | Zero Balance | Negative Sign |
|---|---|---|---|---|
| **1** | Yes | Yes | Blank | No sign |
| **2** | Yes | Yes | Blank | Minus sign |
| **3** | No | Yes | Blank | No sign |
| **4** | No | Yes | Blank | Minus sign |
| **A** | Yes | Yes | .00 | No sign |
| **B** | Yes | Yes | .00 | Minus sign |
| **C** | No | Yes | .00 | No sign |
| **D** | No | Yes | .00 | Minus sign |
| **J** | Yes | Yes | .00 | Trailing minus (−) |
| **K** | No | Yes | .00 | Trailing minus (−) |
| **L** | Yes | Yes | Blank | Trailing minus (−) |
| **M** | No | Yes | Blank | Trailing minus (−) |
| **N** | Yes | Yes | .00 | Parentheses for negative |
| **O** | No | Yes | .00 | Parentheses for negative |
| **P** | Yes | Yes | Blank | Parentheses for negative |
| **Q** | No | Yes | Blank | Parentheses for negative |

### 10.7 Lines and Boxes

Lines and boxes are decorative elements that can be added to sections for visual formatting. They do not contain data but enhance report readability.

---

## 11. Attachments and Comments

### 11.1 Attachments

Attachments are notes that can be added to report objects to document design decisions, usage instructions, or other metadata. Attachments are stored with the report template and do not appear in report output.

### 11.2 Comments

Comments can be added, modified, and deleted on data fields. Comments serve as developer documentation and do not print on the report.

---

## 12. Header and Footer Sections

### 12.1 Report Header

The report header prints once at the beginning of the report. Common fields include:
- Report title
- Company name
- Run date and time
- Custom text or logos

Data fields are inserted via **Insert** menu while the report header section is selected.

### 12.2 Page Header

The page header prints at the top of every page. Common fields include:
- Column headings (automatically generated from data items)
- Page number, Page n of Total
- Report date and time
- Company title

### 12.3 Report Footer

The report footer prints once at the end of the report, after all detail sections and level breaks have completed. Common uses include grand totals, summary statistics, and disclaimer text.

### 12.4 Page Footer

The page footer prints at the bottom of every page. Common fields include:
- Page number
- Confidentiality notices
- Custom text

---

## 13. Level Break Sections

### 13.1 Understanding Level Breaks

Level breaks divide report data into groups based on changes in the value of a designated field. When the batch engine detects that a level break field value has changed, it processes the level break footer (for the completed group) and the level break header (for the new group).

Levels are hierarchical: Level 1 is the highest (least granular), and each subsequent level is more granular. Multiple level breaks can be nested. For example:
- Level 1: Company
- Level 2: Business Unit
- Level 3: Account

### 13.2 Level Break Headers

Level break headers print when a new group begins. They are processed from the highest level to the lowest level (e.g., Company header prints before Business Unit header).

### 13.3 Level Break Footers

Level break footers print when a group ends. They are processed from the lowest level to the highest level (e.g., Business Unit footer prints before Company footer).

Level break footers typically contain aggregates:

| Aggregate Type | Description |
|---|---|
| **Sum** | Total of all values in the group |
| **Count** | Number of records in the group |
| **Average** | Mean value of the group |
| **Minimum** | Smallest value in the group |
| **Maximum** | Largest value in the group |

### 13.4 Reprinting at Page Break

Level break footers can be configured to reprint at page breaks, ensuring that subtotals are visible when a group spans multiple pages.

### 13.5 Associated Descriptions

Level break sections can have associated descriptions that display the level break field value (e.g., "Company: 00001 — ACME Corp").

### 13.6 Assignments in Level Break Footers

You can attach event rules to level break events to perform assignments, calculations, or business function calls. When working with level break footers, attach logic to the **End Lvl Brk Footer Section** event rather than the End Section event.

---

## 14. Smart Fields

### 14.1 Understanding Smart Fields

Smart fields are data dictionary items (glossary group K) with attached business functions. They encapsulate reusable business logic—such as calculations, data derivation, or lookups—so that report developers can add complex functionality without writing event rules manually.

### 14.2 How Smart Fields Work

1. A smart field data dictionary item (glossary group K) references a business function and a named mapping
2. The named mapping defines the source of each parameter in the business function's data structure
3. When the report developer selects a smart field in the Director, the system automatically generates the event rules to call the business function with the correct parameters
4. The smart field's business function executes on the appropriate event (e.g., Column Inclusion for tabular sections, Do Variable for columnar/group sections)

### 14.3 Smart Field Templates

Smart fields must be added to a Smart Field template (P91420) before they can be used in reports. Smart field templates group smart fields that share the same data selection criteria. The smart field template is then attached to a Report Director template.

### 14.4 Creating Custom Smart Fields

The components required to create a custom smart field are:

1. **Data Dictionary Item (Prompt)** — Glossary group D; serves as the user prompt in the Director (e.g., "Quarter to Display")
2. **Data Structure** — Contains all parameters needed by the business function; all data items must reside in the same business view
3. **Named Mapping** — Maps the source of each parameter (Literal, Prompt, Table, Data Dictionary Item, System Value); naming convention begins with `M` followed by the data structure name
4. **Business Function** — Contains the calculation/logic; can be a C business function or Named Event Rule (NER)
5. **Smart Field Data Item** — Glossary group K; links the business function, event, and named mapping via the Smart Field Criteria form

---

## 15. Advanced Report Enhancements

### 15.1 Overview

Advanced report enhancements include:
- **Subsection Joins** — Joining two detail sections with different business views (parent/child)
- **Text Attachments** — Including media objects in reports
- **Drill Down** — Linking tabular report data to interactive applications
- **Database Output** — Using batch applications to insert, update, or delete database records

---

## 16. Subsection Joins

### 16.1 Understanding Subsection Joins

A subsection join links two detail sections (parent and child) that use different business views. This creates a parent/child relationship where the child section processes its records for each record in the parent section.

### 16.2 Join Types

- **Parent/Child Join** — The child section fetches records related to the current parent record using join fields
- **Many-to-Many** — Both sections independently fetch and display their data with a common key

### 16.3 Join Fields

Join fields define the relationship between parent and child sections. The join field in the parent section must correspond to a field in the child section's business view.

### 16.4 Data Sequencing in Subsection Joins

Data sequencing for the child section can be defined independently. The child section uses the Refresh Section event (rather than Initialize Section) for all iterations after the first.

### 16.5 Section Types in Joins

Columnar and group sections can participate in subsection joins. Tabular sections cannot be used in subsection joins.

---

## 17. Text Attachments (Media Objects)

Text attachments enable reports to include media object text from the Media Object (F00165) table. When a record has text attachments, the report can display the associated text.

---

## 18. Drill Down Feature

### 18.1 Understanding Drill Down

The Drill Down feature links data in a tabular report to an interactive application. Users viewing the report output can click on a data value to launch the associated interactive application and view the detail behind the value. This is especially useful for financial reports where auditors need to trace amounts back to source transactions.

### 18.2 Drill Down Components

| Component | Description |
|---|---|
| **Target Application** | The interactive application to launch |
| **Target Form** | The specific form within the application |
| **Target Version** | The version of the application to use |
| **Data Mapping** | Maps report values to the form's data structure |

### 18.3 Drill Down Processing

The Drill Down feature uses the **Do Balance Auditor** event (tabular sections only). At runtime, the system writes drill-down reference records to a work file. When a user clicks a drill-down link in the report output, the system retrieves the reference record and launches the target application with the mapped values.

### 18.4 Purging Drill Down Data

Drill-down work file records should be periodically purged to maintain system performance. Use the **Purge Financial Reporting Drill Down Work File** form to remove old drill-down data.

---

## 19. Database Output

### 19.1 Understanding Database Output

Database output enables batch applications to modify database records (insert, update, delete) as they process. This is distinct from read-only reporting—it allows a report to function as a data processing application.

### 19.2 Configuration

Database output is configured at the section level:
1. Open section properties
2. Select the **Database Output** tab
3. Choose the operation type: **Insert**, **Update**, or **Delete**
4. Map source fields (from the business view or event rules) to target table fields

### 19.3 Environment Override

Database output supports environment overrides, allowing you to direct output to a different database environment than the source data. This is useful for staging or testing scenarios.

### 19.4 Text File Output

Batch applications can also output data to delimited text files rather than (or in addition to) database tables. Text file output is configured in section properties.

---

## 20. Event Rules in Reports

### 20.1 Understanding Event Rules

Event rules are logic statements that instruct the batch engine to perform operations at specific processing points (events). Event rules in reports provide the same fundamental capabilities as in interactive applications, with some batch-specific differences.

### 20.2 If/Else/While Statements

Conditional logic uses If/Else/While constructs:
- **If** — Evaluates a condition; executes the enclosed logic if true
- **Else** — Executes alternative logic when the If condition is false
- **While** — Repeats logic as long as the condition remains true

Conditions are built using the Criteria Design form, selecting left operands, operators (Equal, Not Equal, Greater Than, Less Than, etc.), and right operands from available objects.

### 20.3 Assignments

Assignments set the value of a field or variable. The Assignment form allows you to select a target field and assign a value from:
- Another field
- A literal value
- A calculation or expression
- A system value or variable

### 20.4 Expression Manager

The Expression Manager provides a formula-building interface for complex calculations. Expressions can include:
- Arithmetic operators (+, −, ×, ÷)
- Field references
- Functions
- Parenthetical grouping

### 20.5 Text Variables

Text variables are literal string values defined in RDA for use in event rules. They support translation for multi-language deployments. Text variables are created through **Edit > Text Variables** in the RDA workspace.

### 20.6 System Functions

System functions provide built-in capabilities that can be called from event rules:

| Category | Examples |
|---|---|
| **Object** | Hide Object, Show Object |
| **Section** | Hide Section, Show Section, Suppress Section Write, Do Custom Section, Stop Section Processing |
| **General** | Set Selection Append Flag, Set Sequence Append Flag, Set User Selection, Set User Sequence, Stop Section Processing |
| **Messaging** | Send, Update, Delete messages |
| **Workflow** | Work with processes |
| **Transaction Processing** | Begin Transaction, Commit Transaction, Rollback Transaction |
| **Media Objects** | Work with media objects |

**Key System Functions:**

- **Stop Section Processing** — Stops processing the current section and moves to the next section. Useful for performance when no more relevant records exist
- **Suppress Section Write** — Suppresses the current record only; the engine continues to the next record
- **Hide Object** — Hides an object in group/columnar sections (prints a blank line; use conditional sections to avoid blank lines)
- **Do Custom Section** — Calls a custom (conditional) section from within event rules

### 20.7 Business Functions

Business functions (C or NER) can be called from event rules to perform complex processing. The business function is selected from the Business Function Search form, and its data structure parameters are mapped to available objects.

### 20.8 Event Rule Variables

Event rule variables store temporary values during report processing. They are created using data dictionary items and have three scopes:

| Scope | Prefix | Lifetime |
|---|---|---|
| **Report** | `rpt` | Entire report execution; value persists across all sections |
| **Section** | `sec` | Current section only; reset when the section reinitializes |
| **Event** | `evt` | Current event only; reset after the event completes |

### 20.9 Table I/O

Table I/O operations allow event rules to directly read from and write to database tables, independent of the section's business view:
- **Open** — Opens a table for read or write operations
- **Fetch Single** / **Fetch Next** — Retrieves records from a table
- **Insert** — Adds a record to a table
- **Update** — Modifies an existing record
- **Delete** — Removes a record from a table
- **Close** — Closes the table

### 20.10 Custom Sections

Custom sections are conditional sections that do not print automatically. They are called from event rules using the **Do Custom Section** system function. Custom sections are useful for:
- Printing conditional content (e.g., disclaimers, notes)
- Displaying alternate layouts based on data values
- Appending supplemental information after level breaks

### 20.11 Do Section vs. Column Inclusion

This is a critical distinction for tabular sections:

- **Do Section** event (columnar/group sections) — Fires before each record is processed. Use it to suppress records, manipulate values, or perform calculations before output
- **Column Inclusion** event (tabular sections) — Fires after each record is fetched from the database. Use it to determine whether a fetched record should be included in cell calculations. Do NOT use Column Inclusion for calculations between columns or between variables within a column

### 20.12 ER Compare (BrowsER)

ER Compare allows developers to compare event rules across different objects, versions, or environments. This tool helps identify differences in logic when troubleshooting or reviewing changes.

---

## 21. Understanding Events

### 21.1 Report Level Events

| Event | Description |
|---|---|
| **Do Initialize Printer** | Resolves and validates the printer name. Called once per subsystem trigger. Use Initialize Printer system function here only |
| **Initialize Report** | First event processed. Resets global variables (unless subsystem with existing event rules). Executes once per report |
| **End Report** | Last event processed. Executes once at end of report. In subsystems, executes only after End Subsystem trigger |

### 21.2 Section Level Events

| Event | Description |
|---|---|
| **Initialize Section** | First time a section is encountered. Useful for global variables and preparatory logic. For conditional sections, processed each time called. For subsection joins, only first time child processes |
| **Advance Section** | Each database fetch. Use for pre-fetch processing. If no business view, processed once |
| **Before Level Break** | After fetch, before level break checks. Use for post-fetch, pre-level-break processing |
| **Do Section** | After values assigned, before output. Most commonly used event for columnar/group sections |
| **Do Tabular Break** | Tabular only. Fires when a level break field value changes |
| **Do Balance Auditor** | Tabular only. Used for the Drill Down feature |
| **After Last Object Printed** | After a record is output. Use for post-output processing |
| **End Section** | After last record processed. Useful for end-of-file procedures |
| **Refresh Section** | Subsequent processing of a child section (after first Initialize). Use to reset data selection/sequencing for child sections |
| **Suspend Section** | When content exceeds page space. Use for page-break processing |
| **Init Break Section** | After a level break begins. Initializes child sections joined on level breaks |
| **End Break Section** | After a level break finishes processing |
| **Init Lvl Brk Footer Section** | Before level break footer. Values from previous level are accessed |
| **End Lvl Brk Footer Section** | After level break footer |
| **Init Lvl Brk Header Section** | Before level break header. Processed after footer if both exist |
| **End Lvl Brk Header Section** | After level break header |

### 21.3 Page Header/Footer Events

| Event | Description |
|---|---|
| **Initialize Page Header** | Beginning of report (after report header) and every page break |
| **End Page Header** | After page header finishes |
| **Initialize Page Footer** | Beginning of report; initializes footer values for current page |
| **End Page Footer** | After page footer finishes |

### 21.4 Report Header/Footer Events

| Event | Description |
|---|---|
| **Initialize Report Header** | Once at beginning of report. Similar to Init Section for report header only |
| **End Report Header** | After report header. Page header processes next |
| **Initialize Report Footer** | Once at end of report, before footer prints |
| **End Report Footer** | After report footer. Report terminates |

### 21.5 Constant and Variable (Object) Events

| Event | Description |
|---|---|
| **Initialize Variable / Initialize Constant** | Before each object is processed. Use for pre-processing (e.g., position adjustments) |
| **Do Variable / Do Constant** | Before font/color selection and before value is output. Last chance to manipulate values |
| **Do Column Heading** | When column heading is initialized. Use to populate headings via business functions |
| **End Variable / End Constant** | After object is processed (even if invisible or suppressed) |
| **Suspend Object** | When an object spans pages (partial fit). Halts until next page |
| **Column Inclusion** | Tabular only. After each fetch. Use for inclusion/exclusion criteria in cell calculations |
| **Cell Inclusion** | Tabular only. During Do Object, after cell calculations. Use to manipulate cell data before display |

---

## 22. Report Processing

### 22.1 Batch Processing Overview

When a batch application executes, the batch engine processes:
1. Report-level events (Initialize Report)
2. Report Header section (if exists)
3. Page Header section (if exists)
4. Detail sections in order (top to bottom in the template)
5. Level break processing (when break field values change)
6. Page Footer section (if exists)
7. Report Footer section (if exists)
8. Report-level events (End Report)

### 22.2 Section Processing Order

Sections are processed in the order they appear in the report template (top to bottom). Within each section:
1. Initialize Section
2. Advance Section (fetch record)
3. Before Level Break
4. Do Section
5. Process objects (Init Object → Do Object → End Object for each)
6. After Last Object Printed
7. Repeat from step 2 for next record
8. End Section (after all records processed)

### 22.3 Level Break Processing

Level break processing follows this sequence:
1. **Footer processing** (lowest level to highest level) — When a break field value changes, footers process from the most granular level upward
2. **Header processing** (highest level to lowest level) — After footers complete, headers process from the least granular level downward

### 22.4 Subsection Join Processing

For parent/child joins:
1. Parent section fetches a record
2. Child section is initialized (Initialize Section on first occurrence; Refresh Section on subsequent occurrences)
3. Child section fetches and processes all matching records
4. Parent section fetches the next record
5. Repeat

### 22.5 Custom Section Processing

Custom sections are not processed automatically. They execute only when called via the **Do Custom Section** system function in event rules.

### 22.6 Tabular Section Processing

Tabular sections process differently from columnar/group sections:
- Data rows fetch records and accumulate values into cells
- Sum rows automatically calculate totals
- Calculation rows evaluate expressions
- Level breaks in tabular sections use the **Do Tabular Break** event
- The **Column Inclusion** event controls which fetched records contribute to cell calculations

---

## 23. Runtime Processing

### 23.1 Available Objects at Runtime

Runtime objects are identified by two-character alphabetical codes:

| Code | Object | Description |
|---|---|---|
| **BC** | Business View Columns | Values fetched from the database |
| **PO** | Processing Options | Values from the batch version's processing options |
| **VA** | Event Rule Variables | Developer-created variables in event rules |
| **SV** | System Variables | Environment variables accessible to event rules |
| **SL** | System Values | Constant system values accessible to event rules |
| **TV** | Text Variables | Literal strings created in RDA for event rules |
| **RC** | Report Constants | Column headings (columnar) and constant portions of fields (group) |
| **RV** | Report Variables | Report-level variables |
| **PC** | Previous Business View Columns | Previous values of business view columns (before current fetch) |
| **PV** | Previous Report Variables | Previous values of report variables |

### 23.2 Event Flow for Group Sections

The runtime engine processes events in this order, populating runtime structures at each step:

1. **Initialize Section** — Variables initialized; BC, RV, PC, PV all at initial/zero values
2. **Advance Section** — First fetch performed; BC populated with first record values
3. **Before Level Break** — Level break fields checked; PC holds previous values
4. **Do Section** — Values assigned for output; RV populated
5. **After Last Object Printed** — Record output complete; PV updated with current RV values
6. **Advance Section** — Next fetch; BC updated with new record; PC holds previous BC values
7. Repeat steps 3–6 until all records fetched

---

## 24. Report Interconnects

### 24.1 Understanding Report Interconnects

Report interconnects launch reports or batch applications from:
- Another batch application
- An interactive application

### 24.2 Processing Methods

| Method | Description |
|---|---|
| **Synchronous** (default) | The initiating process waits for the called batch application to finish before continuing |
| **Asynchronous** | The initiating process starts the called batch application and continues running. Both execute simultaneously |

### 24.3 Creating Report Interconnects

1. Open the primary report template in RDA
2. Access Event Rules Design on the detail section and select an event (commonly **After Last Object Printed**)
3. Click the **Report Interconnection** toolbar button
4. Select the target batch application and version
5. Map parameters from Available Objects to the Data Structure-Value column
6. Set the direction of data flow between Value and Data Items
7. Optionally select **Asynchronously** and/or **Include in Transaction**
8. Add notes and click **OK**

### 24.4 Report Data Structures

The secondary (called) batch application uses a report data structure to receive values from the primary batch application. The report data structure is defined under **File > Report Data Structure** in RDA.

---

## 25. Transaction Processing

### 25.1 System Functions

| System Function | Description |
|---|---|
| **Begin Transaction** | Starts a manual transaction. Takes a Transaction ID (MathNumeric) parameter. Only one transaction can be active at a time from Event Rules |
| **Commit Transaction** | Commits all database operations since Begin Transaction. If commit fails, system automatically rolls back |
| **Rollback Transaction** | Cancels all database operations since Begin Transaction. Use only when absolutely necessary |

### 25.2 Enabling Transaction Processing

Transaction processing must be enabled in Report Properties:
1. **File > Report Properties > Advanced tab**
2. Select the **Transaction Processing** option

### 25.3 Table I/O with Transactions

To include Table I/O operations in a transaction:
1. Open the Table I/O statement's properties
2. In Advanced Operations, select **Open**
3. Click **Advanced Options**
4. Select **Include in Transaction**

### 25.4 System Variable — SV TP Commit Status

| Value | Meaning |
|---|---|
| **CO TP_ACTION_FAIL** | Last transaction action (Commit or Rollback) failed |
| **CO TP_ACTION_SUCCESS** | Last transaction action succeeded |
| **CO TP_IN_TRANSACTION** | Transaction started; no Commit or Rollback called yet |
| **CO TP_NO_TRANSACTION** | No transaction started or completed |

### 25.5 Transaction Processing Example

```
Begin Transaction (transaction ID)
  Table IO_Open Table 1
  Table IO_Insert Table 1
  Table IO_Open Table 2
  Table IO_Insert Table 2
Commit Transaction (transaction ID)

If (SV TP_Commit_Status == CO TP_ACTION_FAIL)
  // Transaction failed — system has rolled it back
  // Call business function to roll back external operations
Else
  // Transaction successful
End If
```

---

## 26. Business View Favorites

### 26.1 Understanding Favorites

Business view favorites organize frequently used business views into a tree structure of folders and subfolders. During report creation, the Director can present favorited business views for quick selection.

### 26.2 Managing Favorites

| Application | Form ID | Purpose |
|---|---|---|
| **Favorites (P9100)** | W91100A | Work with favorites folders and subfolders |
| **Object Folder Revisions** | W91100B | Add/edit favorite folders |
| **Favorites Revisions** | W91100C | Add business views to folders |
| **Notes Revisions** | W91100E | Add/edit notes on favorites |

### 26.3 Multilingual Support

Favorites descriptions can be translated to multiple languages using the Favorites Description Translation form (W91100F → W91100G). Translated descriptions appear when users select the corresponding language.

---

## 27. Date Titles in Financial Reports

### 27.1 Understanding Date Titles

Date titles indicate the time period covered by financial report data. They appear in the page header.

| Date Title Type | Example |
|---|---|
| **A (As of)** | As of 03/31/07 |
| **B (Balance sheet)** | As of March 31, 2007 |
| **P (Profit and Loss)** | For the Three Months Ending March 31, 2007 |
| **S (Single period)** | For the Month Ending March 31, 2007 |

### 27.2 Text Substitution Parameters

| Parameter | Description |
|---|---|
| **@1: Period Name** | Name of the period (e.g., month name) from F83110 table |
| **@2: Day Period Ends** | Day of the month from Date Fiscal Patterns (F0008) |
| **@3: Century and Year** | Full year (e.g., 2007) |
| **@4: Year** | Two-digit year |
| **@5: Text for Period Number** | Text representation of period count (UDC 83/PT) |
| **@6: Date** | Date in MM/DD/YY format |

### 27.3 Business Function

The **User Defined Date Title** business function (B8300007) retrieves and formats date titles. It uses the company number to determine the fiscal year pattern. Map the date title type, language preference, company, period number (PO), and fiscal year (PO) in the business function data structure.

### 27.4 Implementing Date Titles

1. Insert an alpha variable in the page header (Display Length = 100, Global Variable = Yes)
2. In the tabular section's Initialize Section event, call business function B8300007
3. Map the data structure parameters:
   - `cDateTitleType` → Literal (date title type code)
   - `szLanguagePreference` → SL LanguagePreference (or a literal language code)
   - `szCompany` → Literal (company number)
   - `mnPOPeriodNumber` → PO PeriodNoGeneralLedger
   - `szPOFiscalYear` → PO szFiscalYear
   - `szDateTitle` → RV (the alpha variable created in step 1)

### 27.5 Accounting Period Column Headings

Column headings for accounting periods are managed through:
- **Column Headings (P83110)** — For standard 12/13/14 period fiscal years
- **52 Period Column Headings (P83110B)** — For 52-period fiscal years

Each fiscal date pattern type can have unique period names to accommodate company-specific patterns.

---

## 28. Processing Option Templates

### 28.1 Understanding Processing Option Templates

Processing option templates define parameters that users can configure at runtime for batch applications. They control how reports process data, set default values, customize versions, control formatting, page breaks, and totaling.

### 28.2 Template Structure

- One or more **tabs** (pages) categorize parameters (e.g., Print, Defaults, Process)
- Each tab contains **comments** (descriptive text) and **data items** (parameters)
- Each data item has a **member name** for identification in Event Rules Design

### 28.3 Member Name Convention

| Component | Description |
|---|---|
| **Prefix** | Hungarian notation for data type (e.g., `c` for character, `sz` for string, `mn` for math numeric) |
| **Suffix** | Data item alias preceded by underscore |
| **Example** | `cDisplayCommentsColumn_A` |

### 28.4 Creating Processing Option Templates

1. In OMW, add a **Data Structure** object with Object Use `360`
2. Select **Processing Option Template** type
3. Open Processing Option Design Aid
4. Add tabs with Short Name and Long Name
5. Add comment boxes with descriptive text
6. Drag data items from the Data Dictionary Browser
7. Modify descriptions and member names
8. Test using **Edit > Test**

### 28.5 Attaching to Reports

1. In RDA, select **File > Select Processing Options**
2. Search for and select the processing option template
3. Create event rules to process processing option values
4. Processing option values are stored with each batch version
5. At runtime: **Prompt for Values** (user enters values) or **Blind Execution** (predefined values)

---

## 29. Subsystem Jobs

### 29.1 Understanding Subsystem Jobs

Subsystem jobs are batch processes that continuously run independent of JD Edwards applications. They process records from a data queue (the Subsystem Job Master table F986113) asynchronously. Use subsystem jobs to:
- Off-load processor resources
- Protect server processes
- Perform repetitive, high-throughput processes

### 29.2 How Subsystem Jobs Work

1. An interactive application (e.g., Sales Order Entry) issues a subsystem job request
2. The system places a record in the Subsystem Job Master (F986113) table with status and key information
3. The continuously running subsystem monitors F986113 for matching records
4. When found, the subsystem processes the record and updates the status

### 29.3 Defining Reports as Subsystem Jobs

1. Open the report template in RDA
2. **File > Report Data Structure** — Add required data items
3. **File > Report Properties > Advanced tab** — Select **Subsystem** option
4. Set the **Wait Time (ms)** — Milliseconds the subsystem sleeps between queue checks
5. Click **Generate** to create the header file (Report_Name.h in the `include` subdirectory)

### 29.4 Adding Records via API

The `ubeReport_AddSubsystemRecord` API adds records to the subsystem table:
```c
bRet = ubeReport_AddSubsystemRecord(
    hUser,          // User Handle
    "R98SSUBE",     // Subsystem report name
    "XJDE0001",     // Subsystem version
    NULL,           // Override environment (NULL for default)
    szServer,       // Server name
    &dsRI           // Report interconnect data structure
);
```

---

## 30. Report Director Templates

### 30.1 Understanding Report Director Templates

Report Director templates define parameters that guide the Director wizard during report creation. They store specifications in these tables:

| Table | Content |
|---|---|
| **Report Director Templates (F91400)** | Default business view and processing option information |
| **Report Director Templates Sequence Items (F91410)** | Preferred data sequencing |
| **Report Director Templates Smart Field Activation (F91420)** | Smart field display configuration |

### 30.2 Template Specifications

For each Report Director template, you define:
- Detail section type (columnar, group, or tabular)
- Default business view
- Processing option template (optional)
- Smart field template (optional; dependent on business view)
- Default data sequencing and level breaks (first two items become level break fields)
- Additional properties (financial vs. generic criteria) — tabular only
- Drill Down feature configuration — tabular only

### 30.3 Naming Convention

Custom Report Director template names should begin with **DT** followed by a product code (55–59) and a system-related suffix.

### 30.4 Template Tabs

| Tab | Availability | Content |
|---|---|---|
| **Building Blocks** | All templates | Section type, business view, processing options, smart field template, default sequencing |
| **Properties** | Tabular only | Financial description, level of detail, AAI subtotal, adjust sign, suppress zero rows, generic/financial criteria |
| **Drill Down** | Tabular only | Drill Down activation, target application/form/version |

### 30.5 Managing Templates

| Application | Form ID | Purpose |
|---|---|---|
| **Report Director Templates (P91400)** | W91400A | Work with templates |
| **Report Director Templates Revisions** | W91400B | Add/edit template specifications |

---

## 31. Batch Error Messages

### 31.1 Understanding Batch Error Messaging

The error message system provides a consistent interface to review batch application errors in the Work Center (P012503). Error messages use a tree structure (parent/child) to group related messages.

### 31.2 Message Types

| Type | Description |
|---|---|
| **Non-text substituted** | Static error text (e.g., "Document number is invalid") |
| **Text substituted** | Dynamic text with runtime values (e.g., "Document number 55.5555 is invalid"). Uses `&1`, `&2`, etc. as placeholders |
| **Active (Action) messages** | Include a link to launch the associated interactive application for error resolution |

### 31.3 Level Break Messages

Level break messages group errors hierarchically:
- **Level 1** — High-level summary (e.g., "Job completed with errors")
- **Level 2** — Detail grouping (e.g., "Batch 3230 has errors")
- **Level 3** — Specific error (e.g., "Voucher 14787 contains errors")
- Additional levels as needed

### 31.4 Work Center APIs

| API / Function | Purpose |
|---|---|
| **B0100025** (F01131 Edit JDEM Error Message) | Initialize Work Center error processing. Call in Initialize Section event of primary section |
| **ProcessErrorsToPPAT** (B0100011) | Process level break messages. Call at each level break point and at level 1 to terminate |
| **jdeSetGBRError** / **jdeSetGBRErrorSubText** | Set error messages in the runtime error stack |

### 31.5 API Call Sequence Rules

- Calls must follow a valid parent/child order (e.g., 4, 4, 4, 3, 4, 4, 3, 2, 1)
- Never skip a level — all intermediate levels must be called
- Level 1 must be called once at termination (typically End Section of primary section)
- Level 1 creates the "job completed" message and frees workspace

### 31.6 Components for Custom Level Break Messages

1. **Data Dictionary Item** — Glossary group Y (PPAT Level Messages); alias begins with `LM`
2. **Text Substituted Data Structure** — Named `DELM` + unique number (e.g., DELM5509)
3. **Business Function Data Structure** — Named `DLM` + unique number; must include `EV01` (renamed to `cIncludeInterconnect`) and `GENLNG` (renamed to `idGenlong`)
4. **Business Function** — Named `BLM` + unique number; processes level break errors and action message mappings

### 31.7 cAllowUserIdToChange Parameter

The initialize API supports routing error messages to the user who created the original records rather than the person who submitted the batch job. Set `cAllowUserIdToChange` to `1` when initializing, then specify the target user via `szUserid` on the ProcessErrorsToPPAT call.

---

## 32. Runtime System Information API

### 32.1 Overview

Effective with JD Edwards EnterpriseOne Tools Release 9.2.7, the **GetRuntimeInfo** business function (B986110R) retrieves batch job runtime information from the virtual job batch queue.

### 32.2 Available Information

| Field | Description |
|---|---|
| **Report Name** | Name of the executing report |
| **Version Name** | Version being executed |
| **User Name** | Short user name |
| **Environment Name** | EnterpriseOne environment |
| **Execution Start Time** | UTC timestamp when spec load completed and execution began |
| **Job Queue** | Queue name (blank on Dev Client) |
| **Execution Host Name** | Virtual or actual hostname ("WinClient" on Dev Client) |
| **Actual Host Name** | Physical enterprise server hostname |
| **Job Number** | Current job number (0 on Dev Client) |
| **Parent Job Number** | Job number of calling UBE (0 if top-level) |
| **Oldest Parent Job Number** | Job number of topmost UBE in synchronous chain (0 if top-level) |
| **Printer Name** | Current printer |
| **PDF File Name** | Assigned at End Report event only |
| **CSV File Name** | Assigned at End Report event only; valid only if CSV output activated |
| **OSA File Name** | Assigned at End Report event only; valid only if OSA stream activated |

### 32.3 System API

The system-level API `ubeReport_GetRuntimeInfo()` is the underlying C function used by B986110R. It uses the `UBE_INFO_TYPE` enum (defined in `jdekdfn.h`) to specify which data to retrieve. The API returns a void pointer to allocated memory that must be freed with `jdeFree()` after use.

### 32.4 Typical Usage

Call B986110R from the **Initialize Section** event of the main driver section, passing section-level or report-level variables to be populated by the function.

---

## 33. Naming Conventions

### 33.1 Report Objects

| Component | Convention |
|---|---|
| **Report Object** | `Rxxxxxxxx` — R prefix + product code (55–59) + sequence number |
| **Report Director Template** | `DTxxxxxxxx` — DT prefix + product code (55–59) + system suffix |
| **Smart Field Template** | `SFTxxxxxxxx` — SFT prefix + product code (55–59) + system suffix |
| **Named Mapping** | `Mxxxxxxxx` — M prefix + data structure name (append sequential letter for multiples: M550101A, M550101B) |
| **Level Break Message DD Item** | Alias begins with `LM` |
| **Level Break Message DS (text sub)** | `DELM` + unique number |
| **Level Break Message DS (BF)** | `DLM` + unique number |
| **Level Break Message BF** | `BLM` + unique number |

### 33.2 Processing Option Templates

The naming convention follows: `Txxxxxyyyy` where T is the prefix, xxxxx is the program number, and yyyy is a sequence identifier. Member names use Hungarian notation prefix + data item alias (e.g., `cDisplayCommentsColumn_A`).

### 33.3 Event Rule Variables

| Scope | Prefix |
|---|---|
| **Report scope** | `rpt` |
| **Section scope** | `sec` |
| **Event scope** | `evt` |

### 33.4 Batch Versions

| Pattern | Usage |
|---|---|
| `XJDE****` | Oracle-shipped; do not modify |
| `ZJDE****` | Oracle-shipped; can be copied |
| Custom names | Must not begin with XJDE or ZJDE |

---

## 34. Key Tables

| Table | Description |
|---|---|
| **F91400** | Report Director Templates |
| **F91410** | Report Director Templates Sequence Items |
| **F91420** | Report Director Templates Smart Field Activation |
| **F83100** | Date Title definitions |
| **F83110** | Period column heading names |
| **F0008** | Date Fiscal Patterns |
| **F00165** | Media Objects (text attachments) |
| **F986113** | Subsystem Job Master |
| **F98611** | Data Source Master |
| **F98306** | Processing option template specifications |
| **F983051** | Processing option data values |
| **F98VAR** | Table of Variables (system values) |

---

## 35. Key Applications

| Application | ID | Purpose |
|---|---|---|
| **Object Management Workbench** | P98220 | Create and manage report objects |
| **Report Design Aid** | — | Design report templates |
| **Processing Option Design Aid** | — | Create processing option templates |
| **Report Director Templates** | P91400 | Define Report Director templates |
| **Smart Field Templates** | P91420 | Manage smart field templates |
| **Favorites** | P9100 | Organize business view favorites |
| **Date Titles** | P83100 | Define financial report date titles |
| **Column Headings** | P83110 | Assign accounting period column headings |
| **52 Period Column Headings** | P83110B | Column headings for 52-period fiscal years |
| **Work Center** | P012503 | Review batch error messages |

---

## 36. Glossary

| Term | Definition |
|---|---|
| **Business Function** | A named set of reusable business rules and logic that can be called through event rules. Can be written in C or as Named Event Rules (NERs). Business functions contain APIs enabling them to be called from forms, database triggers, or non-JDE applications |
| **Business View** | A means for selecting specific columns from one or more JDE tables for use in an application or report. Contains no actual data — it is a view definition |
| **Edit Rule** | A method for formatting and validating user entries against predefined rules |
| **Embedded Event Rule** | An event rule specific to a particular table or application (e.g., form-to-form calls, hiding fields based on processing options) |
| **Event Rule** | A logic statement instructing the system to perform operations based on an activity at a specific processing point |
| **Named Event Rule (NER)** | Encapsulated, reusable business logic created using event rules rather than C programming. Also called business function event rules. Stored in a database as a JDE object; when built, generates C code |
| **UBE (Universal Batch Engine)** | The runtime engine that processes batch applications (reports). UBE is both the engine name and the object type code for report objects |
| **Workbench** | A program providing access to a group of related programs from a single entry point for completing a large business process |
| **Smart Field** | A data dictionary item (glossary group K) with an attached business function that performs reusable calculations or lookups |
| **Level Break** | A division point in report data where the value of a designated field changes, triggering header and footer processing |
| **Subsection Join** | A parent/child link between two detail sections using different business views |
| **Drill Down** | A feature linking tabular report values to interactive applications for detailed review |
| **Report Interconnect** | A mechanism to launch one batch application from another (synchronously or asynchronously) |
| **Processing Option** | A runtime parameter that customizes how a report processes data, set through processing option templates |
| **Subsystem Job** | A continuously running batch process that monitors a data queue and processes records asynchronously |
| **Column Inclusion** | Tabular section event that determines whether a fetched record is included in cell calculations |
| **Cell Override** | Modification of data or properties at a specific column-row intersection in a tabular section |
| **Decimal Scaling** | Simplifying large numbers by dividing values by a specified factor (e.g., show in thousands) |
| **Custom Section** | A conditional section called from event rules via Do Custom Section system function |
| **Report Director** | A wizard integrated into RDA that guides developers through report template creation |
| **Dynamic Positioning** | Automatic repositioning of report objects when fonts change due to language or platform differences |
| **Font Substitution** | Automatic font replacement based on language settings or output device type |

---

*This reference was synthesized from the complete JD Edwards EnterpriseOne Tools Report Design Aid Guide (292 pages, 34 chapters). It covers report creation, the Report Director wizard, all section types (columnar, group, tabular), properties at all levels, object types, tabular-specific features (rows, cells, calculation columns, decimal scaling), appearance modification (fonts, dynamic positioning, edit codes, lines/boxes), headers/footers, level breaks, smart fields, subsection joins, drill down, database output, event rules (If/Else/While, assignments, system functions, business functions, Table I/O, custom sections), complete event reference tables, report processing flow, runtime structures, report interconnects, transaction processing, business view favorites, financial date titles, processing option templates, subsystem jobs, Report Director templates, batch error messaging, and the runtime information API.*
