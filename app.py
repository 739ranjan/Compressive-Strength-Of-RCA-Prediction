# flask, sciket-learn, pandas, pickle-mixin
import pandas as pd
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
# data = pd.read_csv("MeanImputedData.csv")
xgb = pickle.load(open("XGB_model.pkl", 'rb'))

@app.route('/')
def index():
    return render_template("index.html", results = "")


# noinspection PyInterpreter
@app.route('/', methods=['POST'])
def predict():
    eff_water_cement = request.form.get('eff_water_cement')
    agg_cement = request.form.get('agg_cement')
    RCA_replacement = request.form.get('RCA_replacement')
    parent_con_strength = request.form.get('parent_con_strength')
    nominal_RCA = request.form.get('nominal_RCA')
    nominal_NA = request.form.get('nominal_NA')
    water_abs_RCA = request.form.get('water_abs_RCA')
    water_abs_NA = request.form.get('water_abs_NA')
    los_angeles_RCA = request.form.get('los_angeles_RCA')
    los_angeles_NA = request.form.get('los_angeles_NA')
    print(eff_water_cement, agg_cement, RCA_replacement, parent_con_strength, nominal_RCA, nominal_NA, water_abs_RCA,
          water_abs_NA, los_angeles_RCA, los_angeles_NA)
    input = pd.DataFrame([
        [eff_water_cement, agg_cement, RCA_replacement, parent_con_strength, nominal_RCA, nominal_NA, water_abs_RCA,
         water_abs_NA, los_angeles_RCA, los_angeles_NA]],
        columns=['Effective water- to-cement ratio', 'Aggregate-to-cement ratio (a/c)', 'RCA replacement ratio (RCA %)',
                 'Parent concrete strength(MPa)', 'Nominal maximum RCA size(mm)', 'Nominal maximum NA size(mm)',
                 'Water absorption of RCA(WARCA) (%)', 'Water absorption of NA', 'Los Angeles abrasion of RCA',
                 'Los Angeles abrasion of NA'])
    input = input.astype(float)
    prediction = xgb.predict(input)[0]

    return render_template("index.html", results = f'Compressive Strength Of RCA Predicted : {prediction} MPa')


# if __name__ == "__main__":
#     app.run(debug=True, port=5001)
