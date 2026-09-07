# JD Edwards EnterpriseOne — Form Design Aid Reference (APPL Objects)

*Source: JD Edwards EnterpriseOne Tools — Form Design Aid Guide, Release 9.2 (Part Number E53555-07)*

---

## 1. Overview

Form Design Aid (FDA) is the JD Edwards EnterpriseOne design-time tool used to create and modify interactive application forms. An interactive application (object type `APPL`) is composed of one or more forms — each form is the interface between a user and a database table. FDA enables developers to design forms, place controls, define form interconnections, configure transaction processing, and attach event rules to form and control events.

**Object Type Code:** `APPL` (Interactive Application)
**Design Tool:** Form Design Aid (FDA)
**Management Tool:** Object Management Workbench (OMW, Form `W98220A` / Web OMW `W98220WAC`)

### 1.1 FDA Interface Components

| Component | Description |
|---|---|
| **Main Toolbar** | Standard tools for file operations, undo/redo, and design actions |
| **Insert Controls Toolbar** | Drag-and-drop palette for placing controls onto forms |
| **Layout Toolbar** | Alignment, spacing, and sizing tools for positioning controls |
| **Tab Sequence Toolbar** | Tools for defining the tab order of controls |
| **Application Tree View** | Hierarchical view of the application's forms, events, and data structures |
| **Property Browser** | View/edit properties of the selected form or control |
| **Business View Columns Browser** | Lists available columns from the attached business view |
| **Data Dictionary Browser** | Search and attach DD items to controls |
| **Status Bar** | Displays context-sensitive information |

### 1.2 Implementation Steps

1. Create an application object in OMW
2. Launch FDA from OMW to design the application
3. Add forms (selecting the appropriate form type for each)
4. Attach a business view to each form
5. Place controls on each form and bind them to BV columns or DD items
6. Configure form properties (title, entry point, transaction processing, etc.)
7. Define form interconnections between forms
8. Write event rules for business logic
9. Check in and build the application

### 1.3 Naming Conventions

| Element | Convention | Example |
|---|---|---|
| **Application** | `Pnnnnnn` (P + product code + sequence) | `P4210` |
| **Form** | `Wnnnnnnx` (W + application number + creation sequence letter A–Z) | `W4210A` |
| **Subform** | `Snnnnnnx` (S + application number + creation sequence letter) | `S4210A` |
| **Product Codes** | 55–59 reserved for client customizations; L00–L99, M00–M99, P00–P99 for business partners | — |

---

## 2. Form Types

FDA supports the following form types. Each form type has a predefined layout and runtime behavior suited to a particular interaction pattern.

### 2.1 Standard Form Types

| Form Type | Purpose | Key Characteristics |
|---|---|---|
| **Find/Browse** | Search and display records in a grid | Grid with QBE line; read-only grid rows; typically the entry-point form |
| **Fix/Inspect** | View/edit a single record (header fields only) | No grid; used for detail editing of one record |
| **Header Detail** | Header fields + editable detail grid | Header section with filter fields; detail grid below for line-item entry |
| **Headerless Detail** | Editable grid without a header section | Update grid with QBE; used when no header context is needed |
| **Search & Select** | Select a value and return it to the calling form | Similar to Find/Browse but returns selected value via data structure |
| **Message** | Display a message or confirmation dialog | Small pop-up; configurable push button; can be used as hover form (9.2.1) |
| **Parent/Child Browse** | Browse records with a parent/child tree + grid | Combines tree control and grid sharing a single business view |
| **Power Browse** | Multi-pane form with subforms (read-only) | Uses subforms for multiple simultaneous data views |
| **Power Edit** | Multi-pane form with subforms (editable) | Like Power Browse but supports editing and transactions |
| **Wizard** | Step-by-step guided workflow | Pages implemented as subforms; progress indicator; single transaction on Finish |

### 2.2 Specialized Form Types (Release 9.2+)

| Form Type | Purpose | Key Characteristics |
|---|---|---|
| **External Form (9.2.1)** | Container for non-FDA content | Hosts ADF pages, JavaScript/JET, Composed EnterpriseOne Pages, or Soft Coding references |
| **Browse Portlet** | Portlet displayed in the portal | Read-only grid portlet with personalization support |
| **Edit Portlet** | Editable portlet displayed in the portal | Editable grid portlet with personalization; supports transaction processing |

---

## 3. Form Properties

Form-level properties control the overall behavior and appearance of a form.

| Property | Description |
|---|---|
| **Business View Name** | The BV attached to the form; determines available data columns |
| **Data Structure** | The form's data structure used for passing values via form interconnections |
| **Enable In-Your-Face-Error Display** | When enabled, error text appears directly on the form rather than only in the status bar |
| **End Form on Add** | Automatically closes the form after a successful add operation |
| **Entry Point** | Designates this form as the first form shown when the application launches |
| **Fetch on Form Business View** | Automatically fetches data into header fields on form initialization |
| **Fetch on Grid Business View** | Automatically fetches data into the grid on form initialization |
| **Form Guide** | Associates a Form Guide (guided help) with the form |
| **Form Name** | The system-assigned form identifier (e.g., W4210A) |
| **Form Type** | The type of form (Find/Browse, Fix/Inspect, etc.) |
| **Height / Width** | Dimensions of the form in pixels |
| **Mapping Links** | Data mappings for power form parent-child communication |
| **Title** | The text displayed in the form's title bar |
| **Total Controls on a Form** | Read-only count of controls placed on the form |
| **Transaction** | Transaction processing settings (enabled/disabled, include in parent) |
| **Update on Form Business View** | BV used for updating header-level data (can differ from fetch BV) |
| **Update on Grid Business View** | BV used for updating grid-level data |
| **Wallpaper / Tile Wallpaper** | Background image settings for the form |

---

## 4. Form Interconnections

Form interconnections define how forms call and communicate with each other. Data is passed between forms via form data structures.

### 4.1 Interconnection Types

| Type | Behavior |
|---|---|
| **Modal** (default) | Called form must be closed before returning to the calling form. User cannot interact with the parent form while the child is open. |
| **Modeless** | Called form opens alongside the calling form. Both forms remain interactive. Only Find/Browse forms can be called modelessly. |
| **Pop-up** (Release 9.2.1) | Called form opens as a lightweight overlay anchored to the calling control. Dismissed on click-away. |
| **Dynamic Modal** (Web Only) | Like modal but the application ID, form ID, and data structure values are determined at runtime rather than design time. Uses the Dynamic Form Interconnect system function. |

### 4.2 Creating Form Interconnections

**Modal:** In FDA, select the control that triggers the interconnection → Form menu → Form Interconnections → select the target application/form → map data structure fields.

**Modeless:** Same as modal but check the "Modeless" option. Only valid when calling a Find/Browse form.

**Pop-up (9.2.1):** Use the Show Popup system function on a Message form to display it as a hover form anchored to a static text or other control.

**Dynamic Modal:** Call the Dynamic Form Interconnect system function, passing application ID, form ID, version, and DS values as pipe-delimited strings at runtime.

### 4.3 Data Structure Mapping

When creating a form interconnection, map fields between the calling form's data structure and the called form's data structure. Fields can be mapped as:
- **Input:** Value passed from calling form to called form
- **Output:** Value returned from called form to calling form
- **Both:** Value passed in both directions

---

## 5. Form Controls

FDA provides 22 control types that can be placed on forms. Each control type has specific properties, events, and system functions.

### 5.1 Control Types Summary

| Control | Description |
|---|---|
| **Calendar** | Graphical day/week/month calendar with activity management |
| **Check Box** | Binary toggle with configurable checked/unchecked values |
| **Combo Box** | Drop-down selection list loaded from UDC, cache, or Add Item |
| **Edit** | Text entry field bound to a BV column or DD item |
| **Grid** | Tabular data display (browse or update mode) |
| **Group** | Visual container for grouping related controls; supports collapse |
| **Image** | Displays bitmap or animated GIF images |
| **Media Object** | Manages text, OLE, images, and URL attachments |
| **Parent Child** | Composite tree + grid control sharing a single BV |
| **Push Button** | Clickable button that initiates actions |
| **Radio Button** | Mutually exclusive selection within a group box |
| **Saved Query** | Displays and manages saved QBE queries |
| **Static Text** | Display-only text label; optionally clickable |
| **Subform** | Self-contained section on a power form with its own BV |
| **Subform Alias** | Reusable reference to a subform defined elsewhere |
| **Tab Control** | Container for tab pages |
| **Tab Page** | Individual page within a tab control |
| **Text Block** | Segmented text display with individual formatting per segment; supports chart rendering |
| **Text Search** | Secured Enterprise Search integration |
| **Tree** | Hierarchical tree display loaded from cache |
| **Wizard** | Multi-page guided workflow container |

### 5.2 Common Control Properties

| Property | Description |
|---|---|
| **Always Hidden** | Control is never visible at runtime |
| **Allowed in Saved Query** | Control value can be included in saved queries |
| **Automatic Scroll Horizontal/Vertical** | Enables scrolling when content exceeds control bounds |
| **Automatically Find on Entry** | Triggers automatic data fetch when the form opens |
| **Business View Name** | BV column this control is bound to (subforms) |
| **Button Type** | Push button behavior type |
| **Checked Value / Unchecked Value** | Values stored when a check box is selected/cleared |
| **Clickable** | Control responds to click events (static text, text block segments) |
| **Client Edge / Static Edge / Flat** | Border style rendering options |
| **Collapsable** | Group box or subform can be collapsed/expanded by the user |
| **Column Header One / Two** | Text displayed in grid column headers |
| **Column Order** | Position of a column in the grid |
| **Column Sort Order / Sort Direction** | Default sort configuration for grid columns |
| **Control ID** | System-assigned unique identifier for the control |
| **Data Item Information** | DD item metadata associated with the control |
| **Data Structure** | Data structure used by the control (subforms, form interconnects) |
| **Default Cursor on Add/Update Mode** | Control receives focus when the form opens in add or update mode |
| **Disabled** | Control is visible but cannot receive input |
| **Display Style** | Visual rendering mode |
| **Do Not Clear After Add** | Preserves field value after an add operation instead of clearing |
| **Editable** | Grid column allows user editing |
| **Expand All / Collapse All** | Parent child tree default expansion state |
| **Fetch on Form/Grid Businessview** | Controls automatic data fetching behavior |
| **File Name / Full File Name** | Image file reference for image controls |
| **Filter Criteria** | Comparison operator for filter fields (=, <>, >, <, >=, <=) |
| **Grid Row Count** | Number of visible rows in the grid |
| **Height / Width / Left / Top** | Position and size of the control |
| **Hide HTML Row Selector** | Hides the row selection indicator in web grids |
| **Hide in Grid** | Column exists in the BV but is not displayed |
| **Hide Query By Example** | Hides the QBE input row for this column |
| **Justification** | Text alignment (left, center, right) |
| **Key Relations** | Defines key field relationships for data integrity |
| **Lines** | Number of visible text lines in a multi-line edit |
| **Maintain Aspect Ratio** | Image preserves proportions when resized |
| **Mapping Links** | Parent-child data flow configuration for subforms |
| **Menubar Separator** | Adds a separator in the menu bar |
| **Modal Frame** | Border style for modal display |
| **Multi-Line Edit** | Edit control displays multiple lines |
| **Multiple Select** | Grid or parent child allows selecting multiple rows |
| **New Text Item on Open** | Media object opens with a new text item |
| **Node ID Column** | Identifies the column used for tree node IDs (parent child) |
| **Overrides Button** | Shows DD overrides button on the control |
| **Parent** | Identifies the parent control in a hierarchy |
| **Password** | Masks edit control input with asterisks |
| **Position of Saved Query Links** | Location of saved query links on the form |
| **Prevent Resizing** | Image cannot be resized by the user |
| **Process All Rows in Grid** | Processes every row, not just changed rows |
| **Read Only** | Control displays data but does not accept input |
| **Reclaim Whitespace** | Reclaims space when a subform or group is hidden |
| **Required Field** | Field must have a value before the form can be submitted |
| **Reusable** | Subform can be referenced by alias from other forms |
| **Show Header** | Displays the subform header bar |
| **Sortable by End User** | User can click column headers to sort |
| **Tab Stop** | Control is included in the tab sequence |
| **Tool Tip** | Hover text displayed over the control |
| **Transaction** | Transaction processing settings for subforms |
| **Update Mapping Link** | Mapping link used during update operations |
| **Update Mode** | Grid update behavior (update existing records) |
| **Visible** | Control is visible at runtime |
| **Wildcard** | Enables wildcard characters in QBE searches |
| **Wrap Text** | Long text wraps within the grid column |

---

## 6. Transaction Processing

Transaction processing (TP) ensures data integrity by grouping database operations into atomic units that follow ACID properties (Atomicity, Consistency, Isolation, Durability).

### 6.1 Core Concepts

- **Commit:** Makes all pending database changes permanent
- **Rollback:** Reverses all pending database changes back to the last commit point
- **Transaction Boundary:** The scope of operations included in a single commit/rollback unit

### 6.2 Form Types Supporting TP

Transaction processing is available on these form types: Fix/Inspect, Header Detail, Headerless Detail, Power Edit, Editable Subforms, Wizard, and Edit Portlet.

### 6.3 Transaction Processing Scenarios (A–H)

The runtime behavior depends on the TP settings of the parent and child forms when using form interconnections.

| Scenario | Parent TP | Child TP | Include in Parent | Behavior |
|---|---|---|---|---|
| **A** | Off | Off | — | No TP; each DB operation commits individually |
| **B** | Off | On | — | Child manages its own transaction; parent has no TP |
| **C** | On | Off | — | Parent manages TP; child DB ops commit individually (outside parent boundary) |
| **D** | On | On | No | Parent and child each manage their own independent transactions |
| **E** | On | On | Yes | Child's transaction is included in parent's boundary; commit/rollback happens at the parent level |
| **F** | On | On (multiple children) | Mixed | Each child's TP setting is evaluated independently |
| **G** | On | On | Yes (nested) | Grandchild included in child, child included in parent — single transaction boundary at top level |
| **H** | On | On | Yes (via BSFN) | Business function extends the parent's transaction boundary |

### 6.4 Extending Transaction Boundaries

Transaction boundaries can be extended through:
- **Form Interconnections:** Setting "Include in Parent Transaction" on the child form
- **Business Functions (BSFNs):** BSFNs called within a TP boundary participate in the same transaction
- **Table I/O:** Direct table operations within event rules participate in the current transaction

### 6.5 Events Available During TP (OK Processing)

The following events fire during OK button processing and are included in the transaction boundary:

- Post Button Clicked (OK)
- Write Grid Line - Before
- Write Grid Line - After
- Add Record to DB - Before / After
- Update Record to DB - Before / After
- Delete Record to DB - Before / After
- Post Button Clicked - Asynch
- Post Commit (fires after successful commit)

### 6.6 Subform Transaction Settings

| Setting | Behavior |
|---|---|
| **Transaction Disabled** (default) | Subform has no TP; DB operations commit individually |
| **Include in Parent Transaction** | Subform's DB operations are part of the parent's transaction boundary |
| **Subform Only Transaction** | Subform manages its own independent transaction |

---

## 7. Form Type Details — Runtime Processing

Each form type follows a specific runtime processing flow. The three main phases are: Dialog Initialization, Button Processing, and Dialog Close.

### 7.1 Find/Browse Form

**Dialog Initialization:**
1. Dialog Is Initialized
2. Post Dialog Is Initialized
3. Grid Record Is Fetched (per row)
4. Last Grid Record Has Been Read

**Find Button Processing:**
1. Button Clicked (Find)
2. Grid Record Is Fetched (per row)
3. Last Grid Record Has Been Read

**Select/Close:**
1. Button Clicked (Select/Close)
2. Post Button Clicked
3. Dialog Is Closed

**Events List:** Dialog Is Initialized, Post Dialog Is Initialized, Button Clicked, Post Button Clicked, Grid Record Is Fetched, Last Grid Record Has Been Read, Row Is Selected, Row Is Exited, Row Exit & Changed, Set Focus On Grid, Kill Focus On Grid, Column Selection Changed, Double Click On Row Header, Visual Assist Button Clicked, Post Visual Assist Clicked, Dialog Is Closed, Control Is Exited, Grid Column Clicked

### 7.2 Fix/Inspect Form

**Dialog Initialization:**
1. Dialog Is Initialized
2. Post Dialog Is Initialized

**OK Button Processing:**
1. Button Clicked (OK)
2. Add/Update/Delete Record to DB - Before
3. Add/Update/Delete Record to DB - After
4. Post Button Clicked
5. Post Button Clicked - Asynch (if TP enabled)

**Events List:** Dialog Is Initialized, Post Dialog Is Initialized, Button Clicked, Post Button Clicked, Post Button Clicked - Asynch, Add Record to DB - Before/After, Update Record to DB - Before/After, Delete Record to DB - Before/After, Control Is Exited, Dialog Is Closed, Post Commit

### 7.3 Header Detail Form

**Dialog Initialization:**
1. Dialog Is Initialized
2. Post Dialog Is Initialized
3. Grid Record Is Fetched (per row)
4. Last Grid Record Has Been Read

**OK Button Processing:**
1. Button Clicked (OK)
2. Add/Update/Delete Record to DB - Before/After (header)
3. Write Grid Line - Before/After (per changed row)
4. Add/Update/Delete Grid Record to DB - Before/After (per changed row)
5. Post Button Clicked
6. Post Button Clicked - Asynch

**Events List:** All Fix/Inspect events plus: Grid Record Is Fetched, Last Grid Record Has Been Read, Write Grid Line - Before/After, Add/Update/Delete Grid Record to DB - Before/After, Row Is Selected, Row Is Exited, Row Exit & Changed, Set Focus On Grid, Kill Focus On Grid, Get Custom Grid Row, Column Selection Changed, Post Commit

### 7.4 Headerless Detail Form

Same runtime flow as Header Detail but without header-level database operations. All data operations occur at the grid level.

### 7.5 Search & Select Form

Same runtime flow as Find/Browse. The Select button returns the selected row's data to the calling form via the data structure.

### 7.6 Message Form

**Dialog Initialization:**
1. Dialog Is Initialized
2. Post Dialog Is Initialized

**Button Processing:** Button Clicked → Post Button Clicked → Dialog Is Closed

**Hover Form (9.2.1):** Message forms can be displayed as hover pop-ups using the Show Popup system function, anchored to a static text or other clickable control.

### 7.7 Power Browse / Power Edit Forms

Power forms use subforms to display multiple data views simultaneously. Each subform has its own business view and can communicate with other subforms through the parent-child hierarchy.

**Hierarchy Rules:**
- Up to 3 hierarchical levels of subforms
- Communication is parent-to-child or child-to-parent only (no sibling communication)
- Data flows through Mapping Links

**Subform Initialization:** Subforms initialize top-down (parent first, then children). Each subform fires its own Dialog Is Initialized and Post Dialog Is Initialized events.

### 7.8 Wizard Form

**Initialization:**
1. Wizard Is Initialized
2. Post Wizard Is Initialized
3. First page subform initialization (WIZARD:Subform is Initialized, WIZARD:Subform is Entered, WIZARD:Post Subform is Entered)

**Page Navigation (Next/Previous/Jump):**
1. WIZARD:Validate Subform (current page)
2. WIZARD:Subform is Exited (current page)
3. Page is Exited - Before / After
4. WIZARD:Subform is Initialized (target page, if first visit)
5. WIZARD:Subform is Entered / Post Subform is Entered (target page)

**Finish Button:**
1. WIZARD:Validate Subform (current page)
2. Transaction boundary initiates
3. Saves all pages to BV
4. Post Button Clicked fires per Save button
5. Post Button Async
6. Wizard is Finished - Before
7. Wizard is Finished - After
8. Commit or rollback

**Cancel:** WIZARD:Subform is Exited → Wizard is Exited (no commit)

---

## 8. Chart Control

The Chart control renders data visualizations within forms using Data XML and Graph XML templates.

### 8.1 Supported Chart Types

| Chart Type | Template |
|---|---|
| Bar | `bar_basic.xml` |
| Combo (bar + line) | `combo_basic.xml` |
| Line | `line_basic.xml` |
| Pie | `pie_basic.xml`, `pie_ontime.xml` |
| Stacked Bar | `stacked_bar_basic.xml`, `stacked_bar_ontime.xml` |

### 8.2 Chart XML Structure

Charts require two XML inputs:

**Data XML** — Defines the data series and values:
```xml
<graphData>
  <series id="0" name="Series Name">
    <value id="0" name="Label">100</value>
    <value id="1" name="Label">200</value>
  </series>
</graphData>
```

**Graph XML** — Defines the chart appearance and formatting. Based on predefined templates that control colors, labels, legends, axes, and rendering options.

### 8.3 Chart System Functions

- **Create Chart** — Initializes a chart control with data
- **Refresh Chart** — Updates chart data without re-creating
- **Set Chart Property** — Modifies chart appearance properties

### 8.4 Chart C Code Functions

For advanced chart manipulation, C business functions can call chart APIs to programmatically build Data XML and Graph XML strings for complex data scenarios.

---

## 9. Calendar Controls

The Calendar control provides a graphical day/week/month view for managing time-based activities.

### 9.1 Calendar Views

- **Day View** — Hourly time slots for a single day
- **Week View** — Seven-day layout with time slots
- **Month View** — Monthly grid showing activities per day

View visibility is controlled by the Calendar Day/Week/Month View Visible control properties.

### 9.2 Calendar Events

| Event | Fires When |
|---|---|
| **Load Calendar Activity** | Runtime needs to populate an activity on the calendar |
| **Calendar Activity Is Selected** | User clicks an existing activity |
| **Calendar Activity Is Added** | User creates a new activity via the calendar UI |
| **Calendar New Time Is Selected** | User clicks an empty time slot |

### 9.3 Calendar System Functions

| System Function | Description |
|---|---|
| **Add Calendar Activity** | Adds an activity to the calendar display. Parameters: Calendar FC, Activity ID, Start Date/Time, End Date/Time, Subject, Location, Description, Color, All Day flag |
| **Modify Calendar Activity** | Updates an existing activity's properties |
| **Delete Calendar Activity** | Removes an activity from the calendar |
| **Select Calendar View** | Switches between day/week/month views. Parameters: Calendar FC, View (Day/Week/Month), Date |
| **Set View Visible** | Shows or hides a specific view (day/week/month) |
| **Set Add Button Text** | Changes the text on the calendar's Add button |
| **Set Add Button Visible** | Shows or hides the Add button |
| **Set Work Day Hours** | Defines the start and end hours for the working day display |
| **Set Work Week** | Defines which days constitute the work week |
| **Set Day Type** | Assigns a day type (working, non-working, holiday) to specific dates |

### 9.4 Universal Time Support

Calendar controls support Universal Time (UT) for multi-timezone environments. System variables `SL_StartTime` and `SL_EndTime` provide UTC timestamps, and `SL_CalendarActivityID` identifies the current activity.

---

## 10. Check Box Controls

Check boxes provide binary toggle fields with configurable checked and unchecked values.

### 10.1 Key Properties

| Property | Description |
|---|---|
| **Checked Value** | The value stored when the check box is selected (e.g., "Y", "1") |
| **Unchecked Value** | The value stored when the check box is cleared (e.g., "N", "0") |

### 10.2 Events

- **Selection Changed** — Fires when the user toggles the check box state

---

## 11. Combo Box Controls

Combo boxes provide drop-down selection lists. Values can be loaded from three sources.

### 11.1 Loading Methods

| Method | Description |
|---|---|
| **UDC (User Defined Code)** | Automatically loaded from the DD item's UDC table reference. Most common method. |
| **Cache** | Loaded programmatically using the Load from Cache system function. Developer populates a cache business view, then loads it. |
| **Add Item** | Individual items added programmatically using the Add Item system function at runtime. |

### 11.2 Design-Time Considerations

- The default first entry is "-- Select One --" (blank value)
- UDC-based combo boxes translate descriptions automatically based on user language preferences
- Values without descriptions can be entered by mapping the DD item to the combo box without a UDC reference
- Setting the Required Field property forces the user to select a non-blank value
- Static text controls can be visually connected to combo boxes for labeling

### 11.3 Combo Box Events

- **Selection Changed** — Fires when the user selects a different item

### 11.4 Form-Level System Functions

| System Function | Description |
|---|---|
| **Add Item** | Adds an entry to the combo box list |
| **Clear Selection** | Removes the current selection |
| **Delete All Items** | Removes all entries from the list |
| **Delete Item** | Removes a specific entry |
| **Get Selected Item** | Returns the currently selected value |
| **Load from Cache** | Populates the list from a cache business view |
| **Select Item** | Programmatically selects an entry |
| **Set Item Data** | Associates data with a list entry |

### 11.5 Embedded-in-Grid System Functions

When a combo box is embedded in a grid column, these additional system functions are available: Add Item, Clear Selection, Delete All Items, Delete Item, Get Selected Item, Load from Cache, Select Item, Set Item Data — each operating on the combo box within a specific grid row context.

---

## 12. Edit Controls

Edit controls are the primary data entry fields on forms. They can be bound to business view database columns or standalone data dictionary items.

### 12.1 Field Types

| Type | Description |
|---|---|
| **Database Field** | Bound to a BV column; participates in fetch/update operations |
| **DD Field** | Bound to a DD item only; used for calculated values, filters, or transient data |
| **Filter Field** | DD field with a Filter Criteria property set; used in QBE-like filtering |

### 12.2 Filter Field Comparison Types

| Comparison | Operator |
|---|---|
| Equal To | `=` |
| Not Equal To | `<>` |
| Greater Than | `>` |
| Less Than | `<` |
| Greater Than or Equal To | `>=` |
| Less Than or Equal To | `<=` |

### 12.3 Type Ahead Feature

Edit controls support type-ahead functionality — as the user types, the system suggests matching values from the associated UDC or data source, enabling faster data entry.

### 12.4 Edit Control Events

- **Control Is Exited** — Fires when the user tabs out or clicks away from the control

### 12.5 Edit Control System Functions

| System Function | Description |
|---|---|
| **Set Edit Control Color** | Changes the background color of the edit control |
| **Set Edit Control Font** | Changes the font of the edit control text |

---

## 13. Grid Controls

Grid controls display tabular data in rows and columns. Grids are the most feature-rich controls in FDA.

### 13.1 Grid Modes

| Mode | Description |
|---|---|
| **Browse Grid** | Read-only display; used on Find/Browse and Search & Select forms |
| **Update Grid** | Editable rows; used on Header Detail, Headerless Detail, Power Edit forms |

### 13.2 QBE (Query By Example)

The QBE line appears at the top of the grid and allows users to enter filter criteria per column. QBE behavior is controlled by column-level properties (Hide QBE, Wildcard, Filter Criteria) and can be manipulated via system functions.

### 13.3 Design-Time Grid Settings

| Setting | Description |
|---|---|
| **Automatically Find on Entry** | Grid fetches data when the form opens |
| **Fetch on Grid Business View** | BV used for populating the grid |
| **Update on Grid Business View** | BV used for writing grid changes to the database |
| **Grid Row Count** | Number of visible rows |
| **Process All Rows in Grid** | Processes every row on OK, not just changed rows |
| **Display Customized Grid** | Enables user grid customization |
| **No Adds On Update Grid** | Prevents new row entry on an update grid |
| **Multiple Select** | Allows selecting multiple rows simultaneously |
| **Disable Page-at-a-Time Process** | Loads all rows at once instead of page-at-a-time |
| **Alternate Grid Row Format** | Enables alternating row colors/styles |
| **Support Multiple Currencies** | Enables multi-currency display per grid row |

### 13.4 Grid Column Features

- **Icon Display:** Use Set Grid Cell Icon / Set Grid Cell Icon Visibility to display icons in grid cells based on data values, configured through Named Event Rules (NERs)
- **Multiple Currency Support:** Grid columns bound to currency fields can display amounts in different currencies per row
- **Aggregation:** Grid columns can display sum, count, average, min, or max values
- **Sortable by End User:** Column headers become clickable for user-driven sorting
- **Wrap Text:** Long text wraps within the column cell

### 13.5 Grid Events

| Event | Description |
|---|---|
| **Grid Record Is Fetched** | Fires for each row retrieved from the database |
| **Last Grid Record Has Been Read** | Fires after the last row is fetched |
| **Row Is Selected** | User clicks/selects a grid row |
| **Row Is Exited** | User leaves a grid row |
| **Row Exit & Changed - Inline** | User leaves a row that was modified (synchronous) |
| **Row Is Exited & Changed - Asynch** | User leaves a row that was modified (asynchronous) |
| **Write Grid Line - Before** | Fires before a changed row is written to the database |
| **Write Grid Line - After** | Fires after a changed row is written to the database |
| **Add Grid Record to DB - Before/After** | Fires before/after a new row is inserted |
| **Update Grid Record to DB - Before/After** | Fires before/after an existing row is updated |
| **Delete Grid Record to DB - Before/After** | Fires before/after a row is deleted |
| **Set Focus On Grid** | Grid receives input focus |
| **Kill Focus On Grid** | Grid loses input focus |
| **Column Selection Changed** | User changes which column is focused |
| **Grid Column Clicked** | User clicks a column header |
| **Double Click On Row Header** | User double-clicks a row header |
| **Visual Assist Button Clicked** | User clicks a visual assist (magnifying glass) in a grid cell |
| **Post Visual Assist Clicked** | Fires after visual assist processing completes |
| **Get Custom Grid Row** | Fires during custom page-at-a-time fetch processing |
| **Grid Cell Display Changed** | A grid cell's display value changes |
| **Add Last Entry Row to Grid** | Last empty entry row processing |
| **Post Commit** | Fires after a successful database commit |

### 13.6 Custom Fetch (Page-at-a-Time Processing)

For grids with page-at-a-time processing, the Get Custom Grid Row event fires when the grid needs more data. Use Continue Custom Data Fetch system function to signal the runtime to add the current row and request the next one.

### 13.7 Interactivity Levels

| Level | Behavior |
|---|---|
| **Low** | Minimal client-side interaction; each action round-trips to the server |
| **High** | Enhanced client-side processing; reduces server round-trips |
| **Windows** | Full Windows-client interactivity (legacy) |

### 13.8 Grid System Functions — Complete Reference

#### Appearance and Display

| System Function | Description |
|---|---|
| **Set Grid Color** | Sets background/foreground color on a cell, row, column, or entire grid. Parameters: Grid FC, Row, Column, Color |
| **Set Grid Font** | Sets font properties on a cell, row, column, or entire grid. Parameters: Grid FC, Row, Column, Font |
| **Set Grid Column Heading** | Changes the text of a column header. Parameters: Grid FC, Column, Text |
| **Set Grid Row Bitmap** | Assigns a system bitmap icon (checkbox, X mark, etc.) to a row header. Parameters: Grid FC, Row, Bitmap |
| **Set Grid Row Format** | Applies an alternate format string to specific rows |
| **Set Grid Cell Icon** | Displays an icon in a specific grid cell |
| **Set Grid Cell Icon Visibility** | Controls whether a cell icon is visible |

#### Selection and Navigation

| System Function | Description |
|---|---|
| **Change Row Selection** | Programmatically selects or deselects a grid row |
| **Get Next Selected Row** | Returns the next selected row in a multi-select grid |
| **Get Selected Grid Row Count** | Returns the number of currently selected rows |
| **Get Selected Grid Row Number** | Returns the row number of the current selection |
| **Clear Selection** | Removes all programmatic row selections |
| **Set Selection** | Sets the WHERE clause filter for data selection. Parameters: Grid FC, Column, Value, Comparison. Generates SQL: `WHERE column comparison value`. Multiple calls with Set Selection Append Flag build compound WHERE clauses with AND/OR logic |
| **Set Selection Append Flag** | Controls whether the next Set Selection call appends (AND/OR) or replaces. Values: AND flag, OR flag, Group Begin/End for parenthetical grouping |
| **Set Lower Limit** | Sets the WHERE clause for ragged hierarchy queries |

#### Sequencing and Filtering

| System Function | Description |
|---|---|
| **Set Sequencing** | Defines the ORDER BY clause for grid data. Parameters: Grid FC, Column, Direction (Ascending/Descending), Priority |
| **Clear Sequencing** | Removes all programmatic sequencing |
| **Set QBE Column Compare Style** | Sets the comparison operator for a QBE column (Equal To, Not Equal To, Greater Than, Less Than, Greater Than or Equal To, Less Than or Equal To) |
| **Clear QBE Column** | Clears the QBE value for a specific column |

#### Grid Buffer Operations

| System Function | Description |
|---|---|
| **Clear Grid Buffer** | Empties the grid buffer (GB) |
| **Copy Grid Row to Grid Buffer** | Copies a grid row's data into the GB for manipulation |
| **Insert Grid Buffer Row** | Inserts a row from the GB into the grid. Parameters: Grid FC, Row position (After Current Row / After Last Row), Selectable?, Protected?, Updateable?, Deleteable?, Clear After? |
| **Update Grid Buffer Row** | Updates an existing grid row with GB data. Parameters: Grid FC, Row, Selectable?, Protected?, Updateable?, Deleteable?, Clear After? |
| **Get Grid Row** | Copies a specific grid row into the GB. Parameters: Grid FC, Row Number |
| **Delete Grid Row** | Removes a row from the grid display |

#### Grid Information

| System Function | Description |
|---|---|
| **Get Max Grid Rows** | Returns the total number of rows currently in the grid |
| **Was Grid Cell Value Entered** | Returns 1 if a specific cell was changed since last checked; 0 otherwise |
| **Disable Grid / Enable Grid** | Prevents/allows user interaction with the entire grid |

#### Visibility

| System Function | Description |
|---|---|
| **Hide Grid Column / Show Grid Column** | Hides or shows a specific column |
| **Hide Grid Row / Show Grid Row** | Hides or shows a specific row |
| **Suppress Grid Line** | Prevents a row from being written to the grid (used on Write Grid Line Before event) |

#### Export/Import Options

| System Function | Description |
|---|---|
| **Display Customize Grid Option** | Shows/hides the grid customization menu option |
| **Display Export to Excel Option** | Shows/hides the Export to Excel menu option |
| **Display Export to Word Option** | Shows/hides the Export to Word menu option |
| **Display Import from Excel Option** | Shows/hides the Import from Excel menu option |

#### Data Dictionary Overrides

| System Function | Description |
|---|---|
| **Set Data Dictionary Item** | Replaces the DD item for a grid column at runtime |
| **Set Data Dictionary Overrides** | Applies specific DD overrides (edit rules, display rules, etc.) to a column |

---

## 14. Hot Keys

FDA supports both system-defined and application-defined hot keys.

### 14.1 System-Defined Push Button Hot Keys

Pre-assigned keyboard shortcuts for standard form buttons (OK, Cancel, Find, Select, Delete, etc.).

### 14.2 System-Defined Toolbar Button Hot Keys

Pre-assigned keyboard shortcuts for standard toolbar actions.

### 14.3 Application-Defined Hot Keys

Ten key combinations are reserved for application use:

| Hot Key | Available |
|---|---|
| CTRL+SHIFT+B | Yes |
| CTRL+SHIFT+D | Yes |
| CTRL+SHIFT+L | Yes |
| CTRL+SHIFT+M | Yes |
| CTRL+SHIFT+N | Yes |
| CTRL+SHIFT+P | Yes |
| CTRL+SHIFT+Q | Yes |
| CTRL+SHIFT+U | Yes |
| CTRL+SHIFT+X | Yes |
| CTRL+SHIFT+Y | Yes |

To assign a hot key to a push button, include an ampersand (`&`) before the desired letter in the button's Title property.

---

## 15. Image Controls

Image controls display bitmap (`.bmp`) or animated GIF (`.gif`) images on forms.

### 15.1 Key Properties

| Property | Description |
|---|---|
| **File Name** | The image file to display |
| **Clickable** | When enabled, the image responds to click events |
| **Maintain Aspect Ratio** | Preserves the image's proportions when the control is resized |
| **Prevent Resizing** | Prevents the user from resizing the image |
| **Tool Tip** | Hover text displayed over the image |

### 15.2 Events

- **Button Clicked** — The only event; fires when the user clicks a clickable image

---

## 16. Media Object Controls

Media object controls manage attachments associated with database records. Attachments are stored in the F00165 table.

### 16.1 Attachment Types

| Type | Description |
|---|---|
| **Text** | Rich text or plain text content |
| **OLE** | Object Linking and Embedding objects (Windows only) |
| **Images** | Image file attachments |
| **URLs** | Web links associated with the record |

### 16.2 Control Properties

| Property | Description |
|---|---|
| **Allow Text Items** | Enables text attachments |
| **Allow OLE Items** | Enables OLE attachments |
| **Allow Image Items** | Enables image attachments |
| **Allow RTF Text** | Enables rich text formatting for text items |
| **New Text Item on Open** | Opens with a new blank text item |

### 16.3 Media Object System Functions

| System Function | Description |
|---|---|
| **Access Media Object** | Opens the media object viewer for the current record |
| **Manage Media Object** | Opens the media object manager |
| **Activate Item** | Activates (opens) a specific media object item |
| **Insert Text** | Inserts a text attachment programmatically |
| **Insert OLE Object** | Inserts an OLE object attachment |
| **Insert URL** | Inserts a URL attachment |
| **Delete Item** | Removes a media object item |
| **Get OLE Item** | Retrieves an OLE object |
| **Clear Characterization Cache** | Clears the characterization cache for the control |
| **Disable Characterization Cache** | Disables characterization caching |
| **Set Characterization Cache** | Configures characterization cache settings |
| **Hide Viewer Icon Panel** | Hides the icon panel in the media object viewer |
| **Set Cursor Position** | Sets the cursor position within a text attachment |
| **Set Grid Text Indicator** | Displays a paperclip icon in a grid column to indicate that a record has media object attachments |
| **Set Text Color** | Changes the color of text in a text attachment |

---

## 17. Parent Child Controls

The Parent Child control is a composite control combining a tree and a grid that share a single business view.

### 17.1 Key Properties

| Property | Description |
|---|---|
| **Multiple Select** | Allows selecting multiple rows/nodes |
| **Disable Drag and Drop** | Prevents drag-and-drop operations |
| **Location Indicator** | Shows position indicators during drag operations |
| **Expand All / Collapse All** | Default tree expansion state |
| **Indent and Outdent** | Enables horizontal node repositioning |
| **Move Up and Down** | Enables vertical node repositioning |
| **Node ID Column** | Column used as unique node identifier |
| **Product Synch Mode** | Enables lean manufacturing (PSYNC) mode |
| **Disable Page-at-a-Time Process** | Loads all data instead of page-at-a-time |

### 17.2 Node ID Column

When a Node ID column is specified, each tree node is uniquely identified by its node ID value. This enables system functions like Insert Grid Buffer Row By Node ID, Get Node ID, Get Related Node ID, and Set Root Node ID to work with specific nodes by their identifiers.

### 17.3 Parent Child Events

| Event | Description |
|---|---|
| **Tree Node Selection Changed** | User selects a different tree node |
| **Tree Node Is Expanding** | A tree node is about to expand |
| **Tree Node Is Collapsing** | A tree node is about to collapse |
| **Tree - Begin Drag/Cut/Copy** | User initiates a drag, cut, or copy operation |
| **Tree - End Drag Drop/Paste** | Drag-drop or paste operation completes |
| **Tree - Cancel Drag Drop/Paste** | Drag-drop or paste operation is cancelled |
| **Tree Node Bitmap Is Clicked** | User clicks a clickable bitmap on a tree node |
| **Node Is Moved Up / Down** | User moves a node vertically |
| **Node Move Up/Down Verify Before** | Fires before a vertical move for validation |
| **Tree Node Is Indented / Outdented** | User moves a node horizontally |
| **Node Indent/Outdent Verify Before** | Fires before a horizontal move for validation |
| **Grid Record Is Fetched** | Fires for each row retrieved |
| **Write Grid Line - Before/After** | Fires before/after row changes are saved |
| **All standard grid events** | Row selection, focus, DB operation events, etc. |

### 17.4 Parent Child System Functions

| System Function | Description |
|---|---|
| **Add Action** | Adds a context menu action in PSYNC mode |
| **Delete All Actions** | Removes all context menu actions |
| **Get Selected Context Action** | Returns the user's selected context action |
| **Set Action** | Enables/disables a specific context action |
| **Attach Path To Segment** | Attaches a path segment to a tree node |
| **Change Row Selection** | Programmatically selects/deselects a row |
| **Clear Grid Buffer / Cell Error / QBE Column** | Clearing operations (same as grid) |
| **Contract Tree Node / Expand Tree Node** | Programmatically collapses/expands a node |
| **Copy Grid Row To Grid Buffer** | Copies row data to the grid buffer |
| **Delete All Tree Nodes** | Removes all nodes from the tree |
| **Delete Grid Row / Disable Grid Row / Enable Grid Row** | Row-level operations |
| **Get Grid Row / Get Max Grid Rows** | Row retrieval and count |
| **Get Next Selected Row / Get Selected Grid Row Count/Number** | Selection information |
| **Get Node ID / Get Node Level** | Returns the ID or hierarchical level of a node |
| **Get Related Node ID** | Returns the ID of a related node (parent, first child, next sibling, previous sibling) |
| **Get Row Number** | Returns the row number of the selected row |
| **Get Tree Node Handle / Set Tree Node Handle** | Gets/sets the internal handle of a tree node |
| **Hide Grid Column / Show Grid Column** | Column visibility |
| **Insert Grid Buffer Row** | Inserts a GB row; supports position parameters including Under Currently Expanding Node, Under Drop Node |
| **Insert Grid Buffer Row By Node ID** | Inserts a GB row relative to a specified node (First Child, Last Child, Next Sibling, Previous Sibling); includes Insert Mode (Insert/Update) parameter |
| **Set Data Dictionary Item / Overrides** | DD item and override management |
| **Set Drag Cursor** | Assigns cursor image during drag operations |
| **Set Grid Cell Error / Color / Font / Column Heading / Row Bitmap** | Visual formatting |
| **Set QBE Column Compare Style** | Sets QBE comparison operator |
| **Set Tree Bitmap Scheme** | Assigns bitmaps for open/closed/leaf node states |
| **Set Tree Node Bitmap / Clickable Bitmap / Bold** | Individual node visual formatting |
| **Set Tree Root Node ID** | Assigns a node ID to the hidden root node |
| **Show N Levels** | Expands/collapses tree to a uniform depth |
| **Suppress Fetch On Node Expand** | Prevents automatic data fetch when expanding |
| **Suppress Grid Line** | Prevents a row from appearing in the grid |
| **Suppress Node Indent/Outdent** | Prevents horizontal node movement |
| **Suppress Node Move Up/Down** | Prevents vertical node movement |
| **Update Grid Buffer Row** | Updates an existing row from the GB |
| **Was Grid Cell Value Entered** | Checks if a cell was modified |

---

## 18. Push Button Controls

Push buttons initiate actions. A single button can be designated as the Default Pushbutton (activated on Enter key press). Subforms and message forms use push buttons instead of toolbar actions.

### 18.1 Push Button Events

| Event | Description |
|---|---|
| **Button Clicked** | Fires when the user clicks the button |
| **Post Button Clicked** | Fires after Button Clicked processing completes |
| **Post Button Clicked - Asynch** | Fires only for OK buttons, after Post Button Clicked, within the TP boundary |

### 18.2 Behavior

Button Clicked and Post Button Clicked always fire in sequence. Post Button Clicked - Asynch fires only for OK buttons and only when transaction processing is enabled.

---

## 19. Radio Button Controls

Radio buttons provide mutually exclusive selections. Enclose a set of radio buttons in a Group Box control to make them function as a single selection unit.

### 19.1 Key Properties

| Property | Description |
|---|---|
| **Value** | The value stored when this radio button is selected |
| **Filter Criteria** | Comparison operator when used as a filter |

### 19.2 Events

- **Selection Changed** — Fires when the user selects a different radio button in the group

---

## 20. Static Text Controls

Static text controls display read-only text labels on forms.

### 20.1 Key Properties

| Property | Description |
|---|---|
| **Clickable** | When enabled, the text responds to click events |

### 20.2 Events

- **Text Clicked** — Fires when the user clicks a clickable static text control

### 20.3 System Functions

- **Set Control Text** — Changes the display text at runtime

---

## 21. Subforms and Subform Aliases

Subforms are self-contained controls designed for use on power forms. They have their own business view, grid, filter fields, and event rules.

### 21.1 Subform Types

| Type | Description |
|---|---|
| **Embedded Subform** | Defined directly on the power form; cannot be reused |
| **Reusable Subform (Alias)** | Defined as a standalone subform and referenced by alias on one or more power forms |

### 21.2 Subform Characteristics

- Each subform has its own business view (independent from the parent form)
- Subforms can contain grids, edit controls, check boxes, combo boxes, and other controls
- Subforms can be used as tab pages within a tab control
- Subforms do not have toolbars or scroll bars
- Action buttons available: Cancel, OK, Save, Delete, Find, Select, Clear

### 21.3 Parent-Child Communication

**Mapping Links:** Define data flow between parent and child subforms. The "Link To" field specifies the target control or SI variable in the parent. Values flow from parent to child on initialization and from child to parent on update.

**Notify Parent / Notify Child System Functions:** Send explicit notifications between parent and child subforms. The receiving subform handles the notification on its Notified by Parent or Notified by Child event.

**Update Parent System Function:** Pushes current subform values back to the parent through mapping links.

**Call Function:** Subforms can expose named functions that other subforms can invoke via the Call Function system function, enabling a form of controlled reuse.

### 21.4 Subform Events

| Event | Description |
|---|---|
| **Notified by Child** | Parent receives notification from a child subform |
| **Notified by Parent** | Child receives notification from the parent |
| **Enter Focus / Leave Focus** | Subform gains or loses input focus |
| **Tab Page Is Initialized** | Fires when a subform used as a tab page is first visited |
| **Tab Page Is Selected** | Fires when the user selects the subform's tab |
| **Row Is Selected / Grid Record Is Fetched** | Standard grid events within the subform |
| **Write Grid Line - Before/After** | Grid row write events |
| **Add/Update Record to DB - Before/After** | Database operation events |
| **Post Commit** | Fires after a successful commit |

### 21.5 Subform Transaction Settings

| Setting | Description |
|---|---|
| **Transaction Disabled** (default) | No TP; DB ops commit individually |
| **Include in Parent Transaction** | Subform's DB ops join the parent's transaction boundary |
| **Subform Only Transaction** | Subform manages its own independent transaction |

### 21.6 Subform System Functions

| System Function | Description |
|---|---|
| **Enable Subform / Disable Subform** | Enables or disables user interaction with the subform |
| **Show Subform / Hide Subform** | Shows or hides the subform |
| **Expand Subform / Collapse Subform** | Expands or collapses a collapsible subform |
| **Update Parent** | Pushes values to the parent via mapping links |
| **Notify Parent / Notify Child** | Sends a notification to the parent or child subform |
| **Get Error Count / Get Warning Count** | Returns the number of errors or warnings on the subform |
| **Get Subform ID** | Returns the control ID of the subform |
| **Trigger Default Action** | Programmatically triggers the subform's default action button |
| **Call Function** | Invokes a named function defined on the subform |

---

## 22. Tab and Tab Page Controls

Tab controls split a form into multiple tabbed sections, allowing the user to organize related data into separate pages. All tab pages share the form's single business view and commit together on OK.

### 22.1 Events

| Event | Description |
|---|---|
| **Tab Page Is Selected** | Fires when the user clicks a tab to select it |
| **Tab Page Is Initialized** | Fires the first time a tab page is selected (first visit only) |

### 22.2 System Functions

| System Function | Description |
|---|---|
| **Disable Tab Page / Enable Tab Page** | Disables or enables a tab page |
| **Hide Tab Page** | Hides a tab page (call only on Post Dialog Is Initialized) |
| **Set Current Tab Page** | Programmatically switches to a specific tab |
| **Set Tab Page Text** | Changes the tab's label text at runtime |

---

## 23. Text Block Controls

Text block controls display segmented text where each segment can have individual formatting, clickability, and behavior. Text blocks also support chart rendering via XML templates.

### 23.1 Text Segments

Each segment within a text block can be independently formatted with font, color, and style. Segments can be made clickable, and HTML tags can be embedded for additional formatting.

### 23.2 Chart Rendering via Text Block

Text blocks can render charts using XML templates. Available chart templates:
- `bar_basic.xml`
- `combo_basic.xml`
- `line_basic.xml`
- `pie_basic.xml` / `pie_ontime.xml`
- `stacked_bar_basic.xml` / `stacked_bar_ontime.xml`

### 23.3 Events

- **Text Clicked** — Fires when the user clicks a clickable segment

### 23.4 System Functions

| System Function | Description |
|---|---|
| **Add Segment** | Adds a new text segment to the text block |
| **Get Last Clicked Segment** | Returns information about the most recently clicked segment |
| **Get Segment Information** | Returns properties of a specific segment |
| **Remove Segment** | Deletes a segment from the text block |
| **Update Segment** | Modifies properties of an existing segment |

---

## 24. Secured Enterprise Search (SES)

SES integrates Oracle Secured Enterprise Search with JD Edwards forms, enabling full-text search across JDE data.

> **Note:** SES is on Sustaining Support as of July 17, 2026.

### 24.1 Key Components

| Component | Description |
|---|---|
| **sesscr DD Item** | Stores the search relevance score |
| **txtsum DD Item** | Stores the text summary from the search result |
| **Set Text Search Keywords** | System function that initiates the search with specified keywords |

### 24.2 Runtime Filter Operators (by Data Type)

Text search results can be filtered using comparison operators appropriate to the data type of each filterable field (string, numeric, date).

### 24.3 Incremental Indexing

The `SesTextSearchIncrementIndexing` C API enables incremental index builds — updating the search index with only changed records rather than rebuilding the entire index.

---

## 25. Tree Controls

Tree controls display hierarchical data loaded from cache. Unlike parent child controls, standalone tree controls do not share a business view with a grid.

### 25.1 Data Structure

Tree data is loaded from a cache with three key columns:

| Column | Purpose |
|---|---|
| **Node Value** | The unique identifier for each node |
| **Node Description** | The display text for the node |
| **Parent Value** | The node value of this node's parent (defines the hierarchy) |

### 25.2 Key Characteristic

Tree controls have no control-specific FDA design-time properties. They are manipulated exclusively through system functions and events at runtime.

### 25.3 Tree Events

| Event | Description |
|---|---|
| **Set Focus On Tree** | Tree receives input focus |
| **Kill Focus On Tree** | Tree loses input focus |
| **Tree Node Selected** | User selects a tree node |
| **Tree Node Is Expanding** | A node is about to expand (show children) |
| **Tree Node Is Collapsing** | A node is about to collapse (hide children) |
| **Double Click On Leaf Node** | User double-clicks a leaf node (no children) |
| **Get Custom Tree Node** | Fires during custom tree loading for additional nodes |
| **Tree Node Is Deleted** | A node is being removed |

### 25.4 Tree System Functions

| System Function | Description |
|---|---|
| **Bulk Tree Load** | Loads all tree data from cache at once |
| **Insert Tree Node** | Adds a single node to the tree |
| **Delete Tree Node** | Removes a node from the tree |
| **Contract Tree Node / Expand Tree Node** | Programmatically collapses or expands a node |
| **Get Node Information** | Returns properties of a specific node |
| **Set Node Information** | Modifies properties of a node |
| **Get Node Level / Set Node Level** | Gets or sets the hierarchical depth of a node |
| **Get Node Text / Set Node Text** | Gets or sets the display text of a node |
| **Get Tree Node Handle / Set Tree Node Handle** | Gets or sets the internal handle for a node |
| **Set Bitmap Scheme** | Assigns bitmaps for open (expanded), closed (collapsed), and leaf (no children) node states |
| **Set Node Bitmap** | Assigns a custom bitmap to a specific node |

---

## 26. Wizard Controls

Wizard controls implement multi-page guided workflows on wizard form types. Each page is implemented as a subform.

### 26.1 Wizard Properties

| Property | Description |
|---|---|
| **Enable Re-entry Save** | Allows the user to save progress and return later |
| **Enable Progress List** | Displays a list of page names for navigation |
| **Progress Indicator** | Shows completion progress (percentage or "X of Y") |
| **Suppress Validation and Save** | Per-page setting to skip validation when navigating away |

### 26.2 Page Statuses

| Status | Meaning |
|---|---|
| **No State** | Page has not been visited or has no assigned status |
| **Complete** | Page has been successfully completed |
| **Incomplete** | Page has been visited but is not yet complete |

### 26.3 Satellite Pages

Additional forms can be launched from wizard pages via form interconnections. These "satellite" pages operate outside the wizard's main flow but can pass data back through data structures.

### 26.4 Wizard Events

| Event | Description |
|---|---|
| **Wizard Is Initialized** | Fires when the wizard form first opens |
| **Post Wizard Is Initialized** | Fires after Wizard Is Initialized processing |
| **WIZARD:Subform Is Initialized** | Fires when a page subform is initialized (first visit) |
| **WIZARD:Subform Is Entered** | Fires when the user navigates to a page |
| **WIZARD:Post Subform Is Entered** | Fires after Subform Is Entered processing |
| **WIZARD:Save for Re-entry** | Fires when the user saves progress for later |
| **WIZARD:Validate Subform** | Fires before leaving a page (validation logic) |
| **WIZARD:Subform Is Exited** | Fires when the user leaves a page |
| **Page Is Exited - Before / After** | Fires before/after page exit processing |
| **Wizard Is Finished - Before** | Fires before the final commit on Finish |
| **Wizard Is Finished - After** | Fires after the final commit on Finish |
| **Wizard Is Exited** | Fires when the wizard is closed (Cancel or after Finish) |

### 26.5 Wizard Transaction Boundary

The wizard uses a single transaction boundary that encompasses all pages:
1. User clicks Finish → transaction initiates
2. All page data is saved to the business view
3. Post Button Clicked fires per Save button
4. Post Button Async fires
5. Wizard Is Finished - Before fires
6. Wizard Is Finished - After fires
7. Commit (or rollback on error)

### 26.6 Wizard System Functions

| System Function | Description |
|---|---|
| **Get Current Wizard Page ID** | Returns the control ID of the current page |
| **Get Wizard Page Index / Set Wizard Page Index** | Gets or sets the page order index |
| **Set Selected Wizard Page** | Programmatically navigates to a specific page |
| **Set Wizard Form Mode** | Sets the form mode (add, update, etc.) for the wizard |
| **Set Wizard Page Status** | Sets a page's status (no state, complete, incomplete) |
| **Suppress Wizard Page Validation and Save** | Skips validation and save for a specific page |

---

## 27. General System Functions (Appendix A)

These system functions are available across all form types and controls. They reside in various folders within FDA's system function browser.

### 27.1 Control Folder

| System Function | Description |
|---|---|
| **Clear Control Error** | Clears errors set on a control |
| **Disable Control** | Makes a control unavailable for entry (still visible) |
| **Enable Control** | Makes a control available for entry |
| **Go to URL** | Navigates to a specified URL |
| **Hide and Reclaim Space** | Hides a subform or group box and reclaims the space occupied by adjacent controls below it |
| **Hide Control** | Makes a control invisible (can still be manipulated programmatically) |
| **Set Control Error** | Sets an error on a control with a specified error code |
| **Set Control Text** | Changes the label text of a control at runtime |
| **Set Data Dictionary Item** | Replaces the DD item assigned to a control |
| **Set Data Dictionary Overrides** | Applies DD overrides (edit rules, display rules, etc.) to a control |
| **Set Statusbar Text** | Sets text in the status bar for a DD item. Pass blank to clear. |
| **Show Control** | Makes a hidden control visible |
| **Was Value Entered** | Returns 1 if the control value changed since last check, 0 if not. Two flags track changes: form flag (all controls) and control flag (individual). Checking resets the checked flag to zero. |
| **Expand Group Box / Collapse Group Box** | Expands or collapses a collapsible group box. Select `<All Collapsable GroupBoxes>` to affect all. |

### 27.2 General Folder

| System Function | Description |
|---|---|
| **Cancel User Transaction** | Cancels the current user transaction (rollback) |
| **Continue Custom Data Fetch** | Signals runtime to add the current row during custom page-at-a-time fetch and request the next one |
| **Copy Currency Information** | Copies currency type and decimal precision between controls |
| **Dynamic Form Interconnect (Web Only)** | Calls a form with application ID, form ID, version, and DS values determined at runtime. DS values passed as pipe-delimited string: `id|value|id|value...` |
| **Get VCard (9.2.1)** | Retrieves VCard information (string and name) set on a static text control within a hover form |
| **Launch Batch Application** | Establishes a report interconnection and launches a batch application. Parameters include Report Name, Version, Print Preview, Data Selection, Data Sequencing, Push Specs Only, PO Template, Prompt for Values, Date Last Executed, Data Source Override, JDE Log, JDEDebug Log, UBE Logging Level, Jargon Code, Cover Page, Job Queue Name, TC Prompting, Process Type |
| **Launch Processing Options Dialog** | Opens the processing options dialog for a batch application before launching it |
| **Press Button** | Programmatically clicks a button; fires Button Clicked on the target control and moves focus to it |
| **Run Executable** | Launches an external executable program. Parameters: EXE Directory, EXE Name, Parameters #1–#3, Working Directory |
| **Send Email (9.2.1)** | Sends an email from a hover form. Parameters: Recipients, Show Parameterized URL (YES/NO) |
| **Send Meeting Request (9.2.1)** | Sends a meeting request from a hover form |
| **Set Control Focus** | Places input focus on a specific control; fires Control Is Entered on the target |
| **Set Form Title** | Changes the form's title bar text at runtime |
| **Set Modified Web Object Behavior** | Interacts with Queries and One View Reporting from One View Financial Statements applications. Supports multiple actions: LOAD_NAMED_AQ, DOES_AQ_EXIST, PREVIEW, DELETE_AQ_NAME (for queries); SUPPRESS_ONEVIEW_MENU, LAUNCH_MODIFIED_OVR_SIDEPANEL, DOES_OVR_EXIST, PREVIEW, DELETE_OVR_NAME, FETCH_LAYOUTS, FETCH_FORMATS, RUN_MODIFIED_OVR (for One View); EXPORT/IMPORT_FRW_RPT/ROW/COL (for Financial Reporting) |
| **Set Time Zone On Form** | Sets the time zone for the current form |
| **Set VCard (9.2.1)** | Sets VCard information on a static text control within a hover form |
| **Stop Processing** | Stops runtime from processing the remaining ER on the current event |
| **Suppress Add** | Prevents the runtime engine from executing a database add. Call on Add Rec to DB - Before or Add Grid Rec to DB - Before. |
| **Suppress Default Visual Assist Form** | Prevents the default visual assist form from appearing; call on Visual Assist Button Clicked, then open a custom form |
| **Suppress Delete** | Prevents the runtime engine from executing a database delete. Call on Delete Rec to DB - Before. |
| **Suppress Find** | Prevents the runtime engine from executing a database fetch |
| **Suppress Update** | Prevents the runtime engine from executing a database update. Call on Update Rec to DB - Before. |
| **Time Between** | Calculates the difference between two UTC dates. Returns Days, Hours, Minutes, and Seconds. |
| **Was Form Record Fetched** | Returns 1 if a record was successfully fetched, 0 if no fetch was attempted or the fetch failed |

### 27.3 Messaging Folder

| System Function | Description |
|---|---|
| **Send Message Extended** | Sends email messages to users, groups, or distribution lists. Supports AB Number, Contact, Grouped/Hierarchical Distribution List, SMTP Address, and Dynamic Recipient (runtime selection based on Recipient Type codes 00–05). Body can be preset text or DD-item based. Supports media object attachments (RTF Text and URL File types) and application shortcuts. |

### 27.4 Mail Merge & Doc Gen (Web Only)

> **Note:** Deprecated from 9.2.4.0 tools release onward.

| System Function | Description |
|---|---|
| **Upload Template / Upload Template for Doc Gen** | Uploads an RTF mail merge or document generation template |
| **Download Template / Download Template for Doc Gen** | Downloads an RTF template for editing |
| **Get XML Data Model** | Processes an uploaded template into XSL, XML, and image files |
| **Run Mail Merge and Display** | Runs a mail merge using the first two variable sets and displays results |
| **Run Multiple Mail Merge** | Runs a full mail merge across all data sets (runs asynchronously) |
| **Run Doc Gen and Display** | Runs document generation and displays results |
| **Delete Document** | Deletes a generated document |
| **Display Document** | Displays a generated document |

### 27.5 Portlet System Functions

Portlet forms support personalization through DD item values passed via data structures. The **Personalization Applied** event fires when the user applies personalization settings.

---

## 28. FDA Compare Tool

FDA includes a Compare tool that lets developers compare two forms or two versions of the same form side-by-side, highlighting differences in controls, properties, and event rules. This is useful for auditing changes and reviewing customizations.

---

## 29. Quick Form

FDA's Quick Form feature enables rapid form creation by automatically placing controls on a form based on the attached business view's columns. The developer selects the BV and form type, and FDA generates a basic working form layout that can then be refined.

---

## 30. Accessibility Violation Check

FDA includes an accessibility violation checker that scans forms for compliance issues (e.g., missing tab stops, controls without labels, missing tool tips). Developers can run this check to ensure forms meet accessibility standards.

---

## 31. Glossary

| Term | Definition |
|---|---|
| **Add Mode** | Form condition enabling data input for new records |
| **Business Function** | Named set of reusable business rules callable through event rules (C or NER) |
| **Edit Mode** | Form condition enabling changes to existing data |
| **In-Your-Face Error** | Form property that displays error text directly on the form |
| **jde.ini** | Runtime settings file required on every JDE machine |
| **jde.log** | Main diagnostic log file in the root directory |
| **Power Form** | Web-only form enabling multiple interrelated data views via subforms |
| **Subform** | Control designed for use on a power form or another subform |
| **Workbench** | Program providing access to a group of related programs (e.g., Payroll Cycle Workbench P07210) |

---

*This reference was compiled from the JD Edwards EnterpriseOne Tools Form Design Aid Guide, Release 9.2. For the most current information, consult the official Oracle documentation.*
