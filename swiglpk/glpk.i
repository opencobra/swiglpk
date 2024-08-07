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
    if (!PyList_Check(list))
    {
        PyErr_SetString(PyExc_TypeError, "not a list");
        return NULL;
    }

    PyObject *pmod   = PyImport_ImportModule("swiglpk");
    if (!pmod)
    {
        PyErr_SetString(PyExc_ImportError, "swiglpk could not be imported");
        return NULL;
    }

    PyObject *pclass = PyObject_GetAttrString(pmod, "intArray");
    Py_DECREF(pmod);
    if (!pclass)
    {
        PyErr_SetString(PyExc_AttributeError, "swiglpk does not contain intArray");
        return NULL;
    }

    // Call doubleArray constructor with size + 1.
    Py_ssize_t size = PyList_Size(list);
    PyObject *pargs  = Py_BuildValue("(i)", size + 1);
    if (!pargs)
    {
        Py_DECREF(pclass);
        PyErr_SetString(PyExc_RuntimeError, "building arguments list for intArray constructor failed");
        return NULL;
    }

    PyObject *pinst  = PyObject_Call(pclass, pargs);
    Py_DECREF(pclass);
    Py_DECREF(pargs);
    if (!pinst)
    {
        PyErr_SetString(PyExc_RuntimeError, "creating intArray failed");
        return NULL;
    }

    PyObject* pthis = PyObject_GetAttrString(pinst, "this");
    if (!pthis)
    {
        Py_DECREF(pinst);
        PyErr_SetString(PyExc_AttributeError, "intArray 'this' attribute not found");
        return NULL;
    }

    // Convert 'this' to a C-style pointer.
    intArray* int_arr = 0;
    int res = SWIG_ConvertPtr(pthis, (void**)&int_arr, SWIGTYPE_p_intArray, 0);
    Py_DECREF(pthis);
    if (!SWIG_IsOK(res))
    {
        Py_DECREF(pinst);
        PyErr_SetString(PyExc_RuntimeError, "SWIG_ConvertPtr failed");
        return NULL;
    }

    PyObject *item;
    for (Py_ssize_t idx=0; idx<size; idx++)
    {
        item = PyList_GetItem(list, idx);

        if (!PyInt_Check(item))
        {
            Py_DECREF(pinst);
            PyErr_SetString(PyExc_TypeError, "list must contain only integers");
            return NULL;
        }

        int_arr[idx+1] = PyInt_AsLong(item);
    }

    return pinst;
}

doubleArray* as_doubleArray(PyObject *list) {
    if (!PyList_Check(list))
    {
        PyErr_SetString(PyExc_TypeError, "not a list");
        return NULL;
    }

    PyObject *pmod   = PyImport_ImportModule("swiglpk");
    if (!pmod)
    {
        PyErr_SetString(PyExc_ImportError, "swiglpk could not be imported");
        return NULL;
    }

    PyObject *pclass = PyObject_GetAttrString(pmod, "doubleArray");
    Py_DECREF(pmod);
    if (!pclass)
    {
        PyErr_SetString(PyExc_AttributeError, "swiglpk does not contain doubleArray");
        return NULL;
    }

    // Call doubleArray constructor with size + 1.
    Py_ssize_t size = PyList_Size(list);
    PyObject *pargs  = Py_BuildValue("(i)", size + 1);
    if (!pargs)
    {
        Py_DECREF(pclass);
        PyErr_SetString(PyExc_RuntimeError, "building arguments list for doubleArray constructor failed");
        return NULL;
    }

    PyObject *pinst  = PyObject_Call(pclass, pargs);
    Py_DECREF(pclass);
    Py_DECREF(pargs);
    if (!pinst)
    {
        PyErr_SetString(PyExc_RuntimeError, "creating doubleArray failed");
        return NULL;
    }

    PyObject* pthis = PyObject_GetAttrString(pinst, "this");
    if (!pthis)
    {
        Py_DECREF(pinst);
        PyErr_SetString(PyExc_AttributeError, "doubleArray 'this' attribute not found");
        return NULL;
    }

    // Convert 'this' to a C-style pointer.
    doubleArray* double_arr = 0;
    int res = SWIG_ConvertPtr(pthis, (void**)&double_arr, SWIGTYPE_p_doubleArray, 0);
    Py_DECREF(pthis);
    if (!SWIG_IsOK(res))
    {
        Py_DECREF(pinst);
        PyErr_SetString(PyExc_RuntimeError, "SWIG_ConvertPtr failed");
        return NULL;
    }

    PyObject *item;
    for (Py_ssize_t idx=0; idx<size; idx++)
    {
        item = PyList_GetItem(list, idx);

        if (!PyFloat_Check(item))
        {
            Py_DECREF(pinst);
            PyErr_SetString(PyExc_TypeError, "list must contain only floats");
            return NULL;
        }

        double_arr[idx+1] = PyFloat_AsDouble(item);
    }

    return pinst;
}
%}

%module swiglpk
