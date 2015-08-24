/*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*    http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

%module swiglpk

%{
#define SWIG_FILE_WITH_INIT
#include "./glpk.h"

int wrap_glp_term_hook_cb(void *info, const char *s)
{
  PyObject *callback = (PyObject *)info;
  PyObject *args = Py_BuildValue("(s)", s);
  if (args == NULL) {
    PyErr_Print();
    goto out;
  }

  PyObject *r = PyObject_Call(callback, args, NULL);
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

%include glpk.h