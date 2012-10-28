# -*- coding: ascii -*-

import os
from string import Template

def view(filename, template_mapping={}):

    """
    Read and populate a view template.

    Arguments:
        filename: string filename of view-file in ./views/.
        template_mapping: optional template mapping dict.

    Returns: string view data
    """

    filepath = './views/' + filename

    if os.path.exists(filepath):
        f = open(filepath, 'r')
        result = str.encode(Template(f.read()).substitute(template_mapping))
        f.close()

    else:
        raise IOError('View does not exist: ' + filepath)

    return result
