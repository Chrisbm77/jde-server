# Key JDE Rules (Always Apply)

These rules apply to every JDE development task regardless of object type:

1. **Naming conventions**: Custom objects use system codes 55-59. Object names follow `{Prefix}{SystemCode}{Sequence}` (e.g., F5500001, P5500001).

2. **Object prefixes**: F=Table, V=View, B=C BSFN, N=NER BSFN, D=BSFN DS, T=PO DS, P=Interactive App, R=Report/UBE, X=Table Conversion BSFN.

3. **Data Dictionary first**: Every column, parameter, and field must reference a valid DD alias. Create DD items before creating objects that use them.

4. **Business View intermediary**: Applications never access tables directly — always through a Business View. The chain is: APPL → BSVW → TBLE.

5. **PAR file integrity**: GUIDs in GBRLINK must match GBRSPEC filenames. F9862.SIEVSK must match the NER's GBRSPEC GUID. All files must appear in manifest.xml.

6. **Processing Options**: Every interactive application (P-prefix) should have a PO data structure (T-prefix) linked via F9860.SIMID1 and SVRHDR.ProcessingOptionTemplateName.

7. **Event rule data sources**: Use the correct DSOBJ element for each data source type (DSOBJFormControl, DSOBJVariable, DSOBJMember, DSOBJBSTableColumn, DSOBJLiteral, etc.).

8. **UTF encoding**: manifest.xml = UTF-16, F98xx.xml = UTF-8, spec XMLs = UTF-8 with UTF-16 BOM prefix (dual-encoded).

## Workflow for Creating a New JDE Object

1. **Scaffold** → Run `scaffold.py` to generate the directory structure and boilerplate XML
2. **Fill in specifics** → Edit the generated XML files with actual column definitions, event rules, form controls, etc.
3. **Validate** → Run `validate_par.py` to check internal consistency
4. **Transform** → Run `xml_transform.py add-bom` to restore the dual-encoding for spec XMLs
5. **Package** → Run `par_pack.py pack` to create the importable .par file
6. **Review** → Extract and inspect the final PAR to confirm structure

## Workflow for Modifying an Existing JDE Object

1. **Extract** → Run `par_pack.py extract` on the exported .par file
2. **Transform** → Run `xml_transform.py strip-bom` and `prettify` for readable XML
3. **Modify** → Edit the relevant XML files
4. **Validate** → Run `validate_par.py` to check consistency
5. **Transform** → Run `xml_transform.py add-bom` to restore encoding
6. **Package** → Run `par_pack.py pack` to create the modified .par file
