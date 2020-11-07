# pandasboost

Data analysis with no compromises. Efficiency, Accuracy, Assurance - pick any three.

# Documentation


## Sub-modules

* [pandasboost.dataframe](#pandasboost.dataframe)
* [pandasboost.formatter](#pandasboost.formatter)
* [pandasboost.install_boosters](#pandasboost.install_boosters)
* [pandasboost.pandas_flavor](#pandasboost.pandas_flavor)
* [pandasboost.registration](#pandasboost.registration)
* [pandasboost.series](#pandasboost.series)

    
## Functions
    
### Function `check_keep`


>     def check_keep(
>         frame,
>         query,
>         desc
>     )


Filter a dataframe with <code>query</code> and report the number of rows affected.

###### Parameters

**```query```** :&ensp;<code>str</code>
:   Query for filtering the dataframe. Will be passed to pandas.DataFrame.query.


**```desc```** :&ensp;<code>str</code>
:   Description of the filter.



### Function `levels` 




>     def levels(
>         dataframe,
>         show_values=True
>     )


Report the number of unique values (levels) for each variable. 
Useful to inspect categorical variables.

###### Parameters

**```show_values```** :&ensp;<code>bool</code>
:   Whether to report a short sample of level values.


    
### Function `nmissing` 




>     def nmissing(
>         dataframe,
>         show_all=False
>     )


Evaluate the number of missing values in columns in the dataframe 

###### Parameters

**```show_all```** :&ensp;<code>bool</code>
:   Whether to report all columns. <code>False</code> to show only columns with
    one or more missing values.






    
# Module `pandasboost.formatter` 

    
## Functions


    
### Function `bignum`




>     def bignum(
>         n,
>         precision=0
>     )


Transform a big number into a business style representation.

###### Example

```python-repl
>>> bignum(123456)
Output: 123K
```


    
### Function `format_percentage` 




>     def format_percentage(
>         n,
>         precision='auto'
>     )


Display a decimal number in percentage.

###### Parameters

**```n```** :&ensp;<code>float</code>
:   The number to format.


**```percision```** :&ensp;<code>int, str</code>, default `'auto'`
:   The precision of outcome. Default 'auto' to automatically
    choose the least precision on which the outcome is not zero.

###### Examples

format_percentage(0.001) ==> '0.1%'
format_percentage(-0.0000010009) ==> '-0.0001%'
format_percentage(0.001, 4) ==> '0.1000%'




    
### Function `cut_groups` 




>     def cut_groups(
>         srs,
>         rules,
>         right=True,
>         missing='missing'
>     )




    
### Function `frequency` 




>     def frequency(
>         srs,
>         business=True,
>         ascending=None,
>         by_index=False
>     )


Report frequency of values.

###### Parameters

**```ascending```** :&ensp;<code>boolean</code>, default <code>None</code>
:   Whether to sort in ascending order. If none, will use ascending when sorted by index,
    and descending when sorted by frequency.


**```by_index```** :&ensp;<code>boolean</code>, default <code>True</code>
:   Whether sort result by index.


