/*
* swiglpk - Swig Python bindings for the GNU Linear Programming Kit (GLPK)
* Copyright (C) 2015 The Novo Nordisk Foundation Center for Biosustainability
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

%ignore glp_vprintf;
%ignore glp_netgen_prob;

%module swiglpk

%{
#define SWIG_FILE_WITH_INIT
#include "glpk.h"

int wrap_glp_term_hook_cb(void *info, const char *s)
{
  PyObject *callback, *args, *r;

  callback = (PyObject *)info;

  args = Py_BuildValue("(s)", s);
  if (args == NULL) {
    PyErr_Print();
    goto out;
  }

  r = PyObject_Call(callback, args, NULL);
  if (r == NULL) {
    PyErr_Print();
    goto out;
  }

out:
  Py_XDECREF(r);
  Py_XDECREF(args);
  return 1;
}
%}

%rename(glp_term_hook) wrap_glp_term_hook;
%inline %{
PyObject *wrap_glp_term_hook(PyObject *callback)
{
  if (callback == Py_None) {
    glp_term_hook(NULL, NULL);
  } else {
    glp_term_hook(wrap_glp_term_hook_cb, callback);
  }

  Py_RETURN_NONE;
}
%}

%include glpk.h

%include "carrays.i"
%array_class(int, intArray);
%array_class(double, doubleArray);

%inline %{
PyObject* get_col_primals(glp_prob *P) {
    int n = glp_get_num_cols(P);
    PyObject* list = PyList_New(n);
    double prim = 0.0;
    int n_int = glp_get_num_int(P);
    int i = 0;

    if (n_int == 0) {
        for(i=1; i<=n; i++) {
            prim = glp_get_col_prim(P, i);
            PyList_SetItem(list, i-1, PyFloat_FromDouble(prim));
        }
    } else {
        for(i=1; i<=n; i++) {
            prim = glp_mip_col_val(P, i);
            PyList_SetItem(list, i-1, PyFloat_FromDouble(prim));
        }
    }

    return list;
}

PyObject* get_col_duals(glp_prob *P) {
    int n = glp_get_num_cols(P);
    PyObject* list = PyList_New(n);
    double dual = 0.0;
    int i = 0;
    for(i=1; i<=n; i++) {
        dual = glp_get_col_dual(P, i);
        PyList_SetItem(list, i-1, PyFloat_FromDouble(dual));
    }

    return list;
}

PyObject* get_row_primals(glp_prob *P) {
    int n = glp_get_num_rows(P);
    PyObject* list = PyList_New(n);
    double prim = 0.0;
    int n_int = glp_get_num_int(P);
    int i = 0;

    if (n_int == 0) {
        for(i=1; i<=n; i++) {
            prim = glp_get_row_prim(P, i);
            PyList_SetItem(list, i-1, PyFloat_FromDouble(prim));
        }
    } else {
        for(i=1; i<=n; i++) {
            prim = glp_mip_row_val(P, i);
            PyList_SetItem(list, i-1, PyFloat_FromDouble(prim));
        }
    }

    return list;
}

PyObject* get_row_duals(glp_prob *P) {
    int n = glp_get_num_rows(P);
    PyObject* list = PyList_New(n);
    double dual = 0.0;
    int i = 0;
    for(i=1; i<=n; i++){
        dual = glp_get_row_dual(P, i);
        PyList_SetItem(list, i-1, PyFloat_FromDouble(dual));
    }

    return list;
}

intArray* as_intArray(PyObject *list) {
    /* Check if is a list */
    if (PyList_Check(list)) {
        int size = PyList_Size(list);
        int *int_arr = (int *) malloc((size+1) * sizeof(int));
        int i = 0;
        for (i=0; i<size; i++) {
            PyObject *o = PyList_GetItem(list, i);
            if (PyInt_Check(o))
               int_arr[i+1] = PyInt_AsLong(o);
            else {
               PyErr_SetString(PyExc_TypeError, "list must contain integers");
               free(int_arr);
               return NULL;
            }
        }
        return (intArray*)int_arr;
    }
    PyErr_SetString(PyExc_TypeError, "not a list");
    return NULL;
}

doubleArray* as_doubleArray(PyObject *list) {
    /* Check if is a list */
    if (PyList_Check(list)) {
        int size = PyList_Size(list);
        double *double_arr = (double *) malloc((size+1) * sizeof(double));
        int i = 0;
        for (i=0; i<size; i++) {
            PyObject *o = PyList_GetItem(list, i);
            if (PyFloat_Check(o))
               double_arr[i+1] = PyFloat_AsDouble(o);
            else {
               PyErr_SetString(PyExc_TypeError, "list must contain floats");
               free(double_arr);
               return NULL;
            }
        }
        return (doubleArray*)double_arr;
    }
    PyErr_SetString(PyExc_TypeError, "not a list");
    return NULL;
}
%}

%module swiglpk
