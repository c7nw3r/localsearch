import unittest

from test.annoy_search_test import AnnoySearchTest
from test.ensemble_test import SearchEnsembleTest
from test.pipeline_test import PipelineTest
from test.tantivy_search_test import TantivySearchTest


def suite():
    loader = unittest.TestLoader()

    test_suite = unittest.TestSuite()
    test_suite.addTest(loader.loadTestsFromTestCase(TantivySearchTest))
    test_suite.addTest(loader.loadTestsFromTestCase(AnnoySearchTest))
    test_suite.addTest(loader.loadTestsFromTestCase(SearchEnsembleTest))
    test_suite.addTest(loader.loadTestsFromTestCase(PipelineTest))

    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
