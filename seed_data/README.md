## TPOT Programs Registry: Seed Dataset

A characteristic set of data expected in the TPOT Programs Registry. The data is available in three formats:

**1. JSON**

This data format is used for load through Alembic migration

**2. CSV**

This data format is used for load through SQLAlchemy raw psycopg2 connection

**3. SQL**

This data format is the fall back seeding option for load through SQLAlchemy raw psycopg2 connection

### Managing Seed Data

The datasets in the 3 formats can be updated using Mockaroo online data generator and CodeBeautify.

1. Access Mockaroo online > `DATASETS` and upload the current set of csv files. Because there are foreign key associations with this data, all datasets need to be uploaded
2. Go to `SCHEMAS` > `Create a Schema` > `More` > `Import fields from Excel/CSV header...` > paste in the header from respective csv file > `Replace existing fields` and create a schema each of the uploaded CSV datasets
3. For each of the new schemas create, choose column type `Dataset Column` and import the corresponding field from the uploaded csv
4. Apply the required changes (adding/removing/editing fields) and `Download Data` as .SQL file, check the `include create table` option
5. In the .SQL file, Mockaroo will save (intended) blank values as empty strings (`''` or `""`). SQL insert (used to load data from .sql) does not cast empty string for none string fields so for consistency across all field types, blank values need to be represented with a `NULL`. Run _find/replace_ on each of the generated .SQL files to make this change i.e replace any instances of `''` or `""` with `NULL`.
6. Use any SQL-to-JSON converter (e.g [Code Beautify](https://codebeautify.org/sql-to-json-converter)) to generate the corresponding JSON data for each .SQL file
7. Use any SQL-to-CSV converter (e.g [ConvertCSV](http://www.convertcsv.com/sql-to-csv.htm#)) to generate corresponding JSON data from each .SQL file. **_Note: the delimiter in the saved CSV file needs to be `'|'`_**

#### Important Notes 

##### Foreign Key Data Relationships

For schemas that have a foreign key relationship, upload the .CSV dataset with updated foreign key reference data before updating the schema that refers to those fields

##### Conditional Table Creation

To support a smoother upload process, update the create statement in each of the generated .SQL file to `CREATE TABLE **IF NOT EXISTS**` instead of `CREATE TABLE` so that data seeding through Python script continues to seamlessly with schema creation which happens using Alembic migration




