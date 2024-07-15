# project: p7
# submitter: mchen353
# partner: none
# hours: 3

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LogisticRegression

def augment_users(users, logs):
    demo = users.copy()
    seconds_temp = logs.groupby(["user_id"])["seconds"].sum().reset_index(name='total_sec')
    count_temp = logs.groupby(["user_id"])["user_id"].count().reset_index(name='count')
    
    demo = pd.merge(demo, seconds_temp, on='user_id', how="left").fillna(0)
    demo = pd.merge(demo, count_temp, on='user_id', how="left").fillna(0)
    return demo

class UserPredictor:
    def __init__(self):
        self.model = None
        
    def fit(self, train_users, train_logs, train_y):
        demo = augment_users(train_users, train_logs)
        demo["y"] = train_y["y"]
        
        xcols = ["age", "past_purchase_amt", "total_sec", "count"]
        
        model = Pipeline([
            ("pf", PolynomialFeatures(degree=2, include_bias=False)),
            ("sd", StandardScaler()),
            ("lr", LogisticRegression(fit_intercept=True, max_iter = 300))
        ])
        
        self.model = model
        self.model.fit(demo[xcols], demo["y"])
    
    def predict(self, test_users, test_logs):
        demo_pre = augment_users(test_users, test_logs)
        
        xcols = ["age", "past_purchase_amt", "total_sec", "count"]
        return self.model.predict(demo_pre[xcols])