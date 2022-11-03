# Preprocessing in Spark

One of the major limitations of Pandas is that Pandas was designed for small datasets that can be handled on a single machine and thus it does not scale well to big data. On the contrary, Apache spark was designed for big data, but it has a different API and also lacks many of the easy-to-use functionality in Pandas for data wrangling and visualization.


## 1. Loading data
After setup a SparkSession we can read out dataset using set of functions read.option.csv:

```python
df_spark=data_spark.read.option('header','true').csv('airlines.csv')
```

We might see the top 20 rows of dataset using the show() method:
```python
df_spark.show()
```

## 2. Exploring data

### 2.1. Schema of data
Typically, the first step to explore a DataFrame is to understand its schema: column names and corresponding data types.
Using printSchema() function we might check what type of data type and columns of our dataset holds and if these columns consisting any null values:
```python
df_spark.printSchema()
```
```
Output:    
root
 |-- Airport.Code: string (nullable = true)
 |-- Airport.Name: string (nullable = true)
 |-- Time.Label: string (nullable = true)
 |-- Time.Month: string (nullable = true)
 |-- Time.Month Name: string (nullable = true)
 |-- Time.Year: string (nullable = true)
 |-- Statistics.# of Delays.Carrier: string (nullable = true)
 |-- Statistics.# of Delays.Late Aircraft: string (nullable = true)
 |-- Statistics.# of Delays.National Aviation System: string (nullable = true)
 |-- Statistics.# of Delays.Security: string (nullable = true)
 |-- Statistics.# of Delays.Weather: string (nullable = true)
 |-- Statistics.Carriers.Names: string (nullable = true)
 |-- Statistics.Carriers.Total: string (nullable = true)
 |-- Statistics.Flights.Cancelled: string (nullable = true)
 |-- Statistics.Flights.Delayed: string (nullable = true)
 |-- Statistics.Flights.Diverted: string (nullable = true)
 |-- Statistics.Flights.On Time: string (nullable = true)
 |-- Statistics.Flights.Total: string (nullable = true)
 |-- Statistics.Minutes Delayed.Carrier: string (nullable = true)
 |-- Statistics.Minutes Delayed.Late Aircraft: string (nullable = true)
 |-- Statistics.Minutes Delayed.National Aviation System: string (nullable = true)
 |-- Statistics.Minutes Delayed.Security: string (nullable = true)
 |-- Statistics.Minutes Delayed.Total: string (nullable = true)
 |-- Statistics.Minutes Delayed.Weather: string (nullable = true)
``` 
But this way we always obtain the string value in every column, because it is default setting of printSchema(). We may fix it by adding one more argument **inferScema = True** in read.option().
```python
data_spark.read.option('header','true').csv('airlines.csv', inferSchema=True).printSchema()
```
```   
New output:
root
 |-- Airport.Code: string (nullable = true)
 |-- Airport.Name: string (nullable = true)
 |-- Time.Label: string (nullable = true)
 |-- Time.Month: integer (nullable = true)
 |-- Time.Month Name: string (nullable = true)
 |-- Time.Year: integer (nullable = true)
 |-- Statistics.# of Delays.Carrier: integer (nullable = true)
 |-- Statistics.# of Delays.Late Aircraft: integer (nullable = true)
 |-- Statistics.# of Delays.National Aviation System: integer (nullable = true)
 |-- Statistics.# of Delays.Security: integer (nullable = true)
 |-- Statistics.# of Delays.Weather: integer (nullable = true)
 |-- Statistics.Carriers.Names: string (nullable = true)
 |-- Statistics.Carriers.Total: integer (nullable = true)
 |-- Statistics.Flights.Cancelled: integer (nullable = true)
 |-- Statistics.Flights.Delayed: integer (nullable = true)
 |-- Statistics.Flights.Diverted: integer (nullable = true)
 |-- Statistics.Flights.On Time: integer (nullable = true)
 |-- Statistics.Flights.Total: integer (nullable = true)
 |-- Statistics.Minutes Delayed.Carrier: integer (nullable = true)
 |-- Statistics.Minutes Delayed.Late Aircraft: integer (nullable = true)
 |-- Statistics.Minutes Delayed.National Aviation System: integer (nullable = true)
 |-- Statistics.Minutes Delayed.Security: integer (nullable = true)
 |-- Statistics.Minutes Delayed.Total: integer (nullable = true)
 |-- Statistics.Minutes Delayed.Weather: integer (nullable = true)
```
In the output, the value **nullable=True** means that the column might have null values.

We may also check the data types of the columns by:
```python
df_spark.dftypes
```    
This way we obtain a list of tuples. 

By using the columns object, we can see the name of all the columns present in the dataset in the list object:
```python
df_spark.columns
```    
### 2.2 Statistical summary of data
Pyspark’s **describe**() is used to view some basic statistical details like count, mean, stddev, min and max of a DataFrame or a series of numeric:
```python
df_spark.describe().show()
```

### 2.3 Count duplicate row
Another feature we might want to check is number of duplicated rows:
```python
import pyspark.sql.functions as funcs
df_spark.groupBy(df_spark.columns).count().where(funcs.col('count') > 1).select(funcs.sum('count')).show()
```
The output is number of duplicated rows.

## 3. Cleaning data

### 3.1. Missing Data
 Spark DataFrame provide a similar function to fillna() from Pandas, but it only allows a value that matches the data type of the corresponding column.
```python 
df_spark.na.fill(0)
```
### 3.2. Drop null values
Spark provides `dropna()` function, that is used to drop rows with null values in one or multiple (any/all) columns in DataFrame.
```python
df_spark.dropna() 
```

### 3.3 Filtering Data
We can use data filtering to remove outliers.
```python
spark_df.filter("Time.Year > 2002").select("Time.Year","Time.Month")
```
### 3.4 Handle missing value with imputation

Missing numeric value can be replaced using Imputer. We might use different method by changing .setStrategy parameter ("mean", "median", "mode"):
```python
from pyspark.ml.feature import Imputer
imputer = Imputer(inputCols=column_subset, outputCols=[col_ for col_ in column_subset]).setStrategy("mean")
imputer.fit(df_spark).transform(df_spark)
```
## 4. Transforming data

### 4.1 Selecting Columns 
Spark DataFrame provides a different API than Pandas:
```python
spark_df.select('Open', 'Close')
```
### 4.2 Renaming Columns
We use withColumnRenamed() function to rename columns:
```python
spark_df.withColumnRenamed("Airport.Name", "Name")
```
### 4.3 Creating New Columns
We used the withcolumn() function to add the columns or change the existing columns in the Pyspark DataFrame. Then in that function, we will be giving two parameters: the name of the new column and the value that new column will hold.
```python
from pyspark.sql.functions import colp 
df_spark.withColumn("Sum", col("Open") + col("Close"))
```
### 4.4 Dropping Columns
Dropping the column from the dataset is a pretty straightforward task, and for that, we will be using the drop() function from PySpark.
```python
df_spark.drop('Airport.Code')
```    
 If we want to drop multiple columns from the dataset in the same instance, we can pass the list of column names as the parameter.
 
### 4.5 One-hot encoding
Spark DataFrame does not provide  function get_dummies(). A workaround is to convert the DataFrame to Pandas.
#TODO
### 4.6 Reformatting DataFrame for ML

A Spark DataFrame can be converted into a Pandas DataFrame as follows to obtain a corresponding Numpy array easily if the dataset can be handled on a single machine.
```python
spark_df.toPandas()
```
In other way it may works as follows:
```python
spark.createDataFrame(pd_df)
```
![](https://miro.medium.com/max/625/1*vEMpD7FbswFzv82WrpuG4Q.jpeg)



