# Resultados — Modelos Lineares Mistos

**Data:** 07/06/2026 13:18 

**Modelo:** `value ~ lesion * hand + (1 | sub)`  

**Efeito aleatório:** sujeito (`sub`)  

---

## ER

### ANOVA Tipo III (Satterthwaite)

|            |  Sum Sq| Mean Sq| NumDF|   DenDF| F value| Pr(>F)|
|:-----------|-------:|-------:|-----:|-------:|-------:|------:|
|lesion      | 66.8756| 33.4378|     2| 38.7036|  5.6436| 0.0071|
|hand        |  0.8628|  0.8628|     1| 38.0590|  0.1456| 0.7049|
|lesion:hand | 55.0987| 27.5494|     2| 38.0761|  4.6497| 0.0156|


### Post-hoc: Efeitos Simples (interação significativa)

#### Lesão por mão

|contrast |hand | estimate|     SE|      df| t.ratio| p.value|
|:--------|:----|--------:|------:|-------:|-------:|-------:|
|NS - LS  |LH   |  -3.2217| 1.4871| 55.9388| -2.1664|  0.0860|
|NS - RS  |LH   |  -5.0405| 1.4532| 55.9388| -3.4685|  0.0029|
|LS - RS  |LH   |  -1.8188| 1.5790| 55.9388| -1.1519|  0.4867|
|NS - LS  |RH   |  -4.5205| 1.4993| 56.9133| -3.0150|  0.0106|
|NS - RS  |RH   |  -2.2648| 1.4657| 56.9586| -1.5452|  0.2778|
|LS - RS  |RH   |   2.2557| 1.5790| 55.9388|  1.4286|  0.3333|


#### Mão por lesão

|contrast |lesion | estimate|     SE|      df| t.ratio| p.value|
|:--------|:------|--------:|------:|-------:|-------:|-------:|
|LH - RH  |NS     |  -0.2859| 0.8564| 38.7426| -0.3339|  0.7403|
|LH - RH  |LS     |  -1.5848| 0.9937| 38.0356| -1.5948|  0.1190|
|LH - RH  |RS     |   2.4897| 0.9547| 38.0356|  2.6078|  0.0130|


### Post-hoc: Efeitos Principais (interação não significativa)

#### Comparação entre grupos de lesão

|contrast | estimate|     SE|      df| t.ratio| p.value|
|:--------|--------:|------:|-------:|-------:|-------:|
|NS - LS  |  -3.8711| 1.3415| 38.9640| -2.8857|  0.0170|
|NS - RS  |  -3.6526| 1.3110| 38.9786| -2.7861|  0.0219|
|LS - RS  |   0.2185| 1.4207| 38.6548|  0.1538|  0.9871|


### R²

| R2_marginal| R2_condicional|
|-----------:|--------------:|
|       0.417|          0.778|

---

## Int2sub

### ANOVA Tipo III (Satterthwaite)

|            |   Sum Sq| Mean Sq| NumDF|   DenDF| F value| Pr(>F)|
|:-----------|--------:|-------:|-----:|-------:|-------:|------:|
|lesion      | 159.3751| 79.6875|     2| 38.6509|  3.6542| 0.0352|
|hand        |   0.5872|  0.5872|     1| 37.4720|  0.0269| 0.8705|
|lesion:hand |  67.4717| 33.7358|     2| 37.3831|  1.5470| 0.2262|


### Post-hoc: Efeitos Principais (interação não significativa)

#### Comparação entre grupos de lesão

|contrast | estimate|     SE|      df| t.ratio| p.value|
|:--------|--------:|------:|-------:|-------:|-------:|
|NS - LS  |   7.0751| 2.8719| 39.4760|  2.4636|  0.0469|
|NS - RS  |   5.6905| 2.7835| 38.4040|  2.0444|  0.1153|
|LS - RS  |  -1.3845| 3.0464| 39.3552| -0.4545|  0.8927|


### R²

| R2_marginal| R2_condicional|
|-----------:|--------------:|
|       0.406|           0.81|

---

## MT

### ANOVA Tipo III (Satterthwaite)

|            |     Sum Sq|    Mean Sq| NumDF| DenDF| F value| Pr(>F)|
|:-----------|----------:|----------:|-----:|-----:|-------:|------:|
|lesion      | 39474.8062| 19737.4031|     2|    38|  0.7572| 0.4759|
|hand        |   812.5650|   812.5650|     1|    38|  0.0312| 0.8608|
|lesion:hand |   814.3649|   407.1825|     2|    38|  0.0156| 0.9845|


### R²

| R2_marginal| R2_condicional|
|-----------:|--------------:|
|       0.192|          0.513|

---

## ND

### ANOVA Tipo III (Satterthwaite)

|            | Sum Sq| Mean Sq| NumDF|   DenDF| F value| Pr(>F)|
|:-----------|------:|-------:|-----:|-------:|-------:|------:|
|lesion      | 3.3366|  1.6683|     2| 35.0913|  0.4005| 0.6730|
|hand        | 0.7490|  0.7490|     1| 34.3112|  0.1798| 0.6742|
|lesion:hand | 8.0170|  4.0085|     2| 34.2637|  0.9623| 0.3921|


### R²

| R2_marginal| R2_condicional|
|-----------:|--------------:|
|       0.179|          0.502|

---

## ND_RE2sub

### ANOVA Tipo III (Satterthwaite)

|            |  Sum Sq| Mean Sq| NumDF|   DenDF|  F value| Pr(>F)|
|:-----------|-------:|-------:|-----:|-------:|--------:|------:|
|lesion      |  1.6773|  0.8387|     2| 32.7208|   3.8725| 0.0309|
|hand        | 25.0445| 25.0445|     1| 32.0468| 115.6431| 0.0000|
|lesion:hand |  0.0648|  0.0324|     2| 31.9264|   0.1496| 0.8617|


### Post-hoc: Efeitos Principais (interação não significativa)

#### Comparação entre grupos de lesão

|contrast | estimate|     SE|      df| t.ratio| p.value|
|:--------|--------:|------:|-------:|-------:|-------:|
|NS - LS  |   0.4037| 0.1486| 39.0125|  2.7162|  0.0259|
|NS - RS  |   0.2350| 0.1416| 36.7045|  1.6588|  0.2346|
|LS - RS  |  -0.1688| 0.1567| 38.4110| -1.0772|  0.5338|


#### Comparação entre mãos

|contrast | estimate|    SE|      df|  t.ratio| p.value|
|:--------|--------:|-----:|-------:|--------:|-------:|
|LH - RH  |  -1.1583| 0.108| 37.3014| -10.7244|       0|


### R²

| R2_marginal| R2_condicional|
|-----------:|--------------:|
|       0.603|          0.655|

---

## PV

### ANOVA Tipo III (Satterthwaite)

|            |   Sum Sq|  Mean Sq| NumDF|   DenDF| F value| Pr(>F)|
|:-----------|--------:|--------:|-----:|-------:|-------:|------:|
|lesion      | 351.6754| 175.8377|     2| 37.3791|  3.9492| 0.0278|
|hand        |  11.0987|  11.0987|     1| 33.5882|  0.2493| 0.6208|
|lesion:hand | 192.0139|  96.0069|     2| 33.5090|  2.1563| 0.1315|


### Post-hoc: Efeitos Principais (interação não significativa)

#### Comparação entre grupos de lesão

|contrast | estimate|     SE|      df| t.ratio| p.value|
|:--------|--------:|------:|-------:|-------:|-------:|
|NS - LS  |  14.5047| 5.1913| 38.5287|  2.7940|  0.0215|
|NS - RS  |   7.5131| 5.0345| 37.4154|  1.4923|  0.3060|
|LS - RS  |  -6.9916| 5.4196| 37.9807| -1.2901|  0.4094|


### R²

| R2_marginal| R2_condicional|
|-----------:|--------------:|
|       0.448|          0.879|

---

## RE1sub

### ANOVA Tipo III (Satterthwaite)

|            |    Sum Sq|   Mean Sq| NumDF|   DenDF|  F value| Pr(>F)|
|:-----------|---------:|---------:|-----:|-------:|--------:|------:|
|lesion      |   30.5670|   15.2835|     2| 30.1380|   4.8081| 0.0154|
|hand        | 1250.4892| 1250.4892|     1| 26.8951| 393.3993| 0.0000|
|lesion:hand |   26.1636|   13.0818|     2| 26.8145|   4.1155| 0.0276|


### Post-hoc: Efeitos Simples (interação significativa)

#### Lesão por mão

|contrast |hand | estimate|     SE|      df| t.ratio| p.value|
|:--------|:----|--------:|------:|-------:|-------:|-------:|
|NS - LS  |LH   |  -3.3919| 0.9836| 60.5716| -3.4485|  0.0029|
|NS - RS  |LH   |  -2.9644| 0.9425| 58.9434| -3.1452|  0.0072|
|LS - RS  |LH   |   0.4275| 1.0320| 59.5933|  0.4143|  0.9099|
|NS - LS  |RH   |  -1.7783| 1.0285| 63.8562| -1.7290|  0.2024|
|NS - RS  |RH   |  -0.1900| 0.9660| 60.9769| -0.1967|  0.9789|
|LS - RS  |RH   |   1.5883| 1.0539| 61.2866|  1.5071|  0.2947|


#### Mão por lesão

|contrast |lesion | estimate|     SE|      df|  t.ratio| p.value|
|:--------|:------|--------:|------:|-------:|--------:|-------:|
|LH - RH  |NS     |  -9.8215| 0.6782| 36.0696| -14.4817|       0|
|LH - RH  |LS     |  -8.2079| 0.8123| 36.4406| -10.1043|       0|
|LH - RH  |RS     |  -7.0471| 0.6993| 32.3982| -10.0773|       0|


### Post-hoc: Efeitos Principais (interação não significativa)

#### Comparação entre grupos de lesão

|contrast | estimate|     SE|      df| t.ratio| p.value|
|:--------|--------:|------:|-------:|-------:|-------:|
|NS - LS  |  -2.5851| 0.8560| 39.7889| -3.0200|  0.0120|
|NS - RS  |  -1.5772| 0.8206| 37.5512| -1.9219|  0.1466|
|LS - RS  |   1.0079| 0.8948| 37.9782|  1.1265|  0.5040|


#### Comparação entre mãos

|contrast | estimate|     SE|      df|  t.ratio| p.value|
|:--------|--------:|------:|-------:|--------:|-------:|
|LH - RH  |  -8.3588| 0.4228| 35.0494| -19.7701|       0|


### R²

| R2_marginal| R2_condicional|
|-----------:|--------------:|
|       0.778|           0.89|

---

## RT

### ANOVA Tipo III (Satterthwaite)

|            |   Sum Sq|   Mean Sq| NumDF|   DenDF| F value| Pr(>F)|
|:-----------|--------:|---------:|-----:|-------:|-------:|------:|
|lesion      | 64325.34| 32162.670|     2| 39.4087|  3.3808| 0.0441|
|hand        | 46206.90| 46206.896|     1| 37.8396|  4.8571| 0.0337|
|lesion:hand | 19683.85|  9841.925|     2| 37.8472|  1.0345| 0.3652|


### Post-hoc: Efeitos Principais (interação não significativa)

#### Comparação entre grupos de lesão

|contrast |  estimate|      SE|      df| t.ratio| p.value|
|:--------|---------:|-------:|-------:|-------:|-------:|
|NS - LS  | -111.9407| 45.2832| 39.2222| -2.4720|  0.0460|
|NS - RS  |  -78.4653| 43.9619| 38.4968| -1.7848|  0.1881|
|LS - RS  |   33.4754| 47.7008| 38.3459|  0.7018|  0.7639|


#### Comparação entre mãos

|contrast | estimate|      SE|      df| t.ratio| p.value|
|:--------|--------:|-------:|-------:|-------:|-------:|
|LH - RH  |  48.6598| 22.1022| 37.1252|  2.2016|   0.034|


### R²

| R2_marginal| R2_condicional|
|-----------:|--------------:|
|       0.324|          0.658|

---

## RTPV

### ANOVA Tipo III (Satterthwaite)

|            |   Sum Sq| Mean Sq| NumDF|   DenDF| F value| Pr(>F)|
|:-----------|--------:|-------:|-----:|-------:|-------:|------:|
|lesion      | 114.4042| 57.2021|     2| 30.3801|  1.5402| 0.2306|
|hand        |  42.5460| 42.5460|     1| 27.7627|  1.1456| 0.2937|
|lesion:hand |  14.0678|  7.0339|     2| 27.7855|  0.1894| 0.8285|


### R²

| R2_marginal| R2_condicional|
|-----------:|--------------:|
|       0.201|          0.536|

---

## time2Sub_ND

### ANOVA Tipo III (Satterthwaite)

|            |   Sum Sq| Mean Sq| NumDF|   DenDF| F value| Pr(>F)|
|:-----------|--------:|-------:|-----:|-------:|-------:|------:|
|lesion      | 150.4264| 75.2132|     2| 37.2948|  2.0809| 0.1391|
|hand        |   0.9335|  0.9335|     1| 35.0439|  0.0258| 0.8732|
|lesion:hand | 148.1888| 74.0944|     2| 34.9966|  2.0499| 0.1439|


### R²

| R2_marginal| R2_condicional|
|-----------:|--------------:|
|       0.324|          0.712|

---

