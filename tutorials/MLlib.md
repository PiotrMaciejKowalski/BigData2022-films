# Wstęp do pakietu MLlib

Choć domyślnym sposobem pracy we współczesnych modelach analizy danych jest 
budowanie ich w Pythonie, to czasami nie jest możliwe np. gdy mamy do przetworzenia
duże ilości danych. W takich przypadkach należy rozważyć użycie Apache Spark, 
który daje możliwości modelowania w środowisku rozproszonym oraz jest jednym z 
narzędzi o największych możliwościach przetwarzania. 

W tym tutorialu pokażemy jak używać pakietu MLlib oraz zademonstrujemy kilka
prostych modeli ML na przykładzie zbioru Iris. Więcej informacji o pakiecie 
MLlib możemy znaleźć na stronie [Spark Apache](https://spark.apache.org/docs/1.2.1/mllib-guide.html).

## Przygotowanie danych
W naszych przykładach użyjemy popularnego datasetu Iris, w którym wykonaliśmy 
transformację liczbową na kolumnie SPECIES.

```python
from pyspark.sql.functions import col, when

iris = (spark.read.format('csv')
        .option("header", False)
        .schema(schemat)
        .load('/content/drive/MyDrive/iris.data')
)
iris = (iris.withColumn("SPECIES",
                       when(col("SPECIES")=='Iris-virginica', 1)
                       .when(col("SPECIES")=='Iris-setosa', 2)
                       .when(col("SPECIES")=='Iris-versicolor', 3))
       .withColumnRenamed("SPECIES", "labels")
)

iris.show(5)
```
```commandline
+-----+-------+-----+-------+------+
|P_LEN|P_WIDTH|S_LEN|S_WIDTH|labels|
+-----+-------+-----+-------+------+
|  5.1|    3.5|  1.4|    0.2|     2|
|  4.9|    3.0|  1.4|    0.2|     2|
|  4.7|    3.2|  1.3|    0.2|     2|
|  4.6|    3.1|  1.5|    0.2|     2|
|  5.0|    3.6|  1.4|    0.2|     2|
+-----+-------+-----+-------+------+
only showing top 5 rows
```
### Podziału label-features
Klasa `VectorAssembler` transformuje wiele kolumn zawierających cechy i zamienia je 
na wektor.

```python
from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
    inputCols=['P_LEN', 'P_WIDTH', 'S_LEN', 'S_WIDTH'],
    outputCol="features"
    )
stages = [assembler]
```

Przy tworzeniu modelu użyjemy klasy `Pipeline` z biblioteki pyspark.ml.
Definiuje ona sekwencję etapów przetwarzania, przekształcania i modelowania danych. 
Pipeline składa się z szeregu etapów 'Transformers' i 'Estimators', 
które są wykonywane w określonej kolejności.

```python
from pyspark.ml import Pipeline

pipeline = Pipeline(stages = stages)

pipelineModel = pipeline.fit(iris)

iris_training_ready = (
    pipelineModel
    .transform(iris)
    .select('labels', 'features')
)

iris_training_ready.limit(5).toPandas()
```

```commandline
   labels	                                         features
0	2	[5.099999904632568, 3.5, 1.399999976158142, 0....
1	2	[4.900000095367432, 3.0, 1.399999976158142, 0....
2	2	[4.699999809265137, 3.200000047683716, 1.29999...
3	2	[4.599999904632568, 3.0999999046325684, 1.5, 0...
4	2	[5.0, 3.5999999046325684, 1.399999976158142, 0...
```
### Podział na dane treningowe i testowe
Do podziału danych wystarczy użyć metody `randomSplit`. 
Podajemy w niej listę wag, według której podzielony będzie nasz zbiór.

```python
train, test = iris_training_ready.randomSplit([0.9, 0.1])
print(train.count())
print(test.count())
```
```commandline
136
14
```
Widzimy, że w zbiorze treningowym znajduje się 136 obserwacji, a w zbiorze 
testowym 14.

## Przykładowe modele

### Model regresji logistycznej
Rozpoczniemy od prostego modelu regresji logistycznej.

```python
from pyspark.ml.classification import LogisticRegression

model = LogisticRegression(featuresCol = 'features', labelCol = 'labels', maxIter = 10)
```
Uczymy model na danych treningowych.

```python
trained_model = model.fit(train)
```
Wewnątrz obiektu `summary` znajdziemy wszystkie parametry i wyniki dla 
naszego dopasowanego modelu,

```python
[x for x in dir(trained_model.summary) if x[0] != '_']
```
```commandline
['accuracy',
 'fMeasureByLabel',
 'falsePositiveRateByLabel',
 'featuresCol',
 'labelCol',
 'labels',
 'objectiveHistory',
 'precisionByLabel',
 'predictionCol',
 'predictions',
 'probabilityCol',
 'recallByLabel',
 'totalIterations',
 'truePositiveRateByLabel',
 'weightCol',
 'weightedFMeasure',
 'weightedFalsePositiveRate',
 'weightedPrecision',
 'weightedRecall',
 'weightedTruePositiveRate']
```
```python
trained_model.summary.accuracy
```
```commandline
0.9779411764705882
```
Widzimy, że accuracy wyniosło w tym przypadku ponad 97%. \
Jeśli chcielibyśmy ewaluować nasz model oraz dobrać odpowiednie parametry to 
możemy to zrobić za pomocą klasy `TrainValidationSplit`.

```python
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator 
from pyspark.ml.tuning import TrainValidationSplit, ParamGridBuilder

lr = LogisticRegression()

grid = (ParamGridBuilder()
    .baseOn({lr.labelCol: 'label', 
             lr.featuresCol: 'features'})
    .addGrid(lr.regParam, [0.0, 0.5, 1.0, 1.5])
    .build()
)

evaluator = MulticlassClassificationEvaluator()

tvs = TrainValidationSplit(estimator=lr, 
                           estimatorParamMaps=grid, 
                           evaluator=evaluator, 
                           trainRatio=0.9)

tvsModel = tvs.fit(iris_training_ready)
```
Za pomocą `ParamGridBuilder` budujemy siatkę parametrów, po której będzie poruszała 
się wybrana metoda ewaluacji, w tym przypadku `MulticlassClassificationEvaluator`.
Parametr `trainRatio` określa jaka cześć zbioru będzie użyta do treningu. 

```python
tvsModel.bestModel.summary.accuracy
```
```commandline
0.9866666666666667
```
Dzięki przetestowaniu różnych parametrów modeli regresji logistycznej udało się 
znaleźć taki, dla którego accuracy wyniosło ponad 98%. \
Wykorzystanie metody walidacji krzyżowej wygląda analogicznie.
```python
from pyspark.ml.tuning import CrossValidator

cv = CrossValidator(estimator=lr, 
                    estimatorParamMaps=grid, 
                    evaluator=evaluator,
                    numFolds=4,
                    parallelism=2)

cvModel = cv.fit(iris_training_ready)
cvModel.bestModel.summary.accuracy
```
```commandline
0.9866666666666667
```
Parametr `numFolds` określa, na ile podzbiorów będzie podzielony dataset. Natomiast 
`parallelism` odpowiada za zrównoleglenie obliczeń. 


### Predykcja

Predykcji dokonujemy za pomocą metody `transform` w której możemy podać nasz zbiór testowy.

```python
predictions = trained_model.transform(test)
predictions.limit(10).toPandas()
```

```commandline

   labels	                                        features	                                   rawPrediction	                                   probability	 prediction
0	1	[5.599999904632568, 2.799999952316284, 4.90000...	[-3.596499578409393, 9.65763969821197, -10.368...	[1.7447911424833221e-06, 0.9952747771851232, 1...	1.0
1	1	[5.699999809265137, 2.5, 5.0, 2.0]	                [-3.717922609117387, 11.769620734958313, -13.0...	[1.8765908671859442e-07, 0.9989050551880966, 1...	1.0
2	1	[5.800000190734863, 2.700000047683716, 5.09999...	[-3.642944226172327, 10.227192720357504, -11.8...	[9.403353304180036e-07, 0.9931313534493658, 2....	1.0
3	1	[6.099999904632568, 2.5999999046325684, 5.5999...	[-3.658941141463517, 7.97803929797475, -12.052...	[4.954920885715546e-06, 0.5609357445140748, 1....	1.0
4	1	[6.800000190734863, 3.200000047683716, 5.90000...	[-3.6231353953193968, 16.187685997232226, -18....	[2.490339600906048e-09, 0.9999746430096541, 1....	1.0
5	1	[7.199999809265137, 3.5999999046325684, 6.0999...	[-3.5396537422778214, 17.499321834347516, -19....	[7.292671508443068e-10, 0.9999945876527925, 1....	1.0
6	1	[7.599999904632568, 3.0, 6.599999904632568, 2....	[-3.7571999150982336, 19.080848945711455, -23....	[1.206565102623312e-10, 0.9999754956999174, 2....	1.0
7	2	[5.0, 3.5999999046325684, 1.399999976158142, 0...	[-2.7808934186828465, -26.065177562558862, 20....	[1.2757830252307842e-10, 9.85236971645125e-21,...	2.0
8	3	[4.900000095367432, 2.4000000953674316, 3.2999...	[-3.456122376724005, -5.165886206327869, 1.713...	[3.136186054797474e-05, 5.673627550608295e-06,...	3.0
9	3	[5.5, 2.299999952316284, 4.0, 1.2999999523162842]	[-3.6136439077413223, 1.9009824411595986, -5.6...	[1.6474404583137234e-05, 0.004090548256132597,...	3.0
```

### Drzewo decyzyjne

Innym przykładem modelu służącemu do klasyfikacji jest drzewo decyzyjne. 
Wywołanie klasy `DecisionTreeClassifier` oraz dopasowanie modelu wygląda analogicznie 
jak w przypadku regresji logistycznej.

```python
from pyspark.ml.classification import DecisionTreeClassifier

dt = DecisionTreeClassifier(featuresCol = 'features', labelCol = 'labels', maxDepth = 3)
dtModel = dt.fit(train)
predictions = dtModel.transform(test)
predictions.limit(10).toPandas()
```

```commandline
   labels	                                         features	       rawPrediction	           probability	     prediction
0	1	[5.599999904632568, 2.799999952316284, 4.90000...	[0.0, 39.0, 0.0, 1.0]	[0.0, 0.975, 0.0, 0.025]	    1.0
1	1	[5.699999809265137, 2.5, 5.0, 2.0]	                [0.0, 39.0, 0.0, 1.0]	[0.0, 0.975, 0.0, 0.025]	    1.0
2	1	[5.800000190734863, 2.700000047683716, 5.09999...	[0.0, 39.0, 0.0, 1.0]	[0.0, 0.975, 0.0, 0.025]	    1.0
3	1	[6.099999904632568, 2.5999999046325684, 5.5999...	[0.0, 3.0, 0.0, 2.0]	[0.0, 0.6, 0.0, 0.4]	            1.0
4	1	[6.800000190734863, 3.200000047683716, 5.90000...	[0.0, 39.0, 0.0, 1.0]	[0.0, 0.975, 0.0, 0.025]	    1.0
5	1	[7.199999809265137, 3.5999999046325684, 6.0999...	[0.0, 39.0, 0.0, 1.0]	[0.0, 0.975, 0.0, 0.025]	    1.0
6	1	[7.599999904632568, 3.0, 6.599999904632568, 2....	[0.0, 39.0, 0.0, 1.0]	[0.0, 0.975, 0.0, 0.025]	    1.0
7	2	[5.0, 3.5999999046325684, 1.399999976158142, 0...	[0.0, 0.0, 49.0, 0.0]	[0.0, 0.0, 1.0, 0.0]	            2.0
8	3	[4.900000095367432, 2.4000000953674316, 3.2999...	[0.0, 1.0, 0.0, 41.0]	[0.0, 0.023809523809523808...	    3.0
9	3	[5.5, 2.299999952316284, 4.0, 1.2999999523162842]	[0.0, 1.0, 0.0, 41.0]	[0.0, 0.023809523809523808...	    3.0
```

### Klastrowanie

Do klastrowania danych możemy użyć algorytmu k-średnich i klasy `KMeans`. 
W pakiecie MLlib znajdują się również metody ewaluacji modeli jak np `ClusteringEvaluator`.

```python
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.clustering import KMeans

kmeans = KMeans().setK(3)
model = kmeans.fit(train)

predictions = model.transform(train)

evaluator = ClusteringEvaluator()
silhouette = evaluator.evaluate(predictions)
print("Silhouette with squared euclidean distance = " + str(silhouette))

model.summary.predictions.show(5)
```

```commandline
Silhouette with squared euclidean distance = 0.7522124869541736
+------+--------------------+----------+
|labels|            features|prediction|
+------+--------------------+----------+
|     1|[4.90000009536743...|         1|
|     1|[5.80000019073486...|         1|
|     1|[5.80000019073486...|         1|
|     1|[5.90000009536743...|         1|
|     1|[6.0,2.2000000476...|         1|
+------+--------------------+----------+
only showing top 5 rows
```

### PCA
Do zmniejszenia liczby wymiarów możemy użyć algorytmu PCA. Wywołanie 
przebiega następująco:

```python
from pyspark.ml.feature import PCA

pca = PCA(k=2, inputCol="features")
pca.setOutputCol("pca_features")
model = pca.fit(train)

features = model.transform(train)
features.show(5)
```

```commandline
+------+--------------------+--------------------+
|labels|            features|        pca_features|
+------+--------------------+--------------------+
|     1|[4.90000009536743...|[-6.0155091733474...|
|     1|[5.80000019073486...|[-6.9085974889527...|
|     1|[5.80000019073486...|[-7.0791582734907...|
|     1|[5.90000009536743...|[-6.8828186812519...|
|     1|[6.0,2.2000000476...|[-6.7950916056033...|
+------+--------------------+--------------------+
only showing top 5 rows
```
