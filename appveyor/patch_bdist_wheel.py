import os
import wheel

path = os.path.join(os.path.dirname(wheel.__file__), 'bdist_wheel.py')
with open(path) as f:
    patched = f.read().replace("            basedir_observed = os.path.join(self.data_dir, '..')\n", "            basedir_observed = os.path.join(self.data_dir, '..', '.')\n")
with open(path, 'w') as f:
    f.write(patched)