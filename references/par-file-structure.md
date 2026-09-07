# JDE EnterpriseOne 9.2 — PAR File Structure Reference

## Purpose

This document provides a complete technical reference for the PAR (Package Assembly Repository) file format used by JDE EnterpriseOne 9.2 to export, transport, and import development objects. PAR files are the only human-readable representation of JDE specs — objects stored internally as unreadable BLOBs in the database become structured XML when exported to PAR format, making them suitable for programmatic creation, modification, and version control.

---

## 1. PAR File Architecture Overview

### 1.1 Nested ZIP Structure

A PAR file is a **nested ZIP archive**. Despite the `.par` extension, it uses standard ZIP compression throughout.

**Project-level PAR** (outer archive):
```
PRJ_P01012_60_99.par          ← Outer ZIP
├── manifest.xml              ← UTF-16 encoded project manifest
├── APPL_P01012_60_99.par     ← Inner ZIP (application)
├── TBLE_F0101_60_99.par      ← Inner ZIP (table)
├── BSVW_V0101E_60_99.par     ← Inner ZIP (business view)
├── BSFN_B0100032_60_99.par   ← Inner ZIP (C business function)
├── BSFN_N0100062_60_99.par   ← Inner ZIP (NER business function)
├── DSTR_D0100018_60_99.par   ← Inner ZIP (BSFN data structure)
├── DSTR_T01012_60_99.par     ← Inner ZIP (PO data structure)
└── ...                       ← Additional inner PARs
```

**Inner PAR** (single object archive):
```
TBLE_F0101_60_99.par          ← Inner ZIP
├── manifest.xml              ← UTF-16 encoded object manifest
├── F9860.xml                 ← Object Librarian Master (UTF-8)
├── F9861.xml                 ← Object Librarian Status (UTF-8)
├── specs.zip                 ← Specs archive (standard ZIP)
│   └── (type-specific contents)
├── include/                  ← Header files (TBLE, BSVW, BSFN C only)
│   └── F0101.h
└── source/                   ← Source files (BSFN C only)
    └── B0100032.c
```

### 1.2 File Naming Convention

All PAR files follow the pattern:

```
{TYPE}_{OBJECTNAME}_{PACKAGETYPE}_{HOSTTYPE}.par
```

| Segment | Description | Values |
|---------|-------------|--------|
| TYPE | Object type prefix | APPL, TBLE, BSVW, BSFN, DSTR |
| OBJECTNAME | JDE object name | P01012, F0101, V0101E, B0100032, D0100018, T01012 |
| PACKAGETYPE | Package type | 60 (standard) |
| HOSTTYPE | Host type | 99 (standard) |

**Note:** Both C business functions (B-prefix) and NER business functions (N-prefix) use the `BSFN` type prefix. Processing Option data structures (T-prefix) use the `DSTR` type prefix alongside regular BSFN data structures (D-prefix).

### 1.3 Encoding Rules

| File | Encoding | Notes |
|------|----------|-------|
| manifest.xml | UTF-16 | BOM present; declares `encoding='UTF-16'` |
| F9860.xml | UTF-8 | Standard XML declaration |
| F9861.xml | UTF-8 | Standard XML declaration |
| F9862.xml | UTF-8 | BSFN only |
| F9863.xml | UTF-8 | BSFN only |
| F9865.xml | UTF-8 | APPL only (Form Directory) |
| All specs XMLs | UTF-8 with UTF-16 BOM prefix | Dual-encoded: UTF-16 BOM + mirror followed by UTF-8 content. Parsers should skip to the UTF-8 XML declaration. |

---

## 2. Manifest Structure

### 2.1 Outer Manifest (Project Level)

The outer manifest lists all inner PAR files and their OMW (Object Management Workbench) relationships.

```xml
<?xml version='1.0' encoding='UTF-16' ?>
<manifest aggregate='' description='P01012' documentation=''
         hosttype='99' hosttypedescription=''
         name='PRJ_P01012' release='E920'
         sar='0' type='60' typedescription=''>
  <filelist>
    <file filename='BSFN_B0100032_60_99.par' id='BSFN_B0100032_60_99.par'/>
    <file filename='TBLE_F0101_60_99.par' id='TBLE_F0101_60_99.par'/>
    <file filename='APPL_P01012_60_99.par' id='APPL_P01012_60_99.par'/>
    <!-- ... additional files ... -->
  </filelist>
  <omw>
    <omwProject description='P01012' file='PRJ_P01012_60_99.par'
                id='P01012' type='PRJ'>
      <omwObject description='Get Phone' file='BSFN_B0100032_60_99.par'
                 id='B0100032' type='BSFN'/>
      <omwObject description='Address Book Master' file='TBLE_F0101_60_99.par'
                 id='F0101' type='TBLE'/>
      <omwObject description='Address Book' file='APPL_P01012_60_99.par'
                 id='P01012' type='APPL'/>
      <!-- ... additional objects ... -->
    </omwProject>
  </omw>
</manifest>
```

**Manifest Attributes:**

| Attribute | Description | Example |
|-----------|-------------|---------|
| name | Project name | PRJ_P01012 |
| description | Human-readable description | P01012 |
| type | Package type | 60 |
| hosttype | Host type | 99 |
| release | JDE release | E920 |
| sar | SAR number | 0 |

**omwObject Attributes:**

| Attribute | Description |
|-----------|-------------|
| id | Object name (e.g., B0100032) |
| type | Object type: BSFN, TBLE, BSVW, APPL, DSTR |
| description | Object description |
| file | Corresponding inner PAR filename |

### 2.2 Inner Manifest (Object Level)

Each inner PAR contains its own manifest with a `<filelist>` referencing the files within:

```xml
<?xml version='1.0' encoding='UTF-16' ?>
<manifest name='TBLE_F0101' type='60' hosttype='99' release='E920'>
  <filelist>
    <file filename='F9860.xml' id='F9860.xml'/>
    <file filename='F9861.xml' id='F9861.xml'/>
    <file filename='specs.zip' id='specs.zip'/>
    <file filename='include/F0101.h' id='include/F0101.h'/>
  </filelist>
</manifest>
```

---

## 3. Object Librarian XML Files (F98xx)

Every inner PAR contains at minimum F9860.xml and F9861.xml. BSFN objects add F9862.xml and F9863.xml. APPL objects add F9865.xml.

### 3.1 F9860.xml — Object Librarian Master

Defines the object's identity, type, and classification. Format: `<table name="F9860"><row><col name="XXX">value</col>...</row></table>`

**Key Columns:**

| Column | Description | Values/Notes |
|--------|-------------|--------------|
| SIOBNM | Object name | P01012, F0101, V0101E, B0100032, N0100062, D0100018, T01012 |
| SIMD | Description | Free text, 60 chars padded |
| SISY | System code | 01, 09, 42, 73, etc. |
| SISYR | System code (redundant) | Same as SISY |
| SIFUNO | Function type | **APPL** = Application, **TBLE** = Table, **BSVW** = Business View, **BSFN** = Business Function, **DSTR** = Data Structure |
| SIFUNU | Function use code | 164 (interactive app), 210 (master table), 300 (business view), 320 (BSFN DS), 360 (PO DS) |
| SIPFX | Column prefix | AB (for F0101 table); blank for non-tables |
| SISRCLNG | Source language | C (compiled BSFN), NER (Named Event Rule), blank (non-BSFN) |
| SICPYD | Copy data flag | Y/N |
| SIPARDLL | Parent DLL | JDBTRIG (tables), CDIST/CALLBSFN (BSFNs), blank otherwise |
| SIMID1 | Template/link name | T01012 (PO template for APPL), blank otherwise |
| SIAPPLID | Application ID | Numeric |
| SICATO | Category/object code | ADDR (address), blank |
| SIPID | Program ID | P98220 (Object Management) |
| SIUSER | Last user | JDE |
| SIUPMJ | Last update date | Julian date (e.g., 126244) |

**SIFUNU Function Use Codes (key values):**

| Code | Meaning |
|------|---------|
| 164 | Interactive application |
| 180 | Batch application (UBE) |
| 210 | Master file table |
| 300 | Business view |
| 310 | Business function (C) |
| 320 | Data structure (BSFN) |
| 360 | Data structure (Processing Option) |

### 3.2 F9861.xml — Object Librarian Status

Tracks version, status, and merge information.

```xml
<?xml version='1.0' encoding='UTF-8'?>
<table name="F9861">
  <row>
    <col name="SIOBNM">F0101     </col>
    <col name="SIJDEVERS">E920      </col>
    <col name="SISTCE">3</col>
    <col name="SIMRGMOD">C</col>
    <col name="SIMRGOPT">2</col>
    <!-- audit fields: SIPID, SIUSER, SIJOBN, SIUPMJ, SIUPMT -->
  </row>
</table>
```

| Column | Description | Values |
|--------|-------------|--------|
| SIJDEVERS | JDE version | E920 |
| SISTCE | Status code | 3 = production |
| SIMRGMOD | Merge mode | C = complete |
| SIMRGOPT | Merge option | 2 |

### 3.3 F9862.xml — BSFN Function Detail (BSFN only)

Defines the callable function within a BSFN object.

```xml
<table name="F9862">
  <row>
    <col name="SIOBNM">B0100032  </col>
    <col name="SIFCTNM">GetPhone                        </col>
    <col name="SIMD">F0115 Get Primary Phone Number</col>
    <col name="SIDSTNM">D0100032  </col>
    <col name="SIEVSK">                                    </col>
    <col name="SIBUF1">XXX</col>
    <col name="SIBUF2">XXX</col>
    <col name="SIBUF3">3  </col>
  </row>
</table>
```

| Column | Description | Notes |
|--------|-------------|-------|
| SIFCTNM | C function name | GetPhone, PostalCodeAddressSelection |
| SIMD | Function description | |
| SIDSTNM | Data structure template | D0100032 (links to DSTR object) |
| SIEVSK | Event spec key (GUID) | Populated for NERs, blank for C BSFNs |
| SIBUF1-5 | Buffer flags | XXX for compiled C; blank/3 for NER |

**C vs NER distinction in F9862:**
- **C BSFN:** SIEVSK is blank (36 spaces), SIBUF1/SIBUF2 = "XXX"
- **NER BSFN:** SIEVSK contains a GUID (e.g., `cb030930-7ef0-4a7c-9162-ed4fbed99f7c`), SIBUF1/SIBUF2 are blank

### 3.4 F9863.xml — BSFN Table Relationships (BSFN only)

Lists tables the BSFN references. **Empty for NERs** (NER table dependencies are embedded in their GBRSPEC event rules).

```xml
<!-- C BSFN with table relationship -->
<table name="F9863">
  <row>
    <col name="SIOBNM">B0100032  </col>
    <col name="SIFUNO">TBLE</col>
    <col name="SIOBNMRL">F0115     </col>
  </row>
</table>

<!-- NER BSFN — empty -->
<table name="F9863"></table>
```

| Column | Description |
|--------|-------------|
| SIOBNM | BSFN object name |
| SIFUNO | Related object type (TBLE) |
| SIOBNMRL | Related table name (F0115) |

### 3.5 F9865.xml — Form Directory (APPL only)

Lists all forms in the application.

```xml
<table name="F9865">
  <row>
    <col name="SWFMNM">W01012A</col>
    <col name="SWMD">Address Book Revision</col>
    <col name="SWFMPT">FI</col>
    <col name="SWENTRYPT">0</col>
    <col name="SWOBNM">P01012</col>
    <col name="SWSY">01  </col>
    <col name="SWHELPID1">1680990</col>
  </row>
  <row>
    <col name="SWFMNM">W01012B</col>
    <col name="SWMD">Work With Addresses</col>
    <col name="SWFMPT">BR</col>
    <col name="SWENTRYPT">1</col>
    <!-- ... -->
  </row>
  <!-- additional forms ... -->
</table>
```

| Column | Description | Values |
|--------|-------------|--------|
| SWFMNM | Form name | W01012A, W01012B |
| SWMD | Form description | |
| SWFMPT | Form type | **FI** = Fix/Inspect, **BR** = Browse/Search, **MB** = Message Box |
| SWENTRYPT | Entry point flag | **1** = entry point form, **0** = secondary form |
| SWOBNM | Parent application | P01012 |
| SWSY | System code | 01 |
| SWHELPID1 | Help ID | Numeric |

---

## 4. Specs Archive Structure by Object Type

The `specs.zip` inside each inner PAR contains the actual object specifications. Structure varies by object type.

### 4.1 DSTR — Data Structure (BSFN Type)

```
specs.zip/
└── DSTMPL/
    └── D0100018.xml
```

**DSTMPL XML:**

```xml
<DSTemplate szTmplName="D0100018"
            TemplateType="BSFN"
            nVersData="110"
            xmlns="http://peoplesoft.com/e1/metadata/v1.0"
            xmlns:xs="http://www.w3.org/2001/XMLSchema"
            xmlns:et="http://peoplesoft.com/e1/metadata/v1.0/erptypes">
  <DSTemplateDetails>
    <DSTemplateDetail ItemID="1"
                      DisplaySequence="1"
                      CopyWord="EMPTY"
                      DDAlias="AN8"
                      FieldName="mnAddressNumber"
                      LengthInVersData="50"/>
    <DSTemplateDetail ItemID="2"
                      DisplaySequence="2"
                      CopyWord="EMPTY"
                      DDAlias="PAR"
                      FieldName="szPhoneAreaCode"
                      LengthInVersData="14"/>
    <!-- ... -->
  </DSTemplateDetails>
</DSTemplate>
```

**DSTemplate Attributes:**

| Attribute | Description | Values |
|-----------|-------------|--------|
| szTmplName | Template name | D0100018 |
| TemplateType | Template type | **BSFN** (business function DS), **PO** (processing option DS) |
| nVersData | Version data length | Total byte length of all fields |

**DSTemplateDetail Attributes:**

| Attribute | Description | Notes |
|-----------|-------------|-------|
| ItemID | Unique item identifier | Sequential, starts at 1 |
| DisplaySequence | Display order | |
| CopyWord | Parameter direction | EMPTY, IN, OUT, INANDOUT |
| DDAlias | Data Dictionary alias | Links to DD item (e.g., AN8, PAR) |
| FieldName | Generated field name | Hungarian notation (mn=math numeric, sz=string, c=char, jd=julian date) |
| LengthInVersData | Field byte length | |

### 4.2 DSTR — Data Structure (Processing Option Type)

Processing Option data structures use the same DSTMPL format but add **PageNumber** grouping and a **POTEXT/** directory.

```
specs.zip/
├── DSTMPL/
│   └── T01012.xml
└── POTEXT/
    ├── T01012.1.0.0..xml
    ├── T01012.1.0.1..xml
    └── ...
```

**PO DSTemplate additions:**

```xml
<DSTemplate szTmplName="T01012" TemplateType="PO" nVersData="334">
  <DSTemplateDetails>
    <DSTemplateDetail ItemID="16" PageNumber="1"
                      DisplaySequence="0" CopyWord="EMPTY"
                      DDAlias="AT1" FieldName="IT_SearchType"
                      LengthInVersData="8"/>
    <!-- items grouped by PageNumber (0, 1, 2, 3, 4) -->
  </DSTemplateDetails>
  <DSPageTitles>
    <DSPageTitle PageNumber="0" ShortTitleTextID="0" PageTitleTextID="0"/>
    <DSPageTitle PageNumber="1" ShortTitleTextID="0" PageTitleTextID="0"/>
    <!-- ... -->
  </DSPageTitles>
</DSTemplate>
```

**POTEXT Files** (F98306 records — processing option help text):

```xml
<table name="F98306">
  <row>
    <col name="PTOBNM">T01012</col>
    <col name="PTPOTP">1</col>      <!-- PO type -->
    <col name="PTITNUM">0</col>      <!-- Item number -->
    <col name="PTSQNUM">0</col>      <!-- Sequence -->
    <col name="PTLNGP"></col>         <!-- Language -->
    <col name="PTPGTX"></col>         <!-- Page text -->
    <col name="PTGKEY">S0101201</col> <!-- Glossary key -->
    <col name="PTPOTX">1. Supplier Master&#13;
&#13;
Blank = Do not display this form.&#13;
1 = Display this form.</col>           <!-- PO text with descriptions -->
  </row>
</table>
```

POTEXT naming: `{TemplateName}.{PTPOTP}.{PTITNUM}.{PTSQNUM}.{PTLNGP}.xml`

### 4.3 TBLE — Table

```
specs.zip/
├── DDCLMN/
│   ├── F0101.AN8.xml
│   ├── F0101.ALKY.xml
│   └── ... (one per column)
├── GBRSPEC/
│   ├── {guid1}.xml
│   └── ... (table event rule specs)
└── GBRLINK/
    ├── 4.F0101...0.1.xml    (Add trigger)
    ├── 4.F0101...0.3.xml    (Update trigger)
    └── 4.F0101...0.4.xml    (Delete trigger)
```

Additionally, the inner PAR includes an `include/` directory (not inside specs.zip):
```
include/
└── F0101.h                  ← C header with typedef struct
```

#### DDCLMN Files (F98711 — Column Definitions)

One file per table column. Links DD aliases to SQL column names.

```xml
<table name="F98711">
  <row>
    <col name="TDOBNM">F0101</col>    <!-- Table name -->
    <col name="TDOBND">AB3</col>       <!-- DD alias -->
    <col name="TDSQLC">ABAB3</col>     <!-- SQL column name = prefix + alias -->
    <col name="TDPSEQ">19</col>        <!-- Position sequence -->
  </row>
</table>
```

SQL column naming rule: `{TablePrefix}{DDALias}` — e.g., prefix `AB` + alias `AB3` = `ABAB3`.

#### GBRLINK Files (Table Event Rule Links)

Maps table trigger events to GBRSPEC GUIDs.

Naming: `{ProductType}.{TableName}...{EventID}.{ControlID}.xml`

```xml
<GBRLink ProductType="TER"
         ApplicationID="F0101"
         EventID="1"
         EventSpecKey="a423973c-0af9-4c75-87cf-673087d4e7e9"
         xmlns="http://peoplesoft.com/e1/metadata/v1.0"/>
```

Table Event IDs: **1** = After Add, **3** = After Update, **4** = After Delete.

#### GBRSPEC Files (Event Rule Specifications)

GUID-named XML files containing actual event rule logic. See Section 5 for GBRSPEC XML element reference.

### 4.4 BSVW — Business View

```
specs.zip/
└── BUSVIEW/
    └── V0101E.xml
```

Additionally, the inner PAR includes:
```
include/
└── BV0101E.h               ← C header
```

**BUSVIEW XML:**

```xml
<BSVW szView="V0101E" szTable="F0101" szDescription="Address Book Update"
      xmlns="http://peoplesoft.com/e1/metadata/v1.0"
      xmlns:xs="http://www.w3.org/2001/XMLSchema"
      xmlns:et="http://peoplesoft.com/e1/metadata/v1.0/erptypes">
  <Bob_TableCollection>
    <Bob_Table idPrimaryIndex="1" szTable="F0101"/>
  </Bob_TableCollection>
  <DbrefCollection>
    <et:Dbref szTable="F0101" szDict="AN8"/>  <!-- Primary key reference -->
  </DbrefCollection>
  <Bob_ColumnCollection>
    <Bob_Column iFlags="1" nSeq="0" szTable="F0101" szDict="AN8"/>
    <Bob_Column nSeq="1" szTable="F0101" szDict="ALKY"/>
    <Bob_Column nSeq="2" szTable="F0101" szDict="TAX"/>
    <!-- ... up to nSeq="85" ... -->
  </Bob_ColumnCollection>
</BSVW>
```

**BSVW Element Reference:**

| Element | Description |
|---------|-------------|
| `<BSVW>` | Root. `szView`=view name, `szTable`=primary table, `szDescription`=description |
| `<Bob_TableCollection>` | Lists tables joined in the view |
| `<Bob_Table>` | `idPrimaryIndex`=index number, `szTable`=table name |
| `<DbrefCollection>` | Primary key column references |
| `<et:Dbref>` | `szTable`=table, `szDict`=DD alias of key column |
| `<Bob_ColumnCollection>` | All columns selected in the view |
| `<Bob_Column>` | `nSeq`=sequence, `szTable`=source table, `szDict`=DD alias, `iFlags`=1 for key columns |

### 4.5 BSFN — Business Function (C Compiled)

```
specs.zip/
└── BUSFUNC/
    └── GetPhone.xml          ← Named by function name, not object name

source/
└── B0100032.c                ← C source code (outside specs.zip)

include/
└── B0100032.h                ← C header (outside specs.zip)
```

**BUSFUNC XML (C):**

```xml
<BSFN szFcnName="GetPhone"
      szSourceFileName="B0100032"
      cSibflocn="2"
      szAuthor="E820"
      szFcnBriefDesc="F0115 Get Primary Phone Number"
      SystemCode="01"
      szDsTmplName="D0100032"
      wOrdinal="0"
      xmlns="http://peoplesoft.com/e1/metadata/v1.0"/>
```

| Attribute | Description |
|-----------|-------------|
| szFcnName | C function name (matches F9862 SIFCTNM) |
| szSourceFileName | Source file base name |
| szDsTmplName | Data structure template (links to DSTR object) |
| cSibflocn | Location flag: **2** = server, **1** = client |
| SystemCode | System code |
| wOrdinal | Function ordinal within the source file |

The actual logic lives in the C source file, not in the XML.

### 4.6 BSFN — Business Function (NER — Named Event Rule)

```
specs.zip/
├── BUSFUNC/
│   └── PostalCodeAddressSelection.xml
└── GBRSPEC/
    └── cb030930-7ef0-4a7c-9162-ed4fbed99f7c.xml   ← GUID matches F9862.SIEVSK
```

No `source/` or `include/` directories — NER logic is entirely in GBRSPEC XML.

**BUSFUNC XML (NER):**

```xml
<BSFN szFcnName="PostalCodeAddressSelection"
      szSourceFileName="CFIN"
      cSibflocn="1"
      szAuthor="N0100062"
      szFcnBriefDesc="Postal Codes Address Selection"
      SystemCode="01"
      szDsTmplName="D0100062"
      wOrdinal="0"/>
```

Key differences from C BSFN:
- `szSourceFileName` = "CFIN" (generic NER source marker)
- `szAuthor` = NER object name (N0100062)
- `cSibflocn` = "1" (client-side typically)
- GBRSPEC file contains the complete event rule logic

### 4.7 APPL — Interactive Application

The most complex object type. Includes an additional F9865.xml at the inner PAR level and 7 subdirectories inside specs.zip.

```
F9860.xml                     ← Object Librarian Master
F9861.xml                     ← Object Librarian Status
F9865.xml                     ← Form Directory
specs.zip/
├── DSTMPL/                   ← Auto-generated form data structures
│   ├── W01012A.xml
│   ├── W01012B.xml
│   └── ...
├── FDASPEC/                  ← Form Design Aid specifications
│   ├── P01012.1..0.0.0.xml              (application-level)
│   ├── P01012.2.W01012A.0.0.0.xml       (form header)
│   ├── P01012.3.W01012A.1.0.0.xml       (control)
│   ├── P01012.5.W01012B.1.0.1.xml       (grid column)
│   ├── P01012.8.W01012A.0.272.0.xml     (FI template extension)
│   ├── P01012.9.W01012A.9.0.1.xml       (tab page / QBE)
│   ├── P01012.13.W01012A.13.1.0.xml     (tab container)
│   └── P01012.14.W01012A.13.1.1.xml     (tab child control)
├── FDATEXT/                  ← Text resources
│   ├── P01012.2000.  .xml
│   ├── P01012.3539.  .xml
│   └── ...
├── GBRLINK/                  ← Event-to-spec links
│   ├── 1.P01012..W01012A.0.272.xml
│   ├── 1.P01012..W01012A.11.0.xml
│   └── ...
├── GBRSPEC/                  ← Event rule specifications (GUID names)
│   ├── 0124bc40-1062-11d2-9a85-0000f638127c.xml
│   └── ... (77 files for P01012)
├── SVRHDR/                   ← Server header
│   └── P01012.xml
└── SVRDTL/                   ← Server detail (per form)
    ├── P01012.W01012A.xml
    ├── P01012.W01012B.xml
    └── ...
```

#### FDASPEC Naming Convention

```
{AppName}.{TypeCode}.{FormName}.{ControlID}.{TabID}.{Sequence}.xml
```

| TypeCode | Element Type | Example |
|----------|-------------|---------|
| 1 | Application-level settings | P01012.1..0.0.0.xml |
| 2 | Form definition/header | P01012.2.W01012A.0.0.0.xml |
| 3 | Control (button, edit, static) | P01012.3.W01012A.1.0.0.xml |
| 5 | Grid column | P01012.5.W01012B.1.0.1.xml |
| 8 | Form Interconnect DS extension | P01012.8.W01012A.0.272.0.xml |
| 9 | Tab page / QBE / hyper item | P01012.9.W01012A.9.0.1.xml |
| 13 | Tab container | P01012.13.W01012A.13.1.0.xml |
| 14 | Tab child controls | P01012.14.W01012A.13.1.1.xml |

#### FDASPEC XML Elements

**Application-level (type 1):**

```xml
<FDA ApplicationName="P01012" xmlns="http://peoplesoft.com/e1/metadata/v1.0">
  <FDARecord>
    <FDAApplication TextId="2000" NextTextId="8044"
                    ProcessingOptionTemplate="T01012"/>
  </FDARecord>
</FDA>
```

The `ProcessingOptionTemplate` links the application to its PO data structure (T01012 → DSTR_T01012).

**Form definition (type 2):**

```xml
<FDARecord>
  <FDAForm FormName="W01012A"
           BusinessViewName="V0101E"
           FormType="FIX_INSPECT"
           Width="604" Height="230"
           GUIStyleFlag="3503226880"
           FormTitleId="3539"
           NextObjectId="504"
           FormGuideHeight="768" FormGuideWidth="1024"
           CGStyle="3"/>
</FDARecord>
```

| Attribute | Description |
|-----------|-------------|
| FormName | Form identifier (W01012A) |
| BusinessViewName | Associated business view (V0101E) — **key cross-reference** |
| FormType | FIX_INSPECT, BROWSE, MSGBOX, HEADERLESS_DETAIL, HEADERDETAIL, PARENT_CHILD, SEARCH_SELECT |
| FormTitleId | Links to FDATEXT for the form title |
| NextObjectId | Next available control ID |

**Control (type 3):**

```xml
<FDARecord>
  <FDAHyperButtonControl NextEvent="0"
                         FormName="W01012A"
                         TabOrderIndex="1"
                         LeftCoordinate="307" TopCoordinate="129"
                         Width="74" Height="12"
                         WinStyleFlag="1073963016"
                         OverrideTextFlag="true"
                         TextId="3532"
                         ObjectId="9"
                         WindowItemId="5009"
                         StandardFlags="917504"/>
</FDARecord>
```

Control element names vary by control type: `FDAHyperButtonControl`, `FDAEditControl`, `FDAStaticControl`, `FDACheckBoxControl`, `FDAComboControl`, `FDAGridControl`, etc.

**Grid column (type 5):**

```xml
<FDARecord>
  <FDAColumn FormName="W01012B"
             GridID="1" SequenceNumber="1"
             ObjectID="19"
             OverrideText="true" ColumnTitleId="2089"
             NumberOfTextChar="13"
             Visible="true" InputCapable="true"
             SortSequence="1" SortOrder="A"
             CgStyle="8192" Flags="14368">
    <et:Dbref szTable="F0101" szDict="AN8"/>
    <et:DdOverrides nDispDecimals="65535"/>
  </FDAColumn>
</FDARecord>
```

The `<et:Dbref>` inside a column links it to a specific table column via DD alias — this is how form columns map to database columns.

**Tab page (type 13):**

```xml
<FDARecord>
  <FDATabPage FormName="W01012A"
              TabControlObjectId="13"
              PageNumber="1"
              TabPageTitleId="5477"
              ObjectId="14"/>
</FDARecord>
```

**Form Interconnect DS extension (type 8):**

```xml
<FDARecord>
  <FDADSTemplateExtension FormName="W01012A">
    <DSItem itemId="5" displaySeq="1"
            copyWord="INANDOUT" dictionaryId="CCPR"
            dataItem="szCountryForPayroll">
      <DsObjFrom>
        <DSOBJMember szTmplName="W01012A" idItem="5"/>
      </DsObjFrom>
      <DsObjTo>
        <DSOBJUndefined/>
      </DsObjTo>
    </DSItem>
    <DSItem itemId="12" copyWord="INANDOUT"
            dictionaryId="AN8" dataItem="mnAddress_Number">
      <DsObjFrom>
        <DSOBJMember szTmplName="W01012A" idItem="12"/>
      </DsObjFrom>
      <DsObjTo>
        <DSOBJBSTableColumn szView="V0101E">
          <et:Dbref szTable="F0101" szDict="AN8"/>
        </DSOBJBSTableColumn>
      </DsObjTo>
    </DSItem>
    <!-- ... -->
  </FDADSTemplateExtension>
</FDARecord>
```

The `<DsObjTo>` elements show how FI parameters map to business view columns or remain undefined (local-only parameters).

#### FDATEXT Files

Text resources for labels, titles, messages. Each file contains a single text string identified by TextId.

Naming: `{AppName}.{TextId}.{Language}.xml`

```xml
<FDAText ApplicationName="P01012" TextId="3539"
         xmlns="http://peoplesoft.com/e1/metadata/v1.0">
Address Book Revision
</FDAText>
```

#### GBRLINK Files (Application Events)

Maps form events to GBRSPEC GUIDs.

Naming: `{ProductType}.{AppName}..{FormName}.{EventID}.{ControlID}.xml`

```xml
<GBRLink ProductType="FDA"
         ApplicationID="P01012"
         FormOrSectionID="W01012A"
         EventID="272"
         EventSpecKey="de0ef711-fcad-11d1-9a82-0000f638127c"/>
```

When ObjectID is present (e.g., EventID="11" ObjectID="0"), it indicates a control-specific event:

```xml
<GBRLink ProductType="FDA"
         ApplicationID="P01012"
         FormOrSectionID="W01012A"
         ObjectID="11"
         EventID="0"
         EventSpecKey="fe154831-e906-11d1-9a75-0000f638127c"/>
```

**ProductType values:** "FDA" for applications, "TER" for table event rules.

**Common Application EventIDs:**

| EventID | Event | Notes |
|---------|-------|-------|
| 0 | Control-specific event | Combined with ObjectID for specific control |
| 1 | Dialog is Initialized | Form load |
| 2 | Post Dialog is Initialized | After form load |
| 5 | Button Clicked | Combined with ControlID (ObjectId of button) |
| 11 | Dialog Opened | |
| 12 | Dialog Closed | |
| 15 | Grid Record is Fetched | |
| 163-187 | Row/Menu exits | Specific row operations |
| 232 | Form exits | |
| 272 | Specific button ID | Hyper button events |

#### SVRHDR / SVRDTL Files

**SVRHDR (Server Header):**

```xml
<ASVRHeader ApplicationName="P01012"
            ProcessingOptionTemplateName="T01012"/>
```

Links the application to its processing option template at the server level.

**SVRDTL (Server Detail — per form):**

```xml
<ASVRDetail ApplicationName="P01012"
            FormName="W01012A"
            FormInterconnectTemplateName="W01012A"/>
```

Links each form to its Form Interconnect data structure template.

#### DSTMPL (Application Form Data Structures)

Auto-generated data structures for form interconnects. Same format as standalone DSTR but with `TemplateType` implied by context (they correspond to form FI parameters).

---

## 5. GBRSPEC Event Rule XML Reference

GBRSPEC files contain the actual business logic (event rules). They are used by tables (TER), NER business functions, and applications (FDA).

### 5.1 Root Element

```xml
<GBRSPEC szView="V0101E" szLastChangeTime="153330"
         szLastChangeUser="JDEUSER"
         xmlns="http://peoplesoft.com/e1/metadata/v1.0"
         xmlns:xs="http://www.w3.org/2001/XMLSchema"
         xmlns:et="http://peoplesoft.com/e1/metadata/v1.0/erptypes">
  <!-- event rule statements -->
</GBRSPEC>
```

### 5.2 Statement Elements

| Element | Description | Key Attributes |
|---------|-------------|----------------|
| `<GBRVAR>` | Variable declaration | `idVariable`, `szDict`, `wStyle`, `dataType`, `size` |
| `<GBRASSIGN>` | Assignment | `typeEVDT`, `textString` (human-readable description) |
| `<GBRCRIT>` | If condition (start) | `lpszCritDesc` (human-readable condition) |
| `<GBRElse/>` | Else branch | |
| `<GBREndIf/>` | End if | |
| `<GBRBF>` | Business function call | `szFuncName`, `szTmplName` (DS template) |
| `<GBRSLBF>` | System function call | `szFuncName` |
| `<GBRFI>` | Form interconnect | `applicationName`, `tmplName`, `formName`, `versionDesc` |
| `<GBRFileIOOp>` | Database I/O operation | `operation`, `szView`, `indexId`, `fetchCount` |
| `<GBRCOMMENT>` | Comment | Contains `<text>` child |
| `<GBRWhile>` | While loop start | `lpszCritDesc` |
| `<GBREndWhile/>` | While loop end | |
| `<GBRSetVal>` | Set value | |
| `<GBRReturn>` | Return from function | |

### 5.3 Variable Styles (wStyle)

| wStyle | Scope |
|--------|-------|
| 8 | Local variable (within event) |
| 9 | Form-level variable (VA frm_) |
| 32 | Event-level variable |

### 5.4 Data Source Object Elements (DSOBJ*)

Used within assignments, conditions, and parameters to reference data sources:

| Element | Description | Key Attributes |
|---------|-------------|----------------|
| `<DSOBJFormControl>` | Form control value | `idObject` (control ObjectId) |
| `<DSOBJVariable>` | Variable | `idVariable`, `szDict`, `wStyle`, `dataType`, `size` |
| `<DSOBJLiteral>` | Literal value | Contains `<DSOBJLiteralItem>` with `<LiteralString>` or `<LiteralInt>` |
| `<DSOBJSystemVariable>` | System variable | |
| `<DSOBJConstant>` | Named constant | |
| `<DSOBJBSTableColumn>` | Business view column | `szView`; contains `<et:Dbref szTable= szDict=>` |
| `<DSOBJTableColumn>` | Direct table column | |
| `<DSOBJMember>` | DS/PO member | `szTmplName`, `idItem` |
| `<DSOBJSystemValue>` | System value | |
| `<DSOBJHyperItem>` | Hyper item | |
| `<DSOBJTabPage>` | Tab page reference | |
| `<DSOBJTextVariable>` | Text variable | |
| `<DSOBJExpression>` | Calculated expression | |
| `<DSOBJUndefined>` | Unmapped/undefined | |
| `<DSOBJCollection>` | Collection object | |
| `<DSOBJFileIO>` | File I/O handle | |

### 5.5 Parameter Direction (ERPARAM)

```xml
<ERPARAM idItem="1" idType="MathNumeric" wCopyWord="IN">
  <DSOBJFormControl idObject="21"/>
</ERPARAM>
```

| wCopyWord | Direction |
|-----------|-----------|
| IN | Input only |
| OUT | Output only |
| INANDOUT | Bidirectional |
| EMPTY | Not passed |

For `GBRFileIOOp` / `GBRParam` (query conditions):

| wCopyWord | SQL Operator |
|-----------|-------------|
| EQUAL | = |
| LESSOREQ | <= |
| GRTROREQ | >= |

### 5.6 Database I/O Operations

```xml
<GBRFileIOOp operation="FETCH_SINGLE" szView="V0101E"
             indexId="1" fetchCount="1">
  <GBRParam idItem="1" idType="MathNumeric" wCopyWord="EQUAL">
    <DSOBJFormControl idObject="21"/>
  </GBRParam>
</GBRFileIOOp>
```

| operation | Description |
|-----------|-------------|
| SELECT | Open cursor (start query) |
| FETCH_SINGLE | Fetch one record |
| FETCH_NEXT | Fetch next record |
| UPDATE | Update record |
| INSERT | Insert record |
| DELETE | Delete record |
| CLOSE | Close cursor |

### 5.7 Conditional Logic

```xml
<GBRCRIT lpszCritDesc="If VA frm_CSMSFlag is equal to &quot;1&quot;">
  <CRE_HEADER szView="V0101E">
    <CRE_NODE idEVDT="Char">
      <zSubject>
        <DSOBJVariable idVariable="16" szDict="CSFL"
                       wStyle="9" dataType="Char" size="1"/>
      </zSubject>
      <zPredicate>
        <DSOBJLiteral>
          <DSOBJLiteralItem idEVDT="String">
            <LiteralString>1</LiteralString>
          </DSOBJLiteralItem>
        </DSOBJLiteral>
      </zPredicate>
    </CRE_NODE>
    <et:ERPDate Year="98" Month="6" Day="30"/>
  </CRE_HEADER>
</GBRCRIT>
<!-- conditional body -->
<GBRElse/>
<!-- else body -->
<GBREndIf/>
```

### 5.8 Business Function Call

```xml
<GBRBF szFuncName="F17001GetInstalledFlag" szTmplName="D1700056A">
  <ERPARAM idItem="4" idType="Char" wCopyWord="OUT">
    <DSOBJVariable idVariable="16" szDict="CSFL"
                   wStyle="9" dataType="Char" size="1"/>
  </ERPARAM>
</GBRBF>
```

### 5.9 Form Interconnect Call

```xml
<GBRFI versionDesc=" "
       applicationName="P1782"
       tmplName="W1782G"
       formName="W1782G"
       disabled="false">
  <VersionObj>
    <DSOBJLiteral>
      <DSOBJLiteralItem idEVDT="String">
        <LiteralString>! !</LiteralString>  <!-- blank = default version -->
      </DSOBJLiteralItem>
    </DSOBJLiteral>
  </VersionObj>
  <ERPARAM idItem="1" idType="MathNumeric" wCopyWord="IN">
    <DSOBJFormControl idObject="21"/>
  </ERPARAM>
</GBRFI>
```

---

## 6. Cross-Object Reference Map

### 6.1 Object Dependency Graph

```
APPL (P01012)
 ├── F9860.SIMID1 ──────────────────────► DSTR/PO (T01012)
 ├── SVRHDR.ProcessingOptionTemplateName ► DSTR/PO (T01012)
 ├── FDASPEC type-2 .BusinessViewName ───► BSVW (V0101E)
 ├── FDASPEC type-8 .DSOBJBSTableColumn ► BSVW (V0101E) columns
 ├── GBRSPEC.GBRBF.szTmplName ──────────► DSTR (D0100018, etc.)
 ├── GBRSPEC.GBRBF.szFuncName ──────────► BSFN function names
 ├── GBRSPEC.GBRFI.applicationName ─────► Other APPLs (P1782, etc.)
 └── F9865 lists forms ─────────────────► FDASPEC/GBRSPEC per form

BSVW (V0101E)
 ├── BSVW.szTable ──────────────────────► TBLE (F0101)
 └── Bob_Column.szDict ─────────────────► DD aliases

BSFN C (B0100032)
 ├── F9862.SIDSTNM ─────────────────────► DSTR (D0100032)
 ├── F9863.SIOBNMRL ────────────────────► TBLE (F0115)
 └── BUSFUNC.szDsTmplName ──────────────► DSTR (D0100032)

BSFN NER (N0100062)
 ├── F9862.SIDSTNM ─────────────────────► DSTR (D0100062)
 ├── F9862.SIEVSK ──────────────────────► GBRSPEC GUID filename
 ├── BUSFUNC.szDsTmplName ──────────────► DSTR (D0100062)
 └── GBRSPEC.GBRFileIOOp.szView ────────► BSVW references

TBLE (F0101)
 ├── DDCLMN/*.TDOBND ───────────────────► DD aliases
 ├── GBRLINK.EventSpecKey ──────────────► GBRSPEC GUID
 └── F9860.SIPFX ──────────────────────► Column prefix for SQL names

DSTR (D0100018)
 └── DSTemplateDetail.DDAlias ──────────► DD aliases
```

### 6.2 How Objects Reference Each Other in PAR Files

| From Object | Reference Mechanism | To Object | Field/Element |
|-------------|---------------------|-----------|---------------|
| APPL | F9860.SIMID1 | DSTR (PO) | T01012 links app to PO template |
| APPL | FDASPEC type-2 FormDef | BSVW | `BusinessViewName="V0101E"` |
| APPL | FDASPEC type-5 Column | TBLE column | `<et:Dbref szTable="F0101" szDict="AN8"/>` |
| APPL | FDASPEC type-8 FI DS | BSVW column | `<DSOBJBSTableColumn szView="V0101E">` |
| APPL | GBRSPEC GBRBF | BSFN | `szFuncName`, `szTmplName` |
| APPL | GBRSPEC GBRFI | APPL | `applicationName`, `formName` |
| APPL | GBRSPEC GBRFileIOOp | BSVW | `szView="V0101E"` |
| APPL | SVRHDR | DSTR (PO) | `ProcessingOptionTemplateName` |
| APPL | SVRDTL | DSTMPL | `FormInterconnectTemplateName` |
| BSFN | F9862.SIDSTNM | DSTR | Data structure template name |
| BSFN | F9862.SIEVSK | GBRSPEC | GUID filename (NER only) |
| BSFN C | F9863.SIOBNMRL | TBLE | Related table name |
| BSFN NER | GBRSPEC.szView | BSVW | Business view in I/O ops |
| BSVW | BSVW.szTable | TBLE | Source table name |
| BSVW | Bob_Column.szDict | DD | Data dictionary aliases |
| TBLE | DDCLMN.TDOBND | DD | Column DD alias |
| TBLE | GBRLINK.EventSpecKey | GBRSPEC | Table trigger event rules |
| DSTR | DSTemplateDetail.DDAlias | DD | Parameter DD alias |

---

## 7. XML Namespaces

All spec XML files use the following namespace declarations:

| Prefix | URI | Usage |
|--------|-----|-------|
| (default) | `http://peoplesoft.com/e1/metadata/v1.0` | All primary elements |
| et: | `http://peoplesoft.com/e1/metadata/v1.0/erptypes` | `et:Dbref`, `et:DdOverrides`, `et:ERPDate` |
| xs: | `http://www.w3.org/2001/XMLSchema` | Schema reference (declared but not directly used) |

---

## 8. Complete Inner PAR Contents by Object Type

### Summary Table

| Component | TBLE | BSVW | BSFN C | BSFN NER | DSTR (BSFN) | DSTR (PO) | APPL |
|-----------|------|------|--------|----------|-------------|-----------|------|
| manifest.xml | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| F9860.xml | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| F9861.xml | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| F9862.xml | | | ✓ | ✓ | | | |
| F9863.xml | | | ✓ | ✓ | | | |
| F9865.xml | | | | | | | ✓ |
| specs.zip | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| include/ | ✓ | ✓ | ✓ | | | | |
| source/ | | | ✓ | | | | |
| DDCLMN/ | ✓ | | | | | | |
| GBRSPEC/ | ✓ | | | ✓ | | | ✓ |
| GBRLINK/ | ✓ | | | | | | ✓ |
| BUSVIEW/ | | ✓ | | | | | |
| BUSFUNC/ | | | ✓ | ✓ | | | |
| DSTMPL/ | | | | | ✓ | ✓ | ✓ |
| POTEXT/ | | | | | | ✓ | |
| FDASPEC/ | | | | | | | ✓ |
| FDATEXT/ | | | | | | | ✓ |
| SVRHDR/ | | | | | | | ✓ |
| SVRDTL/ | | | | | | | ✓ |

---

## 9. Methodology for Creating and Modifying PAR Files

### 9.1 General Approach

Since PAR files are standard ZIP archives containing structured XML, they can be created and modified programmatically:

1. **Extract** the PAR (unzip) into a working directory
2. **Parse and modify** the XML files
3. **Repackage** the modified files back into ZIP format with `.par` extension

### 9.2 Creating a New Object PAR

**Step 1: Create the directory structure**

For example, a new table `F55TEST`:
```
TBLE_F55TEST_60_99/
├── manifest.xml           (UTF-16)
├── F9860.xml              (UTF-8)
├── F9861.xml              (UTF-8)
├── include/
│   └── F55TEST.h
└── specs/                 (will become specs.zip)
    ├── DDCLMN/
    │   ├── F55TEST.COL1.xml
    │   └── F55TEST.COL2.xml
    ├── GBRSPEC/           (empty if no table triggers)
    └── GBRLINK/           (empty if no table triggers)
```

**Step 2: Generate F9860.xml**

Use the standard `<table name="F9860"><row><col>` format. Set SIFUNO to match the object type, assign the correct SIFUNU use code, set system code and column prefix.

**Step 3: Generate F9861.xml**

Set SIJDEVERS="E920", SISTCE="3" (production), SIMRGMOD="C", SIMRGOPT="2".

**Step 4: Generate type-specific specs**

Follow the XML schemas documented in Section 4 for the relevant object type.

**Step 5: Package**

1. ZIP the contents of `specs/` into `specs.zip`
2. ZIP all files (manifest.xml, F98xx.xml, specs.zip, include/, source/) into the inner PAR
3. For a project PAR, ZIP all inner PARs plus the outer manifest into the project PAR

### 9.3 Modifying an Existing Object

1. Extract the outer PAR (unzip)
2. Extract the target inner PAR (unzip)
3. Extract specs.zip if needed (unzip)
4. Modify the relevant XML files
5. Repackage specs.zip
6. Repackage the inner PAR
7. Update the outer manifest if object references changed
8. Repackage the outer PAR

### 9.4 Key Rules for Valid PAR Files

1. **GUID consistency:** Every GBRSPEC filename GUID must match its corresponding GBRLINK EventSpecKey and (for NERs) the F9862.SIEVSK value
2. **Object name consistency:** SIOBNM in F9860/F9861/F9862/F9863 must all match
3. **DS template linkage:** F9862.SIDSTNM and BUSFUNC.szDsTmplName must reference an existing DSTR object
4. **Manifest completeness:** Every file in the PAR must be listed in the inner manifest's `<filelist>`, and every inner PAR must appear in the outer manifest's `<filelist>` and `<omwProject>`
5. **Namespace declarations:** All spec XMLs must include the three namespace declarations (default, et:, xs:)
6. **Encoding:** manifest.xml must be UTF-16; F98xx.xml must be UTF-8; spec XMLs should include both UTF-16 BOM prefix and UTF-8 content (the dual-encoding pattern observed in JDE-generated files)
7. **Column prefix:** For tables, DDCLMN SQL column names must follow the `{SIPFX}{DDAlias}` pattern
8. **Form/control IDs:** Within an APPL, each control ObjectId must be unique per form; FDASPEC filenames must use the correct type codes

### 9.5 Template Generation Checklist

When creating a new PAR file from scratch, ensure:

- [ ] Outer manifest includes all inner PARs in `<filelist>` and `<omwProject>`
- [ ] Each inner PAR has its own manifest with correct `<filelist>`
- [ ] F9860 has correct SIFUNO (TBLE/BSVW/BSFN/APPL/DSTR) and SIFUNU codes
- [ ] F9861 has E920 version and production status
- [ ] For BSFNs: F9862 has function name and DS template; F9863 lists related tables (C) or is empty (NER)
- [ ] For APPLs: F9865 lists all forms with correct form types and entry point flags
- [ ] All GBRLINK EventSpecKeys resolve to existing GBRSPEC GUID filenames
- [ ] All business view references (szView) point to valid BSVW objects
- [ ] All DD alias references (szDict, DDAlias, TDOBND) use valid Data Dictionary items
- [ ] All DS template references (szTmplName, SIDSTNM) point to valid DSTR objects
- [ ] Processing option template (SIMID1, ProcessingOptionTemplate) links APPL to its T-prefix DSTR

---

## 10. Quick Reference: F9860 SIFUNO/SIFUNU by Object Type

| Object Type | SIFUNO | SIFUNU | Prefix Pattern | SISRCLNG |
|-------------|--------|--------|----------------|----------|
| Table | TBLE | 210 | F + system + seq | blank |
| Business View | BSVW | 300 | V + system + seq | blank |
| BSFN (C) | BSFN | 310* | B + system + seq | C |
| BSFN (NER) | BSFN | 310* | N + system + seq | NER |
| BSFN (Table Conversion) | BSFN | 310* | X + system + seq | NER |
| Data Structure (BSFN) | DSTR | 320 | D + system + seq | blank |
| Data Structure (PO) | DSTR | 360 | T + app number | blank |
| Application (Interactive) | APPL | 164 | P + system + seq | blank |
| Application (Batch/UBE) | APPL | 180 | R + system + seq | blank |

*Note: SIFUNU for BSFNs may vary; the F9860 from the sample shows no explicit 310 but the function use type is implied by SIFUNO=BSFN.

---

## Appendix A: Sample Minimal PAR File Templates

### A.1 Minimal DSTR (BSFN Data Structure)

```xml
<!-- F9860.xml -->
<?xml version='1.0' encoding='UTF-8'?>
<table name="F9860">
  <row>
    <col name="SIOBNM">D5500001  </col>
    <col name="SIMD">Custom Data Structure                                      </col>
    <col name="SISY">55  </col>
    <col name="SISYR">55  </col>
    <col name="SIFUNO">DSTR</col>
    <col name="SIFUNU">320</col>
    <col name="SIPFX">  </col>
    <col name="SISRCLNG">   </col>
    <!-- remaining cols with defaults -->
  </row>
</table>

<!-- F9861.xml -->
<?xml version='1.0' encoding='UTF-8'?>
<table name="F9861">
  <row>
    <col name="SIOBNM">D5500001  </col>
    <col name="SIJDEVERS">E920      </col>
    <col name="SISTCE">3</col>
    <col name="SIMRGMOD">C</col>
    <col name="SIMRGOPT">2</col>
  </row>
</table>

<!-- specs/DSTMPL/D5500001.xml -->
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<DSTemplate szTmplName="D5500001" TemplateType="BSFN" nVersData="100"
            xmlns="http://peoplesoft.com/e1/metadata/v1.0"
            xmlns:xs="http://www.w3.org/2001/XMLSchema"
            xmlns:et="http://peoplesoft.com/e1/metadata/v1.0/erptypes">
  <DSTemplateDetails>
    <DSTemplateDetail ItemID="1" DisplaySequence="1"
                      CopyWord="EMPTY" DDAlias="AN8"
                      FieldName="mnAddressNumber"
                      LengthInVersData="50"/>
    <DSTemplateDetail ItemID="2" DisplaySequence="2"
                      CopyWord="EMPTY" DDAlias="ALPH"
                      FieldName="szAlphaName"
                      LengthInVersData="82"/>
  </DSTemplateDetails>
</DSTemplate>
```

### A.2 Minimal TBLE (Table)

```xml
<!-- F9860.xml -->
<?xml version='1.0' encoding='UTF-8'?>
<table name="F9860">
  <row>
    <col name="SIOBNM">F5500001  </col>
    <col name="SIMD">Custom Table                                                </col>
    <col name="SISY">55  </col>
    <col name="SISYR">55  </col>
    <col name="SIFUNO">TBLE</col>
    <col name="SIFUNU">210</col>
    <col name="SIPFX">CU</col>
    <col name="SIPARDLL">JDBTRIG   </col>
  </row>
</table>

<!-- specs/DDCLMN/F5500001.AN8.xml -->
<?xml version='1.0' encoding='UTF-8'?>
<table name="F98711">
  <row>
    <col name="TDOBNM">F5500001</col>
    <col name="TDOBND">AN8</col>
    <col name="TDSQLC">CUAN8</col>
    <col name="TDPSEQ">1</col>
  </row>
</table>
```

### A.3 Minimal BSVW (Business View)

```xml
<!-- specs/BUSVIEW/V5500001.xml -->
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<BSVW szView="V5500001" szTable="F5500001"
      szDescription="Custom View"
      xmlns="http://peoplesoft.com/e1/metadata/v1.0"
      xmlns:xs="http://www.w3.org/2001/XMLSchema"
      xmlns:et="http://peoplesoft.com/e1/metadata/v1.0/erptypes">
  <Bob_TableCollection>
    <Bob_Table idPrimaryIndex="1" szTable="F5500001"/>
  </Bob_TableCollection>
  <DbrefCollection>
    <et:Dbref szTable="F5500001" szDict="AN8"/>
  </DbrefCollection>
  <Bob_ColumnCollection>
    <Bob_Column iFlags="1" nSeq="0" szTable="F5500001" szDict="AN8"/>
    <Bob_Column nSeq="1" szTable="F5500001" szDict="ALPH"/>
  </Bob_ColumnCollection>
</BSVW>
```

---

## Appendix B: Hungarian Notation Prefixes for Field Names

| Prefix | Data Type | Example |
|--------|-----------|---------|
| mn | Math Numeric (MATH_NUMERIC) | mnAddressNumber |
| sz | String (char array) | szAlphaName |
| c | Single character | cSearchType |
| jd | Julian Date (JDEDATE) | jdDateUpdated |
| IT_ | Processing Option item | IT_SearchType |

---

## Appendix C: Glossary of Key Abbreviations

| Abbreviation | Full Name |
|-------------|-----------|
| APPL | Application (interactive program) |
| BSFN | Business Function |
| BSVW | Business View |
| DSTR | Data Structure |
| TBLE | Table |
| FDA | Form Design Aid |
| GBRSPEC | Event Rule Specification |
| GBRLINK | Event Rule Link |
| NER | Named Event Rule |
| OMW | Object Management Workbench |
| PAR | Package Assembly Repository |
| PO | Processing Option |
| TER | Table Event Rule |
| UBE | Universal Batch Engine |
| DD | Data Dictionary |
| FI | Form Interconnect |
| DS | Data Structure |
