import os
import unittest

from checkov.kubernetes.checks.resource.k8s.HorizontalPodAutoscalerTarget import check
from checkov.kubernetes.runner import Runner
from checkov.runner_filter import RunnerFilter


class TestHorizontalAutoScaler(unittest.TestCase):

    def test_summary(self):
        runner = Runner()
        current_dir = os.path.dirname(os.path.realpath(__file__))

        test_files_dir = current_dir + "/example_HorizontalAutoscalerTarget"
        report = runner.run(root_folder=test_files_dir, runner_filter=RunnerFilter(checks=[check.id]))
        summary = report.get_summary()

        self.assertEqual(summary['passed'], 1)
        self.assertEqual(summary['failed'], 1)
        self.assertEqual(summary['skipped'], 0)
        self.assertEqual(summary['parsing_errors'], 0)


if __name__ == '__main__':
    unittest.main()
