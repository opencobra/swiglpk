# swiglpk - Swig Python bindings for the GNU Linear Programming Kit (GLPK)
# Copyright (C) 2015 The Novo Nordisk Foundation Center for Biosustainability
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import nose
from swiglpk import *

def test_swiglpk():
    print(glp version())
    ia = intArray(1+1000); ja = intArray(1+1000);
    ar = doubleArray(1+1000);
    lp = glp_create_prob();
    glp_set_prob_name(lp, "sample");
    glp_set_obj_dir(lp, GLP_MAX);
    glp_add_rows(lp, 3);
    glp_set_row_name(lp, 1, "p");
    glp_set_row_bnds(lp, 1, GLP_UP, 0.0, 100.0);
    glp_set_row_name(lp, 2, "q");
    glp_set_row_bnds(lp, 2, GLP_UP, 0.0, 600.0);
    glp_set_row_name(lp, 3, "r");
    glp_set_row_bnds(lp, 3, GLP_UP, 0.0, 300.0);
    glp_add_cols(lp, 3);
    glp_set_col_name(lp, 1, "x1");
    glp_set_col_bnds(lp, 1, GLP_LO, 0.0, 0.0);
    glp_set_obj_coef(lp, 1, 10.0);
    glp_set_col_name(lp, 2, "x2");
    glp_set_col_bnds(lp, 2, GLP_LO, 0.0, 0.0);
    glp_set_obj_coef(lp, 2, 6.0);
    glp_set_col_name(lp, 3, "x3");
    glp_set_col_bnds(lp, 3, GLP_LO, 0.0, 0.0);
    glp_set_obj_coef(lp, 3, 4.0);
    ia[1] = 1; ja[1] = 1; ar[1] = 1.0; # a[1,1] = 1
    ia[2] = 1; ja[2] = 2; ar[2] = 1.0; # a[1,2] = 1
    ia[3] = 1; ja[3] = 3; ar[3] = 1.0; # a[1,3] = 1
    ia[4] = 2; ja[4] = 1; ar[4] = 10.0; # a[2,1] = 10
    ia[5] = 3; ja[5] = 1; ar[5] = 2.0; # a[3,1] = 2
    ia[6] = 2; ja[6] = 2; ar[6] = 4.0; # a[2,2] = 4
    ia[7] = 3; ja[7] = 2; ar[7] = 2.0; # a[3,2] = 2
    ia[8] = 2; ja[8] = 3; ar[8] = 5.0; # a[2,3] = 5
    ia[9] = 3; ja[9] = 3; ar[9] = 6.0; # a[3,3] = 6
    glp_load_matrix(lp, 9, ia, ja, ar);
    glp_simplex(lp, None);
    Z = glp_get_obj_val(lp);
    x1 = glp_get_col_prim(lp, 1);
    x2 = glp_get_col_prim(lp, 2);
    x3 = glp_get_col_prim(lp, 3);
    print("\nZ = %g; x1 = %g; x2 = %g; x3 = %g\n" % (Z, x1, x2, x3))

    nose.tools.assert_almost_equal(Z, 733.3333333333333)
    nose.tools.assert_almost_equal(x1, 33.333333333333336)
    nose.tools.assert_almost_equal(x2, 66.66666666666666)
    nose.tools.assert_almost_equal(x3, 0)

    glp_delete_prob(lp);
