import pickle
with open('StoredWeights/weight_dict_till1500.pkl', 'rb') as handle:
    data = handle.read()
weight_dict = pickle.loads(data)

for key,value in weight_dict.items():
    print(key ," -- ", value)
    print("\n\n")