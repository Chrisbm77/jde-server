# JD Edwards EnterpriseOne — Data Dictionary Reference

*Source: JD Edwards EnterpriseOne Tools — Data Dictionary Guide, Release 9.2 (Part Number E53570-03)*

---

## 1. Overview

The Data Dictionary in JD Edwards EnterpriseOne is a central repository that contains all the data items used across the system. Data dictionary items not only define and describe data, but they also trigger the runtime engine to react or process in certain ways by nature of their types. Online help, error messages, term substitutions for different industries, and translations are all tied to data dictionary items.

**Two types of data items exist:**

| Type | Description | Application | Stored in Tables? |
|---|---|---|---|
| **Regular Data Items** | Database items used in applications and reports — define fields on forms, columns in tables, fields in business views, members of data structures, and fields on reports | Data Dictionary Application (P92001) | Yes |
| **Glossary Data Items** | Used primarily as message text (errors, warnings, workflow, processing option help) — do not use all the fields required for regular data items | Data Dictionary - Glossary Items Application (P92002) | No |

**Key capabilities of Data Dictionary items:**
- Define field attributes (data type, size, decimals, description, column headings)
- Provide automatic error checking against attributes at runtime
- Supply glossary text that displays as F1 Help (Item Help / field-level help)
- Attach triggers (default values, visual assists, edit rules, display rules, next numbers, smart fields)
- Enable text substitution in messages using `&1`, `&2` placeholders
- Support jargon and alternate language terms per system code
- Enable Tips of the Day functionality

**Design Tools:**
- **Data Dictionary Application:** P92001 (regular data items)
- **Data Dictionary - Glossary Items Application:** P92002 (glossary data items)
- **Menu:** Data Dictionary Design (GH951)
- **Management Tool:** Object Management Workbench (OMW)

---

## 2. Data Dictionary Concepts

### Regular Data Items

Each regular data item is defined by attributes that describe parameters such as data type, data length, and display format. Most fields in JDE applications are regular data items. Data item attributes define how the item should appear when placed on a form or report, including the title and whether to display default values. The system performs automatic error checking against these attributes at runtime.

**Parameters that define regular data items:**

| Parameter | Overridable in FDA/RDA? |
|---|---|
| Display Decimals | No |
| File Decimals | No |
| Alpha Description | No |
| Data Type | No |
| Size | No |
| Glossary | No |
| Allow Blank Entry | Yes (*) |
| Upper Case Only | Yes (*) |
| All Triggers | Yes (*) |
| Row and Column Headings | Yes (*) |

Parameters marked with (*) can be overridden in Form Design Aid (FDA) and Report Design Aid (RDA). When overrides exist, the application retrieves the overrides instead of the data dictionary values.

**Important:** You create new data items and view existing ones with Object Management Workbench (OMW) or the Data Dictionary Application (P92001). After creating a data item, you can define jargon and language translations for it.

### Glossary Data Items

Glossary data items are items that cannot be attributes in tables. They are typically used as messages in the JDE system and do not use all the fields required for regular data items. Glossary data items use the Data Dictionary - Glossary Items Application (P92002).

> **Note:** The data dictionary does not verify whether a data item is used by an application when you delete an item. If you delete a data item that an application uses, that application will fail.

---

## 3. Glossary Text

Glossary text is used to describe regular data items or to define the text for messages and processing option help. There are two types:

- **Data item glossary text** — describes a regular data item (F1 Help)
- **Glossary item glossary text** — defines message text for errors, workflows, etc.

Both types have User Defined Code (UDC) values that categorize them into glossary groups.

### Data Item Glossary Groups (UDC H95/DG)

| Code | Description | Can Be in Tables? |
|---|---|---|
| **C** | Data Item Class | Yes |
| **D** | Primary Data Elements | Yes |
| **K** | Smart Fields | Yes |
| **S** | Secondary-Dates, Arrays, Etc. | Yes |

Only glossary groups C, D, K, and S can have columns in database tables. Group S is for data item arrays such as Address Line (ADD), which is the parent data item for AddressLine1 (ADD1) through AddressLine15 (ADD15).

### Glossary Item Glossary Groups (UDC 98/GG)

| Code | Description | Usage |
|---|---|---|
| **E** | Interactive Error/Warning/Information Messages | Display during runtime based on user actions |
| **H** | Processing Option Help Text | Used for Item Help in processing options |
| **X** | Log Messages | Log file entries about system operations |
| **Y** | PPAT Level Messages (Batch/Workflow) | Batch error messages and workflow messages in Employee Work Center |

Glossary items are usually designated as types E, H, X, or Y, although other types are available.

**Glossary Group Details:**

- **Group E** — Designates interactive error, warning, and information messages that display during runtime based on user actions
- **Group H** — Used for Item Help in processing options. The glossary item is designated as the Help Override Data Item in the processing option template (e.g., T01012 uses glossary item S0101205 for the Search Type processing option)
- **Group X** — Log file messages that provide information about system operations, events, problems, failures, and warnings
- **Group Y** — PPAT Level Messages (People, Places, and Things). Used for batch level-break messages and workflow messages that display in the Employee Work Center

### Text Substitution

Text substitution enables variable text to be inserted into glossary text at runtime, using placeholders indicated by `&` and a number:

**Example:** `"Batch &1 is out of balance by &2"` — at runtime, `&1` is replaced with the actual batch number and `&2` with the amount.

Text-substituted values are defined by data dictionary items in a data structure. The data structure is associated with the glossary item differently depending on the glossary type:

| Glossary Type | How Data Structure is Attached |
|---|---|
| **E** (Error/Warning/Info) | Attach a pre-defined data structure directly in the data dictionary |
| **Y** (Workflow/Batch) | For workflow: use the Workflow Tool to map placeholders to workflow data structure values. For batch: create a type definition of the data structure and include in a C business function |

---

## 4. Data Dictionary and Data Dictionary Item Storage

Data dictionary items reside on enterprise (logic) servers in relational database tables. Workstations retrieve from the publisher data dictionary only those data items necessary for the applications being used.

Data item retrieval occurs when you use an application for the first time after installing JDE. The data dictionary information is stored on each workstation in a permanent cache under the same local path code and spec directory as these global tables:

- **glbltbl.xdb** — references for the data
- **glbltbl.ddb** — the data items

> **Note:** See *"Administering the Data Dictionary"* in the JD Edwards EnterpriseOne Tools Runtime Administration Guide for administration details.

---

## 5. Data Dictionary Triggers

A **trigger** is an editing or display routine attached at the dictionary level and initiated at runtime. Triggers are reusable objects — they are automatically associated with each application that uses the data item. This saves development time because you create the business logic once and reuse it across multiple applications.

> **Important:** Although you can override any of these triggers in Form Design Aid (FDA), you should anticipate how the data item will most often be used to reduce the need for overrides.

### 5.1 Default Value Triggers

A **default value trigger** is the value assigned to the object based on that data item when the object is blank. It provides the initial value on the data entry screen.

**Rules:**
- The value entered must be the exact same length as the data item size
- Place single quotes around the value if it contains embedded blanks
- Keywords `*BLANKS` and `*ZEROS` can be used as default values
- Leading zeros are suppressed when redisplaying numeric data items

> **CAUTION:** If a blank entry is allowed, default values should not be used.

### 5.2 Visual Assist Triggers

A data item with an associated **visual assist trigger** displays the visual assist button at runtime. Available types:

| Visual Assist Type | Description |
|---|---|
| **Search Form** | Loads a selected search & select form to assist users in selecting values. The form must already exist and must display table values only (not UDC values). |
| **Calculator** | Provides an on-screen calculator for deriving mathematical values |
| **Calendar** | Provides an on-screen calendar for selecting dates |
| **Universal Time** | Provides an on-screen clock and calendar for selecting times and dates |

### 5.3 Edit Rule Triggers

**Edit rule triggers** validate field values based on business functions or rules. Examples:

- Validate and compare a field with a particular value
- Ensure a field value is within a specified range
- Link a field to a specific UDC search & select form
- Check for Y and N values

**Two options:**
- **Business Function** — The business function must already exist. Use Browse to locate and select it.
- **Rule** — Pre-defined edit rules from UDC H98/ER:

| Rule Code | Description |
|---|---|
| EQ | Equal |
| GE | Greater or Equal |
| GT | Greater |
| HNDL | Table Handle |
| LE | Less Than or Equal |
| LT | Less Than |
| NE | Not Equal |
| NRANGE | Not Between |
| RANGE | Between |
| UDC | User Defined Code |
| VALUE | In a List |
| ZLNGTH | Allocated Length (VARLEN fields) |

When you specify an edit rule, one or two parameter fields appear depending on the rule. For example, `RANGE` and `NRANGE` require lower and upper values.

### 5.4 Display Rule Triggers

**Display rule triggers** format the data in a field. Attach a display rule based on either a business function or a UDC.

**Pre-defined display rules (UDC H98/DR):**

| Rule Code | Description | Usage Notes |
|---|---|---|
| **\*RAB** | Right Adjust Blank Fill | Right-adjusts the value and precedes it with blanks. Used by data items that define **business units**. |
| **\*RABN** | Right Adj Blank Fill/not CCtr | Right-adjusts the value and precedes it with blanks. Used by data items that do **not** define business units. |
| **\*RAZ** | Right Adjust Zero Fill | Right-adjusts the value and precedes it with zeroes (e.g., Company appears as 00001). |
| **CODE** | Edit Code Formatting | Uses the specified edit codes to format numeric fields. See UDC 98/EC for valid codes. |
| **MASK** | Edit Mask/Word Formatting | **No longer supported.** |
| **LMASK** | Leading Mask | Embeds leading masks (`*`'s) within data in web client and UBE reports. Example: `*********1234` (mask parameter 4 = number of trailing unmasked digits). Mask can be used only with string data item types. |

### 5.5 Next Number Triggers

The **next number** trigger controls automatic numbering for items such as GL account numbers, voucher numbers, and address numbers. It specifies the numbering system code to use and automatically increments numbers.

**Key details:**
- Next numbers are assigned from an array defined in the Next Number Revisions application (P0002)
- The combination of **system code** and **index** defines how the next number is assigned
- Table **F0002** has one record per system and a 10-element array — the key is system code
- The system uses each element for a specific hard code within the applications for that system code

**Example:** System code 09 — Row 1 defines New Account ID, Row 2 contains Journal Entries.

**Check Digits (Modulus 11):**
- Optionally add a check digit to the end of each next number to prevent transposition errors
- Uses the IBM Modulus 11 Self-Check Algorithm
- Weight factors: 2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7, 2 for positions 1 to 31

> **Warning:** After you set next numbers, do not change them. Changing next numbers can affect system performance, cause duplicate numbers, and prevent position changes or new entries without program modification.

### 5.6 Smart Field Triggers

**Smart fields** are data items with attached business functions that include named mappings. They simplify the process of choosing a data item with particular functionality — end-users do not need to know which business function to use or what parameters to pass.

**Key details:**
- Smart fields are always in glossary group **K**
- Can be used in all section types in Report Design Aid (RDA)
- Example uses: derive a column heading or an object value in a tabular section
- Configuration via Form W9212A — select the business function, event, and named mapping

---

## 6. Defining a Data Item — Item Specifications Tab

Access the Data Item Specifications form (W92001C) to define or modify a regular data item.

### Forms Used to Create a Regular Data Item

| Form Name | Form ID | Navigation | Usage |
|---|---|---|---|
| Add EnterpriseOne Object to the Project | W98220C | Click Add on the OMW form | Create a regular data item (click "No" when asked Regular or Glossary) |
| Data Item Specifications | W92001C | Select Data Item on the Add EnterpriseOne Object form | Define item specs, glossary text, attach triggers |
| Smart Field Criteria | W9212A | Enter K in Glossary Group, select Smart Fields from Form menu | Configure smart field business function, event, and named mapping |

### Item Specifications Field Reference

| Field | Description | Max Length | Editable After Save? |
|---|---|---|---|
| **Data Item** | Text string identifier for the data item. Blanks and `%`, `&`, `+` are not allowed. | 32 characters | No |
| **Alias** | Alphanumeric code that identifies a unit of information. No blanks or special characters (`%`, `&`, `+`). Within the data dictionary all items are referenced by this 4-byte data name. In tables, a 2-character prefix is added to create unique DDS names. | 8 characters | No |
| **Glossary Group** | Code indicating the type of data item (UDC H95/DG). Groups C, D, K, S can be in database tables. | 1 character | — |
| **Item Parent** | For group S (Secondary-Dates, Arrays), enter the parent data item. | — | — |
| **Description** | Case-sensitive description used by the system to search for similar items. | — | Yes |
| **Product Code** | Product code from the 55-59 client reserved range. Business partners: L00-L99, M00-M99, P00-P99. | — | — |
| **Product Reporting Code** | Product code indicating where reporting data resides. | — | — |
| **Data Type** | Style/classification of data. Do not change if used in an existing application. | — | — |
| **Size** | Field size of the data item. All amount fields should be 15 bytes, 0 decimals, type P (packed). | — | — |
| **File Decimals** | Number of stored positions right of the decimal. | — | — |
| **Class** | Code defining the data item class (informational only, used to group items, e.g., QTYINV for quantity fields). | — | — |
| **Display Decimals** | Number of decimals displayed (e.g., USD = 2, JPY = 0, Cameroon Franc = 3). | — | — |
| **Control Type** | Graphical user control associated with the data item (push button, check box, etc.). Used by FDA Quick Form. | — | — |
| **Item Occurrences** | Number of array elements to create (generates child items: ABC1, ABC2, etc.). | — | — |
| **Row Description** | Identifies fields on forms and reports. Base language only unless updated. Should be < 35 characters. | 35 characters | Yes |
| **Column Title** | Text for column headings on reports/forms (1-2 lines). Should be ≤ data item size if possible. | — | Yes |
| **Upper Case Only** | Flag — if Y, user cannot enter lowercase characters. | — | — |
| **Row Security** | Flag — whether the field can be used for row security. Protected names use `$xxx` and `@xxx`. | — | — |
| **Allow Blank Entry** | Flag — whether blank values can be written to DB (overrides UDC validation, overrides mandatory entry). | — | — |
| **Auto Include** | Flag — whether this column is auto-included in all database fetches. Use only for essential trigger/security items. | — | — |
| **Do Not Total** | For numeric items — marks the item "Not to total." In reports, sets Suppress At Total property. Values: 1 = system only, 2 = AS/400 only, blank = both platforms. | — | — |

### Data Types

| Data Type | Description |
|---|---|
| **Character** | A single letter, always the size of one |
| **Date** | A date |
| **Integer** | An integer |
| **Character (Blob)** | Can be translated from EBCDIC to ASCII |
| **Binary (Blob)** | Cannot be translated, appears in machine code (e.g., Win.help executable) |
| **Binary** | Represents two choices (1/0 for on/off or true/false) |
| **String** | Always the same size or length |
| **Variable String** | Variable size |
| **JDE UTime** | Enables business processes to span time zones via Universal Coordinated Time |
| **Identifier (ID)** | Used in program logic for controls — saves a pointer via API that references the ID |
| **Numeric** | A long integer |

### Description Naming Conventions

| Field Type | Convention |
|---|---|
| Date fields | Begin with *Date* |
| Amount fields | Begin with *Amount* |
| Unit/quantity/volume fields | Begin with *Units* |
| 30-byte description fields | Begin with *Name* |
| Y/N prompting fields | Begin with *Prompt* |
| Address numbers (employee, customer, owner) | Begin with *Address Number* |

### Item Occurrences (Arrays)

Data item name length restrictions for array elements:

| Parent Name Length | Max Array Elements |
|---|---|
| 3 bytes | 1 to 9 elements |
| 2 bytes | 10 to 99 elements |
| 1 byte | 100 to 999 elements |

### Common Row Description Abbreviations

| Abbreviation | Meaning |
|---|---|
| U/M | Units of measure |
| YTD | Year-to-date |
| MTD | Month-to-date |
| PYE | Prior year end |
| QTY | Quantity |
| G/L | General ledger |
| A/P | Accounts payable |
| DEPR | Depreciation |

---

## 7. Defining a Data Item — Additional Tabs

### Item Glossary Tab

| Field | Description |
|---|---|
| **Data Item** | Created on Item Specifications — cannot be changed |
| **Alias** | Created on Item Specifications — cannot be changed |
| **Text** | Glossary text for the data item. Displays when user presses F1 on a form field. Example for AN8: *"A number that identifies an entry in the Address Book system, such as employee, applicant, participant, customer, supplier, tenant, or location."* |

### Default Value Tab

| Option | Description |
|---|---|
| **No Default Value** | No default value assigned |
| **Default Value** | Enter the default value (must match exact data item size). Use single quotes for embedded blanks. Keywords: `*BLANKS`, `*ZEROS`. |

### Visual Assist Tab

| Option | Description |
|---|---|
| **No Visual Assist** | No visual assist |
| **Calculator** | Assign calculator — use on numeric data items where users enter amounts |
| **Calendar** | Assign calendar — use on date data items |
| **Search Form** | Assign a search & select form via Browse. Example: AN8 has W0101SA (Address Book Master Search) |
| **EnterpriseOne UTime** | Coordinate workstations to Universal Coordinated Time |

### Edit Rule Tab

| Option | Description |
|---|---|
| **No Edit Rule** | No edit rule assigned |
| **Business Function** | Assign an edit rule based on a business function procedure (use Browse to select) |
| **Rule** | Assign a pre-defined edit rule from UDC H98/ER (EQ, GE, GT, HNDL, LE, LT, NE, NRANGE, RANGE, UDC, VALUE, ZLNGTH) |

### Display Rule Tab

| Option | Description |
|---|---|
| **No Display Rule** | No display rule assigned |
| **Business Function** | Assign a display rule based on a business function (use Browse to select) |
| **Rule** | Assign from UDC H98/DR: \*RAB, \*RABN, \*RAZ, CODE, LMASK, MASK (deprecated) |

### Next Number Tab

| Option | Description |
|---|---|
| **No Next Numbering** | Data item will not auto-increment |
| **Next Number** | Enable next numbering — specify System and Index fields. Numbers assigned from array in P0002. |

---

## 8. Creating a Glossary Data Item

Glossary items are created separately from regular data items because their text cannot be included in tables.

### Forms Used to Create a Glossary Data Item

| Form Name | Form ID | Navigation | Usage |
|---|---|---|---|
| Add EnterpriseOne Object to the Project | W98220C | Click Add on OMW form | Create a glossary data item (click "Yes" when asked Regular or Glossary) |
| Glossary Items | W92002B | Select Data Item on Add form, then click Yes for glossary. Or use GH951 menu: Error Messages / Workflow Messages / Processing Option Glossaries | Define specs, glossary text, data structure template |
| Glossary Text | W92002B | Click Glossary Text tab on Glossary Items form | Enter glossary text |
| Data Structure Template | W92002B | Click Data Structure Template tab on Glossary Items form | Attach data structure for text-substitution placeholders |

### Glossary Item Fields

| Field | Description |
|---|---|
| **Alias** | Up to 8 alphanumeric characters. No blanks or `%`, `&`, `+`. Cannot be changed. For error messages (type E), alias is auto-assigned if left blank — to assign your own, use 4-digit numbers > 5000. For non-database fields (group U): must begin with `#`, `$`, or `@`. For processing option help (group H): begin with `S`. For IBM message file (group J): begin with your own 3 characters (e.g., CLT0001). |
| **Glossary Group** | Type of glossary item (UDC 98/GG) |
| **Product Code** | 55-59 client reserved range. Business partners: L00-L99, M00-M99, P00-P99. |
| **Product Reporting Code** | Where reporting data resides |
| **Description** | Case-sensitive description. For group H and interactive errors, the description and message text display at runtime. For batch errors and workflow messages, the description displays as the subject in Employee Work Center (unless alternate subject text is specified). |
| **Error Level** | Severity: 1 = Error, 2 = Warning, 3 = Informative |
| **Item Glossary** | Message text. For text-substitution messages, use `&1`, `&2`, etc. for runtime-substituted values. |
| **Data Structure Template** | Required for messages with text-substitution placeholders. For all types except Y (workflow), attach via Data Structure Templates tab. Workflow messages use the Workflow Tool instead. |

> **Note:** The Data Structure Template tab is not enabled for PPAT Level Messages (glossary group Y) because those data structures are controlled by other tools (Workflow Tool for workflow messages, C business function for batch level-break messages).

---

## 9. Adding Glossary Text for Languages

For any data item, you can add glossary text for different languages (e.g., French, Spanish, German in addition to the base English language). Glossary text for languages must be added after the data item has been created.

### Steps to Add Glossary Text for Languages

1. Access Work with Data Items (W92001B via GH951)
2. Select the data item you want to change
3. From the Row menu, select **Glossary Overrides**
4. On Work With Data Item Glossary Overrides, click **Add**
5. On Data Item Glossary Header, complete:
   - **Language** — the target language
   - **Form** — (optional) enter a form name to apply the glossary to a specific form only. If left blank, the glossary applies to all forms using this item.
6. Select the row you just added
7. From the Row menu, select **Glossary**
8. Enter the glossary text

---

## 10. Jargon and Alternate Language Terms

### Understanding Vocabulary Overrides

When you create a data dictionary item, you assign descriptions to the row, column, and glossary. Because these descriptions might not offer the flexible terminology needed across different modules, you can assign alternate **jargon** or **language** descriptions to each item.

**Example:** The cost center field `MCU` has a Row Description of *"Business Unit"* (used in financial applications). In distribution applications, it appears as *"Branch/Plant"*. In warehousing applications, it appears as *"Warehouse"*.

### Override Resolution Order

The system checks for and resolves overrides in this priority order:

1. **Application-level language override** — If the user applied a language override in FDA or RDA, the system uses that term
2. **Menu selection system code** — If the menu selection has an attached system code, the system displays the alternate term for that system code
3. **Application system code** — If the application has an attached system code, the system displays that alternate term
4. **Data dictionary text** — If no overrides exist, the base data dictionary text appears

> **Important:** Language and language overrides always take precedence over non-language overrides. If a French translation exists but no French alternate term, the form displays only the main term in French (not the alternate English term).

### Defining Jargon

| Form Name | Form ID | Navigation | Usage |
|---|---|---|---|
| Work with Data Items | W92001B | GH951, Work with Data Dictionary Items | Choose a data item |
| Work with Data Item Descriptions | W92001S | Select a data item, Row menu > Descript. Overrides | Modify language jargon codes |
| Data Item Descriptions | W92001Q | Click Add on Work with Data Item Descriptions | Apply a language and jargon code |

**Jargon Code:** Enter a UDC (98/SY) value that specifies the system number for reporting and jargon purposes.

**Language:** Enter a UDC (01/LP) code for the language. A code for that language must exist at either the system level or in user preferences.

### Deploying Row and Column Changes

Changes to row and column descriptions are **not replicated** through data replication. To deploy changes to workstations, you must deliver a new full or partial package, or an update package that includes the affected applications. The package deletes the existing row and columns stored in the workstation cache.

---

## 11. Data Dictionary Compare Report

The Data Dictionary Compare report (**RD969200NA**) compares data dictionary items between two environments or data sources. Use this report as an audit or validation tool.

**Use cases:**
- **Before an upgrade:** Determine which items were added, deleted, or changed
- **After an upgrade:** Verify that modifications were carried forward to the new release

See *"Data Dictionary Compare Report"* in the JD Edwards EnterpriseOne Tools Software Updates Guide.

---

## 12. Tips of the Day

### Overview

Tips of the Day are sets of short informational text that appear each time you launch an application or access a form. Tips appear sequentially — the system records where in the tip sequence you are and displays the next tip on the next launch.

**Prerequisite:** Create a data dictionary item with glossary text for each tip.

### How It Works

Tips of the Day are the glossary texts of data dictionary items. You create one data dictionary item for each tip. Since data dictionary glossaries can be translated, tips can appear in different languages.

Tips can be associated with:
- An **application**
- A **form**
- An **application version**

### Forms Used

| Form Name | Form ID | Navigation | Usage |
|---|---|---|---|
| Work With Tips of the Day | W91500B | System Administration Tools (GH9011) > Object Management Administration > Advanced and Technical Operations > Tip of the Day | View and select tips |
| Tips of the Day Revisions | W91500C | Click Add on Work With Tips of the Day | Add tips to an object |

### Tips of the Day Revisions Fields

| Field | Description |
|---|---|
| **EnterpriseOne Tool** | The system application to which you are attaching the tip set (only when adding new) |
| **Description** | Description of the system application |
| **Force tip to all users** | Select to prevent users from disabling Tip of the Day for this tip set |
| **Tip Sequence** | The order in which tips appear |
| **Data Item** | The alias of the data dictionary item containing the tip text |

---

## 13. Data Dictionary Implementation

The following implementation steps are required before working with the Data Dictionary:

1. **Configure Object Management Workbench** — See *"Configuring JD Edwards EnterpriseOne OMW"* in the OMW Guide
2. **Configure OMW user roles and allowed actions** — See *"Configuring User Roles and Allowed Actions"*
3. **Configure OMW functions** — See *"Configuring JD Edwards EnterpriseOne OMW Functions"*
4. **Configure OMW activity rules** — See *"Configuring Activity Rules"*
5. **Configure OMW save locations** — See *"Configuring Object Save Locations"*
6. **Set up default location and printers** — See JD Edwards EnterpriseOne Tools Report Printing Administration Technologies Guide

---

## 14. Step-by-Step Procedures

### Creating a Regular Data Item

1. In OMW, select a project (or the item goes to your Default project)
2. Click **Add** on the Object Management Workbench form (W98220C)
3. Select **Data Item** as the object type
4. When prompted whether to create a regular or glossary data item, click **No** (for regular)
5. On the Data Item Specifications form (W92001C):
   - Enter the **Data Item** name (up to 32 characters)
   - Enter the **Alias** (up to 8 characters, 4-byte standard)
   - Select the **Glossary Group** (C, D, K, or S for table-eligible items)
   - Fill in General Information: Description, Product Code, Data Type, Size, Decimals, etc.
   - Enter **Row Description** and **Column Title**
   - Set flags: Upper Case Only, Row Security, Allow Blank Entry, Auto Include, Do Not Total
6. Click the **Item Glossary** tab and enter glossary text
7. Configure triggers on the remaining tabs (Default Value, Visual Assist, Edit Rule, Display Rule, Next Number) as needed
8. Click **OK** to save

### Adding Regular Data Item Glossary Text

1. Access Work With Data Items (W92001B via GH951)
2. Select the data item
3. From the Row menu, select **Glossary**
4. On the Data Item Glossary form, enter the glossary text

### Creating a Glossary Data Item

1. In OMW, select a project
2. Click **Add** on the OMW form (W98220C)
3. Select **Data Item**
4. When prompted, click **Yes** (for glossary data item)
5. On the Glossary Items form (W92002B):
   - Enter the **Alias** (or leave blank for auto-assignment for type E)
   - Select the **Glossary Group** (E, H, X, Y, etc.)
   - Enter Product Code, Description, Error Level
6. Click the **Glossary Text** tab and enter the message text
   - Use `&1`, `&2` for text-substitution placeholders
7. If the message uses text substitution:
   - Click the **Data Structure Template** tab
   - Click **Text Substitution**, then **Browse** to select the data structure template
   - (Not applicable for group Y — those use Workflow Tool or C business functions)
8. Click **OK** to save

---

## 15. XML Par File Considerations

Data dictionary items are part of the JDE specification tables and are included in packages for deployment. Key considerations:

### Package Types Affecting Data Dictionary

| Package Type | Effect on Data Dictionary |
|---|---|
| **Full Package** | Includes all data dictionary items from the source environment |
| **Partial/Update Package** | Includes only changed data dictionary items for affected applications |

### What Gets Packaged

- Data item specifications (all attributes)
- Glossary text (all languages)
- Trigger definitions (default values, visual assists, edit rules, display rules, next numbers)
- Jargon and alternate language terms
- Row and column description overrides

### Deployment Notes

- Row and column description changes are **not replicated** through data replication — they require a new package
- The package deletes existing row and column values stored in the workstation cache (glbltbl.xdb, glbltbl.ddb)
- On the HTML client, the data dictionary is stored as serialized objects with the application specification information — if data items are changed, applications must be regenerated
- On the Microsoft Windows client, applications access the data dictionary at runtime and immediately reflect modifications

### Data Dictionary Items in OMW Projects

When you add a data dictionary item to an OMW project, it follows the same lifecycle rules as other JDE objects:
- Subject to activity rules and status transitions
- Must be checked out before modification
- Must be promoted through environments following the configured transfer activity rules

---

## 16. Quick Reference Card

### Key Applications and Forms

| Application | Form ID | Purpose |
|---|---|---|
| Data Dictionary (P92001) | W92001B | Work With Data Dictionary Items |
| Data Dictionary (P92001) | W92001C | Data Item Specifications (create/edit regular items) |
| Data Dictionary - Glossary Items (P92002) | W92002B | Create/edit glossary data items |
| Next Numbers (P0002) | — | Next Number Revisions |
| Smart Field Criteria | W9212A | Configure smart fields |
| Tips of the Day | W91500B / W91500C | Manage Tips of the Day |

### Key UDC Tables

| UDC Table | Purpose |
|---|---|
| H95/DG | Data Item Glossary Groups (C, D, K, S) |
| 98/GG | Glossary Item Glossary Groups (E, H, X, Y, etc.) |
| H98/ER | Edit Rules (EQ, GE, GT, HNDL, LE, LT, NE, NRANGE, RANGE, UDC, VALUE, ZLNGTH) |
| H98/DR | Display Rules (\*RAB, \*RABN, \*RAZ, CODE, LMASK, MASK) |
| 98/EC | Edit Codes for numeric formatting |
| 98/SY | System Numbers for jargon |
| 01/LP | Language Preferences |

### Key Tables

| Table | Purpose |
|---|---|
| F0002 | Next Numbers (one record per system, 10-element array) |
| glbltbl.xdb | Local cache — data references |
| glbltbl.ddb | Local cache — data items |

### Data Item Constraints

| Constraint | Value |
|---|---|
| Data Item name max length | 32 characters |
| Alias max length | 8 characters (typically 4-byte) |
| Alias characters not allowed | Blanks, `%`, `&`, `+` |
| Row Description recommended max | 35 characters |
| Product codes for client customization | 55-59 |
| Product codes for business partners | L00-L99, M00-M99, P00-P99 |
| Amount fields standard size | 15 bytes, 0 decimals, type P (packed) |
| Error message custom alias range | > 5000 (4-digit numbers) |
| Non-database field aliases | Must begin with `#`, `$`, or `@` |

### Glossary Group Quick Reference

| Group | Name | In Tables? | Typical Use |
|---|---|---|---|
| C | Data Item Class | Yes | Classify data items |
| D | Primary Data Elements | Yes | Standard database fields |
| K | Smart Fields | Yes | Business function-attached fields |
| S | Secondary-Dates, Arrays | Yes | Array/child items |
| E | Error/Warning/Info Messages | No | Interactive runtime messages |
| H | Processing Option Help | No | Processing option Item Help |
| X | Log Messages | No | System log entries |
| Y | PPAT Level Messages | No | Batch/workflow messages |

### Trigger Types Summary

| Trigger Type | Purpose | Configuration |
|---|---|---|
| Default Value | Set initial value when field is blank | Enter value, `*BLANKS`, or `*ZEROS` |
| Visual Assist | Display assist button (search form, calculator, calendar, UTime) | Select type and configure |
| Edit Rule | Validate field input | Business function or pre-defined rule (UDC H98/ER) |
| Display Rule | Format displayed data | Business function or pre-defined rule (UDC H98/DR) |
| Next Number | Auto-increment numeric fields | Specify system code and index (from P0002/F0002) |
| Smart Field | Attach business function with named mappings | Glossary group K, configure via W9212A |

### Troubleshooting

| Symptom | Likely Cause | Resolution |
|---|---|---|
| Application fails after deleting data item | Data dictionary does not verify usage before deletion | Restore the data item; use Cross Reference to find all usages before deleting |
| Data item changes not reflected on workstation | Cached data dictionary on workstation is stale | Deploy a new full/partial/update package to refresh the cache |
| Visual assist not appearing on form | No visual assist trigger defined, or overridden in FDA | Check the Visual Assist tab in data dictionary; check FDA overrides |
| Default value not applying | Allow Blank Entry may be conflicting | Do not use default values when Allow Blank Entry is enabled |
| Text substitution not working | Data structure template not attached or placeholders mismatched | Verify data structure template is attached and `&1`, `&2` numbers match data structure items |
| Jargon override not displaying | Override resolution order — language override may take precedence | Check the 4-level resolution order: application override > menu system code > application system code > data dictionary text |
| Next numbers duplicating | Next numbers were changed after initial setup | Do not change next numbers after they are set; reset if necessary through P0002 |
| HTML client not showing DD changes | Serialized objects not regenerated | Regenerate the application specifications on the HTML client |
| Array child items not created | Parent data item name too long for the number of elements | Check name length restrictions: 3 bytes for 1-9 elements, 2 bytes for 10-99, 1 byte for 100-999 |

### Checklist: Creating a New Data Dictionary Item

- [ ] Determine whether Regular or Glossary data item
- [ ] Choose appropriate Glossary Group (C/D/K/S for regular; E/H/X/Y for glossary)
- [ ] Assign Data Item name (≤ 32 chars, no blanks/`%`/`&`/`+`)
- [ ] Assign Alias (≤ 8 chars, follow naming conventions for the type)
- [ ] Select Product Code (55-59 for client, L/M/P ranges for partners)
- [ ] Set Data Type and Size (amounts: 15 bytes, 0 decimals, type P)
- [ ] Follow description naming conventions (Date*, Amount*, Units*, Name*, Prompt*, Address Number*)
- [ ] Write Row Description (< 35 chars) and Column Title
- [ ] Write glossary text (F1 Help for regular items, message text for glossary items)
- [ ] Configure triggers: Default Value, Visual Assist, Edit Rule, Display Rule, Next Number
- [ ] For glossary items with text substitution: attach Data Structure Template
- [ ] Add language translations if needed (Glossary Overrides)
- [ ] Define jargon/alternate terms if needed (Descript. Overrides)
- [ ] Test the data item in the target application/form
