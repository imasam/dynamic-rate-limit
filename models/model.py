import numpy as np
import keras
import random

checker_intercept_ = [130.79770086]
checker_coef_ = [0.01630432, 0.02698368, 0.00591432, 0.00715666, -0.0059252]
checker_intercept_.extend(checker_coef_)
cherker_model = np.array(checker_intercept_).reshape(1, len(checker_intercept_))


r1_a_intercept_ = [-515.1739106]
r1_a_coef_ = [-2.46566854e+00, -2.69827079e+00, -3.12454731e-01, -6.36709844e+01,
   3.62639698e+01,  1.11543376e+01,  2.10254627e+03, -9.30263163e+01,
  -9.80469871e+01,  3.66763801e+00, -3.15245821e+00, -2.61907753e+00,
   7.87390685e-01,  6.14958595e-03, -5.67904333e-03,  1.75014627e-02,
  -3.90405847e-03,  2.49537212e+05]
r1_a_intercept_.extend(r1_a_coef_)
r1_a_model = np.array(r1_a_intercept_).reshape(1, len(r1_a_intercept_))

def checkerInfer(array_of_params):
    return cherker_model.dot(np.array([1] + array_of_params).reshape(len(checker_intercept_), 1))[0][0]

# print(checkerInfer([11,2,3,4,5]))

def r1_a_predictor(array_of_params):
    # print(len(array_of_params))
    return r1_a_model.dot(np.array([1] + array_of_params).reshape(len(r1_a_intercept_), 1))[0][0]



r1_b_intercept_ = [-41.56630933]
r1_b_coef_ = [6.02837478e+00, 8.81384640e-01, -1.26749936e+00, -5.18272563e+01,
                -2.74347786e+01, -3.57410862e+00, -2.02667501e+03, -1.04269488e+02,
                4.17570386e+01, -8.47889909e+01, 6.28811923e+01, 3.71971239e+02,
                2.46081299e-04, 7.68593560e-01, 1.03918944e-02, 4.22776852e-03,
                -4.31148445e-03, 2.81635921e+03]
r1_b_intercept_.extend(r1_b_coef_)
r1_b_model = np.array(r1_b_intercept_).reshape(1, len(r1_b_intercept_))

def r1_b_predictor(array_of_params):
    return r1_b_model.dot(np.array([1] + array_of_params).reshape(len(r1_b_intercept_), 1))[0][0]


r2_b_intercept_ = [-16.11503558]
r2_b_coef_ = [-1.15214116e+00,  2.44870478e-01,  2.98281190e-01, -1.27200386e+02,
   1.92083329e+01, -1.66816320e+01, -5.37720158e+02,  2.90452828e+02,
  -6.46387724e+00, -3.18489995e+00,  3.09377268e+01,  2.62913564e+01,
   8.53295077e-04, -1.04302178e-03,  8.86255511e-01, -1.17802470e-03,
  -5.46914867e-03, -5.19569912e+00]
r2_b_intercept_.extend(r2_b_coef_)
r2_b_model = np.array(r2_b_intercept_).reshape(1, len(r2_b_intercept_))

def r2_b_predictor(array_of_params):
    return r2_b_model.dot(np.array([1] + array_of_params).reshape(len(r2_b_intercept_), 1))[0][0]



r1_c_intercept_ = [-39.56630933]
r1_c_coef_ = [5.02837478e+00, 7.81384640e-01, -1.29749936e+00, -6.18272563e+01,
                -2.74347786e+01, -4.57410862e+00, -2.02667501e+03, -1.04269488e+02,
                4.17570386e+01, -8.47889909e+01, 6.38811923e+01, 3.71971239e+02,
                1.46081299e-04, 6.68593560e-01, 1.43258944e-02, 5.22776852e-03,
                -2.32148445e-03, 2.81635921e+03]
r1_c_intercept_.extend(r1_c_coef_)
r1_c_model = np.array(r1_c_intercept_).reshape(1, len(r1_c_intercept_))

def r1_c_predictor(array_of_params):
    return r1_c_model.dot(np.array([1] + array_of_params).reshape(len(r1_c_intercept_), 1))[0][0]


r2_d_intercept_ = [-39.56630933]
r2_d_coef_ = [5.02837478e+00, 7.81384640e-01, -1.29749936e+00, -6.18272563e+01,
                -2.74347786e+01, -4.57410862e+00, -2.02667501e+03, -1.04269488e+02,
                4.17570386e+01, -8.47889909e+01, 6.38811923e+01, 3.71971239e+02,
                1.46081299e-04, 6.68593560e-01, 1.43258944e-02, 5.22776852e-03,
                -2.32148445e-03, 2.81635921e+03]
r2_d_intercept_.extend(r2_d_coef_)
r2_d_model = np.array(r2_d_intercept_).reshape(1, len(r2_d_intercept_))

def r2_d_predictor(array_of_params):
    return r2_d_model.dot(np.array([1] + array_of_params).reshape(len(r2_d_intercept_), 1))[0][0]


def fc_model(model_dir, param):
    loaded = keras.models.load_model(model_dir)
    param = np.array(param).reshape(1,18,)
    class_type = np.argmax(loaded.predict(param)[0], axis=0)
    down = class_type * 10
    up = (class_type + 1) * 10
    print(random.randint(down, up))
    return random.randint(down, up)

def lstm_model(model_dir, param):
    loaded = keras.models.load_model("models/dl/r1_service_a_lstm")
    param = np.array(param).reshape(1,5,18)
    class_type = np.argmax(loaded.predict(param)[0], axis=0)
    down = class_type * 10
    up = (class_type + 1) * 10
    print(random.randint(down, up))
    return random.randint(down, up)

# fc_model("./models/dl/r1_service_a_fc", [2.38560000e+00, 3.61449000e+00, 4.78500000e+00, 7.03500000e-02,
#        3.24450000e-01, 6.27300000e-01, 3.12000000e-03, 1.76400000e-02,
#        7.76000000e-02, 5.62031396e-03, 9.79196345e-01, 8.52858482e-04,
#        1.81280000e+02, 5.10000000e+01, 1.20190000e+02, 1.76400000e+02,
#        4.90000000e+01, 2.29950000e-03])
# print(r1_a_predictor([0.76, 4.207, 6.358, 0.014, 0.234, 0.884, 0.003, 0.02, 
# 0.124, 0.042816365, 0.990485252, 0.009514748, 108, 230, 179, 109, 64, 0.00233]))
# param = [2.38560000e+00, 3.61449000e+00, 4.78500000e+00, 7.03500000e-02,
#        3.24450000e-01, 6.27300000e-01, 3.12000000e-03, 1.76400000e-02,
#        7.76000000e-02, 5.62031396e-03, 9.79196345e-01, 8.52858482e-04,
#        1.81280000e+02, 5.10000000e+01, 1.20190000e+02, 1.76400000e+02,
#        4.90000000e+01, 2.29950000e-03]

# lstm_model("models/dl/r1_service_a_lstm", param + param + param + param + param)