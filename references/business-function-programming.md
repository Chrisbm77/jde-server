# JD Edwards EnterpriseOne Tools 9.2 - Business Function Programming Reference

> **Source:** Development Standards for Business Function Programming Guide  
> **Part Number:** E53574-05  
> **Applies to:** JD Edwards EnterpriseOne Tools 9.2

---

## Table of Contents

1. [Overview](#1-overview)
2. [Naming Conventions](#2-naming-conventions)
3. [Ensuring Readability](#3-ensuring-readability)
4. [Declaring and Initializing Variables](#4-declaring-and-initializing-variables)
5. [General Coding Guidelines](#5-general-coding-guidelines)
6. [Coding for Portability](#6-coding-for-portability)
7. [JDE Defined Structures](#7-jde-defined-structures)
8. [Implementing Error Messages](#8-implementing-error-messages)
9. [Data Dictionary Triggers](#9-data-dictionary-triggers)
10. [Unicode Compliance Standards](#10-unicode-compliance-standards)
11. [Standard Header and Source File Templates](#11-standard-header-and-source-file-templates)
12. [Glossary](#12-glossary)

---

## 1. Overview

Business functions are reusable routines that can be called from event rules (ER) or other business functions. They are programmed in C code or as Named Event Rules (NER). Business functions encapsulate complex logic, database operations, and calculations that would be impractical to implement directly in event rules.

This reference covers development standards for writing C-based business functions in JD Edwards EnterpriseOne 9.2, including naming conventions, coding guidelines, portability, Unicode compliance, and standard templates.

---

## 2. Naming Conventions

### 2.1 Source and Header File Names

Business function source and header files follow the format `bxxyyyy`:

| Component | Description |
|-----------|-------------|
| `b` | Identifies the object as a business function (BSFN) |
| `xx` | Two-character system code |
| `yyyy` | Sequential number (up to 5 digits) |

**Rules:**
- Maximum 8 characters total
- Source file extension: `.c`
- Header file extension: `.h`
- Source and header files share the same base name
- Example: `b0100032.c` and `b0100032.h`

### 2.2 Function Names

#### External Business Functions

External business function names have no strict character limit but must be descriptive and use PascalCase.

**Signature format:**
```c
JDEBFRTN (ID) JDEBFWINAPI FunctionName
   (LPBHVRCOM lpBhvrCom,
    LPVOID    lpVoid,
    LPDSDXXXXXXX lpDS);
```

#### Internal Function Names

Internal functions follow the format `Ixxxxxx_a`:

| Component | Description |
|-----------|-------------|
| `I` | Prefix identifying an internal function |
| `xxxxxx` | Source file name (without extension) |
| `_` | Separator |
| `a` | Function description (max 32 chars, PascalCase, no spaces) |

**Rules:**
- Maximum 42 characters total
- Description portion: maximum 32 characters
- Use PascalCase for the description portion
- No spaces allowed

**Example:** `Ib0100032_ValidateAddressNumber`

**Internal function prototype format:**
```c
type XXXXXXXX_AAAAAAAA(parameter list...);
```

### 2.3 Variable Names

All variables use Hungarian prefix notation with a maximum of 32 characters.

| Prefix | Data Type | Description |
|--------|-----------|-------------|
| `c` | JCHAR | Single character |
| `sz` | JCHAR[] | NULL-terminated JCHAR string |
| `z` | ZCHAR | Non-Unicode character |
| `zz` | ZCHAR[] | NULL-terminated ZCHAR string |
| `n` | short | Short integer |
| `l` | long | Long integer |
| `b` | BOOL | Boolean |
| `mn` | MATH_NUMERIC | Math numeric |
| `jd` | JDEDATE | JDE date |
| `lp` | pointer | Long pointer |
| `i` | int | Integer |
| `by` | BYTE | Byte |
| `ul` | unsigned long | Unsigned long |
| `us` | unsigned short | Unsigned short |
| `ds` | struct | Data structures |
| `h` | handle | Handle |
| `e` | enum | Enumerated type |
| `id` | ID (long int) | JDE return type |
| `ut` | JDEUTIME | JDE time |

**Rules:**
- Maximum 32 characters per variable name
- Use descriptive names after the prefix
- Follow PascalCase after the prefix (e.g., `szCustomerName`)

### 2.4 Business Function Data Structure Names

Data structures follow the format `DxxyyyyA`:

| Component | Description |
|-----------|-------------|
| `D` | Identifies object as a data structure |
| `xx` | Two-character system code |
| `yyyy` | Next available sequential number |
| `A` | Alphabetical suffix |

**Rules:**
- Always include the alphabetical suffix `A` even for a single data structure
- If multiple data structures exist for the same function, increment the suffix: `A`, `B`, `C`, etc.
- Example: `D0100032A`, `D0100032B`

---

## 3. Ensuring Readability

### 3.1 Change Log

Every business function must maintain a modification log recording all changes. The change log uses the format:

| Field | Description |
|-------|-------------|
| SAR Number | Software Action Request number |
| Date | Date of the change |
| Initials | Programmer's initials |
| Comment | Description of the change |

**Example:**
```c
/*****************************************************************
 * Source File: B0100032
 * Description: Example Business Function
 *   History:
 *     Date      Programmer  SAR# - Description
 *     ---------- ---------- ----------------------------
 *   Author 03/15/2006       - Created
 *   JDE    09/22/2007  SAR 1234567 - Added validation
 **********************************************************/
```

### 3.2 Comments

**Rules:**
- Use only C-style comments: `/* */`
- Do NOT use C++ style comments: `//`
- Maximum 80 characters per line width
- Place comments on a separate line before the code they describe
- Never nest comments within comments (causes server build errors)

**Correct comment style:**
```c
/* SAR 1234567 Begin*/
/* Populate the lpDS->OrderedPlacedBy value from the userID only in
   the ADD mode */
   if ( lpDS->cHeaderActionCode == _J('1'))
   {
      if (IsStringBlank(lpDS->szOrderedPlacedBy))
      {
         jdeStrcpy((JCHAR *)(lpDS->szOrderedPlacedBy),
                    (const JCHAR *)(lpDS->szUserID));
      }
   }
/* SAR 1234567 End */
```

**INCORRECT - Comments within comments (causes build errors on some servers):**
```c
/* SAR 1234567 Begin
/* Populate the lpDS->OrderedPlacedBy value from the userID only in
   the ADD mode
*/
```

### 3.3 Indentation

- Use **3 spaces** for each level of indentation
- Do NOT use tabs

### 3.4 Compound Statements

- Always use braces `{ }` for compound statements, even single-line bodies
- Place opening and closing braces on separate lines
- One statement per line

**Correct:**
```c
if (condition)
{
   statement;
}
else
{
   statement;
}
```

---

## 4. Declaring and Initializing Variables

### 4.1 Define Statements (`#define`)

- Place `#define` statements in the **source file** by default
- If a `#define` must be shared across files, place it in the **header file** and prefix with the BSFN name to ensure uniqueness
- Enter names in uppercase, separated by underscores

### 4.2 Typedef Statements

Structure names should be prefixed by the Source File Name to prevent conflicts with structures in other business functions.

### 4.3 Function Prototypes

#### External BSFN Prototype (in header file):
```c
JDEBFRTN (ID) JDEBFWINAPI GenericBusinessFunction
              (LPBHVRCOM    lpBhvrCom,
               LPVOID       lpVoid,
               LPDSDXXXXXXX lpDS);
```

#### Internal Function Prototype (in header file):
```c
type XXXXXXXX_AAAAAAAA(parameter list...);
```

### 4.4 Initializing Variables

**Rules:**
- Declare all variables at the **beginning** of the function block
- One variable per line
- Explicitly initialize every variable
- Initialize pointers to NULL with a type cast
- Initialize data structures to zero using `memset`
- Initialize MATH_NUMERIC and JDEDATE to `{0}`

**Example:**
```c
/***********************************************************
 * Variable Definitions
 ***********************************************************/
   ID          idReturnValue  = ER_SUCCESS;
   ID          idJDBReturn    = JDEDB_PASSED;
   HUSER       hUser          = (HUSER) NULL;
   HREQUEST    hRequestF0101  = (HREQUEST) NULL;
   short       nNumColsF0101  = 0;
   JCHAR       szErrorMessageID[5] = _J("\0");
   MATH_NUMERIC mnVariable    = {0};
   JDEDATE     jdToDate;

/***********************************************************
 * Initialize Data Structures
 ***********************************************************/
   memset((void *)(&dsF0101), (int)('\0'),
          sizeof(dsF0101));
```

### 4.5 Standard Variables

#### Flag Variables
```c
BOOL  bReturnPointer   = FALSE;  /* Return Pointer Flag */
BOOL  bErrorCode       = FALSE;  /* Error Code Flag     */
```

#### I/O Parameters
| Variable | Description |
|----------|-------------|
| `cReturnPointer` | Controls pointer return behavior |
| `cErrorCode` | Error code character |
| `cSuppressErrorMessage` | When `1`, suppresses error display |
| `szErrorMessageId` | 4-character error message ID |

#### Fetch Variables
```c
ID          idJDEDBResult       = JDEDB_PASSED;
ID          idReturnValue       = ER_SUCCESS;
ID          idTableXXXXID       = 0;
ID          idIndexXXXXID       = 0;
unsigned short usXXXXNumColToFetch = 0;
unsigned short usXXXXNumOfKeys     = 0;
```

---

## 5. General Coding Guidelines

### 5.1 Calling External Business Functions (jdeCallObject)

Use `jdeCallObject` to call external business functions:

```c
idReturnCode = jdeCallObject(
   _J("FunctionName"),        /* Business function name */
   NULL,                      /* Function library (NULL = default) */
   lpBhvrCom,                 /* Behavior communications */
   lpVoid,                    /* Void pointer */
   (void *)&dsDataStructure,  /* Data structure */
   (CALLMAP *)&cm_DXXXXXXX,   /* Call map */
   ND0000000,                 /* Number of CALLMAP entries */
   (JCHAR *)NULL,             /* Transaction key */
   (JCHAR *)NULL,             /* Reserved */
   (int)0);                   /* Flags */
```

**CALLMAP** is used to map error IDs between the calling and called business functions:
```c
CALLMAP cm_D0000026[2] = {{IDERRmnDisplayExchgRate_62,
                            IDERRmnExchangeRate_2}};
```

### 5.2 Calling Internal Business Functions

#### Without return value (CALLIBF):
```c
CALLIBF(Ib0100032_ValidateAddress,
        lpBhvrCom,
        lpVoid,
        lpDS);
```

#### With return value (CALLIBFRET):
```c
idReturnValue = CALLIBFRET(Ib0100032_CalculateAmount,
                           lpBhvrCom,
                           lpVoid,
                           lpDS);
```

**Note:** CALLIBF and CALLIBFRET are used only for internal functions within the same DLL.

### 5.3 Passing Pointers Between Business Functions

Use the pointer storage array (maximum 100 locations) with a GENLNG index passed through the data structure:

**Store a pointer:**
```c
jdeStoreDataPtr(lpBhvrCom,
                (void *)lpPointer,
                (LPGENLNG)&lpDS->idPointerIndex);
```

**Retrieve a pointer:**
```c
lpPointer = (TYPE *)jdeRetrieveDataPtr(
               lpBhvrCom,
               lpDS->idPointerIndex);
```

**Remove a pointer (when done):**
```c
jdeRemoveDataPtr(lpBhvrCom,
                 lpDS->idPointerIndex);
```

### 5.4 Memory Management

**Allocating memory:**
```c
lpBuffer = (TYPE *)jdeAlloc(JDE_ALLOC_SIZE,
                             nBufferSize,
                             MEM_ZEROINIT);
```

**Releasing memory:**
```c
jdeFree((void *)lpBuffer);
lpBuffer = NULL;
```

**For event rule callers** (releasing memory passed from a BSFN):
Use `B4000640 - FreePtrToDataStructure` to allow event rules to free memory allocated by a BSFN.

### 5.5 Database Operations (hUser / hRequest)

**Initialize behavior (hUser):**
```c
idJDBReturn = JDB_InitBhvr(lpBhvrCom,
                            &hUser,
                            (JCHAR *) NULL,
                            JDEDB_COMMIT_AUTO);
```

**Open a table (hRequest):**
```c
eJDBReturn = JDB_OpenTable(hUser,
                           ID_F0911,
                           ID_F0911_DOC_TYPE__NUMBER___B,
                           idColF0911,
                           nNumColsF0911,
                           (JCHAR *)NULL,
                           &hRequestF0911);
```

**Close table and free behavior:**
```c
JDB_CloseTable(hRequestF0911);
JDB_FreeBhvr(hUser);
```

### 5.6 Typecasting

- Always typecast if your parameter does not match the function parameter
- `JCHAR szArray[13]` is NOT the same as `(JCHAR *)` in a function declaration; typecast `(JCHAR *)` as required
- **Never** typecast on the left-hand side of an assignment (causes data loss)

**Incorrect:**
```c
(short)nValue = (long)lValue;  /* WRONG - data loss */
```

### 5.7 Comparison Testing

- Use explicit comparison tests (not implicit truthy/falsy)
- No embedded assignments inside conditions
- Use `<=` or `>=` for floating-point comparisons (never `==`)

### 5.8 String Operations

#### jdeStrcpy (same-length strings):
```c
jdeStrcpy((JCHAR *)(lpDS->szOrderedPlacedBy),
          (const JCHAR *)(lpDS->szUserID));
```

#### jdeStrncpy (different-length strings):
```c
jdeStrncpy((JCHAR *)(lpDS->szDescription),
           (const JCHAR *)(_J("DefaultValue")),
           DIM(lpDS->szDescription) - 1);
```

**Note:** The count parameter in `jdeStrncpy` is the number of **characters** (not bytes), and it excludes the NULL terminator. Use `DIM()` macro for character count, not `sizeof()`.

### 5.9 Function Cleanup Area

All resource cleanup should occur in a designated "Function Clean Up" section:

```c
/***********************************************************
 * Function Clean Up
 ***********************************************************/
   if (hRequestF0911)
   {
      JDB_CloseTable(hRequestF0911);
   }
   if (hUser)
   {
      JDB_FreeBhvr(hUser);
   }
   return idReturnValue;
```

### 5.10 Exit Points

- **Prefer a single exit point** at the end of the function
- Use `idReturnValue` (set to `ER_SUCCESS` or `ER_ERROR`) to control flow
- Avoid multiple `return` statements scattered throughout the function

**Pattern:**
```c
ID idReturnValue = ER_SUCCESS;

/* Main processing */
if (error_condition)
{
   idReturnValue = ER_ERROR;
}

if (idReturnValue == ER_SUCCESS)
{
   /* Continue processing */
}

/* Function Clean Up */
return idReturnValue;
```

### 5.11 Terminating a Function

Always end a business function by returning a value. The standard return types are:
- `ER_SUCCESS` - Function completed successfully
- `ER_ERROR` - Function encountered an error

---

## 6. Coding for Portability

### 6.1 Portability Concepts

Portability is the ability to run a program on more than one system platform without modification. JD Edwards EnterpriseOne is a portable environment. Standards affecting portability include ANSI, X/OPEN, and ISO SQL standards.

### 6.2 Portability Guidelines

| Guideline | Details |
|-----------|---------|
| ANSI Compatibility | Business functions must be ANSI-compatible. Do not use non-ANSI exceptions without approval from the Business Function Standards Committee. |
| Data Alignment | Do not create programs that depend on data alignment (byte vs. word allocation varies by system). |
| Vendor Libraries | Vendor libraries and function calls are system-dependent. Programs compiled with a different compiler may fail. |
| Pointer Arithmetic | Use caution; pointer arithmetic is system-dependent and based on data alignment. |
| Variable Initialization | Always explicitly initialize variables. Do not assume all systems initialize the same way. |
| Offsets | Use caution with offsets to retrieve values within data structures (relates to data alignment). |
| Typecasting | Always typecast if your parameter does not match the function parameter. |
| Left-hand Typecasting | Never typecast on the left-hand side of an assignment (causes data loss). |
| C++ Comments | Do not use C++ comments (`//`). Use C-style `/* */` only. |

### 6.3 Preventing Common Server Build Errors

#### Comments within Comments
Never nest comments. Each `/*` must be followed by `*/` before another `/*` appears.

#### New Line Character at End of File
Always add a new line character (press Enter) at the end of every source and header file. Some servers require this to build correctly.

#### NULL Character
Use `'\0'` (backslash zero), NOT `'/0'` (forward slash zero). The forward slash version is NOT the NULL character and will not be caught by the compiler.

**Correct:**
```c
memset((void *)(&dsStructure), (int)('\0'), sizeof(DSD4000260A));
```

#### Lowercase Letters in Include Statements
Always use **lowercase** letters in `#include` statements. Uppercase letters cause build errors.

**Incorrect:** `#include <B0000130.h>` (uppercase B)  
**Correct:** `#include <b0000130.h>` (lowercase b)

#### Initialized Variables That Are Not Referenced
Every variable declared and initialized must be used somewhere in the program.

---

## 7. JDE Defined Structures

### 7.1 MATH_NUMERIC Data Type

Used to represent numeric values in JD Edwards EnterpriseOne. Always use Common Library APIs to manipulate; do not access members directly.

**Structure definition:**
```c
struct tag MATH_NUMERIC
{
   ZCHAR  String[MAXLEN_MATH_NUMERIC + 1];
   BYTE   Sign;
   ZCHAR  EditCode;
   short  nDecimalPosition;
   short  nLength;
   WORD   wFlags;
   ZCHAR  szCurrency[4];
   Short  nCurrencyDecimals;
   short  nPrecision;
};
typedef struct tag MATH_NUMERIC MATH_NUMERIC, FAR *LPMATH_NUMERIC;
```

**MATH_NUMERIC Members:**

| Element | Description |
|---------|-------------|
| String | The digits without separators |
| Sign | Minus sign indicates negative; otherwise 0x00 |
| EditCode | Data dictionary edit code for formatting display |
| nDecimalPosition | Number of digits from the right to place the decimal |
| nLength | Number of digits in the String |
| wFlags | Processing flags |
| szCurrency | Currency code |
| nCurrencyDecimals | Number of currency decimals |
| nPrecision | Data dictionary size |

**Key APIs:**
- **MathCopy** - Assign MATH_NUMERIC values (preserves currency info). Always use instead of flat assignment.
- **ZeroMathNumeric** - Initialize local MATH_NUMERIC variables (prevents invalid currency data)
- **FormatMathNumeric** - Retrieve string value in JCHAR format
- **jdeMathGetRawString** - Retrieve string value in ZCHAR format
- **jdeMathSetCurrencyCode / jdeMathSetCurrencyCodeUNI** - Set currency code (ZCHAR / JCHAR versions)

**Initialization pattern:**
```c
MATH_NUMERIC  mnVariable = {0};

ZeroMathNumeric(&mnVariable);
MathCopy(&mnVariable, &lpDS->mnVariable);
```

### 7.2 JDEDATE Data Type

Used to represent dates in JD Edwards EnterpriseOne.

**Structure definition:**
```c
struct tag JDEDATE
{
   short nYear;
   short nMonth;
   short nDay;
};
typedef struct tag JDEDATE JDEDATE, FAR *LPJDEDATE;
```

**Assigning JDEDATE variables:**
Always use `memcpy` (not flat assignment) to prevent lost data from scoping issues:

```c
JDEDATE  jdToDate;

memcpy((void*) &jdToDate,
       (const void *) &lpDS->jdFromDate,
       sizeof(JDEDATE));
```

**JDEDATECopy macro:**
```c
#define JDEDATECopy(pDest, pSource)
        memcpy(pDest, pSource, sizeof(JDEDATE))
```

---

## 8. Implementing Error Messages

### 8.1 Understanding Error Messages

Messages communicate information to end-users. Two types of text substitution messages exist:
- **Error messages** (glossary group E)
- **Workflow messages** (glossary group Y)

Text substitution messages replace variables in the message with specific information at runtime.

### 8.2 Standard JDB Error Codes

| Error ID | Description |
|----------|-------------|
| 078D | Open Table Failed |
| 078E | Close Table Failed |
| 078F | Insert to Table Failed |
| 078G | Delete from Table Failed |
| 078H | Update to Table Failed |
| 078I | Fetch from Table Failed |
| 078J | Select from Table Failed |
| 078K | Set Sequence of Table Failed |
| 078S | Initialization of Behavior Failed (no text substitution) |

### 8.3 Standard JDE Cache Error Codes

| Error ID | Description |
|----------|-------------|
| 078L | Initialization of Cache Failed |
| 078M | Open Cursor Failed |
| 078N | Fetch from Cache Failed |
| 078O | Add to Cache Failed |
| 078P | Update to Cache Failed |
| 078Q | Delete from Cache Failed |
| 078R | Terminate of Cache Failed |

### 8.4 Error Message Parameters in lpDS

Include these parameters in every business function data structure:

| Parameter | Alias | Description |
|-----------|-------|-------------|
| `cSuppressErrorMessage` | SUPPS | When `1`, suppress `jdeErrorSet` from auto-displaying errors. Valid: `1` or `0`. |
| `szErrorMessageID` | DTAI | 4-character error message ID returned by the BSFN. **Must be initialized to 4 spaces** at function start. |

### 8.5 Setting Error Messages

**Standard error pattern:**
```c
if ((!IsStringBlank(lpDS->szErrorMessageID)) &&
    (lpDS->cSuppressErrorMessage != _J('1')))
{
   jdeStrcpy((JCHAR*)(lpDS->szErrorMessageID),
              (const JCHAR*)(_J("0653")));
   jdeErrorSet(lpBhvrCom, lpVoid, (ID) IDERRcMethodofComputation_1,
               lpDS->szErrorMessageID, (LPVOID) NULL);
   idReturnValue = ER_ERROR;
}
```

### 8.6 Initializing Behavior Errors

Call the Initialize Behavior function before any database operations. Set error 078S if it fails:

```c
idJDBReturn = JDB_InitBhvr(lpBhvrCom,
                            &hUser,
                            (JCHAR *) NULL,
                            JDEDB_COMMIT_AUTO);
if (idJDBReturn != JDEDB_PASSED)
{
   jdeStrcpy(lpDS->szErrorMessageID, _J("078S"));
   if (lpDS->cSuppressErrorMessage != _J('1'))
   {
      jdeErrorSet(lpBhvrCom, lpVoid, (ID)0, _J(078S), (LPVOID) NULL);
   }
   return ER_ERROR;
}
```

### 8.7 Text Substitution for Error Messages

Text substitution is accomplished through the data dictionary. To use text substitution:

1. Load a data structure with the information to substitute in the error message
2. Call `jdeErrorSet` to set the error

**Example with JDB_OpenTable failure:**
```c
if (eJDBReturn != JDEDB_PASSED)
{
   memset((void *)(&dsDE0022), 0x00, sizeof(dsDE0022));
   jdeStrncpy((JCHAR *)dsDE0022.szDescription,
              (const JCHAR *)(_J("F0911")),
              DIM(dsDE0022.szDescription)-1);
   jdeErrorSet(lpBhvrCom, lpVoid, (ID)0, _J("078D"), &dsDE0022);
}
```

### 8.8 Mapping Data Structure Errors with jdeCallObject

When calling an external BSFN, match error IDs from the original function to the called function's IDs using CALLMAP:

```c
CALLMAP cm_D0000026[2] = {{IDERRmnDisplayExchgRate_62,
                            IDERRmnExchangeRate_2}};

idReturnCode = jdeCallObject(_J("EditExchangeRateTolerance"),
                             NULL,
                             lpBhvrCom,
                             lpVoid,
                             (void *)&dsD0000026,
                             (CALLMAP *)&cm_D0000026,
                             ND0000026,
                             (JCHAR *)NULL,
                             (JCHAR *)NULL,
                             (int)0);
```

---

## 9. Data Dictionary Triggers

Data dictionary triggers attach edit-and-display logic to data dictionary items. The application runtime engine executes the trigger when a DD item is accessed in a form.

Custom data dictionary triggers:
- Can be written in C or as Named Event Rules (NER)
- Require a specific data structure with 3 predefined members and 1 variable member

**Custom Trigger Data Structure:**

| Structure Member | Alias | Description |
|-----------------|-------|-------------|
| `idBhvrErrorId` | BHVRERRID | Returns error status (ER_ERROR or ER_SUCCESS) to the application |
| `szBehaviorEditString` | BHVREDTST | Used by the runtime engine to pass the data dictionary field value to the trigger function |
| `szDescription001` | DL01 | Returns the description value to the application |
| `szHomeCompany, mnAddressNumber` | HMCO, AN8 | Used to set errors (CALLMAP field) |

The three predefined members are the same for every custom trigger. The variable member is different for each trigger, created using the specific data element associated with the data dictionary item.

---

## 10. Unicode Compliance Standards

### 10.1 Unicode Concepts

The Unicode Standard is the universal character-encoding scheme. Key facts:
- Unicode uses two bytes per character
- Supports up to 64,000 characters (with surrogates for an additional 1 million)
- `0x00` is a valid byte in a Unicode character
- Normal string functions (`strlen`, `strcpy`) do NOT work with Unicode data

**Character type mapping:**

| Old Syntax | Non-Unicode (ZCHAR) | Unicode (JCHAR) |
|------------|-------------------|-----------------|
| `char` | ZCHAR | JCHAR |
| `char *`, PSTR | ZCHAR*, PZSTR | JCHAR*, PJSTR |
| `'A'` | `_Z('A')` | `_J('A')` |
| `"string"` | `_Z("string")` | `_J("string")` |

### 10.2 Unicode String Functions

| Old Function | Non-Unicode | Unicode |
|-------------|-------------|---------|
| `strcpy()` | `jdeZStrcpy()` | `jdeStrcpy()` |
| `strlen()` | `jdeZStrlen()` | `jdeStrlen()` |
| `strstr()` | `jdeZStrstr()` | `jdeStrstr()` |
| `sprintf()` | `jdeZSprintf()` | `jdeSprintf()` |
| `strncpy()` | `jdeZStrncpy()` | `jdeStrncpy()` |

**Important notes:**
- The `jdeStrcpy()` function replaced the older `jdestrcpy()` function
- Use `jdeStrncpyTerminate()` where `jdestrcpy()` was previously used
- Do not use traditional string functions (`strcpy`, `strlen`, `printf`)
- All `jdeStrxxxxxx` functions handle strings explicitly
- Use **character length** (not byte count) with `sizeof()` returns bytes; use `DIM()` for character count
- The third parameter of `jdeStrncpy()` is the number of **characters**, not bytes

**Example:**
```c
/* Unicode Compliant */
jdeStrncpy(dsKey1F38112.dxdcto,
           (const JCHAR *)(dsF4311ZDetail->pwdcto),
           DIM(dsKey1F38112.dxdcto) - 1);
```

### 10.3 Unicode Memory Functions

The `memset()` function works byte-by-byte. For Unicode:
- Use `memset` when filling with NULL (`'\0'`)
- Use `jdeMemset` when setting characters to values other than NULL

**jdeMemset** sets memory character-by-character (the third parameter is the number of **bytes**):
```c
/* Unicode Compliant */
jdeMemset((void *)(szSubsidiaryBlank), _J(' '),
          (sizeof(szSubsidiaryBlank) - (1*sizeof(JCHAR))));
```

### 10.4 Pointer Arithmetic

When advancing a JCHAR pointer, add the **character count** (not byte count). Since pStringPtr is declared as `JCHAR *`, adding MAXSTRLENGTH to it advances by `MAXSTRLENGTH * sizeof(JCHAR)` bytes automatically.

```c
#define MAXSTRLENGTH 10
JCHAR *pStringPtr;

/* This advances by 10 characters (20 bytes in Unicode) */
pStringPtr = pStringPtr + MAXSTRLENGTH;
```

**Warning:** Do NOT use `MAXSTRLENGTH * sizeof(JCHAR)` — this would advance twice as far as intended, causing memory corruption.

### 10.5 Offsets

When using byte offsets with a JCHAR pointer, cast to `(BYTE *)` first:
```c
lpTemp1 = (BYTE *)lpData + lpKeyStruct->CacheKey[n].nOffset;
```

In a Unicode environment, if casting to `(JCHAR *)`, the pointer advances by `nOffset * 2` bytes, which is incorrect. Cast to `(BYTE *)` to get the correct byte-based offset.

### 10.6 MATH_NUMERIC APIs (Unicode)

MATH_NUMERIC string members are in **ZCHAR** format. The Common Library API provides both JCHAR and ZCHAR versions:

**Retrieve string value (JCHAR):**
```c
JCHAR szJobNumber[MAXLEN_MATH_NUMERIC+1] = _J("\0");
FormatMathNumeric(szJobNumber, &lpDS->mnJobnumber);
```

**Retrieve string value (ZCHAR):**
```c
ZCHAR zzJobNumber[MAXLEN_MATH_NUMERIC+1] = _Z("\0");
zzJobNumber = jdeMathGetRawString(&lpDS->mnJobnumber);
```

**Set currency code:**
```c
ZCHAR zzCurrencyCode[4] = _Z("USD");
JCHAR szCurrencyCode[4] = _J("USD");

/* ZCHAR version */
jdeMathSetCurrencyCode(&lpDs->mnAmount, (ZCHAR *) zzCurrencyCode);

/* JCHAR version */
jdeMathSetCurrencyCodeUNI(&lpDs->mnAmount, (JCHAR *) szCurrencyCode);
```

### 10.7 Third-Party APIs

When calling non-Unicode third-party APIs:
1. Declare both a Unicode and non-Unicode variable for each string parameter
2. Convert Unicode strings to non-Unicode before calling: `jdeFromUnicode()`
3. Call the API with non-Unicode strings
4. Convert returned strings back to Unicode: `jdeToUnicode()`

```c
JCHAR szStateName[31] = _J("\0");
ZCHAR zzStateName[31] = _Z("\0");
/* Convert to non-unicode */
jdeFromUnicode(zzStateName, szStateName, DIM(zzStateName), NULL);
/* Call API */
bReturnStatus = GetStateName(zzStateName, zzStateName);
/* Convert back to unicode */
jdeToUnicode(szStateName, zzStateName, DIM(szStateName), NULL);
```

### 10.8 Flat-File APIs

Default flat-file I/O (e.g., `jdeFprintf()`) converts data to Unicode. For files read by third-party systems, use the encoding-aware APIs:
- `fwrite`/`fread`, `fprintf`/`fscanf`, `fputs`/`fgets`, `fputc`/`fgetc` (converted versions)
- Pass `lpBhvrCom` as an additional parameter for code page configuration

**JDE internal file (Unicode encoding):**
```c
FILE *fp;
fp = jdeFopen(_J( c:/testBSFNZ.txt), _J(w+));
jdeFprintf(fp, _J("%s%d\n"), _J("Line "), 1);
jdeFclose(fp);
```

**Third-party file (configured encoding):**
```c
FILE *fp;
fp = jdeFopen(_J( c:/testBSFNZ.txt), _J(w+));
jdeFprintfConvert(lpBhvrCom, fp, _J("%s%d\n"), _J("Line "), 1);
jdeFclose(fp);
```

### 10.9 Cryptographic APIs

#### HMAC-SHA-256 (Release 9.2.9.3)
```c
jde_HMAC_SHA256_string()  /* Compute HMAC-SHA256 hash */
```

#### AES-128 CTR Mode Encryption (Release 9.2.26.2)
```c
/* Initialize encryption context */
jdeSystemEncryptDataAESCTRInit(huser, key_b64, key_b64len,
                                iv_b64, iv_b64len, &enc_ctx);

/* Encrypt and Base64 encode */
jdeSystemEncryptDataAESCTR(huser, enc_ctx,
                           (BYTE *)plaintext, plaintext_len,
                           &b64ciphertext, &b64ciphertext_len);

/* Free context */
jdeSystemFreeDataAESCTR(huser, enc_ctx);
```

#### SHA-256 Hash of a File (Release 9.2.26.2)
```c
jdeSystemSHA256HashFile(huser, filename, sha256hash, &sha256hash_len);
```

---

## 11. Standard Header and Source File Templates

### 11.1 Standard Header File Template

```c
/*****************************************************************
 * Header File: BXXXXXXX.h
 * Description: Generic Business Function Header File
 *   History:
 *     Date      Programmer  SAR# - Description
 *     ---------- ---------- ----------------------------
 *   Author MM/DD/YYYY       - Created
 *
 * Copyright (c) Oracle, YYYY
 *
 * This unpublished material is proprietary to Oracle.
 * All rights reserved. The methods and
 * techniques described herein are considered trade secrets
 * and/or confidential. Reproduction or distribution, in whole
 * or in part, is forbidden except by express written permission
 * of Oracle.
 **********************************************************/
#ifndef __BXXXXXXX_H
#define __BXXXXXXX_H

/*****************************************************************
 * Table Header Inclusions
 *****************************************************************/

/*****************************************************************
 * External Business Function Header Inclusions
 *****************************************************************/

/*****************************************************************
 * Global Definitions
 *****************************************************************/

/*****************************************************************
 * Structure Definitions
 *****************************************************************/

/*****************************************************************
 * DS Template Type Definitions
 *****************************************************************/

/*****************************************************************
 * Source Preprocessor Definitions
 *****************************************************************/
#if defined (JDEBFRTN)
   #undef JDEBFRTN
#endif

#if defined (WIN32)
   #if defined (WIN32)
      #define JDEBFRTN(r) __declspec(dllexport) r
   #else
      #define JDEBFRTN(r) __declspec(dllimport) r
   #endif
#else
   #define JDEBFRTN(r) r
#endif

/*****************************************************************
 * Business Function Prototypes
 *****************************************************************/
JDEBFRTN (ID) JDEBFWINAPI GenericBusinessFunction
              (LPBHVRCOM    lpBhvrCom,
               LPVOID       lpVoid,
               LPDSDXXXXXXXX lpDS);

/*****************************************************************
 * Internal Function Prototypes
 *****************************************************************/

#endif /* __BXXXXXXX_H */
```

### 11.2 Header File Sections Explained

| Section | Description |
|---------|-------------|
| **Business Function Name and Description** | Define the name, describe the function, maintain the modification log |
| **Copyright Notice** | Oracle copyright notice (required, do not modify) |
| **Header Definition** | The `#define` of the business function, generated by the tool (do not modify) |
| **Table Header Inclusions** | `#include` statements for table headers accessed by the BSFN (use **lowercase** letters) |
| **External Business Function Header Inclusions** | `#include` statements for externally called BSFNs (use **lowercase** letters) |
| **Global Definitions** | Global constants in UPPERCASE, separated by underscores |
| **Structure Definitions** | Structures used by the BSFN, prefixed by source file name |
| **DS Template Type Definitions** | Business function data structure definitions (generated from OMW or Data Structure Design) |
| **Source Preprocessing Definitions** | Entry point definition and opening bracket (do not modify) |
| **Business Function Prototypes** | External function prototypes |
| **Internal Function Prototypes** | Internal function prototypes |

---

## 12. Glossary

| Term | Definition |
|------|-----------|
| **Business Function** | A reusable routine that encapsulates business logic, callable from event rules or other business functions. Can be written in C or as Named Event Rules (NER). |
| **Named Event Rule (NER)** | A business function implemented using the Event Rules scripting language rather than C code. |
| **BSFN** | Abbreviation for Business Function. |
| **Data Structure** | A defined set of parameters used to pass data between a calling program and a business function. |
| **CALLMAP** | A mapping structure used with `jdeCallObject` to match error IDs between calling and called business functions. |
| **Hungarian Notation** | A naming convention where variable names begin with a lowercase prefix indicating the data type. |
| **MATH_NUMERIC** | A JDE-defined structure for representing numeric values with currency and precision information. |
| **JDEDATE** | A JDE-defined structure for representing dates with year, month, and day components. |
| **JCHAR** | A Unicode character type (2 bytes) used throughout JDE for internationalization. |
| **ZCHAR** | A non-Unicode character type (1 byte) used for legacy and non-Unicode APIs. |
| **jdeCallObject** | The API used to call an external business function from within another business function. |
| **CALLIBF / CALLIBFRET** | Macros for calling internal business functions within the same DLL (without/with return value). |
| **hUser** | A handle to a database user session, obtained via `JDB_InitBhvr`. |
| **hRequest** | A handle to a database table request, obtained via `JDB_OpenTable`. |
| **lpBhvrCom** | Pointer to the behavior communications structure passed to every business function. |
| **lpVoid** | A void pointer passed to every business function for framework use. |
| **lpDS** | Pointer to the business function's data structure. |
| **ER_SUCCESS** | Return value indicating successful function completion. |
| **ER_ERROR** | Return value indicating a function error occurred. |
| **SAR** | Software Action Request - a change tracking identifier. |
| **DIM()** | Macro that returns the number of characters in an array (as opposed to `sizeof()` which returns bytes). |
| **ODBC** | Open Database Connectivity - a standard database interface for portability. |
| **Text Substitution** | A method of inserting variable values into predefined error or workflow messages at runtime. |

---

## Quick Reference: Complete Business Function Skeleton

```c
/* === HEADER FILE (bxx0001.h) === */

#ifndef __BXX0001_H
#define __BXX0001_H

/* Table Header Inclusions */
#include <b0100032.h>

/* External BSFN Header Inclusions */

/* Global Definitions */
#define BXX0001_MAX_RECORDS  100

/* DS Template Type Definitions */
/* (paste from OMW/Data Structure Design) */

/* Source Preprocessing Definitions */
#if defined (JDEBFRTN)
   #undef JDEBFRTN
#endif
/* ... platform-specific defines ... */

/* Business Function Prototypes */
JDEBFRTN (ID) JDEBFWINAPI MyBusinessFunction
              (LPBHVRCOM    lpBhvrCom,
               LPVOID       lpVoid,
               LPDSDXX0001A lpDS);

/* Internal Function Prototypes */
static ID Ibxx0001_ValidateInput(LPBHVRCOM, LPVOID, LPDSDXX0001A);

#endif /* __BXX0001_H */


/* === SOURCE FILE (bxx0001.c) === */

#include <jde.h>
#include "bxx0001.h"

/******************************************************************
 * Business Function: MyBusinessFunction
 * Description: Performs specific business logic
 * Parameters:
 *   LPBHVRCOM  lpBhvrCom - Behavior communications
 *   LPVOID     lpVoid    - Void pointer
 *   LPDSDXX0001A lpDS    - Data structure pointer
 * Returns: ER_SUCCESS or ER_ERROR
 ******************************************************************/
JDEBFRTN (ID) JDEBFWINAPI MyBusinessFunction
              (LPBHVRCOM    lpBhvrCom,
               LPVOID       lpVoid,
               LPDSDXX0001A lpDS)
{
   /************************************************************
    * Variable Definitions
    ************************************************************/
   ID           idReturnValue      = ER_SUCCESS;
   ID           idJDBReturn        = JDEDB_PASSED;
   HUSER        hUser              = (HUSER) NULL;
   HREQUEST     hRequestF0101      = (HREQUEST) NULL;
   JCHAR        szErrorMessageID[5] = _J("\0");
   MATH_NUMERIC mnAmount           = {0};
   JDEDATE      jdEffectiveDate;

   /************************************************************
    * Initialize Data Structures
    ************************************************************/
   memset((void *)(&jdEffectiveDate), (int)('\0'),
          sizeof(JDEDATE));

   /************************************************************
    * Initialize Behavior
    ************************************************************/
   idJDBReturn = JDB_InitBhvr(lpBhvrCom,
                               &hUser,
                               (JCHAR *) NULL,
                               JDEDB_COMMIT_AUTO);
   if (idJDBReturn != JDEDB_PASSED)
   {
      jdeStrcpy(lpDS->szErrorMessageID, _J("078S"));
      if (lpDS->cSuppressErrorMessage != _J('1'))
      {
         jdeErrorSet(lpBhvrCom, lpVoid, (ID)0,
                     _J("078S"), (LPVOID) NULL);
      }
      return ER_ERROR;
   }

   /************************************************************
    * Main Processing
    ************************************************************/
   ZeroMathNumeric(&mnAmount);

   /* Validate input */
   idReturnValue = CALLIBFRET(Ibxx0001_ValidateInput,
                              lpBhvrCom,
                              lpVoid,
                              lpDS);

   if (idReturnValue == ER_SUCCESS)
   {
      /* Perform business logic here */
   }

   /************************************************************
    * Function Clean Up
    ************************************************************/
   if (hRequestF0101)
   {
      JDB_CloseTable(hRequestF0101);
   }
   if (hUser)
   {
      JDB_FreeBhvr(hUser);
   }

   return idReturnValue;
}
```

---

*Reference document generated from JD Edwards EnterpriseOne Tools 9.2 Development Standards for Business Function Programming Guide (E53574-05).*
