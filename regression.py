import pandas as pd
from random import choices
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


class NewRegressionModel():
    
    def __init__(self, dataframe:pd.DataFrame):
        
        self.df = dataframe
        self.equation = None
        self.model = None
        self.accuracy = None
        
        self.vars = {}
        
    def create_model(self):
        '''Create and evaluate a regression model'''
        
        test_areas = choices(self.df.section_area.value_counts().index, k=2)
        
        train_df = self.df.drop(
            self.df[self.df.section_area == test_areas[0]].index
            )
        X_train = train_df.section_area.values.reshape(-1, 1)
        y_train = train_df.max_force
        
        self.model = LinearRegression().fit(X_train, y_train)
        
        # Evaluation
        
        test_df = self.df[
            (self.df.section_area == test_areas[0]) 
            |  
            (self.df.section_area == test_areas[1])
            ]
        X_test = test_df.section_area.values.reshape(-1, 1)
        y_test = test_df.max_force
        
        y_predicted = self.model.predict(X_test)
        self.accuracy = round(r2_score(y_pred=y_predicted, y_true=y_test), 3)
        X = round(self.model.coef_[0], 3)
        Y = round(self.model.intercept_, 3)
        self.equation = f'Max Force = {X} * Section Area + {Y}'
        
        self.vars = {
            'equation': self.equation,
            'model' : self.model,
            'accuracy': self.accuracy,
            'coefficients': {
                'coef' : self.model.coef_[0],
                'intercept': self.model.intercept_
            }
        }
        
        
        
        
    
    

    
    
    