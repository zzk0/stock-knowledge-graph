import tushare as ts

# the interface is deprecated

# get and save industry classification
df_industry = ts.get_industry_classified()
df_industry.to_csv("./data/stock_industry_prep1.csv", index=False, sep=',')

# get and save concept classification
df_concept = ts.get_concept_classified()
df_concept.to_csv("./data/stock_concept_prep1.csv", index=False, sep=',')

