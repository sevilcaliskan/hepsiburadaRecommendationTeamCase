# hepsiburadaRecommendation

hepsiburadaRecommendation is a Python library for dealing with product recommendations.

## Method and Models
sameCartProducts.ipynb shows the calculations for the lift values of the same cart product pairs. Only the top 90th percentile / most purchased products are included for the calculation ease and result confidence. 

nameSimilarity.ipynb show the similar product pairs similarity calculations. Similarities are calculated for the product pairs which are from the same subcategory. Name similarities of the products are calculated with cosine similarity by getting the sentence embeddings of the names for each pair with sBERT library. More information can be found by the link: https://www.sbert.net/docs/quickstart.html

Both the similarity and lift values are saved into files all_categories_backup.txt and product_90pct.txt. Because of Github's file size restriction, they are shared via drive with the link: https://drive.google.com/drive/folders/1hi4tCAEhVtS04uyJWnmgO8NQcvGWTrb8?usp=sharing

main.py is the script where similarity and lift values are read and processed for the given cart products. For all the products in the cart, top 10 products with the highest similarity and lift values are found and ranked among themselves, and top 10 among those are returned in the end. It is shown in the output that with which products, the recommended products are related.

Because of time limitation, explations and code review might be overlooked. Please do not hesitate to ask any question, sevilcalskn@gmail.com.

## Usage
Please give the products in the cart with argument --c, by splitting them with comma.

```bash
python main.py --c="ZYKOM8699300270064,HBV00000SP6UN"
```

