import pickle
with open('StoredWeights/param_dict_2.pkl', 'rb') as handle:
    data = handle.read()
weight_dict = pickle.loads(data)
print(weight_dict["BW1"].shape)
print(weight_dict["dBW1"].shape)
print(weight_dict["BW2"].shape)
print(weight_dict["dBW2"].shape)
for value in weight_dict["X_train"]:
    print(value) 
# for key,value in weight_dict.items():
#     print(key ," -- ", value)
#     print("\n\n")