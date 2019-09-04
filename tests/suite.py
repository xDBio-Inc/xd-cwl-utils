import unittest
import logging
import tempfile
import os
import argparse
from unittest import defaultTestLoader, TestSuite
from tests.test_tool_metadata import TestMakeToolMetadata, TestMakeParentToolMetadata, TestMakeSubtoolMetadata, TestAddTools
from tests.test_script_metadata import TestScriptMetadata
from tests.test_content_maps import TestToolMaps
from tests.test_workflow_metadata import TestWorkflowMetadata
from tests.test_get_metadata import TestMetadataFromBioTools
from tests.test_validate import TestValidateMetadata
from tests.test_validate_all_metadata_in_maps import TestValidateContent
from tests.test_validate_tool_inputs import TestValidateInputs


parser = argparse.ArgumentParser()
parser.add_argument("module", nargs='?', default='full',
                    help='Specify the test suite that you would like to run. All suites will run if not specified')
parser.add_argument("--log_level", help="Set logging level", choices=['debug', 'info', 'warning', 'error', 'critical'])
args = parser.parse_args()


def suite_full():
    suite = TestSuite()
    suite.addTest(suite_content_maps())
    suite.addTest(suite_get_metadata())
    suite.addTest(suite_script_metadata())
    suite.addTest(suite_validate())
    suite.addTest(suite_validate_all_metadata_in_maps())
    suite.addTest(suite_validate_tool_inputs())
    suite.addTest(suite_workflow_metadata())
    return suite


def suite_content_maps():
    suite = defaultTestLoader.loadTestsFromTestCase(TestToolMaps)
    return suite

def suite_get_metadata():
    suite = defaultTestLoader.loadTestsFromTestCase(TestMetadataFromBioTools)
    return suite

def suite_script_metadata():
    suite = defaultTestLoader.loadTestsFromTestCase(TestScriptMetadata)
    return suite

def suite_tool_metadata():
    suite = defaultTestLoader.loadTestsFromTestCase(TestMakeToolMetadata)
    suite.addTest(defaultTestLoader.loadTestsFromTestCase(TestMakeSubtoolMetadata))
    suite.addTest(defaultTestLoader.loadTestsFromTestCase(TestMakeParentToolMetadata))
    suite.addTest(defaultTestLoader.loadTestsFromTestCase(TestAddTools))
    return suite

def suite_validate():
    suite = defaultTestLoader.loadTestsFromTestCase(TestValidateMetadata)
    return suite

def suite_validate_all_metadata_in_maps():
    suite = defaultTestLoader.loadTestsFromTestCase(TestValidateContent)
    return suite

def suite_validate_tool_inputs():
    suite = defaultTestLoader.loadTestsFromTestCase(TestValidateInputs)
    return suite



def suite_workflow_metadata():
    suite = defaultTestLoader.loadTestsFromTestCase(TestWorkflowMetadata)
    return suite


def run_tests():
    logging.basicConfig(level=logging.CRITICAL)
    if args.log_level:
        if args.log_level=='debug':
            log_level = logging.DEBUG
        elif args.log_level=='info':
            log_level = logging.INFO
        elif args.log_level=='warning':
            log_level = logging.WARNING
        elif args.log_level=='error':
            log_level = logging.ERROR
        elif args.log_level=='critical':
            log_level = logging.CRITICAL
        else:
            raise ValueError  # Should never hit this.
    else:
        log_level = logging.WARNING  # default level.

    logging.getLogger().setLevel(log_level)

    # update this dictionary when new suites are added.
    suite_dict = {'content_maps': suite_content_maps(),
                  'get_metadata': suite_get_metadata(),
                  'full': suite_full(),
                  'script_metadata': suite_script_metadata(),
                  'tool_metadata': suite_tool_metadata(),
                  'validate': suite_validate(),
                  'validate_all_metadata_in_maps': suite_validate_all_metadata_in_maps(),
                  'validate_tool_inputs': suite_validate_tool_inputs(),
                  'workflow_metadata': suite_workflow_metadata(),
                  }


    try:
        test_suite = suite_dict[args.module]
    except KeyError:
        raise ValueError(f"Test suite {args.module} not recognized.")


    # Set temp directory
    test_temp_dir = tempfile.TemporaryDirectory(prefix='cwlTest_')
    os.environ['TEST_TMP_DIR'] = test_temp_dir.name
    unittest.TextTestRunner().run(test_suite)
    return


if __name__ == '__main__':
    run_tests()