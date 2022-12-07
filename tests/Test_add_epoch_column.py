import pytest

def test_add_epoch_column(sample_size):
  
  result = []
  exp_result = []

  title_basics_epoch = add_epoch_column(title_basics)
  columns_names = title_basics_epoch.columns
  periods = [0,1901,1918,1926,1939,1954,1970,1985,1994,2009,2050]

  sample =  title_basics_epoch.rdd.takeSample(False,sample_size)

  periods_index = columns_names.index("period")
  startYear_index = columns_names.index("startYear")
  
  for i in range(sample_size):
    result.append(sample[i][periods_index])  
    for k in range(len(periods) - 1):
      if int(sample[i][startYear_index]) <= periods[k+1] and int(sample[i][startYear_index]) > periods[k]:
        exp_result.append(k+1)
  
  result = list(map(int, result))
  assert result == exp_result, 'function add_epoch_column returns wrong output'
