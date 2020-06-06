import sys
from anyfig.figutils import *
from anyfig.anyfig_setup import *

# Some features are only supported in Python 3.7+
python_v = sys.version_info
if python_v.major >= 3 and python_v.minor >= 7:
  from anyfig.fields import *
else:
  from anyfig.dummyfields import *
