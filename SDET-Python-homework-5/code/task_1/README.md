# Подсчет общего количества запросов

## Bash версия
#### Использование:
```Bash
    total_requests.sh <inputfile> <outputfile> [-h]
```
#### Описание работы:
* Подсчитываем количество строк в *inputfile* с помощью
```Bash
    wc -l
```
* Выводим результат в *outputfile*

## Python версия
#### Использование:
```Bash
    python total_requests.py [-h] -i INPUTFILE -o OUTPUTFILE [--json]
```

#### Описание работы:
* Подсчитываем количество строк в *inputfile*
* Выводим результат в *outputfile*