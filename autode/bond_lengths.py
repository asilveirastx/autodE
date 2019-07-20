# Dictionary of average bond lengths (Å) for common organic molecules from
# http://www.science.uwaterloo.ca/~cchieh/cact/c120/bondel.html and
# https://www.chem.tamu.edu/rgroup/connell/linkfiles/bonds.pdf
import numpy as np
from .log import logger


def get_xyz_bond_list(xyzs, relative_tolerance=0.1):
    """
    Determine the 'bonds' between
    :param xyzs:
    :param relative_tolerance:
    :return:
    """
    xyz_bond_list = []

    for i in range(len(xyzs)):
        i_coords = np.array(xyzs[i][1:])
        for j in range(len(xyzs)):
            if i > j:
                j_coords = np.array(xyzs[j][1:])
                dist = np.linalg.norm(j_coords - i_coords)

                atom_i_label, atom_j_label = xyzs[i][0], xyzs[j][0]
                key1, key2 = atom_i_label + atom_j_label, atom_j_label + atom_i_label

                if key1 in avg_bond_lengths:
                    i_j_bond_length = avg_bond_lengths[key1]
                elif key2 in avg_bond_lengths:
                    i_j_bond_length = avg_bond_lengths[key2]
                else:
                    logger.warning('Couldn\'t find a default bond for {}–{}'.format(atom_i_label, atom_j_label))
                    i_j_bond_length = 1.5  # Default bonded distance

                if dist < i_j_bond_length * (1.0 + relative_tolerance):
                    xyz_bond_list.append((i, j))
    return xyz_bond_list


def get_bond_list_from_rdkit_bonds(rdkit_bonds_obj):

    bond_list = []

    for bond in rdkit_bonds_obj:
        atom_i = bond.GetBeginAtomIdx()
        atom_j = bond.GetEndAtomIdx()
        if atom_i > atom_j:
            bond_list.append((atom_i, atom_j))
        else:
            bond_list.append((atom_j, atom_i))

    return bond_list


def get_ideal_bond_length_matrix(xyzs, bonds):
    logger.info('Getting ideal bond length matrix')

    n_atoms = len(xyzs)
    ideal_bondl_matrix = np.zeros((n_atoms, n_atoms))
    for i in range(n_atoms):
        for j in range(n_atoms):
            if (i, j) in bonds or (j, i) in bonds:
                ideal_bondl_matrix[i, j] = get_avg_bond_length(atom_i_label=xyzs[i][0], atom_j_label=xyzs[j][0])

    return ideal_bondl_matrix


def get_avg_bond_length(atom_i_label=None, atom_j_label=None, mol=None, bond=None):

    if mol is not None and bond is not None:
        atom_i_label = mol.get_atom_label(bond[0])
        atom_j_label = mol.get_atom_label(bond[1])

    key1, key2 = atom_i_label + atom_j_label, atom_j_label + atom_i_label
    if key1 in avg_bond_lengths.keys():
        return avg_bond_lengths[key1]
    elif key2 in avg_bond_lengths.keys():
        return avg_bond_lengths[key2]
    else:
        logger.warning('Couldn\'t find a default bond length for ({},{})'.format(atom_i_label, atom_j_label))
        return 1.5


avg_bond_lengths = {
    'HH': 0.74,
    'CC': 1.54,
    'NN': 1.45,
    'OO': 1.48,
    'FF': 1.42,
    'ClCl': 1.99,
    'II': 2.67,
    'CN': 1.47,
    'CO': 1.43,
    'CS': 1.82,
    'CF': 1.45,
    'CCl': 1.77,
    'CBr': 1.94,
    'CI': 2.14,
    'CSi': 1.85,
    'CP': 1.84,
    'CLi': 2.31,
    'HC': 1.09,
    'HN': 1.01,
    'HO': 0.96,
    'HBr': 1.41,
    'HCl': 1.27,
    'HI': 1.61,
    'HSi': 1.48,
    'SiSi': 2.33,
    'SiO': 1.63,
    'SiF': 1.60,
    'SiCl': 2.02,
    'SH': 1.34,
    'NO': 1.40,
    'NF': 1.36,
    'NCl': 1.75,
    'HF': 0.92,
    'ClF': 1.628,
    'HLi': 1.60,
    'LiO': 1.69,
    'PO': 1.63,
    'PH': 1.44,
    'PF': 1.54,
    'FO': 1.41,
    'RhC': 2.0,
    'RhH': 1.27,
    'RhP': 2.20
}
