# JD Edwards EnterpriseOne — Data Structure Design Reference (DSTR Objects)

*Source: JD Edwards EnterpriseOne Tools — Data Structure Design Guide, Release 9.2 (Part Number E53555-04)*

---

## 1. Overview

Data Structure Design in Oracle JD Edwards EnterpriseOne Tools is used to create and modify data structures. Data structures are composed of data items defined in the data dictionary and are used to pass data to and from interactive and batch applications.

A data structure is a collection of data items used to pass data to other components of the same application or to another application entirely. The Oracle JD Edwards EnterpriseOne objects that use data structures are forms, reports, and business functions. Data structures pass data among objects and applications to aid in the execution of JDE applications.

**Object Type Code:** `DSTR` (Data Structure)  
**Default Object Use:** `360` (data structures; see UDC 98/FU)  
**Design Tool (Classic):** Data Structure Design (Form `W9860A`)  
**Design Tool (Web OMW, Release 9.2.7+):** Data Structure Revisions (Form `W9861AWC`)  
**Processing Option Design Aid:** Processing Option Design (Form `W9860A`)  
**Management Tool:** Object Management Workbench (OMW, Form `W98220A` / Web OMW `W98220WAC`)

---

## 2. Data Structure Categories

Data structures are either system-generated or created by the application developer.

### 2.1 System-Generated Data Structures

There are two types of system-generated data structures:

**Form Data Structures** — Each form of an interactive application contains a form data structure. This data structure is used to pass values to and from the form. You can modify the form data structure during development of the application. If you need to modify the data structure after development is complete, verify that any data items you wish to remove are not used in the form's event rules. You must redefine the affected event rules if you modify fields included in the form data structure. Form data structures are modified in Form Design Aid.

**Report Data Structures** — A report is a batch application. A batch application can receive values from a data structure or write values to a data structure. By default, the system creates an empty data structure for a batch application. You can add and delete fields for the data structure from the File menu in JD Edwards Report Design Aid.

### 2.2 User-Generated Data Structures

An application developer can create three types of data structures:

**Media Object Data Structures** — Media objects are attachments to records. They store data related to the record attached. Media objects are stored in the F00165 table. The different types of media objects available are text, image, OLE (on Windows platform), shortcut, or URL file. You must select a data structure when attaching media objects. This data structure passes data between the application and the media object table. Typically, the data items included in this data structure are the primary key fields of the record. Media object data structures are developed using Data Structure Design.

**Business Function Data Structures** — A business function requires a data structure. The data structure defines values passed in and out of the business function. Business function data structures are developed using Data Structure Design. These data structures are created using data items defined in the data dictionary. They are attached to business functions which can be called from Event Rules. All business functions require a data structure — both C business functions and named event rule business functions. The data structure provides the parameters for passing data between the business function and the interactive or batch application. Modifying an existing data structure can have a significant impact on your system. Use the Cross Reference Facility to review all applications that will be affected by modifying the data structure.

**Processing Options Data Structures** — Processing options are used to provide initial values to an interactive application or report when it is started. Processing Options can be used to customize an application or report. A processing option data structure defines data items that can be customized for the application or report. Processing option data structures are developed in Processing Option Design. Processing options can be displayed when a user launches an application or report, or they can be stored when a particular version is created.

---

## 3. Processing Options

### 3.1 Understanding Processing Options

Processing options are a set of start-up values that are provided to an interactive or batch application when it is launched. You can use processing options to change the way in which an application or a report appears or behaves. You can attach different processing option values to different versions of the same application, which enables you to change the behavior of an application without creating a new application. Additionally, you can use processing options to:

- Control the path that a user can use to navigate through a system
- Set up default values
- Customize an application for different companies or different users
- Control the format of forms and reports
- Control page breaks and totaling for reports
- Specify the default version of a related application or batch process

### 3.2 Understanding Processing Options Templates

A processing option template is a special kind of data structure. It contains one or more data dictionary items. It can also contain one or more tab pages that you can use to categorize data items.

Each tab page has a descriptive title. You can add data items on processing option templates — each data item contains a descriptive label and an edit field. You can also add comments on a tab page. A comment is a text string that is displayed on the processing option dialog. It helps users understand the data items.

At runtime, a processing option dialog displays a set of tabs. Each tab represents a category of processing options. When you click the tab header, the tab body displays the set of processing options for that category.

**Important:** Changes to processing option text can conflict with changes to processing option templates. Template changes do not take effect until another package is built, but text changes occur immediately.

### 3.3 Implementation and Storage

Processing option templates are created through Oracle's JD Edwards Processing Option Design Aid. When working with processing option design aid (PODA), all processing option template information is stored in Processing Option Text (POTEXT) Table Access Management (TAM) specifications until you check it in. When you check in the processing option template, it is moved from POTEXT TAM to the F98306 table. Data values for processing options are stored in the F983051 table. For batch versions, the Versions List table has an identifier that points to specifications for overrides (report overrides, data sequencing, data selection, or override location).

Each version of an application can be associated with a list of processing option values.

### 3.4 Creating and Implementing Processing Options — Workflow

The following steps describe how to create and implement processing options:

1. Create a processing option template
2. Attach this template to an application and create event rules so that the application uses these values
3. Create versions of the application — save different processing option values to different versions and specify the default version
4. Specify how the processing options are handled at application launch time. You can set up the menu to do one of the following:
   - The processing options dialog appears — the user can select to supply values to processing options
   - A version list appears — the user can select a version to launch
   - The system runs a particular version with the processing option values saved for that version

---

## 4. Naming Conventions

### 4.1 Processing Option Data Structure

The name of a data structure can be a maximum of 10 characters only if you begin the name with a `T` and is formatted as:

**Txxxxxyyyy**

| Position | Meaning |
|---|---|
| **T** | Prefix — Processing option data structure |
| **xxxxx** | The program number for the application or report |
| **yyyy** | Additional identifying characters (if needed) |

**Example:** The processing option data structure name for the P0101 application is `T0101`.

### 4.2 Business Function Data Structure

Business function data structures follow the standard naming conventions:

| Field | Details |
|---|---|
| **Object Name** | Unique name within the entire JDE system |
| **Product Code** | UDC 98/SY identifying the system (e.g., 01 = Address Book, 03B = Accounts Receivable, 04 = Accounts Payable, 09 = General Accounting, 11 = Multicurrency) |
| **Product System Code** | UDC 98/SY specifying the system number for reporting and jargon purposes |
| **Object Use** | Code designating use of the object — default is 360 for data structures (UDC 98/FU) |

### 4.3 Media Object Data Structure

Media object data structures follow the same naming convention as business function data structures but with Object Use defaulting to "Undefined".

### 4.4 Custom Data Structures

Product codes 55-59 are reserved for client customizations; L00-L99, M00-M99, P00-P99 for business partners.

---

## 5. Processing Option Naming Standards

JDE recommends following these naming standards for processing option templates.

### 5.1 Tab Title Guidelines

- Avoid abbreviations
- For future processing options, indicate unavailability by entering the word `FUTURE` behind the extended description for the tab. If a single processing option is unavailable, place `FUTURE` behind the data item description
- Ensure that each tab exists only one time and is not divided into multiple tabs. For example, use Process instead of Process 1, Process 2
- Include the application name (such as P4310) in the text when referencing versions to be used. The Version tab should always begin with the comment block. Enter the version to be used for each program. If left blank, `ZJDE0001` will be used
- Use application-specific tabs sparingly and only when no other categories are appropriate. To allow for increased length of text when translated, the name of an application-specific tab should be no longer than 10 characters in English
- Use one of the eight standard tab titles:
  - **Display** — Options that determine whether specific fields appear or which format of a form appears on entry
  - **Defaults** — Options that assign default values to specific fields
  - **Edits** — Options that indicate whether the system performs data validation for specific fields
  - **Process** — Options that control the process flow of the application
  - **Currency** — Options that are specific to currency
  - **Categories** — Options that assign default category codes
  - **Print** — Options that control the output of a report
  - **Versions** — Options that specify which versions the system runs of applications that are called from this application

### 5.2 Comment Guidelines

- Number every option on a tab using sequential numbering, starting at 1 for each tab
- Use nouns (such as Customer Master) to describe the processing option — the action required is defined in the glossary for that processing option
- Add the word "Required" to the end of the processing option if it is required
- Use a comment block when multiple processing options refer to the same topic — the comment block is a title for the logical group of processing options

### 5.3 Data Item Guidelines

- When necessary, change the name of the data item to be descriptive
- When renaming the data item element, the field element should comply with the naming standards for event rule variables, with the alias appended (such as `szCategoryCode3_CT03`)
- Use a relevant data item when the data dictionary glossary applies — the user can display the glossary from the processing options. Do not use generic work fields (such as `EV01`)
- When you change the name of a data item on a processing option template, you should change the member name as well. Using Hungarian Notation rules, change the member name. Leave the prefix that indicates the field type and modify the name to associate it with the description. Append an underline and the alias of the data item (e.g., `cLabels_EV01`). Do not use spaces or special characters in the member name

---

## 6. Creating Business Function Data Structures

### 6.1 Forms Used (Classic Client)

| Form Name | FormID | Navigation | Usage |
|---|---|---|---|
| Object Management Workbench | W98220A | In the Fast Path field, type `OMW` | Add and manage objects |
| Add EnterpriseOne Object to the Project | W98220C | Select a project on OMW and click Add | Select a new object to add to a project |
| Add Object | W9861AF | Select Data Structure on the Add Object form and click OK | Enter name, description, and product code. For a regular data structure, select **Regular Data Structure** |
| Data Structure Design | W9860A | Complete the Add Object form and select Regular Data Structure, then click OK | Select Design Tools tab, then click Data Structure Design button |

### 6.2 Add Object Form Fields

**Object Name** — Enter a unique name for the data structure. It needs to be unique within the entire JDE system.

**Product Code** — Enter a user-defined code (98/SY) that identifies a system. Common values: 01 (Address Book), 03B (Accounts Receivable), 04 (Accounts Payable), 09 (General Accounting), 11 (Multicurrency).

**Product System Code** — Enter a user-defined code (98/SY) that specifies the system number for reporting and jargon purposes.

**Object Use** — Enter a code that designates the use of the object. By default, data structure is 360. See UDC 98/FU.

**Regular Data Structure** — Select this option if this is a business function data structure.

### 6.3 Selecting Data Items

To select data items for business function data structures:

1. Click the **Design Tools** tab, and then click the **Data Structure Design** button
2. On the **Dictionary Items** tab, use the QBE line to locate the data dictionary items that you want to include in the business function data structure
3. To include data items in the data structure, drag them from the Dictionary Items tab to **Structure Members**. You can view detailed information about data items after they have been moved to Structure Members — click the data item and select **Data Dictionary Detail** from the toolbar
4. To remove data items from the data structure, select the data item in Structure Members and click the **Delete** button on the toolbar
5. Optionally, you can define data items as required and indicate the direction the data will flow. If the business function data structure will be used in a smart field, you must define the appropriate fields as required and set the direction arrows. Selecting an **X** in the required field indicates optional; a **check mark** indicates required
6. Optionally, you can add attachments to the data structure or to a data item:
   - Click **Data Structure Attachments** on the toolbar to add attachments to the data structure
   - Click a data item and then click **Data Structure Item Attachments** on the toolbar
7. Click **XREF** on the toolbar to launch the Cross Reference Facility from Data Structure Design. Use Cross Reference Facility when modifying existing data structures — validate all references after the change
8. When the data structure is complete, click **OK**

### 6.4 Creating a Type Definition

When the business function data structure is complete and you are ready to use it in a C business function, you need to create a type definition. A type definition is a C code representation of a data structure definition. The type definition is stored in the clipboard so that you can easily paste it into the appropriate section of the `.h` file. This process is more efficient because you do not have to type the code into the `.h` file and therefore minimizes errors.

To create a type definition:
1. Click the **Design Tools** tab
2. Click the **Create a type definition** button
3. A message on the status bar indicates that the type definition is stored in the clipboard. You can now paste it into the appropriate section of the `.h` file using the `CTRL+V` key combination

---

## 7. Creating Business Function Data Structures in Web Client (Release 9.2.7)

### 7.1 Forms Used (Web Client)

| Form Name | FormID | Navigation | Usage |
|---|---|---|---|
| Object Management Workbench - Web | W98220WAC | In the Fast Path, type `P98220W` | Add and manage objects |
| Add EnterpriseOne Object to Project | W98220WAB | On OMW-Web, select Add and select object type from General Object drop-down, then click OK | Add a new object from Web OMW |
| Add Object | W9861AWC | Click the Object Name on the Project Object tab, or select Data Structure and Select Design from More Row Actions | Launch Data Structure Design Tool on the Web |

### 7.2 Step-by-Step Procedure

1. Access the Object Management Workbench - Web form
2. Select the project to which you want to add the data structure object and click **Add**
3. In the Create EnterpriseOne Object form, select **Data Structure** from the General Object drop-down list and click **OK**
4. In the Add Object form, complete these fields:
   - **Object Name** — enter a name that identifies the data structure object
   - **Description** — enter a description for the data structure object (this is the description of a record in the Software Versions Repository file; the member description is consistent with the base member description)
   - **Product Code** — enter a user-defined code that identifies a system (use the Search icon to search for the product code)
   - **Product System Code** — enter a user-defined code that specifies the system number for reporting and jargon purposes (use the Search icon)
5. The data structure object is displayed in the **Project Objects** tab in the OMW-Web form
6. Select the object and click **Design** from the More Row Actions drop-down list
7. On the **Data Structure Revisions** form, click **Find** to search for the data items. Select the data items and then click the left-pointing arrow to move the data items to the **Structure Members** grid
8. Click **OK** to save the data structure
9. After the data structure is created, you can check in the data structure object by clicking the button in the **Object Actions** column. Alternatively, select the object and then select **Check-In/Approve/Share** from the More Row Actions drop-down list

**Note:** You can create business function data structures objects using both the Web OMW and the classic OMW.

---

## 8. Creating Processing Option Data Structures

### 8.1 Forms Used (Classic Client)

| Form Name | FormID | Navigation | Usage |
|---|---|---|---|
| Object Management Workbench | W98220A | In the Fast Path field, type `OMW` | Add and manage objects |
| Add EnterpriseOne Object to the Project | W98220C | Select a project on OMW and click Add | Select a new object to add to a project |
| Add Object | W9861AF | Select Data Structure on the Add Object form and click OK | Enter name, description, and product code. For a processing option template, select **Processing Option Template** |
| Processing Option Design | W9860A | Complete the Add Object form and select Processing Template, then click OK | Select Design Tools tab, then click Start Processing Option Design Aid button |

### 8.2 Add Object Form Fields

**Object Name** — Enter a unique name for the data structure. It needs to be unique within the entire JDE system.

**Product Code** — Enter a user-defined code (98/SY) that identifies a system.

**Product System Code** — Enter a user-defined code (98/SY) that specifies the system number for reporting and jargon purposes.

**Object Use** — Enter a code that designates the use of the object. The default value for data structure is 360 (see UDC 98/FU).

**Processing Option Template** — Select this option when creating processing option data structures.

### 8.3 Selecting Data Items for Processing Option Data Structures

1. Click the **Design Tools** tab, and then click **Start the Processing Option Design Aid**
2. Right-click the processing option tab (`<New Tab>`) and select **Current Tab Properties**
3. In the **Sort Name** and **Long Name** fields, enter a name for the processing option tab according to the recommended naming conventions. Click **OK**
4. Optionally, click the letter **A** on the toolbar and click the processing option template — this drops a Comment Text field on the template. Double-click the field and highlight the text. Enter comments to explain the options
5. On the **Data Dictionary Browser** form, use the QBE line to locate the data items you want to include on the processing option template. All data items on a single tab should be related. To add additional unrelated data items, create new tabs
6. To include data items in the processing option, drag them from the Data Dictionary Browser form to the processing option template
7. Optionally, double-click the data item description and enter descriptive text. This is necessary when you select a generic data item such as `EV01` — change the text to describe the expected values (e.g., "Enter 1 to print a single column of labels, enter 2 to print two columns of labels")
8. To remove data items from the processing option, select the data item on the processing option template and click **Cut Item** on the toolbar
9. Optionally, right-click the processing option tab and select **New Tab** — enter the Sort Name and Long Name, then add related data items
10. When all tabs and data items have been added, select **Test** from the Edit menu. This enables you to view the processing option template as it will appear to the user. If any data items are defined to include a visual assist, you will be able to access it from this test template
11. **Save** the processing option data structure. The processing option is now ready to be attached to an interactive or batch application. In the application, you must create event rules that define to the system how each processing option value should be processed

---

## 9. Creating Media Object Data Structures

### 9.1 Forms Used

| Form Name | FormID | Navigation | Usage |
|---|---|---|---|
| Object Management Workbench | W98220A | Enter `OMW` in the Fast Path field | View and manage objects in projects |
| Add EnterpriseOne Object to the Project | W98220C | From OMW, select a project and click Add | Select the type of object to add to the project |
| Add Object | W9861AF | Select Media Object Data Structure and click OK | Enter information about the media object data structure |
| Data Structure Design | W9860AL | Complete the Add Object form and click OK | Select Design Tools tab, then click Data Structure Design button to add data items |

### 9.2 Add Object Form Fields

**Object Name** — Enter a unique name for the data structure. Unique within the entire JDE system.

**Product Code** — Enter a user-defined code (98/SY) that identifies a system.

**Product System Code** — Enter a user-defined code (98/SY) that specifies the system number for reporting and jargon purposes.

**Object Use** — Enter a code that designates the use of the object. The default value is "Undefined" (see UDC 98/FU).

### 9.3 Selecting Data Items for Media Object Data Structures

1. Click the **Design Tools** tab, and then click the **Data Structure Design** button
2. On the **Dictionary Items** tab, use the QBE line to locate the data dictionary items you want to include in the media object data structure
3. To include data items, drag them from the Dictionary Items tab to **Structure Members**. You can view detailed information about data items — click the data item and select **Data Dictionary Detail** from the toolbar
4. To remove data items, select the data item in Structure Members and click the **Delete** button on the toolbar
5. Optionally, add attachments to the data structure or to a data item:
   - Click **Data Structure Attachments** on the toolbar for data structure attachments
   - Click a data item and then click **Data Structure Item Attachments** on the toolbar
6. Click **XREF** on the toolbar to launch the Cross Reference Facility from Data Structure Design. Use this when modifying existing data structures — validate all references after the change
7. When the data structure is complete, click **OK**

---

## 10. Working with Processing Options

### 10.1 Defining a Processing Options Data Structure (Template)

Access the JD Edwards Object Management Workbench form.

1. Check out the processing options data structure with which you want to work
2. Ensure that the data structure is highlighted, and then click the **Design** button in the center column
3. On Processing Option Design, click the **Design Tools** tab, and then click **Start the Processing Option Design Aid**. The Processing Options Design tool launches. The area on the left of the form displays how the processing option will look to the user
4. Locate the data items that you need for the processing options with the **Data Dictionary Browser**
5. Use one of these methods to select the data items you want to add to the processing options:
   - Double-click the item in the Data Dictionary Browser — the item appears in the left side of the form under the tab
   - Drag the item from the Data Dictionary Browser to the position where you want it in the structure members
6. Click an item to edit it. You can use the hatching around the control to reposition it. You can select text, and then delete or overwrite it. Processing Options Design automatically adjusts the size and position of data items to fit the width of the tab
7. Click the text button (**A**) to add comments
8. Choose an object in the area on the left side of the form, and select **Properties** from the View menu. Right-click a data item to view its properties and change the item name if necessary (item name should be unique). You can click the **Help Override Data Item** tab to add an alternate data dictionary name from which to get the help
9. Right-click the processing option, and then select **Properties** from the menu
10. On Data Item Properties, click the **Help Override Data Item** tab, and then complete the **Data Item Help Override Name** field. (When naming Help Override Data Items, use the naming guidelines as defined in the JD Edwards EnterpriseOne Tools Development Guidelines for Application Design Guide)
11. Click **OK**
12. To view tab properties, click the tab and select **Properties** from the View menu. On Current Tab Properties, you can enter a short and long name for the tab. Use the Help File Name field to add the name of the help file for the tab
13. To add a new tab, select **New Tab** from the File menu (you can also right-click an existing tab and select New Tab)

### 10.2 Changing a Template for Text Translation

Access the Work With PO Text Translations form (W98306A — type `P98306` in the Fast Path).

1. Complete these fields and click **Find**:
   - Template Name
   - To Language
2. Work with PO Text Translations displays processing option text for the specified template and language
3. Choose a row with the text type that you want to change and click **Select** (text types include tabs, items, and comments)
4. On PO Text Translation, enter the new text

### 10.3 Attaching a Processing Options Template

Access the Form Design Aid.

1. On JD Edwards Form Design Aid, from the File menu, select **Application Properties**
2. On the Application tab, click the **..** button under the **Processing Options Template**
3. On Select Processing Option Template, select the processing option template that you want to use and click **OK**

**Important:** If you disconnect a template from an application or connect a different template, the application might not run properly. To change the processing option template: first remove all existing versions of the application, then examine all event rules within the application to ensure that references to the old processing option items are removed, then attach the new processing option template.

### 10.4 Language Considerations for Processing Options

When you add a new processing option template for an application that is language-enabled, complete the following tasks:

1. Create the application
2. Create the processing option template for the base language
3. Add the language text

---

## 11. Implementation Steps

The following implementation steps need to be performed before working with Data Structure Design:

1. **Configure JD Edwards Object Management Workbench** — See "Configuring JD Edwards EnterpriseOne OMW" in the OMW Guide
2. **Configure OMW user roles and allowed actions** — See "Configuring User Roles and Allowed Actions" in the OMW Guide
3. **Configure OMW functions** — See "Configuring JD Edwards EnterpriseOne OMW Functions" in the OMW Guide
4. **Configure OMW activity rules** — See "Configuring Activity Rules" in the OMW Guide
5. **Configure OMW save locations** — See "Configuring Object Save Locations" in the OMW Guide
6. **Set up default location and printers** — See the JD Edwards EnterpriseOne Tools Report Printing Administration Technologies Guide

---

## 12. Key Tables and Storage

| Table / Object | Description |
|---|---|
| **F98306** | Processing option template specifications (after check-in) |
| **F983051** | Processing option data values (per version) |
| **F00165** | Media Object Storage (generic text/attachments) |
| **POTEXT TAM** | Processing option text — local TAM specification storage before check-in |
| **Versions List Table** | Contains identifier pointing to specifications for overrides (report overrides, data sequencing, data selection, override location) for batch versions |

---

## 13. Glossary of Terms

| Term | Definition |
|---|---|
| **Activity Rule** | The criteria by which an object progresses from one given point to the next in a flow |
| **Data Structure** | A collection of data items used to pass data to other components of the same application or to another application entirely. Composed of data items defined in the data dictionary |
| **Embedded Event Rule** | An event rule specific to a particular table or application (e.g., form-to-form calls, hiding a field based on a processing option value, calling a business function). Contrast with business function event rule |
| **Event Rule** | A logic statement that instructs the system to perform one or more operations based on an activity that can occur in a specific application (e.g., entering a form, exiting a field) |
| **Media Storage Object** | Files that use naming conventions Gxxx, xxxGT, or GTxxx — not organized into table format |
| **Processing Option** | A data structure that enables users to supply parameters regulating the running of a batch program or report |
| **Table Access Management (TAM)** | The JDE component that handles storage and retrieval of use-defined data — stores data dictionary definitions, application and report specifications, event rules, table definitions, business function input parameters and library information, and data structure definitions |

---

## 14. Quick Reference Card

### Data Structure Types at a Glance

| Type | Created By | Tool | Object Selection | Key Characteristic |
|---|---|---|---|---|
| Form Data Structure | System | Form Design Aid | Automatic with each form | Passes values to/from forms |
| Report Data Structure | System | Report Design Aid | Empty by default | Receives/writes batch values |
| Business Function DS | Developer | Data Structure Design (W9860A) | Select "Regular Data Structure" | Parameters for BSFN calls |
| Processing Option DS | Developer | Processing Option Design Aid | Select "Processing Option Template" | Start-up values for apps/reports |
| Media Object DS | Developer | Data Structure Design (W9860AL) | Select "Media Object Data Structure" | Primary keys for F00165 attachments |

### Common Product Codes (UDC 98/SY)

| Code | System |
|---|---|
| 01 | Address Book |
| 03B | Accounts Receivable |
| 04 | Accounts Payable |
| 09 | General Accounting |
| 11 | Multicurrency |
| 55-59 | Reserved for client customizations |
| L00-L99, M00-M99, P00-P99 | Business partners |

### Standard Processing Option Tab Names

| Tab Name | Purpose |
|---|---|
| Display | Which fields or form formats appear |
| Defaults | Default values for specific fields |
| Edits | Whether the system validates specific fields |
| Process | Process flow of the application |
| Currency | Currency-specific options |
| Categories | Default category codes |
| Print | Report output control |
| Versions | Which versions of called applications to run |

### Troubleshooting Checklist

| Issue | Possible Cause | Resolution |
|---|---|---|
| Processing option changes not taking effect | Template changes require a package build | Build and deploy a new package; text changes occur immediately |
| Application not running after template swap | Old event rules still reference removed PO items | Remove all versions, clean up event rules, then attach new template |
| Data structure modification breaks dependent apps | Cross-reference not validated | Use Cross Reference Facility (XREF toolbar button) before modifying |
| Type definition paste fails | Type definition button not clicked | Click "Create a type definition" on Design Tools tab — definition copies to clipboard |
| Processing option help not appearing | Help Override Data Item not configured | Right-click the processing option, select Properties, set the Help Override Data Item tab |
| Member names not unique | Duplicate data item names | Right-click data item, select Properties, rename to unique value following Hungarian Notation |
| Web OMW data structure design unavailable | Release older than 9.2.7 | Upgrade to Tools Release 9.2.7+ for web client data structure design support |

### Step-by-Step Checklist: Creating a Business Function Data Structure

- [ ] Check out or add a new data structure object in OMW
- [ ] Enter Object Name, Product Code, Product System Code
- [ ] Select "Regular Data Structure" option
- [ ] Open Data Structure Design from Design Tools tab
- [ ] Search and drag data items from Dictionary Items to Structure Members
- [ ] Set Required/Optional flags and direction arrows (especially for smart fields)
- [ ] Add attachments if needed (Data Structure Attachments / Item Attachments)
- [ ] Run XREF to validate cross-references (critical for modifications)
- [ ] Click OK to save
- [ ] Create type definition (for C business functions — copies to clipboard for `.h` file)
- [ ] Check in the data structure

### Step-by-Step Checklist: Creating a Processing Option Template

- [ ] Check out or add a new data structure object in OMW
- [ ] Enter Object Name (format: Txxxxxyyyy), Product Code, Product System Code
- [ ] Select "Processing Option Template" option
- [ ] Open Processing Option Design Aid from Design Tools tab
- [ ] Create tabs with descriptive names (use standard 8 tab names when possible)
- [ ] Add data items by dragging from Data Dictionary Browser
- [ ] Edit data item descriptions and member names (Hungarian Notation with alias suffix)
- [ ] Add comments to explain groups of related options
- [ ] Configure Help Override Data Items as needed
- [ ] Test the template (Edit > Test) to preview the user view
- [ ] Save and check in the processing option data structure
- [ ] Attach the template to the application via Form Design Aid (Application Properties)
- [ ] Create event rules to process each processing option value
- [ ] Create versions with different processing option values as needed
- [ ] Add language translations if the application is language-enabled (P98306)

---

*Document generated from JD Edwards EnterpriseOne Tools Data Structure Design Guide, Release 9.2*
