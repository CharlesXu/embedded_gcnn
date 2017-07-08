from unittest import TestCase

import numpy as np
from numpy.testing import assert_equal
import scipy.sparse as sp

from .spatial import node_selection, neighborhood_selection


class SpatialTest(TestCase):
    def test_node_selection(self):
        points = np.array([[2, 4], [0, 1], [2.1, 2.5], [0.2, 3], [0.1, 4]])

        assert_equal(node_selection(points, size=6), [1, 3, 4, 2, 0, -1])
        assert_equal(node_selection(points, size=2), [1, 3])
        assert_equal(node_selection(points, size=3, stride=3), [1, 2, -1])
        assert_equal(node_selection(points, size=4, stride=2), [1, 4, 0, -1])
        assert_equal(
            node_selection(points, size=6, delta=3), [1, 2, 3, 0, 4, -1])

    def test_neighborhood_selection(self):
        points = np.array([[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]])

        adj = [[0, 1, 1, 1, 1], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0],
               [1, 0, 0, 0, 0], [1, 0, 0, 0, 0]]
        adj = sp.coo_matrix(adj)

        neighborhood_selection(0, points, adj)
