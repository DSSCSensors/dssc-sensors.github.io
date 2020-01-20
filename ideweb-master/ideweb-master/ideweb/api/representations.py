# -*- coding: utf-8 -*-
"""
ideweb.api.representations
~~~~~~~~~~~~~~~~~~~~~~~~~~

API response formats.

:copyright: Copyright 2016 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy
from io import BytesIO
import logging

import dicttoxml
import pandas as pd
from flask import make_response, abort, Response
#from rdkit import Chem
#from rdkit.Chem import AllChem

from . import api


log = logging.getLogger(__name__)


@api.representation('application/xml')
def output_xml(data, code, headers):
    resp = make_response(dicttoxml.dicttoxml(data, attr_type=False, custom_root='job'), code)
    resp.headers.extend(headers)
    return resp


@api.representation('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
def output_xlsx(data, code, headers):
    if 'result' not in data:
        abort(400, 'Result not ready')

    bio = BytesIO()
    writer = pd.ExcelWriter(bio, engine='xlsxwriter')

    # Create sheet for document metadata
    for result in data['result']:
        result['biblio']['doc_id'] = result['biblio'].get('doi', result['biblio']['filename'])
        result['biblio']['authors'] = ', '.join(result['biblio'].get('authors', []))
    df = pd.DataFrame.from_records([result['biblio'] for result in data['result']])
    df.to_excel(writer, sheet_name='documents', index=False)

    # Create sheets for compound identifiers
    data_view = []
    for result in data['result']:
        for compound_num, record in enumerate(result.get('records', [])):
            for name in record.get('names', []):
                data_view.append({'compound_id': compound_num, 'name': name, 'doc_id': result['biblio']['doc_id']})
    df = pd.DataFrame.from_records(data_view)
    df.to_excel(writer, sheet_name='compound_names', index=False)
    data_view = []
    for result in data['result']:
        for compound_num, record in enumerate(result.get('records', [])):
            for label in record.get('labels', []):
                data_view.append({'compound_id': compound_num, 'label': label, 'doc_id': result['biblio']['doc_id']})
    df = pd.DataFrame.from_records(data_view)
    df.to_excel(writer, sheet_name='compound_labels', index=False)

    # Create sheet for each spectrum/property type
    for prop_type in ['ir_spectra', 'nmr_spectra', 'uvvis_spectra', 'melting_points', 'electrochemical_potentials', 'fluorescence_lifetimes', 'quantum_yields']:
        data_view = []
        for result in data['result']:
            for compound_num, record in enumerate(result.get('records', [])):
                for prop_num, prop in enumerate(record.get(prop_type, [])):
                    if 'peaks' in prop:
                        for peak in prop['peaks']:
                            # Create row from peak value
                            row = copy.copy(peak)
                            # Add index numbers
                            row['doc_id'] = result['biblio']['doc_id']
                            row['compound_id'] = compound_num
                            row['compound_spectrum_id'] = prop_num
                            # Pull in parent values to row
                            if 'names' in record and record['names']:
                                    row['compound_name'] = record['names'][0]
                            for metaprop in prop:
                                if not metaprop == 'peaks':
                                    row[metaprop] = prop[metaprop]
                            data_view.append(row)
                    else:
                        # Create row from prop value
                        row = copy.copy(prop)
                        # Add index numbers
                        row['doc_id'] = result['biblio']['doc_id']
                        row['compound_id'] = compound_num
                        row['compound_property_id'] = prop_num
                        # Pull in parent values to row
                        if 'names' in record and record['names']:
                            row['compound_name'] = record['names'][0]
                        data_view.append(row)

        df = pd.DataFrame.from_records(data_view)
        df.to_excel(writer, sheet_name=prop_type, index=False)

    writer.book.close()
    bio.seek(0)
    resp = make_response(bio.read(), code)
    resp.headers.extend(headers)
    return resp


# @api.representation('chemical/x-mdl-sdfile')
# def output_sdf(data, code, headers):
#     if 'result' not in data:
#         abort(400, 'Result not ready')
#
#     # Create RDKit Mols
#     mols = []
#     for result in data['result']:
#         for record in result.get('records', []):
#             if 'smiles' in record:
#                 mol = Chem.MolFromSmiles(record['smiles'])
#                 if mol:
#                     if 'names' in record:
#                         mol.SetProp(b'_Name', record['names'][0].encode('utf-8'))
#                     if 'labels' in record:
#                         mol.SetProp(b'labels', ', '.join([('Compound %s' % l) for l in record['labels']]).encode('utf-8'))
#                     if 'nmr_spectra' in record:
#                         mol.SetIntProp(b'nmr_spectra', len(record.get('nmr_spectra', [])))
#                     if 'ir_spectra' in record:
#                         mol.SetIntProp(b'ir_spectra', len(record.get('ir_spectra', [])))
#                     if 'uvvis_spectra' in record:
#                         mol.SetIntProp(b'uvvis_spectra', len(record.get('uvvis_spectra', [])))
#                     if 'melting_points' in record:
#                         mol.SetIntProp(b'melting_points', len(record.get('melting_points', [])))
#                     if 'quantum_yields' in record:
#                         mol.SetIntProp(b'quantum_yields', len(record.get('quantum_yields', [])))
#                     if 'fluorescence_lifetimes' in record:
#                         mol.SetIntProp(b'fluorescence_lifetimes', len(record.get('fluorescence_lifetimes', [])))
#                     if 'electrochemical_potentials' in record:
#                         mol.SetIntProp(b'electrochemical_potentials', len(record.get('electrochemical_potentials', [])))
#
#                     AllChem.Compute2DCoords(mol)
#                     mols.append(mol)
#
#     # Write to file object
#     bio = BytesIO()
#     writer = Chem.SDWriter(bio)
#     for mol in mols:
#         writer.write(mol)
#     writer.close()
#     bio.seek(0)
#     return Response(response=bio.read(), status=200, mimetype='chemical/x-mdl-molfile', headers={'Content-Disposition': 'attachment;filename=%s.sdf' % data['job_id']})
