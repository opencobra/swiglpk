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

%module swiglpk

%{
#define SWIG_FILE_WITH_INIT
#include "./glpk_clean.h"

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

%include "carrays.i"
%array_class(int, intArray);
%array_class(double, doubleArray);

%include glpk_clean.h

%module swiglpk