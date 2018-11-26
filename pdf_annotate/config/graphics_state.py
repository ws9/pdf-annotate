# -*- coding: utf-8 -*-
import attr
from pdfrw import PdfDict
from pdfrw import PdfName

from pdf_annotate.config.constants import ALLOWED_LINE_CAPS
from pdf_annotate.config.constants import ALLOWED_LINE_JOINS
from pdf_annotate.util.validation import between
from pdf_annotate.util.validation import Enum
from pdf_annotate.util.validation import Field
from pdf_annotate.util.validation import Number
from pdf_annotate.util.validation import positive


def validate_dash_array(obj, value, attr):
    # TODO validate dash array
    pass


NAME_TO_PDF_ATTR = {
    'line_width': 'LW',
    'line_cap': 'LC',
    'line_join': 'LJ',
    'miter_limit': 'ML',
    'dash_array': 'D',
    'stroke_transparency': 'CA',
    'fill_transparency': 'ca',
}


@attr.s
class GraphicsState(object):
    """External graphics state config object, that can be used with explicit
    content streams to control annotation appearance.

    Some of these values can also be specified by their own operators in the
    content stream. For example, the line_width property can also be specified
    by the StrokeWidth (w) content stream operator.

    See the full PDF spec for constraints on and descriptions of these values.
    There are a lot more graphics state options, but they are highly technical
    and beyond the scope of this library.
    """
    line_width = Number(default=None, validator=positive)
    line_cap = Enum(ALLOWED_LINE_CAPS, default=None)
    line_join = Enum(ALLOWED_LINE_JOINS, default=None)
    miter_limit = Number(default=None)
    dash_array = Field(list, validator=validate_dash_array, default=None)
    stroke_transparency = Number(default=None, validator=between(0, 1))
    fill_transparency = Number(default=None, validator=between(0, 1))

    def as_pdf_dict(self):
        pdf_dict = PdfDict(Type=PdfName('ExtGState'))
        for attr_name, pdf_name in NAME_TO_PDF_ATTR.items():
            attr_value = getattr(self, attr_name, None)
            if attr_value is not None:
                pdf_dict[PdfName(pdf_name)] = attr_value
        return pdf_dict